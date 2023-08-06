from django.apps import AppConfig


class DjangoPyctxConfig(AppConfig):
    name = 'django_pyctx'

    def ready(self):
        from .app_settings import DJANGO_PYCTX
        from django.conf import settings

        for key, value in DJANGO_PYCTX.items():
            if not hasattr(settings, 'DJANGO_PYCTX'):
                setattr(settings['DJANGO_PYCTX'], key, value)
