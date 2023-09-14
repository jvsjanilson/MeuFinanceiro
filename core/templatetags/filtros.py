from django import template

register = template.Library()

@register.simple_tag
def pagination_filtros(request, page_number):
    queries = request.GET.copy()
    queries.pop('page', None)
    querystring = f'?page={page_number}'

    for q in queries.items():
        querystring += f"&{q[0]}={q[1]}"

    return querystring

@register.simple_tag
def page_current(request):
    page_number = request.GET.get('page', 1)
    if page_number == 1:
        return ""
    return f'?page={page_number}'