from core.views import UserAccessMixin, InvalidFormMixin, DeleteExceptionMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from core.constants import REGISTROS_POR_PAGINA, MSG_CREATED_SUCCESS, MSG_UPDATED_SUCCESS, \
    MSG_DELETED_SUCCESS
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from cadastro.models import Contato
from cadastro.forms import ContatoForm

template_root = 'cadastro/contato/'


class ContatoListView(UserAccessMixin, ListView):
    permission_required = ["cadastro.view_contato"]
    model = Contato
    template_name = f'{template_root}list.html'
    paginate_by = REGISTROS_POR_PAGINA

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        context['verbose_name_plural'] = self.model._meta.verbose_name_plural.title
        context['count'] = Contato.objects.all().count()
        search = self.request.GET.get('search')

        if search:
            context['search'] = search

        return context

    def get_queryset(self):
        queryset = super(ContatoListView, self).get_queryset()
        search = self.request.GET.get('search')
        if search:
            return queryset.filter(
                Q(razao_social__icontains=search) |
                Q(nome_fantasia__icontains=search) |
                Q(cpf_cnpj__icontains=search) |
                Q(inscricao_estadual__icontains=search) |
                Q(celular__icontains=search) |
                Q(fone__icontains=search)
            )
        return queryset


class ContatoCreateView(UserAccessMixin, InvalidFormMixin, CreateView):
    permission_required = ["cadastro.add_contato"]
    model = Contato
    form_class = ContatoForm
    template_name = f'{template_root}form.html'
    success_url = reverse_lazy('contato-list')
    fail_url = reverse_lazy('contato-list')
    success_message = MSG_CREATED_SUCCESS

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class ContatoUpdateView(UserAccessMixin, InvalidFormMixin, UpdateView):
    permission_required = ["cadastro.change_contato"]
    model = Contato
    form_class = ContatoForm
    template_name = f'{template_root}form.html'
    success_message = MSG_UPDATED_SUCCESS

    def get_success_url(self):
        page_number = self.request.GET['page']
        return f'{reverse("contato-list")}?page={page_number}'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class ContatoDeleteView(UserAccessMixin, SuccessMessageMixin, DeleteExceptionMixin, DeleteView):
    permission_required = ["cadastro.delete_contato"]
    model = Contato
    template_name = f'{template_root}confirm_delete.html'
    success_url = reverse_lazy('contato-list')
    success_message = MSG_DELETED_SUCCESS
