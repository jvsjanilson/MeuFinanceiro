from django.core.serializers import serialize
from django.http import HttpResponse
from cadastro.models import Municipio


def municipios(request, estado):
    print(estado)
    data = serialize("json", Municipio.objects.filter(estado=estado), fields=('nome', 'capital'))
    print(data)
    return HttpResponse(data)
