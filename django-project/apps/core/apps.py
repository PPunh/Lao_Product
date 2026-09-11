from django.apps import AppConfig


# make sure to update AppClassName and App name
class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'apps.core'
    verbose_name = 'Core'
    label = 'core'
