from django.apps import AppConfig


class GetchConfig(AppConfig):
    name = 'getch'

    def ready(self):
        import getch.signals
