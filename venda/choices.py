from django.db import models
from django.utils.translation import gettext_lazy as _


class SituacaoPedido(models.IntegerChoices):
    ORCAMENTO = 1, _('Orçamento')
    PEDIDO = 2, _('Pedido')
    CANCELADO = 3, _('Cancelado')

