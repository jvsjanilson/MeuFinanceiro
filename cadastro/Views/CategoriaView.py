from cadastro.models import Categoria
from cadastro.forms import CategoriaForm
from core.views import UserAccessMixin, InvalidFormMixin, DeleteExceptionMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from core.constants import REGISTROS_POR_PAGINA, MSG_CREATED_SUCCESS, MSG_UPDATED_SUCCESS, \
    MSG_DELETED_SUCCESS
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

template_root = 'cadastro/categoria/'


class CategoriaListView(UserAccessMixin, ListView):
    permission_required = ["cadastro.view_categoria"]
    model = Categoria
    template_name =  f'{template_root}list.html'
    paginate_by = REGISTROS_POR_PAGINA
    ordering = ('-id',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        context['verbose_name_plural'] = self.model._meta.verbose_name_plural.title
        search = self.request.GET.get('search')

        if search:
            context['search'] = search

        return context

    def get_queryset(self):
        queryset = super(CategoriaListView, self).get_queryset()
        search = self.request.GET.get('search')
        if search:
            return queryset.filter(
                Q(nome__icontains=search)
            )
        return queryset


class CategoriaCreateView(UserAccessMixin, InvalidFormMixin, CreateView):
    permission_required = ["cadastro.add_categoria"]
    model = Categoria
    form_class = CategoriaForm
    template_name = f'{template_root}form.html'
    success_url = reverse_lazy('categoria-list')
    fail_url = reverse_lazy('categoria-list')
    success_message = MSG_CREATED_SUCCESS

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class CategoriaUpdateView(UserAccessMixin, InvalidFormMixin, UpdateView):
    permission_required = ["cadastro.change_categoria"]
    model = Categoria
    form_class = CategoriaForm
    template_name = f'{template_root}form.html'
    success_url = reverse_lazy('categoria-list')
    success_message = MSG_UPDATED_SUCCESS

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class CategoriaDeleteView(UserAccessMixin, SuccessMessageMixin, DeleteExceptionMixin, DeleteView):
    permission_required = ["cadastro.delete_categoria"]
    model = Categoria
    template_name = f'{template_root}confirm_delete.html'
    success_url = reverse_lazy('categoria-list')
    success_message = MSG_DELETED_SUCCESS
