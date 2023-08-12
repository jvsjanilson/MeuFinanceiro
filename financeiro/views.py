from django.views.generic.list import ListView
from django.views.generic import CreateView, UpdateView, DeleteView
from financeiro.models import ContaReceber
from core.constants import REGISTROS_POR_PAGINA
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from core.views import UserAccessMixin, InvalidFormMixin
from financeiro.forms import ContaReceberForm


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
        print(context)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context
    
    def form_invalid(self, form):
        print(form)
        return super().form_invalid(form)    
    
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


class ContaReceberDeleteView(UserAccessMixin, DeleteView):
    permission_required = ["financeiro.delete_contareceber"]
    model = ContaReceber
    template_name = 'financeiro/contareceber/confirm_delete.html'
    success_url = '/contarecebers'
