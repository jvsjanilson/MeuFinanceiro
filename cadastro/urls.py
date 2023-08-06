from django.urls import path
from cadastro.views import UnidadeListView, UnidadeCreateView, \
    UnidadeUpdateView, UnidadeDeleteView, MarcaListView, MarcaCreateView, MarcaUpdateView, \
    MarcaDeleteView, CategoriaListView, CategoriaCreateView, CategoriaUpdateView, CategoriaDeleteView, \
    PaisListView, PaisCreateView, PaisUpdateView, PaisDeleteView, EstadoListView, EstadoCreateView, \
    EstadoUpdateView, EstadoDeleteView, MunicipioListView, MunicipioCreateView, MunicipioUpdateView, \
    MunicipioDeleteView, ProdutoListView, ProdutoCreateView, ProdutoUpdateView, ProdutoDeleteView, \
    ContatoListView, ContatoCreateView, ContatoUpdateView, ContatoDeleteView, municipios, FormaPagamentoListView, \
    FormaPagamentoDeleteView, FormaPagamentoCreateView, FormaPagamentoUpdateView, CondicaoPagamentoListView, \
    CondicaoPagamentoCreateView, CondicaoPagamentoUpdateView, CondicaoPagamentoDeleteView
        

urlpatterns = [
    path('api/municipios/<int:estado>', municipios),

    path("condicaopagamentos/", CondicaoPagamentoListView.as_view(), name="condicaopagamento-list"),
    path("condicaopagamentos/create", CondicaoPagamentoCreateView.as_view(), name="condicaopagamento-create"),
    path("condicaopagamentos/<int:pk>/update/", CondicaoPagamentoUpdateView.as_view(), name="condicaopagamento-update"),
    path("condicaopagamentos/<int:pk>/delete/", CondicaoPagamentoDeleteView.as_view(), name="condicaopagamento-delete"),

    path("formapagamentos/", FormaPagamentoListView.as_view(), name="formapagamento-list"),
    path("formapagamentos/create", FormaPagamentoCreateView.as_view(), name="formapagamento-create"),
    path("formapagamentos/<int:pk>/update/", FormaPagamentoUpdateView.as_view(), name="formapagamento-update"),
    path("formapagamentos/<int:pk>/delete/", FormaPagamentoDeleteView.as_view(), name="formapagamento-delete"),

    path("contatos/", ContatoListView.as_view(), name="contato-list"),
    path("contatos/create", ContatoCreateView.as_view(), name="contato-create"),
    path("contatos/<int:pk>/update/", ContatoUpdateView.as_view(), name="contato-update"),
    path("contatos/<int:pk>/delete/", ContatoDeleteView.as_view(), name="contato-delete"),

    path("produtos/", ProdutoListView.as_view(), name="produto-list"),
    path("produtos/create", ProdutoCreateView.as_view(), name="produto-create"),
    path("produtos/<int:pk>/update/", ProdutoUpdateView.as_view(), name="produto-update"),
    path("produtos/<int:pk>/delete/", ProdutoDeleteView.as_view(), name="produto-delete"),


    path("municipios/", MunicipioListView.as_view(), name="municipio-list"),
    path("municipios/create", MunicipioCreateView.as_view(), name="municipio-create"),
    path("municipios/<int:pk>/update/", MunicipioUpdateView.as_view(), name="municipio-update"),
    path("municipios/<int:pk>/delete/", MunicipioDeleteView.as_view(), name="municipio-delete"),

    path("estados/", EstadoListView.as_view(), name="estado-list"),
    path("estados/create", EstadoCreateView.as_view(), name="estado-create"),
    path("estados/<int:pk>/update/", EstadoUpdateView.as_view(), name="estado-update"),
    path("estados/<int:pk>/delete/", EstadoDeleteView.as_view(), name="estado-delete"),

    path("pais/", PaisListView.as_view(), name="pais-list"),
    path("pais/create", PaisCreateView.as_view(), name="pais-create"),
    path("pais/<int:pk>/update/", PaisUpdateView.as_view(), name="pais-update"),
    path("pais/<int:pk>/delete/", PaisDeleteView.as_view(), name="pais-delete"),

    path("categorias/", CategoriaListView.as_view(), name="categoria-list"),
    path("categorias/create", CategoriaCreateView.as_view(), name="categoria-create"),
    path("categorias/<int:pk>/update/", CategoriaUpdateView.as_view(), name="categoria-update"),
    path("categorias/<int:pk>/delete/", CategoriaDeleteView.as_view(), name="categoria-delete"),

    path("marcas/", MarcaListView.as_view(), name="marca-list"),
    path("marcas/create", MarcaCreateView.as_view(), name="marca-create"),
    path("marcas/<int:pk>/update/", MarcaUpdateView.as_view(), name="marca-update"),
    path("marcas/<int:pk>/delete/", MarcaDeleteView.as_view(), name="marca-delete"),


    path("unidades/", UnidadeListView.as_view(), name="unidade-list"),
    path("unidades/create", UnidadeCreateView.as_view(), name="unidade-create"),
    path("unidades/<int:pk>/update/", UnidadeUpdateView.as_view(), name="unidade-update"),
    path("unidades/<int:pk>/delete/", UnidadeDeleteView.as_view(), name="unidade-delete"),
]
