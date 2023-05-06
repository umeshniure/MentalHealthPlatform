from django.apps import AppConfig
from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules

class HealthplatformConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'healthplatform'

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'healthplatform'

