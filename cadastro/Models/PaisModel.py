from django.db import models
from core.models import GenericoModel


class Pais(GenericoModel):
    codigo = models.IntegerField('Código', unique=True)
    nome = models.CharField('Nome', max_length=120)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'País'
        verbose_name_plural = 'Países'
        ordering = ["id"]
