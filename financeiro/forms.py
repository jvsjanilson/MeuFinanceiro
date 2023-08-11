from django import forms
from core.forms import *
from financeiro.models import ContaReceber

class ContaReceberForm(forms.ModelForm):
    class Meta:
        model = ContaReceber
        fields = ['codigo', 'nome']
        widgets = {
            'codigo': TextInputBootstrap(),
            'nome': TextInputBootstrap(),
        }