from django.core.serializers import serialize
from django.http import HttpResponse
from cadastro.models import Municipio


def municipios(estado):
    data = serialize("json", Municipio.objects.filter(estado=estado), fields=('nome', 'capital'))
    return HttpResponse(data)
