from django.apps import AppConfig


class CtmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CTM'

    def ready(self):
        import CTM.signals
