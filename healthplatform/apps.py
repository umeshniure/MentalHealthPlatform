from django.apps import AppConfig
from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules

class HealthplatformConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'healthplatform'

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'healthplatform'
# 
    def ready(self):
        # Autodiscover all modules in the app to ensure signals are connected
        autodiscover_modules('signals')

        # Send the startup signal
        from .signals import startup_signal
        startup_signal.send(sender=self.__class__)
# 