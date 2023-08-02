from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from cadastro.models import Unidade, Marca, Categoria, Pais, Estado, Municipio, Produto
from core.constants import REGISTROS_POR_PAGINA
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.views import redirect_to_login
from cadastro.forms import ProdutoForm, UnidadeForm


class InvalidFormMixin:
    """
        Autor: Janilson Varele
        Mixin para preencher os input com a class is-invalid 
        do bootstrap quando houver error
    """
    def form_invalid(self, form):
        for field in form.errors:
            form[field].field.widget.attrs['class'] += ' is-invalid'
        return self.render_to_response(self.get_context_data(form=form))


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'base.html'


class UserAccessMixin(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(),
                                     self.get_login_url(), self.get_redirect_field_name())
        if not self.has_permission():
            return redirect('/')

        return super(UserAccessMixin, self).dispatch(request, *args, **kwargs)


class UnidadeListView(UserAccessMixin, ListView):
    permission_required = ["cadastro.view_unidade"]
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


class UnidadeCreateView(UserAccessMixin, InvalidFormMixin, CreateView):
    permission_required = ["cadastro.add_unidade"]
    model = Unidade
    form_class = UnidadeForm
    template_name = 'cadastro/unidade/form.html'
    success_url = '/unidades'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class UnidadeUpdateView(UserAccessMixin, InvalidFormMixin, UpdateView):
    permission_required = ["cadastro.change_unidade"]
    model = Unidade
    form_class = UnidadeForm
    template_name = 'cadastro/unidade/form.html'
    success_url = '/unidades'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class UnidadeDeleteView(UserAccessMixin, DeleteView):
    permission_required = ["cadastro.delete_unidade"]
    model = Unidade
    template_name = 'cadastro/unidade/confirm_delete.html'
    success_url = '/unidades'


class MarcaListView(UserAccessMixin, ListView):
    permission_required = ["cadastro.view_marca"]
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
    model = Marca
    template_name = 'cadastro/marca/confirm_delete.html'
    success_url = '/marcas'


class CategoriaListView(UserAccessMixin, ListView):
    permission_required = ["cadastro.view_categoria"]
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
    model = Categoria
    template_name = 'cadastro/categoria/confirm_delete.html'
    success_url = '/categorias'


class PaisListView(UserAccessMixin, ListView):
    permission_required = ["cadastro.view_pais"]

    model = Pais
    template_name = 'cadastro/pais/list.html'
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
        queryset = super(PaisListView, self).get_queryset()
        search = self.request.GET.get('search')
        if search:
            return queryset.filter(
                Q(codigo__icontains=search) |
                Q(nome__icontains=search)
            )
        return queryset


class PaisCreateView(UserAccessMixin, CreateView):
    permission_required = ["cadastro.add_pais"]
    model = Pais
    template_name = 'cadastro/pais/form.html'
    fields = ['codigo', 'nome']
    success_url = '/pais'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class PaisUpdateView(UserAccessMixin, UpdateView):
    permission_required = ["cadastro.change_pais"]
    model = Pais
    template_name = 'cadastro/pais/form.html'
    fields = ['codigo', 'nome']
    success_url = '/pais'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class PaisDeleteView(UserAccessMixin, DeleteView):
    permission_required = ["cadastro.delete_pais"]
    model = Pais
    template_name = 'cadastro/pais/confirm_delete.html'
    success_url = '/pais'


class EstadoListView(UserAccessMixin, ListView):
    permission_required = ["cadastro.view_estado"]
    model = Estado
    template_name = 'cadastro/estado/list.html'
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
        queryset = super(EstadoListView, self).get_queryset()
        search = self.request.GET.get('search')
        if search:
            return queryset.filter(
                Q(codigo__icontains=search) |
                Q(uf__icontains=search) |
                Q(pais__nome__icontains=search) |
                Q(nome__icontains=search)
            )
        return queryset


class EstadoCreateView(UserAccessMixin, CreateView):
    permission_required = ["cadastro.add_estado"]
    model = Estado

    template_name = 'cadastro/estado/form.html'
    fields = ['codigo', 'uf', 'pais', 'nome']
    success_url = '/estados'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class EstadoUpdateView(UserAccessMixin, UpdateView):
    permission_required = ["cadastro.change_estado"]
    model = Estado
    template_name = 'cadastro/estado/form.html'
    fields = ['codigo', 'uf', 'pais', 'nome']
    success_url = '/estados'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class EstadoDeleteView(UserAccessMixin, DeleteView):
    permission_required = ["cadastro.delete_estado"]
    model = Estado
    template_name = 'cadastro/estado/confirm_delete.html'
    success_url = '/estados'



class MunicipioListView(UserAccessMixin, ListView):
    permission_required = ["cadastro.view_municipio"]
    model = Municipio
    template_name = 'cadastro/municipio/list.html'
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
        queryset = super(MunicipioListView, self).get_queryset()
        search = self.request.GET.get('search')
        if search:
            return queryset.filter(
                Q(codigo__icontains=search) |
                Q(estado__uf__icontains=search) |
                Q(nome__icontains=search)
            )
        return queryset


class MunicipioCreateView(UserAccessMixin, CreateView):
    permission_required = ["cadastro.add_municipio"]
    model = Municipio

    template_name = 'cadastro/municipio/form.html'
    fields = ['codigo', 'nome', 'estado', 'capital']
    success_url = '/municipios'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class MunicipioUpdateView(UserAccessMixin, UpdateView):
    permission_required = ["cadastro.change_municipio"]
    model = Municipio
    template_name = 'cadastro/municipio/form.html'
    fields = ['codigo', 'nome', 'estado', 'capital']
    success_url = '/municipios'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class MunicipioDeleteView(UserAccessMixin, DeleteView):
    permission_required = ["cadastro.delete_municipio"]
    model = Municipio
    template_name = 'cadastro/municipio/confirm_delete.html'
    success_url = '/municipios'



class ProdutoListView(UserAccessMixin, ListView):
    permission_required = ["cadastro.view_produto"]
    model = Produto
    template_name = 'cadastro/produto/list.html'
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
        queryset = super(ProdutoListView, self).get_queryset()
        search = self.request.GET.get('search')
        if search:
            return queryset.filter(
                Q(codigo__icontains=search) |
                Q(nome__icontains=search)
            )
        return queryset    
    

class ProdutoCreateView(UserAccessMixin, InvalidFormMixin, CreateView):
    permission_required = ["cadastro.add_produto"]
    model = Produto
    form_class = ProdutoForm
    template_name = 'cadastro/produto/form.html'
    success_url = '/produtos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class ProdutoUpdateView(UserAccessMixin, InvalidFormMixin, UpdateView):
    permission_required = ["cadastro.change_produto"]
    model = Produto
    form_class = ProdutoForm
    template_name = 'cadastro/produto/form.html'
    success_url = '/produtos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class ProdutoDeleteView(UserAccessMixin, DeleteView):
    permission_required = ["cadastro.delete_produto"]
    model = Produto
    template_name = 'cadastro/produto/confirm_delete.html'
    success_url = '/produtos'    