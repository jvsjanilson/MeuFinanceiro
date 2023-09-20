from django.db import models
from core.models import GenericoModel
from core.validators import number_only
from cadastro.choices import TipoPagamento


class FormaPagamento(GenericoModel):
    codigo = models.CharField('Codigo', max_length=3, unique=True, validators=[number_only])
    tipo_pagamento = models.SmallIntegerField('Tipo Pagto', choices=TipoPagamento.choices, default=TipoPagamento.AVISTA)
    nome = models.CharField('Nome', max_length=60)
    ativo = models.BooleanField('Ativo?', default=True)

    def __str__(self):
        return f'{self.codigo} - {self.nome}'

    class Meta:
        verbose_name = 'Forma de Pagamento'
        verbose_name_plural = 'Formas de Pagamento'
        ordering = ["id"]
