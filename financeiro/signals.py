from financeiro.models import BaixaReceber, ContaReceber, BaixaPagar, ContaPagar
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models import Sum
from financeiro.choices import SituacaoFinanceiro


@receiver(pre_save, sender=BaixaReceber)
def pre_save_baixareceber(sender, instance, **kwargs):
    baixas = BaixaReceber.objects.filter(contareceber=instance.contareceber.id).aggregate(total=Sum('valor_pago'))['total']
    if baixas is None: 
        baixas = 0

    obj = ContaReceber.objects.get(pk=instance.contareceber.id)
    if baixas + instance.valor_pago >= instance.contareceber.valor_titulo:
        obj.situacao = SituacaoFinanceiro.PAGO_TOTAL
    else:
        obj.situacao = SituacaoFinanceiro.PAGO_PARCIAL
    obj.save()


@receiver(pre_save, sender=BaixaPagar)
def pre_save_baixapagar(sender, instance, **kwargs):
    baixas = BaixaPagar.objects.filter(contapagar=instance.contapagar.id).aggregate(total=Sum('valor_pago'))['total']
    if baixas is None: 
        baixas = 0

    obj = ContaPagar.objects.get(pk=instance.contapagar.id)
    if baixas + instance.valor_pago >= instance.contapagar.valor_titulo:
        obj.situacao = SituacaoFinanceiro.PAGO_TOTAL
    else:
        obj.situacao = SituacaoFinanceiro.PAGO_PARCIAL
    obj.save()
