from django.db import models
from django.utils.translation import gettext_lazy as _


class TipoPagamento(models.IntegerChoices):
    AVISTA = 1, _('A Vista')
    PRAZO = 2, _('A Prazo')

