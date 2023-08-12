from django import forms
from core.forms import *
from financeiro.models import ContaReceber

class ContaReceberForm(forms.ModelForm):
    # data_vencimento = forms.DateField(
    #     widget=forms.DateInput(format='%Y-%m-%d'),

    #     #input_formats=('%m-%d-%Y', )
    #  )


    class Meta:
        model = ContaReceber
        fields = ['documento', 'parcela', 'contato', 'data_emissao', 'data_vencimento', 'valor_titulo', 'observacao', 'situacao']
        widgets = {
            'documento': TextInputBootstrap(),
            'parcela': NumberInputBootstap(),
            'contato': SelectBootstrap(),
            'data_emissao': DateInputBootstrap(format='%Y-%m-%d'),
            'data_vencimento': DateInputBootstrap(format='%Y-%m-%d'),
            'valor_titulo': NumberInputBootstap(),
            'observacao': TextInputBootstrap(),
            'situacao': SelectBootstrap()
        }