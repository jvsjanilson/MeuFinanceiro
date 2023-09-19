from django.db import models
from core.models import GenericoModel
from cadastro.models import FormaPagamento
from cadastro.choices import TipoIntervalo, TipoVisibilidade
from django.core.validators import MinValueValidator, MaxValueValidator


class CondicaoPagamento(GenericoModel):
    nome = models.CharField('Nome', max_length=60)
    formapagamento = models.ForeignKey(FormaPagamento, on_delete=models.CASCADE, verbose_name='Forma Pagamento')
    visibilidade = models.SmallIntegerField('Visibilidade', choices=TipoVisibilidade.choices,
                                            default=TipoVisibilidade.AMBOS)
    tipo_intervalo = models.CharField('Tipo Intervalo', max_length=1, choices=TipoIntervalo.choices,
                                      default=TipoIntervalo.MENSAL)
    intervalo = models.IntegerField('Intervalo', default=1, validators=[MinValueValidator(1)])
    numero_maximo_parcela = models.IntegerField('N. Máx. Parcela', default=1,
                                                validators=[MinValueValidator(1), MaxValueValidator(360)])
    dia_fixo = models.BooleanField('Dia Fixo?', default=True)
    ativo = models.BooleanField('Ativo?', default=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Condição de Pagamento'
        verbose_name_plural = 'Condições de Pagamento'
