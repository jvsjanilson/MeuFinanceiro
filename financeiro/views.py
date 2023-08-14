from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView, DeleteView, FormView
from financeiro.models import ContaReceber, BaixaReceber
from core.constants import REGISTROS_POR_PAGINA
from django.db.models import Q
from django.shortcuts import redirect
from core.views import UserAccessMixin, InvalidFormMixin
from financeiro.forms import ContaReceberForm, BaixaReceberForm
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from financeiro.choices import SituacaoFinanceiro
from django.db.models import Sum


class BaixarTitulo(UserAccessMixin, InvalidFormMixin, CreateView):
    template_name = 'financeiro/baixareceber/form.html'
    form_class = BaixaReceberForm
    success_url = reverse_lazy('contareceber-list')
    permission_required = ['financeiro.add_baixareceber']
    model = BaixaReceber

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contareceber = ContaReceber.objects.get(pk=self.kwargs['contareceber'])
        total_pago = BaixaReceber.objects.filter(contareceber=self.kwargs['contareceber']).aggregate(total=Sum('valor_pago'))['total']
        saldo = contareceber.valor_titulo - total_pago

        context['verbose_name'] = self.model._meta.verbose_name.title
        context['conta'] = contareceber
        context['saldo'] = saldo
        return context
    

    def get(self, request, *args, **kwargs):
        conta = ContaReceber.objects.get(pk=kwargs['contareceber'])
        if conta.situacao == SituacaoFinanceiro.PAGO_TOTAL:
            messages.add_message(request, messages.WARNING, 'Titulo ja foi pago totalmente.')
            return redirect('/contarecebers')
        self.object = None
        return super().get(request, *args, **kwargs)


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
