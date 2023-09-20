from django.db import models
from core.models import GenericoModel
from cadastro.models import Estado


class Municipio(GenericoModel):
    codigo = models.IntegerField('Código', unique=True)
    nome = models.CharField('Nome', max_length=120)
    capital = models.BooleanField(default=False)
    estado = models.ForeignKey(Estado, on_delete=models.RESTRICT)

    class Meta:
        verbose_name = 'Município'
        verbose_name_plural = 'Municípios'
        ordering = ["id"]

    def __str__(self):
        return self.nome
