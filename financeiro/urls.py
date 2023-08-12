from django.urls import path
from financeiro.views import ContaReceberListView, ContaReceberCreate, ContaReceberUpdateView, ContaReceberDeleteView

urlpatterns = [
    path("contarecebers/", ContaReceberListView.as_view(), name="contareceber-list"),
    path("contarecebers/create", ContaReceberCreate.as_view(), name="contareceber-create"),
    path("contarecebers/<int:pk>/update/", ContaReceberUpdateView.as_view(), name="contareceber-update"),
    path("contarecebers/<int:pk>/delete/", ContaReceberDeleteView.as_view(), name="contareceber-delete"),

]
