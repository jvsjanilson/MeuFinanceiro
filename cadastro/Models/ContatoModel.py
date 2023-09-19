from django.db import models
from core.models import GenericoModel
from cadastro.models import Estado
from cadastro.models import Municipio
from core.validators import valida_cpfcnpj


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
