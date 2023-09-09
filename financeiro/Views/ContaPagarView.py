import datetime
from core.views import UserAccessMixin, InvalidFormMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from financeiro.models import ContaPagar
from core.constants import REGISTROS_POR_PAGINA, MSG_CREATED_SUCCESS, MSG_DELETED_SUCCESS, MSG_UPDATED_SUCCESS
from django.shortcuts import redirect
from django.db.models import Q
from financeiro.choices import SituacaoFinanceiro
from django.db.models import Case, Value, When
from django.contrib.messages.views import SuccessMessageMixin
from financeiro.forms import ContaPagarForm
from django.contrib import messages
from django.urls import reverse_lazy


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


class ContaPagarUpdateView(UserAccessMixin, InvalidFormMixin, SuccessMessageMixin, UpdateView):
    permission_required = ["financeiro.change_contapagar"]
    model = ContaPagar
    form_class = ContaPagarForm
    template_name = 'financeiro/contapagar/form.html'
    success_url = '/contapagars'
    success_message = MSG_UPDATED_SUCCESS

    def __init__(self):
        super().__init__()
        self.object = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.situacao != 1:
            messages.add_message(request, messages.WARNING, 'Titulo pago ou parcialmente pago não pode ser editado.')
            return redirect('/contapagars')
        return super().get(request, *args, **kwargs)


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
