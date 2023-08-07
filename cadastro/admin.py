from django.contrib import admin
from cadastro.models import (Pais, Estado, Municipio, Contato, Unidade, Marca, Categoria, Produto )
from core.constants import REGISTROS_POR_PAGINA

admin.site.disable_action('delete_selected')


@admin.register(Pais)
class AdminPais(admin.ModelAdmin):
    list_display = ('codigo', 'nome')
    fields = ('codigo', 'nome')
    search_fields = ('nome', )
    list_per_page = REGISTROS_POR_PAGINA


@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'uf', 'nome', 'pais')
    fields = ('codigo', 'uf', 'nome', 'pais')
    search_fields = ('nome', 'uf')
    list_per_page = REGISTROS_POR_PAGINA


@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'capital', 'estado')
    fields = ('codigo', 'nome', 'estado', 'capital')
    search_fields = ('nome', )
    list_per_page = REGISTROS_POR_PAGINA


@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ('razao_social', 'nome_fantasia', 'cpf_cnpj', 'celular', 'ativo')
    fields = (('razao_social', 'nome_fantasia'), ('cpf_cnpj', 'inscricao_estadual'), ('inscricao_municipal',
              'inscricao_suframa', 'inscricao_cnae'), ('endereco', 'numero'), ('complemento', 'bairro', 'cep'),
              ('estado', 'municipio'), ('celular', 'fone', 'email', 'foto'))
    search_fields = ('razao_social', 'nome_fantasia', 'cpf_cnpj', 'inscricao_estadual', 'celular', 'fone')
    list_per_page = REGISTROS_POR_PAGINA
    actions = ['delete_selected']


@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome')
    fields = ('codigo', 'nome')
    search_fields = ('codigo', 'nome')
    list_per_page = REGISTROS_POR_PAGINA
    # actions = ['delete_selected']


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nome', )
    fields = ('nome', )
    search_fields = ('nome', )
    list_per_page = REGISTROS_POR_PAGINA


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', )
    fields = ('nome', )
    search_fields = ('nome', )
    list_per_page = REGISTROS_POR_PAGINA


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'preco_venda', 'estoque', 'ativo')
    search_fields = ('codigo', 'nome')
    fields = (('codigo', 'nome'), ('unidade', 'marca', 'categoria'), ('preco_compra', 'preco_venda'), 'estoque', 'ativo')
    list_filter = ('categoria', )
    list_per_page = REGISTROS_POR_PAGINA
    actions = ["ativar"]

    @admin.action(description='Marque para ativar ou inativar o produto')
    def ativar(self, request, queryset):
        for obj in queryset:
            obj.ativo = not obj.ativo
            obj.save()
