from django.db import models
from core.models import GenericoModel


class Marca(GenericoModel):
    nome = models.CharField('Nome', max_length=60)

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        ordering = ["id"]

    def __str__(self):
        return self.nome
