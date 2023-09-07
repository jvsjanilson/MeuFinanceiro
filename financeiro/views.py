import datetime
from typing import Any
from django.http import HttpRequest, HttpResponse
from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView, DeleteView, FormView, TemplateView
from financeiro.models import ContaReceber, BaixaReceber, ContaPagar, BaixaPagar
from core.constants import REGISTROS_POR_PAGINA, MSG_CREATED_SUCCESS, MSG_DELETED_SUCCESS, MSG_UPDATED_SUCCESS
from django.db.models import Q
from django.shortcuts import redirect
from core.views import UserAccessMixin, InvalidFormMixin
from financeiro.forms import ContaReceberForm, ContaPagarForm, BaixaPagarForm
from django.urls import reverse_lazy
from django.contrib import messages
from financeiro.choices import SituacaoFinanceiro
from financeiro.forms import BaixaReceberForm
from django.db.models import ProtectedError
from django.db.models import Case, Value, When
from django.contrib.messages.views import SuccessMessageMixin
from decimal import Decimal


def fluxo_pagamento_resumo_dia(data_inicial, data_final) -> list:
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute(
        """
            SELECT 
                q.data_baixa,
                q.total_pagar_pago,
                q.total_receber_pago,
                SUM(q.total_receber_pago-q.total_pagar_pago) AS saldo
            FROM  (
                SELECT 
                    data_baixa,
                    SUM(
                        case 
                            when tipo = 'pagar' then 
                                br_total_pago
                            ELSE 
                            0
                        END 
                    ) AS total_pagar_pago,
                    
                    SUM(
                        case 
                            when tipo = 'receber' then 
                            br_total_pago
                        ELSE 
                            0
                        END 
                    ) AS total_receber_pago
                FROM (
                    (
                        SELECT 
                            'receber' AS tipo,
                            br.data_baixa, 
                            SUM(COALESCE(br.valor_pago,0)) AS br_total_pago
                        FROM financeiro_baixareceber br
                        GROUP BY br.data_baixa
                        ORDER by br.data_baixa
                    )
                    UNION
                    (
                        SELECT 
                            'pagar' AS tipo,
                            br.data_baixa, 
                            SUM(COALESCE(br.valor_pago,0)) AS bp_total_pago
                        FROM financeiro_baixapagar br
                        GROUP BY br.data_baixa
                        ORDER by br.data_baixa
                    )
                ) t
                GROUP BY data_baixa
            ) q where q.data_baixa >= %s  and q.data_baixa <= %s
            GROUP BY q.data_baixa
            ORDER BY q.data_baixa
        """, [data_inicial, data_final]
    )
    
    columns = [col[0] for col in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    saldo = Decimal('0.00')
    for i in rows:
        saldo += i['saldo']
    return [saldo, rows]


class FluxoCaixaView(UserAccessMixin, TemplateView):
    template_name = 'financeiro/fluxo/list.html'
    tipos_fluxo = {'1': 'Resumo por dia'}
    permission_required = ['financeiro.fluxo_contareceber']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data_inicial = self.request.GET.get('data_inicial')
        data_final = self.request.GET.get('data_final')
        tipo_fluxo = self.request.GET.get('tipo_fluxo')

        if tipo_fluxo is None:
            tipo_fluxo = '1'

        context['titulo'] = f'Fluxo de pagamento - {self.tipos_fluxo[tipo_fluxo]}'
        context['tipo_fluxo'] = tipo_fluxo

        if data_final == "":
            data_final = None

        if data_inicial == "":
            data_inicial = None
        
        context['data_inicial'] = data_inicial
        context['data_final'] = data_final
        context['saldo'] = Decimal('0.00')

        if [data_final, data_inicial] is not None:
            context['saldo'], context['recebers'] = fluxo_pagamento_resumo_dia(data_inicial, data_final)

        return context
        

class EstornarContaReceberView(UserAccessMixin, FormView):
    success_url = reverse_lazy('contareceber-list')
    template_name = 'financeiro/baixareceber/estorno.html'
    form_class = BaixaReceberForm
    permission_required = ['financeiro.add_baixareceber']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        baixas = BaixaReceber.objects.filter(contareceber=self.kwargs['contareceber'])
        conta = ContaReceber.objects.get(pk=self.kwargs['contareceber'])
        context['baixas'] = baixas
        context['conta'] = conta
        return context

    def get(self, request, *args, **kwargs):
        baixas = BaixaReceber.objects.filter(contareceber=kwargs['contareceber'])
        if len(baixas) == 0:
            messages.add_message(request, messages.INFO, 'Sem baixa para estorno')
            return redirect('/contarecebers')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pk = request.POST.get('contareceber')
        ids = request.POST.getlist('check')
        baixas = self.get_context_data()['baixas']

        if pk is not None:
            if len(ids) == 0:
                messages.add_message(request, messages.ERROR, 'Nenhum titulo foi marcado para estorno.')
                conta = ContaReceber.objects.get(pk=request.POST.get('contareceber'))
                return self.render_to_response({'baixas': baixas, 'conta': conta})
            try:
                BaixaReceber.objects.filter(contareceber=pk, pk__in=ids).delete()
                receber = ContaReceber.objects.get(pk=pk)

                if BaixaReceber.objects.filter(contareceber=pk).exists():
                    receber.situacao = SituacaoFinanceiro.PAGO_PARCIAL
                else:
                    receber.situacao = SituacaoFinanceiro.ABERTO

                receber.save()

                messages.add_message(request, messages.SUCCESS, 'Titulo estornado com sucesso.')
                return redirect('/contarecebers')
            except ProtectedError:
                messages.add_message(request, messages.ERROR, 'Erro ao estornar titulo.')
                return redirect('/contarecebers')
        return super().post(request, *args, **kwargs)


class BaixarContaReceberView(UserAccessMixin, InvalidFormMixin, SuccessMessageMixin, CreateView):
    template_name = 'financeiro/baixareceber/form.html'
    form_class = BaixaReceberForm
    success_url = reverse_lazy('contareceber-list')
    permission_required = ['financeiro.add_baixareceber']
    model = BaixaReceber
    fail_url = '/contarecebers'
    success_message = 'Baixa efetuada com sucesso.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conta = ContaReceber.objects.get(pk=self.kwargs['contareceber'])
        context['verbose_name'] = self.model._meta.verbose_name.title
        context['conta'] = conta
        return context

    def get(self, request, *args, **kwargs):
        conta = ContaReceber.objects.get(pk=kwargs['contareceber'])
        if conta.situacao == SituacaoFinanceiro.PAGO_TOTAL:
            messages.add_message(request, messages.WARNING, 'Titulo ja foi pago totalmente.')
            return redirect('/contarecebers')
        return super().get(request, *args, **kwargs)


def checa_filtro_preenchido(request):
    search = request.GET.get('search')
    emissao_inicial = request.GET.get('emissao_inicial')
    emissao_final = request.GET.get('emissao_final')
    vencto_inicial = request.GET.get('vencto_inicial')
    vencto_final = request.GET.get('vencto_final')
    situacao_aberto = request.GET.get('situacao_aberto')
    situacao_pago_parcial = request.GET.get('situacao_pago_parcial')
    situacao_pago_total = request.GET.get('situacao_pago_total')

    if (search == "" and emissao_inicial == "" and emissao_final == "" and vencto_inicial == "" and
            vencto_final == "" and situacao_pago_total is None and situacao_pago_parcial is None and
            situacao_aberto is None):
        return True
    else:
        return False


class ContaReceberListView(UserAccessMixin, ListView):
    permission_required = ["financeiro.view_contareceber"]
    model = ContaReceber
    template_name = 'financeiro/contareceber/list.html'
    paginate_by = REGISTROS_POR_PAGINA

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if checa_filtro_preenchido(request):
            return redirect('/contarecebers')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        context['verbose_name_plural'] = self.model._meta.verbose_name_plural.title
        search = self.request.GET.get('search')

        emissao_inicial = self.request.GET.get('emissao_inicial')
        emissao_final = self.request.GET.get('emissao_final')

        vencto_inicial = self.request.GET.get('vencto_inicial')
        vencto_final = self.request.GET.get('vencto_final')

        situacao_aberto = self.request.GET.get('situacao_aberto')
        situacao_pago_parcial = self.request.GET.get('situacao_pago_parcial')
        situacao_pago_total = self.request.GET.get('situacao_pago_total')

        if situacao_aberto is not None:
            context['situacao_aberto'] = situacao_aberto

        if situacao_pago_parcial is not None:
            context['situacao_pago_parcial'] = situacao_pago_parcial

        if situacao_pago_total is not None:
            context['situacao_pago_total'] = situacao_pago_total

        if emissao_inicial is not None and emissao_inicial != "":
            context['emissao_inicial'] = emissao_inicial

        if emissao_final is not None and emissao_final != "":
            context['emissao_final'] = emissao_final

        if vencto_inicial is not None and vencto_inicial != "":
            context['vencto_inicial'] = vencto_inicial

        if vencto_final is not None and vencto_final != "":
            context['vencto_final'] = vencto_final

        if search:
            context['search'] = search

        return context

    def get_queryset(self):
        queryset = super(ContaReceberListView, self).get_queryset()
       
        search = self.request.GET.get('search')
        emissao_inicial = self.request.GET.get('emissao_inicial')
        emissao_final = self.request.GET.get('emissao_final')
        vencto_inicial = self.request.GET.get('vencto_inicial')
        vencto_final = self.request.GET.get('vencto_final')
        situacao_aberto = self.request.GET.get('situacao_aberto')
        situacao_pago_parcial = self.request.GET.get('situacao_pago_parcial')
        situacao_pago_total = self.request.GET.get('situacao_pago_total')

        if search:
            queryset = queryset.filter(
                Q(documento__icontains=search) |
                Q(contato__razao_social__icontains=search) |
                Q(contato__cpf_cnpj__icontains=search)
            )

        lista = []

        if situacao_aberto:
            lista.append(SituacaoFinanceiro.ABERTO)

        if situacao_pago_parcial:
            lista.append(SituacaoFinanceiro.PAGO_PARCIAL)

        if situacao_pago_total:
            lista.append(SituacaoFinanceiro.PAGO_TOTAL)

        if len(lista) > 0:
            queryset = queryset.filter(
                situacao__in=lista
            )

        if emissao_inicial:
            queryset = queryset.filter(
                data_emissao__gte=emissao_inicial
            )
        if emissao_final:
            queryset = queryset.filter(
                data_emissao__lte=emissao_final
            )

        if vencto_inicial:
            queryset = queryset.filter(
                data_vencimento__gte=vencto_inicial
            )

        if vencto_final:
            queryset = queryset.filter(
                data_vencimento__lte=vencto_final
            )

        queryset = queryset.annotate(
            vencido=Case(
                When(situacao__in=[SituacaoFinanceiro.ABERTO, SituacaoFinanceiro.PAGO_PARCIAL],
                     data_vencimento__lt=datetime.date.today(), then=Value(True)),
                When(data_vencimento__gte=datetime.date.today(), then=Value(False)),
                default=Value(False)
            )
        )
        return queryset
    

class ContaReceberCreate(UserAccessMixin, InvalidFormMixin, SuccessMessageMixin, CreateView):
    permission_required = ["financeiro.add_contareceber"]
    model = ContaReceber
    form_class = ContaReceberForm
    template_name = 'financeiro/contareceber/form.html'
    success_url = '/contarecebers'
    success_message = MSG_CREATED_SUCCESS 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context

    
class ContaReceberUpdateView(UserAccessMixin, InvalidFormMixin, SuccessMessageMixin, UpdateView):
    permission_required = ["financeiro.change_contareceber"]
    model = ContaReceber
    form_class = ContaReceberForm
    template_name = 'financeiro/contareceber/form.html'
    success_url = '/contarecebers'
    success_message = MSG_UPDATED_SUCCESS

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.situacao != 1:
            messages.add_message(request, messages.WARNING, 'Titulo pago ou parcialmente pago não pode ser editado.')
            return redirect('/contarecebers')
        return super().get(request, *args, **kwargs)  


class ContaReceberDeleteView(UserAccessMixin, SuccessMessageMixin, DeleteView):
    permission_required = ["financeiro.delete_contareceber"]
    model = ContaReceber
    template_name = 'financeiro/contareceber/confirm_delete.html'
    success_url = reverse_lazy('contareceber-list')
    success_message = MSG_DELETED_SUCCESS

    def get(self, request, *args, **kwargs):
        conta = ContaReceber.objects.get(pk=self.kwargs['pk'])
        if conta.situacao != 1:
            messages.add_message(request, messages.WARNING, "Título pago ou parcialmente pago não pode ser removido.")
            return redirect('/contarecebers')
        return super().get(request, *args, **kwargs)


class ContaPagarListView(UserAccessMixin, ListView):
    permission_required = ["financeiro.view_contapagar"]
    model = ContaPagar
    template_name = 'financeiro/contapagar/list.html'
    paginate_by = REGISTROS_POR_PAGINA

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        context['verbose_name_plural'] = self.model._meta.verbose_name_plural.title
        search = self.request.GET.get('search')

        emissao_inicial = self.request.GET.get('emissao_inicial')
        emissao_final = self.request.GET.get('emissao_final')

        vencto_inicial = self.request.GET.get('vencto_inicial')
        vencto_final = self.request.GET.get('vencto_final')

        situacao_aberto = self.request.GET.get('situacao_aberto')
        situacao_pago_parcial = self.request.GET.get('situacao_pago_parcial')
        situacao_pago_total = self.request.GET.get('situacao_pago_total')

        if situacao_aberto is not None:
            context['situacao_aberto'] = situacao_aberto

        if situacao_pago_parcial is not None:
            context['situacao_pago_parcial'] = situacao_pago_parcial

        if situacao_pago_total is not None:
            context['situacao_pago_total'] = situacao_pago_total

        if emissao_inicial is not None and emissao_inicial != "":
            context['emissao_inicial'] = emissao_inicial

        if emissao_final is not None and emissao_final != "":
            context['emissao_final'] = emissao_final

        if vencto_inicial is not None and vencto_inicial != "":
            context['vencto_inicial'] = vencto_inicial

        if vencto_final is not None and vencto_final != "":
            context['vencto_final'] = vencto_final

        if search:
            context['search'] = search

        return context

    def get_queryset(self):
        queryset = super(ContaPagarListView, self).get_queryset()

        search = self.request.GET.get('search')
        emissao_inicial = self.request.GET.get('emissao_inicial')
        emissao_final = self.request.GET.get('emissao_final')
        vencto_inicial = self.request.GET.get('vencto_inicial')
        vencto_final = self.request.GET.get('vencto_final')
        situacao_aberto = self.request.GET.get('situacao_aberto')
        situacao_pago_parcial = self.request.GET.get('situacao_pago_parcial')
        situacao_pago_total = self.request.GET.get('situacao_pago_total')

        if search:
            queryset = queryset.filter(
                Q(documento__icontains=search) |
                Q(contato__razao_social__icontains=search) |
                Q(contato__cpf_cnpj__icontains=search)
            )

        lista = []

        if situacao_aberto:
            lista.append(SituacaoFinanceiro.ABERTO)

        if situacao_pago_parcial:
            lista.append(SituacaoFinanceiro.PAGO_PARCIAL)

        if situacao_pago_total:
            lista.append(SituacaoFinanceiro.PAGO_TOTAL)

        if len(lista) > 0:
            queryset = queryset.filter(
                situacao__in=lista
            )

        if emissao_inicial:
            queryset = queryset.filter(
                data_emissao__gte=emissao_inicial
            )
        if emissao_final:
            queryset = queryset.filter(
                data_emissao__lte=emissao_final
            )

        if vencto_inicial:
            queryset = queryset.filter(
                data_vencimento__gte=vencto_inicial
            )

        if vencto_final:
            queryset = queryset.filter(
                data_vencimento__lte=vencto_final
            )

        queryset = queryset.annotate(
            vencido=Case(
                When(situacao__in=[SituacaoFinanceiro.ABERTO, SituacaoFinanceiro.PAGO_PARCIAL],
                     data_vencimento__lt=datetime.date.today(), then=Value(True)),
                When(data_vencimento__gte=datetime.date.today(), then=Value(False)),
                default=Value(False)
            )
        )
        return queryset


class ContaPagarUpdateView(UserAccessMixin, InvalidFormMixin, SuccessMessageMixin, UpdateView):
    permission_required = ["financeiro.change_contapagar"]
    model = ContaPagar
    form_class = ContaPagarForm
    template_name = 'financeiro/contapagar/form.html'
    success_url = '/contapagars'
    success_message = MSG_UPDATED_SUCCESS

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class ContaPagarCreateView(UserAccessMixin, InvalidFormMixin, SuccessMessageMixin, CreateView):
    permission_required = ["financeiro.add_contapagar"]
    model = ContaPagar
    form_class = ContaPagarForm
    template_name = 'financeiro/contapagar/form.html'
    success_url = '/contapagars'
    success_message = MSG_CREATED_SUCCESS

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class ContaPagarDeleteView(UserAccessMixin, SuccessMessageMixin, DeleteView):
    permission_required = ["financeiro.delete_contapagar"]
    model = ContaPagar
    template_name = 'financeiro/contapagar/confirm_delete.html'
    success_url = reverse_lazy('contapagar-list')
    success_message = MSG_DELETED_SUCCESS

    def get(self, request, *args, **kwargs):
        conta = ContaPagar.objects.get(pk=self.kwargs['pk'])
        if conta.situacao != SituacaoFinanceiro.ABERTO:
            messages.add_message(request, messages.WARNING, "Título pago ou parcialmente pago não pode ser removido.")
            return redirect('/contapagars')
        return super().get(request, *args, **kwargs)


class BaixarContaPagarView(UserAccessMixin, InvalidFormMixin, SuccessMessageMixin, CreateView):
    template_name = 'financeiro/baixapagar/form.html'
    form_class = BaixaPagarForm
    success_url = reverse_lazy('contapagar-list')
    permission_required = ['financeiro.add_baixapagar']
    model = BaixaPagar
    fail_url = '/contapagars'
    success_message = 'Baixa efetuada com sucesso.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conta = ContaPagar.objects.get(pk=self.kwargs['contapagar'])
        context['verbose_name'] = self.model._meta.verbose_name.title
        context['conta'] = conta
        return context

    def get(self, request, *args, **kwargs):
        conta = ContaPagar.objects.get(pk=kwargs['contapagar'])
        if conta.situacao == SituacaoFinanceiro.PAGO_TOTAL:
            messages.add_message(request, messages.WARNING, 'Titulo ja foi pago totalmente.')
            return redirect('/contapagars')
        return super().get(request, *args, **kwargs)


class EstornarContaPagarView(UserAccessMixin, FormView):
    success_url = reverse_lazy('contapagar-list')
    template_name = 'financeiro/baixapagar/estorno.html'
    form_class = BaixaPagarForm
    permission_required = ['financeiro.add_baixapagar']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        baixas = BaixaPagar.objects.filter(contapagar=self.kwargs['contapagar'])
        conta = ContaPagar.objects.get(pk=self.kwargs['contapagar'])
        context['baixas'] = baixas
        context['conta'] = conta
        return context

    def get(self, request, *args, **kwargs):
        baixas = BaixaPagar.objects.filter(contapagar=kwargs['contapagar'])
        if len(baixas) == 0:
            messages.add_message(request, messages.INFO, 'Sem baixa para estorno')
            return redirect('/contapagars')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pk = request.POST.get('contapagar')
        ids = request.POST.getlist('check')
        baixas = self.get_context_data()['baixas']

        if pk is not None:
            if len(ids) == 0:
                messages.add_message(request, messages.ERROR, 'Nenhum titulo foi marcado para estorno.')
                conta = ContaPagar.objects.get(pk=request.POST.get('contapagar'))
                return self.render_to_response({'baixas': baixas, 'conta': conta})
            try:
                BaixaPagar.objects.filter(contapagar=pk, pk__in=ids).delete()
                pagar = ContaPagar.objects.get(pk=pk)

                if BaixaPagar.objects.filter(contapagar=pk).exists():
                    pagar.situacao = SituacaoFinanceiro.PAGO_PARCIAL
                else:
                    pagar.situacao = SituacaoFinanceiro.ABERTO

                pagar.save()

                messages.add_message(request, messages.SUCCESS, 'Titulo estornado com sucesso.')
                return redirect('/contapagars')
            except ProtectedError:
                messages.add_message(request, messages.ERROR, 'Erro ao estornar titulo.')
                return redirect('/contapagars')
        return super().post(request, *args, **kwargs)
