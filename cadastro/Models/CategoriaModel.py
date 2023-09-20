from django.db import models
from core.models import GenericoModel


class Categoria(GenericoModel):
    nome = models.CharField('Nome', max_length=60)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ["id"]

    def __str__(self):
        return self.nome
