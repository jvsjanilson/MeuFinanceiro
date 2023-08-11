from django.urls import path
from financeiro.views import ContaReceberListView

urlpatterns = [
    path("contarecebers/", ContaReceberListView.as_view(), name="contareceber-list"),
    # path("condicaopagamentos/create", CondicaoPagamentoCreateView.as_view(), name="condicaopagamento-create"),
    # path("condicaopagamentos/<int:pk>/update/", CondicaoPagamentoUpdateView.as_view(), name="condicaopagamento-update"),
    # path("condicaopagamentos/<int:pk>/delete/", CondicaoPagamentoDeleteView.as_view(), name="condicaopagamento-delete"),

]
