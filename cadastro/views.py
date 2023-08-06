from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from cadastro.models import Unidade, Marca, Categoria, Pais, Estado, Municipio, Produto, \
Contato, FormaPagamento
from core.constants import REGISTROS_POR_PAGINA
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.views import redirect_to_login
from cadastro.forms import ProdutoForm, UnidadeForm, ContatoForm, CategoriaForm, MarcaForm, \
PaisForm, EstadoForm, MuncipioForm, FormaPagamentoForm
from django.http import HttpResponse
from django.core.serializers import serialize


def municipios(request, estado):
    data = serialize("json", Municipio.objects.filter(estado=estado), fields=('nome', 'capital'))
    return HttpResponse(data)


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


class MarcaCreateView(UserAccessMixin, InvalidFormMixin, CreateView):
    permission_required = ["cadastro.add_marca"]
    model = Marca
    form_class = MarcaForm
    template_name = 'cadastro/marca/form.html'
    success_url = '/marcas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class MarcaUpdateView(UserAccessMixin, InvalidFormMixin, UpdateView):
    permission_required = ["cadastro.change_marca"]
    model = Marca
    form_class = MarcaForm
    template_name = 'cadastro/marca/form.html'
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


class CategoriaCreateView(UserAccessMixin, InvalidFormMixin, CreateView):
    permission_required = ["cadastro.add_categoria"]
    model = Categoria
    form_class = CategoriaForm
    template_name = 'cadastro/categoria/form.html'
    
    success_url = '/categorias'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class CategoriaUpdateView(UserAccessMixin, InvalidFormMixin, UpdateView):
    permission_required = ["cadastro.change_categoria"]
    model = Categoria
    form_class = CategoriaForm
    template_name = 'cadastro/categoria/form.html'
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


class PaisCreateView(UserAccessMixin, InvalidFormMixin, CreateView):
    permission_required = ["cadastro.add_pais"]
    model = Pais
    form_class = PaisForm
    template_name = 'cadastro/pais/form.html'
    success_url = '/pais'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class PaisUpdateView(UserAccessMixin, InvalidFormMixin, UpdateView):
    permission_required = ["cadastro.change_pais"]
    model = Pais
    form_class = PaisForm
    template_name = 'cadastro/pais/form.html'
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


class EstadoCreateView(UserAccessMixin, InvalidFormMixin, CreateView):
    permission_required = ["cadastro.add_estado"]
    model = Estado
    form_class = EstadoForm
    template_name = 'cadastro/estado/form.html'
    success_url = '/estados'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class EstadoUpdateView(UserAccessMixin, InvalidFormMixin, UpdateView):
    permission_required = ["cadastro.change_estado"]
    model = Estado
    form_class = EstadoForm
    template_name = 'cadastro/estado/form.html'
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


class MunicipioCreateView(UserAccessMixin, InvalidFormMixin, CreateView):
    permission_required = ["cadastro.add_municipio"]
    model = Municipio
    form_class = MuncipioForm
    template_name = 'cadastro/municipio/form.html'
    success_url = '/municipios'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class MunicipioUpdateView(UserAccessMixin, InvalidFormMixin, UpdateView):
    permission_required = ["cadastro.change_municipio"]
    model = Municipio
    form_class = MuncipioForm
    template_name = 'cadastro/municipio/form.html'
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
        # context['save_top'] = True
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


class ContatoListView(UserAccessMixin, ListView):
    permission_required = ["cadastro.view_contato"]
    model = Contato
    template_name = 'cadastro/contato/list.html'
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
    template_name = 'cadastro/contato/form.html'
    success_url = '/contatos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class ContatoUpdateView(UserAccessMixin, InvalidFormMixin, UpdateView):
    permission_required = ["cadastro.change_contato"]
    model = Contato
    form_class = ContatoForm
    template_name = 'cadastro/contato/form.html'
    success_url = '/contatos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context



class ContatoDeleteView(UserAccessMixin, DeleteView):    
    permission_required = ["cadastro.delete_contato"]
    model = Contato
    template_name = 'cadastro/contato/confirm_delete.html'
    success_url = '/contatos'



class FormaPagamentoListView(UserAccessMixin, ListView):
    permission_required = ["cadastro.view_formpagamento"]
    model = FormaPagamento
    template_name = 'cadastro/formapagamento/list.html'
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
                Q(nome__icontains=search)
            )
        return queryset


class FormaPagamentoCreateView(UserAccessMixin, InvalidFormMixin, CreateView):
    permission_required = ["cadastro.add_formapagamento"]
    model = FormaPagamento
    form_class = FormaPagamentoForm
    template_name = 'cadastro/formapagamento/form.html'
    success_url = '/formapagamentos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class FormaPagamentoUpdateView(UserAccessMixin, InvalidFormMixin, UpdateView):
    permission_required = ["cadastro.change_formapagamento"]
    model = FormaPagamento
    form_class = FormaPagamentoForm
    template_name = 'cadastro/formapagamento/form.html'
    success_url = '/formapagamentos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title
        return context


class FormaPagamentoDeleteView(UserAccessMixin, DeleteView):    
    permission_required = ["cadastro.delete_formpagamento"]
    model = FormaPagamento
    template_name = 'cadastro/formapagamento/confirm_delete.html'
    success_url = '/formapagamentos'