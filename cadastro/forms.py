from cadastro.models import Produto, Unidade, Marca, Categoria, Contato, Pais, Estado, Municipio, \
    FormaPagamento, CondicaoPagamento
from core.forms import *


class UnidadeForm(forms.ModelForm):
    class Meta:
        model = Unidade
        fields = ['codigo', 'nome']
        widgets = {
            'codigo': TextInputBootstrap(attrs={'autofocus': 'true'}),
            'nome': TextInputBootstrap(),
        }


class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nome']
        widgets = {
            'nome': TextInputBootstrap(attrs={'autofocus': 'true'}),
        }


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = [ 'nome']
        widgets = {
            'nome': TextInputBootstrap(attrs={'autofocus': 'true'}),
        }


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = '__all__'
        # help_texts = {
        #     'codigo': 'Codigo do produto 13 caracteres',
        # }
        widgets = {
            'codigo': TextInputBootstrap(attrs={'autofocus': 'true'}),
            'nome': TextInputBootstrap(),
            'unidade': SelectBootstrap(),
            'marca': SelectBootstrap(),
            'categoria': SelectBootstrap(),
            'preco_compra': NumberInputBootstap(),
            'preco_venda': NumberInputBootstap(),
            'estoque': NumberInputBootstap(),
            'ativo': CheckboxInputBootstrap(),
        }


class ContatoForm(forms.ModelForm):
    
    class Meta:
        model = Contato
        fields = '__all__'
        # labels = {
        #     "razao_social": "Ola"
        # }
        # help_texts = {
        #      'razao_social': 'Conforme lei 8.253/98',
        #  }

        widgets = {
            'razao_social': TextInputBootstrap(attrs={'autofocus': 'true'}),
            'nome_fantasia': TextInputBootstrap(),
            'cpf_cnpj': TextInputBootstrap(),
            'inscricao_estadual': TextInputBootstrap(),
            'inscricao_municipal': TextInputBootstrap(),
            'inscricao_suframa': TextInputBootstrap(),
            'inscricao_cnae': TextInputBootstrap(),
            'endereco': TextInputBootstrap(),
            'numero': TextInputBootstrap(),
            'complemento': TextInputBootstrap(),
            'bairro': TextInputBootstrap(),
            'cep': TextInputBootstrap(),
            'estado': SelectBootstrap(),
            'municipio': SelectBootstrap(),
            'celular': TextInputBootstrap(),
            'fone': TextInputBootstrap(),
            'email': TextInputBootstrap(),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control form-control-sm'}),
            'ativo': CheckboxInputBootstrap(),
        }
        

class PaisForm(forms.ModelForm):
    class Meta:
        model = Pais
        fields = ['codigo', 'nome']
        widgets = {
            'codigo': NumberInputBootstap(attrs={'autofocus': 'true'}),
            'nome': TextInputBootstrap(),
        }        


class EstadoForm(forms.ModelForm):
    class Meta:
        model = Estado
        fields = ['codigo', 'uf', 'nome', 'pais']
        widgets = {
            'codigo': NumberInputBootstap(attrs={'autofocus': 'true'}),
            'uf': TextInputBootstrap(),
            'nome': TextInputBootstrap(),
            'pais': SelectBootstrap()
        }                


class MuncipioForm(forms.ModelForm):
    class Meta:
        model = Municipio
        fields = ['codigo', 'nome', 'capital', 'estado']
        widgets = {
            'codigo': NumberInputBootstap(attrs={'autofocus': 'true'}),
            'nome': TextInputBootstrap(),
            'capital': CheckboxInputBootstrap(),
            'estado': SelectBootstrap()
        }                        


class FormaPagamentoForm(forms.ModelForm):
    class Meta:
        model = FormaPagamento
        fields = ['codigo', 'tipo_pagamento', 'nome', 'ativo']
        widgets = {
            'codigo': TextInputBootstrap(attrs={'autofocus': 'true'}),
            'nome': TextInputBootstrap(),
            'tipo_pagamento': SelectBootstrap(),
            'ativo': CheckboxInputBootstrap,
        }


class CondicaoPagamentoForm(forms.ModelForm):
    class Meta:
        model = CondicaoPagamento
        fields = ['nome', 'formapagamento', 'visibilidade', 'tipo_intervalo', 'intervalo', 'numero_maximo_parcela', 'dia_fixo', 'ativo']
        widgets = {
            'nome': TextInputBootstrap(attrs={'autofocus': 'true'}),
            'formapagamento': SelectBootstrap(),
            'visibilidade': SelectBootstrap(),
            'tipo_intervalo': SelectBootstrap(),
            'intervalo': NumberInputBootstap(),
            'numero_maximo_parcela': NumberInputBootstap(),
            'dia_fixo': CheckboxInputBootstrap,
            'ativo': CheckboxInputBootstrap,
        }
