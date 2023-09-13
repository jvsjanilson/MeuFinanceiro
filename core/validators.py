from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from itertools import cycle
from core.constants import LENGTH_CNPJ, LENGTH_CPF
from django.core.validators import  RegexValidator


def valor_limite_pago(self, saldo_pagar, field = 'valor_pago'):
    """
     Valida se o valor pago é maior que o saldo, caso seja retorna error
    """
    if self.valor_pago - self.valor_juros - self.valor_multa + self.valor_desconto > saldo_pagar:
        raise ValidationError({field: 'Informe valor igual ou menor'})


def valida_cpfcnpj(value):
    if len(value) == LENGTH_CNPJ:
        if value in (c * LENGTH_CNPJ for c in "1234567890"):
            raise ValidationError(_('O CNPJ %(value)s é inválido. '), params={'value': value})

        cnpj_r = value[::-1]
        for i in range(2, 0, -1):
            cnpj_enum = zip(cycle(range(2, 10)), cnpj_r[i:])
            dv = sum(map(lambda x: int(x[1]) * x[0], cnpj_enum)) * 10 % 11
            if cnpj_r[i - 1:i] != str(dv % 10):
                raise ValidationError(_('O CNPJ %(value)s é inválido. '), params={'value': value})
    elif len(value) == LENGTH_CPF:
        if value in (c * LENGTH_CPF for c in "1234567890"):
            raise ValidationError(_('O CPF %(value)s é inválido. '), params={'value': value})

        cpf_r = value[::-1]
        for i in range(2, 0, -1):
            cpf_enumerado = enumerate(cpf_r[i:], start=2)
            dv_calculado = sum(map(lambda x: int(x[1]) * x[0], cpf_enumerado)) * 10 % 11
            if cpf_r[i - 1:i] != str(dv_calculado % 10):
                raise ValidationError(_('O CPF %(value)s é inválido. '), params={'value': value})

    else:
        raise ValidationError(_('O tamanho do CPF/CNPJ %(value)s é inválido. '), params={'value': value})


def number_only(value):
    RegexValidator(r'^[0-9]*$', 'Somente números.').__call__(value)


def letter_only(value):
    RegexValidator(r'^[a-zA-Z\s]*$', 'Somente letras sem acentos.').__call__(value)


def alfa_numerico(value):
    RegexValidator(r'^[a-zA-Z0-9\s]*$', 'Somente letras e números').__call__(value)