from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from cadastro.models import Unidade, Marca, Categoria
from core.constants import REGISTROS_POR_PAGINA
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.views import redirect_to_login


def home(request):
    return render(request, 'base.html')


class UserAccessMixin(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(),
                                     self.get_login_url(), self.get_redirect_field_name())
        if not self.has_permission():
            return redirect('/' if self.login_url is None else self.login_url)

        return super(UserAccessMixin, self).dispatch(request, *args, **kwargs)


class UnidadeListView(UserAccessMixin, ListView):
    permission_required = ["cadastro.view_unidade"]
    login_url = '/unidades/'
    model = Unidade
    template_name = 'cadastro/unidade/list.html'
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
        queryset = super(UnidadeListView, self).get_queryset()
        search = self.request.GET.get('search')
        if search:
            return queryset.filter(
                Q(codigo__icontains=search) |
                Q(nome__icontains=search)
            )
        return queryset


class UnidadeCreateView(UserAccessMixin, CreateView):
    permission_required = ["cadastro.add_unidade"]
    login_url = '/unidades/'
    model = Unidade
    template_name = 'cadastro/unidade/form.html'
    fields = ['codigo', 'nome']
    success_url = '/unidades'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class UnidadeUpdateView(UserAccessMixin, UpdateView):
    permission_required = ["cadastro.change_unidade"]
    login_url = '/unidades/'
    model = Unidade
    template_name = 'cadastro/unidade/form.html'
    fields = ['codigo', 'nome']
    success_url = '/unidades'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class UnidadeDeleteView(UserAccessMixin, DeleteView):
    permission_required = ["cadastro.delete_unidade"]
    login_url = '/unidades/'
    model = Unidade
    template_name = 'cadastro/unidade/confirm_delete.html'
    success_url = '/unidades'


class MarcaListView(UserAccessMixin, ListView):
    permission_required = ["cadastro.view_marca"]
    login_url = '/marcas/'
    model = Marca
    template_name = 'cadastro/marca/list.html'
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
        queryset = super(MarcaListView, self).get_queryset()
        search = self.request.GET.get('search')
        if search:
            return queryset.filter(
                Q(nome__icontains=search)
            )
        return queryset


class MarcaCreateView(UserAccessMixin, CreateView):
    permission_required = ["cadastro.add_marca"]
    login_url = '/marcas/'
    model = Marca
    template_name = 'cadastro/marca/form.html'
    fields = ['nome']
    success_url = '/marcas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class MarcaUpdateView(UserAccessMixin, UpdateView):
    permission_required = ["cadastro.change_marca"]
    login_url = '/marcas/'
    model = Marca
    template_name = 'cadastro/marca/form.html'
    fields = ['nome']
    success_url = '/marcas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class MarcaDeleteView(UserAccessMixin, DeleteView):
    permission_required = ["cadastro.delete_marca"]
    login_url = '/marcas/'
    model = Marca
    template_name = 'cadastro/marca/confirm_delete.html'
    success_url = '/marcas'


class CategoriaListView(UserAccessMixin, ListView):
    permission_required = ["cadastro.view_categoria"]
    login_url = '/categorias/'
    model = Categoria
    template_name = 'cadastro/categoria/list.html'
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


class CategoriaCreateView(UserAccessMixin, CreateView):
    permission_required = ["cadastro.add_categoria"]
    login_url = '/categorias/'
    model = Categoria
    template_name = 'cadastro/categoria/form.html'
    fields = ['nome']
    success_url = '/categorias'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class CategoriaUpdateView(UserAccessMixin, UpdateView):
    permission_required = ["cadastro.change_categoria"]
    login_url = '/categorias/'
    model = Categoria
    template_name = 'cadastro/categoria/form.html'
    fields = ['nome']
    success_url = '/categorias'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class CategoriaDeleteView(UserAccessMixin, DeleteView):
    permission_required = ["cadastro.delete_categoria"]
    login_url = '/categorias/'
    model = Categoria
    template_name = 'cadastro/marca/confirm_delete.html'
    success_url = '/categorias'
