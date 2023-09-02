from django.urls import path
from financeiro.views import ContaReceberListView, ContaReceberCreate, ContaReceberUpdateView, \
    ContaReceberDeleteView, BaixarContaReceberView, EstornarContaReceberView, ContaPagarListView, \
    ContaPagarCreateView, ContaPagarUpdateView, ContaPagarDeleteView, BaixarContaPagarView, EstornarContaPagarView

urlpatterns = [
    # Contas a pagar
    path("contapagars/", ContaPagarListView.as_view(), name="contapagar-list"),
    path("contapagars/create", ContaPagarCreateView.as_view(), name="contapagar-create"),
    path("contapagars/<int:pk>/update/", ContaPagarUpdateView.as_view(), name="contapagar-update"),
    path("contapagars/<int:pk>/delete/", ContaPagarDeleteView.as_view(), name="contapagar-delete"),
    path("baixapagars/<int:contapagar>/baixar", BaixarContaPagarView.as_view(), name="baixapagar-baixar"),
    path("baixapagars/<int:contapagar>/estornar", EstornarContaPagarView.as_view(), name="baixapagar-estornar"),

    # Contas a receber
    path("contarecebers/", ContaReceberListView.as_view(), name="contareceber-list"),
    path("contarecebers/create", ContaReceberCreate.as_view(), name="contareceber-create"),
    path("contarecebers/<int:pk>/update/", ContaReceberUpdateView.as_view(), name="contareceber-update"),
    path("contarecebers/<int:pk>/delete/", ContaReceberDeleteView.as_view(), name="contareceber-delete"),
    path("baixarecebers/<int:contareceber>/baixar", BaixarContaReceberView.as_view(), name="baixareceber-baixar"),
    path("baixarecebers/<int:contareceber>/estornar", EstornarContaReceberView.as_view(), name="baixareceber-estornar"),
]
