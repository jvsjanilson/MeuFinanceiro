import datetime
from typing import Any
from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView
from core.views import UserAccessMixin
from django.contrib import messages
from decimal import Decimal


def fluxo_pagamento_resumo_dia(data_inicial, data_final) -> list:
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute(
        """
            SELECT 
                q.data_baixa,
                q.total_pagar_pago,
                q.total_receber_pago,
                SUM(q.total_receber_pago-q.total_pagar_pago) AS saldo
            FROM  (
                SELECT 
                    data_baixa,
                    SUM(
                        case 
                            when tipo = 'pagar' then 
                                br_total_pago
                            ELSE 
                            0
                        END 
                    ) AS total_pagar_pago,

                    SUM(
                        case 
                            when tipo = 'receber' then 
                            br_total_pago
                        ELSE 
                            0
                        END 
                    ) AS total_receber_pago
                FROM (
                    (
                        SELECT 
                            'receber' AS tipo,
                            br.data_baixa, 
                            SUM(COALESCE(br.valor_pago,0)) AS br_total_pago
                        FROM financeiro_baixareceber br
                        GROUP BY br.data_baixa
                        ORDER by br.data_baixa
                    )
                    UNION
                    (
                        SELECT 
                            'pagar' AS tipo,
                            br.data_baixa, 
                            SUM(COALESCE(br.valor_pago,0)) AS bp_total_pago
                        FROM financeiro_baixapagar br
                        GROUP BY br.data_baixa
                        ORDER by br.data_baixa
                    )
                ) t
                GROUP BY data_baixa
            ) q where q.data_baixa >= %s  and q.data_baixa <= %s
            GROUP BY q.data_baixa
            ORDER BY q.data_baixa
        """, [data_inicial, data_final]
    )

    columns = [col[0] for col in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    saldo = Decimal('0.00')
    for i in rows:
        saldo += i['saldo']
    return [saldo, rows]


class FluxoCaixaView(UserAccessMixin, TemplateView):
    template_name = 'financeiro/fluxo/list.html'
    tipos_fluxo = {'1': 'Resumo por dia'}
    permission_required = ['financeiro.fluxo_contareceber']

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        params = request.GET
        try:
            if len(params) > 0:
                if params['tipo_fluxo'] is None or params['tipo_fluxo'] == "":
                    messages.add_message(request, messages.ERROR, 'Tipo do fluxo não informado')
                elif params['data_inicial'] is None or params['data_inicial'] == "":
                    messages.add_message(request, messages.ERROR, 'Data Inicial deve ser informado')
                elif params['data_final'] is None or params['data_final'] == "":
                    messages.add_message(request, messages.ERROR, 'Data Final deve ser informado')

                data_inicial = datetime.datetime.strptime(params['data_inicial'], "%Y-%m-%d").date()
                data_final = datetime.datetime.strptime(params['data_final'], "%Y-%m-%d").date()
                if data_inicial.year != data_final.year:
                    messages.add_message(request, messages.ERROR, 'Informe o mesmo ano na data inicial e final')
        except ValueError:
            pass

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data_inicial = self.request.GET.get('data_inicial')
        data_final = self.request.GET.get('data_final')
        tipo_fluxo = self.request.GET.get('tipo_fluxo')

        if tipo_fluxo is None:
            tipo_fluxo = '1'

        context['titulo'] = f'Fluxo de pagamento - {self.tipos_fluxo[tipo_fluxo]}'
        context['tipo_fluxo'] = tipo_fluxo

        if data_final == "":
            data_final = None

        if data_inicial == "":
            data_inicial = None

        context['data_inicial'] = data_inicial
        context['data_final'] = data_final
        context['saldo'] = Decimal('0.00')

        if not any(x is None for x in [data_inicial, data_final]):
            d_inicial = datetime.datetime.strptime(data_inicial, "%Y-%m-%d").date()
            d_final = datetime.datetime.strptime(data_final, "%Y-%m-%d").date()
            if d_inicial.year == d_final.year:
                context['saldo'], context['recebers'] = fluxo_pagamento_resumo_dia(data_inicial, data_final)

        return context
