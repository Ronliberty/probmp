from django.apps import AppConfig


class CustomAccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_account'
    def ready(self):
        import custom_account.signals
