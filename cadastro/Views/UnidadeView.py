from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from cadastro.models import Unidade
from core.views import UserAccessMixin, InvalidFormMixin, DeleteExceptionMixin
from core.constants import REGISTROS_POR_PAGINA, MSG_CREATED_SUCCESS, MSG_UPDATED_SUCCESS, \
    MSG_DELETED_SUCCESS
from cadastro.forms import UnidadeForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db.models import Q

template_root = 'cadastro/unidade/'


class UnidadeListView(UserAccessMixin, ListView):
    permission_required = ["cadastro.view_unidade"]
    model = Unidade
    template_name = f'{template_root}list.html'
    paginate_by = REGISTROS_POR_PAGINA

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name
        context['verbose_name_plural'] = self.model._meta.verbose_name_plural
        search = self.request.GET.get('search')

        if search:
            context['search'] = search

        return context

    def get_queryset(self):
        queryset = super(UnidadeListView, self).get_queryset()
        search = self.request.GET.get('search')
        if search:
            return queryset.filter(
                Q(codigo__icontains=search) |
                Q(nome__icontains=search)
            )
        return queryset


class UnidadeCreateView(UserAccessMixin, InvalidFormMixin, SuccessMessageMixin, CreateView):
    permission_required = ["cadastro.add_unidade"]
    model = Unidade
    form_class = UnidadeForm
    template_name = f'{template_root}form.html'
    success_url = reverse_lazy('unidade-list')
    success_message = MSG_CREATED_SUCCESS
    fail_url = reverse_lazy('unidade-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class UnidadeUpdateView(UserAccessMixin, InvalidFormMixin, SuccessMessageMixin, UpdateView):
    permission_required = ["cadastro.change_unidade"]
    model = Unidade
    form_class = UnidadeForm
    template_name = f'{template_root}form.html'
    success_url = reverse_lazy('unidade-list')
    success_message = MSG_UPDATED_SUCCESS

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context

    def form_invalid(self, form):
        return super().form_invalid(form)


class UnidadeDeleteView(UserAccessMixin, SuccessMessageMixin, DeleteExceptionMixin, DeleteView):
    permission_required = ["cadastro.delete_unidade"]
    model = Unidade
    template_name = f'{template_root}confirm_delete.html'
    success_url = reverse_lazy('unidade-list')
    success_message = MSG_DELETED_SUCCESS
