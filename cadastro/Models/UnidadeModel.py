from django.db import models
from core.models import GenericoModel


class Unidade(GenericoModel):
    codigo = models.CharField('Codigo', max_length=3, unique=True)
    nome = models.CharField('Nome', max_length=60)

    class Meta:
        ordering = ['codigo']
        verbose_name = 'Unidade'
        verbose_name_plural = 'Unidades'

    def __str__(self):
        return self.codigo
