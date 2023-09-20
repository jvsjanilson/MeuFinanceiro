import requests
from django.http import HttpRequest, HttpResponse, JsonResponse
from cadastro.models import Municipio
from django.db.models import Case, Value, When


def consulta_cep(cep):
    consulta = requests.get(f'https://viacep.com.br/ws/{cep}/json')
    json = consulta.json()
    lista_municipios = Municipio.objects.filter(estado__uf=json['uf']).values('id', 'nome').annotate(
        selected=Case(
            When(codigo=json['ibge'], then=Value(True)),
            default=Value(False)
        )
    )

    json["municipios"] = list(lista_municipios)
    return JsonResponse(json)