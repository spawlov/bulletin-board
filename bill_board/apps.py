from django.apps import AppConfig


class BillBoardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bill_board'
    verbose_name = 'Доска объявлений'

    def ready(self):
        from . import signals
