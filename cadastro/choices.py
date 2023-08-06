from django.db import models
from django.utils.translation import gettext_lazy as _


class TipoPagamento(models.IntegerChoices):
    AVISTA = 1, _('A Vista')
    PRAZO = 2, _('A Prazo')


class TipoIntervalo(models.TextChoices):
    DIARIO = 'D', _('Diario')
    SEMANAL = 'S', _('Semanal')
    MENSAL = 'M', _('Mensal')
    ANUAL = 'A', _('Anual')


class TipoVisibilidade(models.IntegerChoices):
    PEDIDO = 1, _('Pedido')
    COMPRA = 2, _('Compra')
    AMBOS = 3, _('Ambos')
    