from django.db import models
from core.models import GenericoModel
from cadastro.models import Pais
from core.validators import letter_only


class Estado(GenericoModel):
    codigo = models.IntegerField('Código', unique=True)
    uf = models.CharField('UF', max_length=2, unique=True, validators=[letter_only])
    nome = models.CharField('Nome', max_length=120)
    pais = models.ForeignKey(Pais, on_delete=models.RESTRICT, verbose_name='Pais')

    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'

    def __str__(self):
        return self.uf
