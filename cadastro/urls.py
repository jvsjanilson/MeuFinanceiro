from django.urls import path
from cadastro.views import UnidadeListView, UnidadeCreateView, \
    UnidadeUpdateView, UnidadeDeleteView, MarcaListView, MarcaCreateView, MarcaUpdateView, \
    MarcaDeleteView, CategoriaListView, CategoriaCreateView, CategoriaUpdateView, CategoriaDeleteView

urlpatterns = [

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
