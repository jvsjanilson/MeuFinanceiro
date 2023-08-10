from django.db import models
from django.utils.translation import gettext_lazy as _


class SituacaoFinanceiro(models.IntegerChoices):
    ABERTO = 1, _('Aberto')
    PAGO_TOTAL = 2, _('Pago Total')
    PAGO_PARCIAL = 3, _('Pago Parcial')

