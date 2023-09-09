from django.db import models
from core.models import GenericoModel
from cadastro.models import Contato
from core.validators import alfa_numerico
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal
from financeiro.choices import SituacaoFinanceiro
from django.db.models import Sum


class ContaPagar(GenericoModel):
    documento = models.CharField('Documento', max_length=20, validators=[alfa_numerico])
    parcela = models.IntegerField('Parcela', default=1)
    contato = models.ForeignKey(Contato, on_delete=models.RESTRICT, verbose_name='Fornecedor')
    data_emissao = models.DateField('Data Emissão', default=timezone.now)
    data_vencimento = models.DateField('Data Vencto', default=timezone.now)
    valor_titulo = models.DecimalField('Vlr. Titulo', max_digits=15, decimal_places=2, default=0,
                                       validators=[MinValueValidator(limit_value=Decimal('0.01'),
                                                                     message='Informe um valor maior que 0,00')])
    observacao = models.CharField('Observação', max_length=500, null=True, blank=True)
    situacao = models.IntegerField('Situação', null=True, blank=True, choices=SituacaoFinanceiro.choices,
                                   default=SituacaoFinanceiro.ABERTO)

    class Meta:
        verbose_name = 'Conta pagar'
        verbose_name_plural = 'Contas pagar'
        # unique_together = ['documento', 'parcela', 'contato']

    def __str__(self):
        return self.documento

    @property
    def saldo_pagar(self):
        return self.valor_titulo - self.total_pago

    @property
    def total_pago(self) -> float:
        total_pago = self.baixas.aggregate(saldo=Sum('valor_pago'))['saldo']
        if total_pago is None:
            total_pago = Decimal('0.00')
        return total_pago

