from django import forms
from cadastro.models import Produto, Unidade, Marca, Categoria
from core.forms import *


class UnidadeForm(forms.ModelForm):
    class Meta:
        model = Unidade
        fields = ['codigo', 'nome']
        widgets = {
            'codigo': TextInputBootstrap(),
            'nome': TextInputBootstrap(),
        }



class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['nome']
        widgets = {
            'nome': TextInputBootstrap(),
        }



class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = [ 'nome']
        widgets = {
            'nome': TextInputBootstrap(),
        }



class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = '__all__'
        # help_texts = {
        #     'codigo': 'Codigo do produto 13 caracteres',
        # }
        widgets = {
            'codigo': TextInputBootstrap(),
            'nome': TextInputBootstrap(),
            'unidade': SelectBootStrap(),
            'marca': SelectBootStrap(),
            'categoria': SelectBootStrap(),
            'preco_compra': NumberInputBootstap(),
            'preco_venda': NumberInputBootstap(),
            'estoque': NumberInputBootstap(),
            'ativo': CheckboxInputBootstrap(),
        }
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['codigo'].required = False
