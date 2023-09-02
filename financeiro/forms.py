from core.forms import *
from financeiro.models import ContaReceber, BaixaReceber, ContaPagar, BaixaPagar


class ContaReceberForm(forms.ModelForm):
    class Meta:
        model = ContaReceber
        fields = ['documento', 'parcela', 'contato', 'data_emissao', 'data_vencimento', 'valor_titulo', 'observacao',
                  'situacao']
        widgets = {
            'documento': TextInputBootstrap(attrs={'autofocus': 'true'}),
            'parcela': NumberInputBootstap(),
            'contato': SelectBootstrap(),
            'data_emissao': DateInputBootstrap(format='%Y-%m-%d'),
            'data_vencimento': DateInputBootstrap(format='%Y-%m-%d'),
            'valor_titulo': NumberInputBootstap(),
            'observacao': TextareaInputBootstrap(),
            'situacao': SelectBootstrap()
        }


class BaixaReceberForm(forms.ModelForm):
    class Meta:
        model = BaixaReceber
        fields = ['contareceber', 'condicaopagamento', 'valor_juros', 'valor_multa', 'valor_desconto', 'valor_pago',
                  'data_baixa']
        widgets = {
            'contareceber': SelectBootstrap(),
            'condicaopagamento': SelectBootstrap(),
            'valor_juros': NumberInputBootstap(),
            'valor_multa': NumberInputBootstap(),
            'valor_desconto': NumberInputBootstap(),
            'valor_pago': NumberInputBootstap(attrs={'autofocus': 'true'}),
            'data_baixa': DateInputBootstrap(format='%Y-%m-%d'),
        }



class ContaPagarForm(forms.ModelForm):
    class Meta:
        model = ContaPagar
        fields = ['documento', 'parcela', 'contato', 'data_emissao', 'data_vencimento', 'valor_titulo', 'observacao',
                  'situacao']
        widgets = {
            'documento': TextInputBootstrap(attrs={'autofocus': 'true'}),
            'parcela': NumberInputBootstap(),
            'contato': SelectBootstrap(),
            'data_emissao': DateInputBootstrap(format='%Y-%m-%d'),
            'data_vencimento': DateInputBootstrap(format='%Y-%m-%d'),
            'valor_titulo': NumberInputBootstap(),
            'observacao': TextareaInputBootstrap(),
            'situacao': SelectBootstrap()
        }


class BaixaPagarForm(forms.ModelForm):
    class Meta:
        model = BaixaPagar
        fields = ['contapagar', 'condicaopagamento', 'valor_juros', 'valor_multa', 'valor_desconto', 'valor_pago',
                  'data_baixa']
        widgets = {
            'contapagar': SelectBootstrap(),
            'condicaopagamento': SelectBootstrap(),
            'valor_juros': NumberInputBootstap(),
            'valor_multa': NumberInputBootstap(),
            'valor_desconto': NumberInputBootstap(),
            'valor_pago': NumberInputBootstap(attrs={'autofocus': 'true'}),
            'data_baixa': DateInputBootstrap(format='%Y-%m-%d'),
        }
