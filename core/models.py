from django.db import models


class GenericoModel(models.Model):
    created_at = models.DateTimeField('Criado em ', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em ', auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
