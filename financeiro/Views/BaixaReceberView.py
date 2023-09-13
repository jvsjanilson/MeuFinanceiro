from financeiro.models import ContaReceber, BaixaReceber
from core.views import UserAccessMixin, InvalidFormMixin
from django.contrib.messages.views import SuccessMessageMixin
from financeiro.forms import BaixaReceberForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView, FormView
from financeiro.choices import SituacaoFinanceiro
from django.shortcuts import redirect
from django.db.models import ProtectedError


class BaixarContaReceberView(UserAccessMixin, InvalidFormMixin, SuccessMessageMixin, CreateView):
    template_name = 'financeiro/baixareceber/form.html'
    form_class = BaixaReceberForm
    success_url = reverse_lazy('contareceber-list')
    permission_required = ['financeiro.add_baixareceber']
    model = BaixaReceber
    fail_url = '/contarecebers'
    success_message = 'Baixa efetuada com sucesso.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conta = ContaReceber.objects.get(pk=self.kwargs['contareceber'])
        context['verbose_name'] = self.model._meta.verbose_name.title
        context['conta'] = conta
        return context

    def get(self, request, *args, **kwargs):
        conta = ContaReceber.objects.get(pk=kwargs['contareceber'])
        if conta.situacao == SituacaoFinanceiro.PAGO_TOTAL:
            messages.add_message(request, messages.WARNING, 'Titulo ja foi pago totalmente.')
            return redirect('/contarecebers')
        return super().get(request, *args, **kwargs)


class EstornarContaReceberView(UserAccessMixin, FormView):
    success_url = reverse_lazy('contareceber-list')
    template_name = 'financeiro/baixareceber/estorno.html'
    form_class = BaixaReceberForm
    permission_required = ['financeiro.add_baixareceber']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        baixas = BaixaReceber.objects.filter(contareceber=self.kwargs['contareceber'])
        conta = ContaReceber.objects.get(pk=self.kwargs['contareceber'])
        context['baixas'] = baixas
        context['conta'] = conta
        return context

    def get(self, request, *args, **kwargs):
        baixas = BaixaReceber.objects.filter(contareceber=kwargs['contareceber'])
        if len(baixas) == 0:
            messages.add_message(request, messages.INFO, 'Sem baixa para estorno')
            return redirect('/contarecebers')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pk = request.POST.get('contareceber')
        ids = request.POST.getlist('check')
        baixas = self.get_context_data()['baixas']

        if pk is not None:
            if len(ids) == 0:
                messages.add_message(request, messages.ERROR, 'Nenhum titulo foi marcado para estorno.')
                conta = ContaReceber.objects.get(pk=request.POST.get('contareceber'))
                return self.render_to_response({'baixas': baixas, 'conta': conta})
            try:
                BaixaReceber.objects.filter(contareceber=pk, pk__in=ids).delete()
                receber = ContaReceber.objects.get(pk=pk)

                if BaixaReceber.objects.filter(contareceber=pk).exists():
                    receber.situacao = SituacaoFinanceiro.PAGO_PARCIAL
                else:
                    receber.situacao = SituacaoFinanceiro.ABERTO

                receber.save()

                messages.add_message(request, messages.SUCCESS, 'Titulo estornado com sucesso.')
                return redirect('/contarecebers')
            except ProtectedError:
                messages.add_message(request, messages.ERROR, 'Erro ao estornar titulo.')
                return redirect('/contarecebers')
        return super().post(request, *args, **kwargs)
