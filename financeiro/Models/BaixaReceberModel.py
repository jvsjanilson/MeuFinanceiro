from django.db import models
from core.models import GenericoModel
from financeiro.Models.ContaReceberModel import ContaReceber
from cadastro.models import FormaPagamento
from decimal import Decimal
from django.core.validators import MinValueValidator
from core.validators import valor_limite_pago


class BaixaReceber(GenericoModel):
    contareceber = models.ForeignKey(ContaReceber, on_delete=models.CASCADE, related_name='baixas')
    formapagamento = models.ForeignKey(FormaPagamento, on_delete=models.RESTRICT, verbose_name='Forma de Pagamento')
    valor_juros = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(
        limit_value=Decimal('0.00'))])
    valor_multa = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(
        limit_value=Decimal('0.00'))])
    valor_desconto = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(
        limit_value=Decimal('0.00'))])
    valor_pago = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(
        limit_value=Decimal('0.01'))])
    data_baixa = models.DateField()

    def clean(self) -> None:
        valor_limite_pago(self, self.contareceber.saldo_pagar)
        return super().clean()

    def __str__(self):
        return f'Documento: {self.contareceber.documento}'

    class Meta:
        verbose_name = 'Baixa Receber'
        verbose_name_plural = 'Baixas Receber'
