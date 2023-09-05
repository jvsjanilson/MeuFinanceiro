from django.contrib import admin
from financeiro.models import ContaReceber, BaixaReceber, ContaPagar, BaixaPagar
from core.constants import REGISTROS_POR_PAGINA


@admin.register(ContaReceber)
class ContaReceberAdmin(admin.ModelAdmin):
    list_display = ('documento', 'parcela', 'contato', 'data_emissao', 'data_vencimento', 'valor_titulo', 'situacao')
    fields = ['documento', 'parcela', 'contato', 'data_emissao', 'data_vencimento', 'valor_titulo', 'observacao', 'situacao']
    search_fields = ('documento', 'contato__razao_social')
    readonly_fields = ('situacao', )
    list_per_page = REGISTROS_POR_PAGINA


@admin.register(BaixaReceber)
class BaixaReceberAdmin(admin.ModelAdmin):
    list_display = ('contareceber', 'formapagamento', 'valor_juros', 'valor_multa', 'valor_desconto', 'valor_pago', 'data_baixa')
    fields = ['contareceber', 'formapagamento', 'valor_juros', 'valor_multa', 'valor_desconto', 'valor_pago', 'data_baixa']
    search_fields = ('contareceber__documento', )
    list_per_page = REGISTROS_POR_PAGINA
    

@admin.register(ContaPagar)
class ContaPagarAdmin(admin.ModelAdmin):
    list_display = ('documento', 'parcela', 'contato', 'data_emissao', 'data_vencimento', 'valor_titulo', 'situacao')
    fields = ['documento', 'parcela', 'contato', 'data_emissao', 'data_vencimento', 'valor_titulo', 'observacao', 'situacao']
    search_fields = ('documento', 'contato__razao_social')
    list_per_page = REGISTROS_POR_PAGINA
    readonly_fields = ('situacao', )


@admin.register(BaixaPagar)
class BaixaPagarAdmin(admin.ModelAdmin):
    list_display = ('contapagar', 'formapagamento', 'valor_juros', 'valor_multa', 'valor_desconto', 'valor_pago', 'data_baixa')
    fields = ['contapagar', 'formapagamento', 'valor_juros', 'valor_multa', 'valor_desconto', 'valor_pago', 'data_baixa']
    search_fields = ('contapagar__documento', )
    list_per_page = REGISTROS_POR_PAGINA
    
