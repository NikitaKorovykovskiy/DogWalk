from django.apps import AppConfig


class DwConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dw'
    verbose_name = "Заказы выгула собак"