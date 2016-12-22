from django.apps import AppConfig

class ScopesConfig(AppConfig):
    name = 'compose.core.scopes'
    verbose_name = "Scopes"

    def ready(self):
        import signals
