from django.db import models
from core.models import GenericoModel
from core.validators import valida_cpfcnpj, number_only
from cadastro.choices import TipoPagamento, TipoIntervalo, TipoVisibilidade
from django.core.validators import MinValueValidator, MaxValueValidator


class Pais(GenericoModel):
    codigo = models.IntegerField('Código', unique=True)
    nome = models.CharField('Nome', max_length=120)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'País'
        verbose_name_plural = 'Países'


class Estado(GenericoModel):
    codigo = models.IntegerField('Código', unique=True)
    uf = models.CharField('UF', max_length=2)
    nome = models.CharField('Nome', max_length=120)
    pais = models.ForeignKey(Pais, on_delete=models.RESTRICT, verbose_name='Pais')

    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'

    def __str__(self):
        return self.uf


class Municipio(GenericoModel):
    codigo = models.IntegerField('Código', unique=True)
    nome = models.CharField('Nome', max_length=120)
    capital = models.BooleanField(default=False)
    estado = models.ForeignKey(Estado, on_delete=models.RESTRICT)

    class Meta:
        verbose_name = 'Município'
        verbose_name_plural = 'Municípios'

    def __str__(self):
        return self.nome


class Contato(GenericoModel):
    razao_social = models.CharField('Razão Social', max_length=120)
    nome_fantasia = models.CharField('Nome Fantasia', max_length=120, null=True, blank=True)
    cpf_cnpj = models.CharField('CPF/CNPJ', max_length=14, null=True, blank=True, validators=[valida_cpfcnpj])
    inscricao_estadual = models.CharField('I.E', max_length=14, null=True, blank=True)
    inscricao_municipal = models.CharField('I.M', max_length=14, null=True, blank=True)
    inscricao_suframa = models.CharField('I.S', max_length=14, null=True, blank=True)
    inscricao_cnae = models.CharField('CNAE', max_length=14, null=True, blank=True)
    endereco = models.CharField('Endereço', max_length=120, null=True, blank=True)
    numero = models.CharField('Número', max_length=30, null=True, blank=True)
    complemento = models.CharField('Compl.', max_length=120, null=True, blank=True)
    bairro = models.CharField('Bairro', max_length=60, null=True, blank=True)
    cep = models.CharField('CEP', max_length=8, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.RESTRICT, verbose_name='UF')
    municipio = models.ForeignKey(Municipio, on_delete=models.RESTRICT, verbose_name='Município')
    celular = models.CharField('Celular', max_length=14, null=True, blank=True)
    fone = models.CharField('Telefone', max_length=14, null=True, blank=True)
    email = models.EmailField('E-mail', null=True, blank=True)
    foto = models.ImageField('Foto', upload_to='clientes/fotos/', null=True, blank=True)
    ativo = models.BooleanField('Ativo?', default=True)

    def __str__(self):
        return self.razao_social
    
    class Meta:
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'


class Unidade(GenericoModel):
    codigo = models.CharField('Codigo', max_length=3, unique=True)
    nome = models.CharField('Nome', max_length=60)

    class Meta:
        ordering = ['codigo']
        verbose_name = 'Unidade'
        verbose_name_plural = 'Unidades'

    def __str__(self):
        return self.codigo


class Marca(GenericoModel):
    nome = models.CharField('Nome', max_length=60)

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'

    def __str__(self):
        return self.nome


class Categoria(GenericoModel):
    nome = models.CharField('Nome', max_length=60)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nome


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


class FormaPagamento(GenericoModel):
    codigo = models.CharField('Codigo', max_length=3, unique=True, validators=[number_only])
    tipo_pagamento = models.SmallIntegerField('Tipo Pagto', choices=TipoPagamento.choices, default=TipoPagamento.AVISTA)
    nome = models.CharField('Nome', max_length=60)
    ativo = models.BooleanField('Ativo?', default=True)

    def __str__(self):
        return f'{self.codigo} - {self.nome}'
    
    class Meta:
        verbose_name = 'Forma de Pagamento'
        verbose_name_plural = 'Formas de Pagamento'


class CondicaoPagamento(GenericoModel):
    nome = models.CharField('Nome', max_length=60)
    formapagamento = models.ForeignKey(FormaPagamento, on_delete=models.CASCADE, verbose_name='Forma Pagamento')
    visibilidade = models.SmallIntegerField('Visibilidade', choices=TipoVisibilidade.choices, default=TipoVisibilidade.AMBOS)
    tipo_intervalo = models.CharField('Tipo Intervalo', max_length=1,  choices=TipoIntervalo.choices, default=TipoIntervalo.MENSAL)
    intervalo = models.IntegerField('Intervalo', default=1, validators=[MinValueValidator(1)])
    numero_maximo_parcela = models.IntegerField('N. Máx. Parcela', default=1,
                                                validators=[MinValueValidator(1), MaxValueValidator(360)])
    dia_fixo = models.BooleanField('Dia Fixo?', default=True)
    ativo = models.BooleanField('Ativo?', default=True)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Condição de Pagamento'
        verbose_name_plural = 'Condições de Pagamento'

