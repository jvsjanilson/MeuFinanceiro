import decimal
from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView, DeleteView, FormView
from financeiro.models import ContaReceber, BaixaReceber
from core.constants import REGISTROS_POR_PAGINA
from django.db.models import Q
from django.shortcuts import redirect
from core.views import UserAccessMixin, InvalidFormMixin
from financeiro.forms import ContaReceberForm
from django.urls import reverse_lazy
from django.contrib import messages
from financeiro.choices import SituacaoFinanceiro
from financeiro.forms import BaixaReceberForm
from django.db.models import ProtectedError


class EstornarContaReceber(UserAccessMixin, FormView):
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
        conta = request.POST.get('contareceber')
        if conta is not None:
            try:
                BaixaReceber.objects.filter(contareceber=conta).delete()
                receber = ContaReceber.objects.get(pk=conta)
                receber.situacao = SituacaoFinanceiro.ABERTO
                receber.save()

                messages.add_message(request, messages.SUCCESS, 'Titulo estornado com sucesso.')
                return redirect('/contarecebers')
            except ProtectedError:
                messages.add_message(request, messages.ERROR, 'Erro ao estornar titulo.')
                return redirect('/contarecebers')
        return super().post(request, *args, **kwargs)


class BaixarContaReceber(UserAccessMixin, InvalidFormMixin, CreateView):
    template_name = 'financeiro/baixareceber/form.html'
    form_class = BaixaReceberForm
    success_url = reverse_lazy('contareceber-list')
    permission_required = ['financeiro.add_baixareceber']
    model = BaixaReceber
    fail_url = '/contarecebers'

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

    def post(self, request, *args, **kwargs):
        self.object = None
        context = self.get_context_data()
        conta = ContaReceber.objects.get(pk=kwargs['contareceber'])

        if decimal.Decimal(request.POST.get('valor_pago')) > conta.saldo_pagar:
            messages.add_message(request, messages.WARNING,
                                 'Valor do pagamento maior que o saldo devedor. Informe um valor menor ou igual.')
            return self.render_to_response(context)
        else:
            return super().post(request, *args, **kwargs)


class ContaReceberListView(UserAccessMixin, ListView):
    permission_required = ["financeiro.view_contareceber"]
    model = ContaReceber
    template_name = 'financeiro/contareceber/list.html'
    paginate_by = REGISTROS_POR_PAGINA

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        context['verbose_name_plural'] = self.model._meta.verbose_name_plural.title
        search = self.request.GET.get('search')

        if search:
            context['search'] = search

        return context

    def get_queryset(self):
        queryset = super(ContaReceberListView, self).get_queryset()
        search = self.request.GET.get('search')
        if search:
            return queryset.filter(
                Q(documento__icontains=search) |
                Q(contato__razao_social__icontains=search)
            )
        return queryset
    

class ContaReceberCreate(UserAccessMixin, InvalidFormMixin, CreateView):
    permission_required = ["financeiro.add_contareceber"]
    model = ContaReceber
    form_class = ContaReceberForm
    template_name = 'financeiro/contareceber/form.html'
    success_url = '/contarecebers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context

    
class ContaReceberUpdateView(UserAccessMixin, InvalidFormMixin, UpdateView):
    permission_required = ["financeiro.change_contareceber"]
    model = ContaReceber
    form_class = ContaReceberForm
    template_name = 'financeiro/contareceber/form.html'
    success_url = '/contarecebers'

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


class ContaReceberDeleteView(UserAccessMixin, DeleteView):
    permission_required = ["financeiro.delete_contareceber"]
    model = ContaReceber
    template_name = 'financeiro/contareceber/confirm_delete.html'
    success_url = reverse_lazy('contareceber-list')

    def get(self, request, *args, **kwargs):
        conta = ContaReceber.objects.get(pk=self.kwargs['pk'])
        if conta.situacao != 1:
            messages.add_message(request, messages.WARNING, "Título pago ou parcialmente pago não pode ser removido.")
            return redirect('/contarecebers')
        return super().get(request, *args, **kwargs)
