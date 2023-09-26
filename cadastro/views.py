from cadastro.Views.UnidadeView import UnidadeListView, UnidadeCreateView, UnidadeUpdateView, UnidadeDeleteView
from cadastro.Views.MarcaView import MarcaListView, MarcaCreateView, MarcaUpdateView, MarcaDeleteView
from cadastro.Views.CategoriaView import (CategoriaListView, CategoriaCreateView, CategoriaUpdateView,
                                          CategoriaDeleteView)
from cadastro.Views.PaisView import PaisListView, PaisCreateView, PaisUpdateView, PaisDeleteView
from cadastro.Views.EstadoView import EstadoListView, EstadoCreateView, EstadoUpdateView, EstadoDeleteView
from cadastro.Views.MunicipioView import (MunicipioListView, MunicipioCreateView, MunicipioUpdateView,
                                          MunicipioDeleteView)
from cadastro.Views.ProdutoView import ProdutoListView, ProdutoCreateView, ProdutoUpdateView, ProdutoDeleteView
from cadastro.Views.ContatoView import ContatoListView, ContatoCreateView, ContatoUpdateView, ContatoDeleteView
from cadastro.Views.FormaPagamentoView import (FormaPagamentoListView, FormaPagamentoCreateView,
                                               FormaPagamentoUpdateView, FormaPagamentoDeleteView)
from cadastro.Views.CondicaoPagamentoView import (CondicaoPagamentoListView, CondicaoPagamentoCreateView,
                                                  CondicaoPagamentoUpdateView, CondicaoPagamentoDeleteView)
from cadastro.Views.HomeView import Home
from cadastro.Views.ApiExternaView import consulta_cep
from cadastro.Views.ApiInternaView import municipios
from django.http import JsonResponse
import requests
import json
from cadastro.models import Municipio


def consulta_cnpj(request, cnpj):
    res = requests.get(f'https://publica.cnpj.ws/cnpj/{cnpj}')
    if res.status_code == 200:
        json_parse = json.loads(res.text)
        cidade = Municipio.objects.filter(codigo=json_parse['estabelecimento']['cidade']['ibge_id']).first()
        json_parse['estabelecimento']['cidade']['cidade_pk'] = cidade.pk

        return JsonResponse(json_parse)
    else:
        return JsonResponse({"status": res.status_code})
