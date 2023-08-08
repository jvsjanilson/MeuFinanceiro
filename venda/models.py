from django.db import models
from core.models import GenericoModel
from cadastro.models import Contato
from django.contrib.auth.models import User
from venda.choices import SituacaoPedido
from cadastro.models import Produto, CondicaoPagamento

class Pedido(GenericoModel):
    numero = models.CharField('Numero', max_length=20, null=True, blank=True)
    data_emissao = models.DateField('Data Emissão')
    contato = models.ForeignKey(Contato, on_delete=models.CASCADE, verbose_name='Cliente')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    valor_desconto = models.DecimalField('Vlr. Desconto', max_digits=15, decimal_places=2, default=0)
    percentual_desconto = models.DecimalField('Pc. Desconto', max_digits=5, decimal_places=2, default=0)
    valor_total = models.DecimalField('Total', max_digits=15, decimal_places=2)
    observacao = models.CharField('Obs:', max_length=1000, null=True, blank=True)
    situacao = models.IntegerField('Situação', choices=SituacaoPedido.choices, default=SituacaoPedido.ORCAMENTO)

    def __str__(self):
        return self.numero


class PedidoItem(GenericoModel):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, verbose_name='Pedido')
    produto = models.ForeignKey(Produto, on_delete=models.RESTRICT, verbose_name='Produto')
    quantidade = models.DecimalField('Quantdade', max_digits=18, decimal_places=4, default=0)
    valor_unitario = models.DecimalField('Vlr. Unitário', max_digits=15, decimal_places=2, default=0)
    valor_desconto = models.DecimalField('Vlr. Desconto', max_digits=15, decimal_places=2, default=0)
    percentual_desconto = models.DecimalField('Pc. Desconto', max_digits=5, decimal_places=2, default=0)
    total = models.DecimalField('Total', max_digits=15, decimal_places=2, default=0)
    info_adicional = models.CharField('Inf. Adicional', max_length=500, null=True, blank=True)

    def __str__(self) -> str:
        return f'Pedido: {self.pedido.pk} - Item: {self.pk}' 



class PedidoPagamento(GenericoModel):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, verbose_name='Pedido')
    condicaopagamento = models.ForeignKey(CondicaoPagamento, on_delete=models.RESTRICT, verbose_name='Condição Pagamento')
    data_vencimento = models.DateField('Data Vencto')
    valor_parcela = models.DecimalField('Valor Parcela', max_digits=15, decimal_places=2, default=0)

    def __str__(self) -> str:
        return f'Número: {self.pk} - Pedido: {self.pedido.pk}'
    