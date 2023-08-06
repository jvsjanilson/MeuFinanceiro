from django.apps import AppConfig

class CadastroConfig(AppConfig):
    from . import signals
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cadastro'

