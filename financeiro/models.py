from django.db import models
from core.models import GenericoModel
from financeiro.choices import SituacaoFinanceiro
from cadastro.models import CondicaoPagamento, Contato


class ContaReceber(GenericoModel):
    documento = models.CharField('Documento', max_length=20)
    parcela = models.IntegerField('Parcela', default=1)
    contato = models.ForeignKey(Contato, on_delete=models.RESTRICT, verbose_name='Cliente')
    data_emissao = models.DateField('Data Emissão')
    data_vencimento = models.DateField('Data Vencto')
    valor_titulo = models.DecimalField('Vlr. Titulo', max_digits=15, decimal_places=2, default=0)
    observacao = models.CharField('Observação', max_length=500, null=True, blank=True)
    situacao = models.IntegerField('Situação', choices=SituacaoFinanceiro.choices, default=SituacaoFinanceiro.ABERTO)

    def __str__(self) -> str:
        return self.documento
    
    class Meta:
        verbose_name = 'Conta Receber'
        verbose_name_plural = 'Contas Receber'



class BaixaReceber(GenericoModel):
    contareceber = models.ForeignKey(ContaReceber, on_delete=models.CASCADE)
    condicaopagamento = models.ForeignKey(CondicaoPagamento, on_delete=models.RESTRICT, verbose_name='Condição Pagamento')
    valor_juros = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    valor_multa = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    valor_desconto = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    valor_pago = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    data_baixa = models.DateField()

    def __str__(self) -> str:
        return f'Documento: {self.contareceber.documento}'
    

class ContaPagar(GenericoModel):
    documento = models.CharField('Documento', max_length=20)
    parcela = models.IntegerField('Parcela', default=1)
    contato = models.ForeignKey(Contato, on_delete=models.RESTRICT, verbose_name='Fornecedor')
    data_emissao = models.DateField('Data Emissão')
    data_vencimento = models.DateField('Data Vencto')
    valor_titulo = models.DecimalField('Vlr. Titulo', max_digits=15, decimal_places=2, default=0)
    observacao = models.CharField('Observação', max_length=500, null=True, blank=True)
    situacao = models.IntegerField('Situação', choices=SituacaoFinanceiro.choices, default=SituacaoFinanceiro.ABERTO)

    def __str__(self) -> str:
        return self.documento



class BaixaPagar(GenericoModel):
    contapagar = models.ForeignKey(ContaPagar, on_delete=models.CASCADE)
    condicaopagamento = models.ForeignKey(CondicaoPagamento, on_delete=models.RESTRICT, verbose_name='Condição Pagamento')
    valor_juros = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    valor_multa = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    valor_desconto = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    valor_pago = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    data_baixa = models.DateField()

    def __str__(self) -> str:
        return f'Documento: {self.contapagar.documento}'    