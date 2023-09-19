from django.db import models
from core.models import GenericoModel
from cadastro.models import Unidade, Marca, Categoria


class Produto(GenericoModel):
    codigo = models.CharField('Codigo', max_length=13, unique=True)
    nome = models.CharField('Nome', max_length=60)
    unidade = models.ForeignKey(Unidade, on_delete=models.RESTRICT, verbose_name='Unidade')
    marca = models.ForeignKey(Marca, on_delete=models.RESTRICT, verbose_name='Marca')
    categoria = models.ForeignKey(Categoria, on_delete=models.RESTRICT, verbose_name='Categoria')
    preco_compra = models.DecimalField('Preço Compra', max_digits=18, decimal_places=2, default=0)
    preco_venda = models.DecimalField('Preço Venda', max_digits=18, decimal_places=2, default=0)
    estoque = models.DecimalField('Estoque', max_digits=18, decimal_places=3, default=0)
    ativo = models.BooleanField('Ativo?', default=True)

    def __str__(self):
        return self.codigo

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
