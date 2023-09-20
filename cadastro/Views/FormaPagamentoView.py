from core.views import UserAccessMixin, InvalidFormMixin, DeleteExceptionMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from core.constants import REGISTROS_POR_PAGINA, MSG_CREATED_SUCCESS, MSG_UPDATED_SUCCESS, \
    MSG_DELETED_SUCCESS
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from cadastro.models import FormaPagamento
from cadastro.forms import FormaPagamentoForm

template_root = 'cadastro/formapagamento/'


class FormaPagamentoListView(UserAccessMixin, ListView):
    permission_required = ["cadastro.view_formpagamento"]
    model = FormaPagamento
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
        queryset = super(FormaPagamentoListView, self).get_queryset()
        search = self.request.GET.get('search')
        if search:
            return queryset.filter(
                Q(nome__icontains=search) |
                Q(codigo__icontains=search)
            )
        return queryset


class FormaPagamentoCreateView(UserAccessMixin, InvalidFormMixin, CreateView):
    permission_required = ["cadastro.add_formapagamento"]
    model = FormaPagamento
    form_class = FormaPagamentoForm
    template_name = f'{template_root}form.html'
    success_url = reverse_lazy('formapagamento-list')
    fail_url = reverse_lazy('formapagamento-list')
    success_message = MSG_CREATED_SUCCESS

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class FormaPagamentoUpdateView(UserAccessMixin, InvalidFormMixin, UpdateView):
    permission_required = ["cadastro.change_formapagamento"]
    model = FormaPagamento
    form_class = FormaPagamentoForm
    template_name = f'{template_root}form.html'
    success_url = reverse_lazy('formapagamento-list')
    success_message = MSG_UPDATED_SUCCESS

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class FormaPagamentoDeleteView(UserAccessMixin, SuccessMessageMixin, DeleteExceptionMixin, DeleteView):
    permission_required = ["cadastro.delete_formapagamento"]
    model = FormaPagamento
    template_name = f'{template_root}confirm_delete.html'
    success_url = reverse_lazy('formapagamento-list')
    success_message = MSG_DELETED_SUCCESS

