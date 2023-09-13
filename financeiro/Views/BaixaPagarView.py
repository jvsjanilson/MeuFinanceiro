from financeiro.models import ContaPagar, BaixaPagar
from core.views import UserAccessMixin, InvalidFormMixin
from django.contrib.messages.views import SuccessMessageMixin
from financeiro.forms import BaixaPagarForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView, FormView, TemplateView
from financeiro.choices import SituacaoFinanceiro
from django.shortcuts import redirect
from django.db.models import ProtectedError


class BaixarContaPagarView(UserAccessMixin, InvalidFormMixin, SuccessMessageMixin, CreateView):
    template_name = 'financeiro/baixapagar/form.html'
    form_class = BaixaPagarForm
    success_url = reverse_lazy('contapagar-list')
    permission_required = ['financeiro.add_baixapagar']
    model = BaixaPagar
    fail_url = '/contapagars'
    success_message = 'Baixa efetuada com sucesso.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conta = ContaPagar.objects.get(pk=self.kwargs['contapagar'])
        context['verbose_name'] = self.model._meta.verbose_name.title
        context['conta'] = conta
        return context

    def get(self, request, *args, **kwargs):
        conta = ContaPagar.objects.get(pk=kwargs['contapagar'])
        if conta.situacao == SituacaoFinanceiro.PAGO_TOTAL:
            messages.add_message(request, messages.WARNING, 'Titulo ja foi pago totalmente.')
            return redirect('/contapagars')
        return super().get(request, *args, **kwargs)


class ListaBaixaPagarView(UserAccessMixin, TemplateView):
    success_url = reverse_lazy('contapagar-list')
    template_name = 'financeiro/baixapagar/list.html'
    permission_required = ['financeiro.view_baixapagar']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        baixas = BaixaPagar.objects.filter(contapagar=self.kwargs['contapagar'])
        conta = ContaPagar.objects.get(pk=self.kwargs['contapagar'])
        context['baixas'] = baixas
        context['conta'] = conta
        return context


class EstornarContaPagarView(UserAccessMixin, FormView):
    success_url = reverse_lazy('contapagar-list')
    template_name = 'financeiro/baixapagar/estorno.html'
    form_class = BaixaPagarForm
    permission_required = ['financeiro.undo_baixapagar']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        baixas = BaixaPagar.objects.filter(contapagar=self.kwargs['contapagar'])
        conta = ContaPagar.objects.get(pk=self.kwargs['contapagar'])
        context['baixas'] = baixas
        context['conta'] = conta
        return context

    def get(self, request, *args, **kwargs):
        baixas = BaixaPagar.objects.filter(contapagar=kwargs['contapagar'])
        if len(baixas) == 0:
            messages.add_message(request, messages.INFO, 'Sem baixa para estorno')
            return redirect('/contapagars')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pk = request.POST.get('contapagar')
        ids = request.POST.getlist('check')
        baixas = self.get_context_data()['baixas']

        if pk is not None:
            if len(ids) == 0:
                messages.add_message(request, messages.ERROR, 'Nenhum titulo foi marcado para estorno.')
                conta = ContaPagar.objects.get(pk=request.POST.get('contapagar'))
                return self.render_to_response({'baixas': baixas, 'conta': conta})
            try:
                BaixaPagar.objects.filter(contapagar=pk, pk__in=ids).delete()
                pagar = ContaPagar.objects.get(pk=pk)

                if BaixaPagar.objects.filter(contapagar=pk).exists():
                    pagar.situacao = SituacaoFinanceiro.PAGO_PARCIAL
                else:
                    pagar.situacao = SituacaoFinanceiro.ABERTO

                pagar.save()

                messages.add_message(request, messages.SUCCESS, 'Titulo estornado com sucesso.')
                return redirect('/contapagars')
            except ProtectedError:
                messages.add_message(request, messages.ERROR, 'Erro ao estornar titulo.')
                return redirect('/contapagars')
        return super().post(request, *args, **kwargs)
