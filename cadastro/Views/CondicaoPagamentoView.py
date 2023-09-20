from core.views import UserAccessMixin, InvalidFormMixin, DeleteExceptionMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from core.constants import REGISTROS_POR_PAGINA, MSG_CREATED_SUCCESS, MSG_UPDATED_SUCCESS, \
    MSG_DELETED_SUCCESS
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from cadastro.models import CondicaoPagamento
from cadastro.forms import CondicaoPagamentoForm

template_root = 'cadastro/condicaopagamento/'


class CondicaoPagamentoListView(UserAccessMixin, ListView):
    permission_required = ["cadastro.view_condicaopagamento"]
    model = CondicaoPagamento
    template_name = f'{template_root}list.html'
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
        queryset = super(CondicaoPagamentoListView, self).get_queryset()
        search = self.request.GET.get('search')
        if search:
            return queryset.filter(
                Q(nome__icontains=search)
            )
        return queryset


class CondicaoPagamentoCreateView(UserAccessMixin, InvalidFormMixin, CreateView):
    permission_required = ["cadastro.add_condicaopagamento"]
    model = CondicaoPagamento
    form_class = CondicaoPagamentoForm
    template_name = f'{template_root}form.html'
    success_url = reverse_lazy('condicaopagamento-list')
    fail_url = reverse_lazy('condicaopagamento-list')
    success_message = MSG_CREATED_SUCCESS

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class CondicaoPagamentoUpdateView(UserAccessMixin, InvalidFormMixin, UpdateView):
    permission_required = ["cadastro.change_condicaopagamento"]
    model = CondicaoPagamento
    form_class = CondicaoPagamentoForm
    template_name = f'{template_root}form.html'
    success_url = reverse_lazy('condicaopagamento-list')
    success_message = MSG_UPDATED_SUCCESS

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class CondicaoPagamentoDeleteView(UserAccessMixin, SuccessMessageMixin, DeleteExceptionMixin, DeleteView):
    permission_required = ["cadastro.delete_condicaopagamento"]
    model = CondicaoPagamento
    template_name = f'{template_root}confirm_delete.html'
    success_url = reverse_lazy('condicaopagamento-list')
    success_message = MSG_DELETED_SUCCESS
