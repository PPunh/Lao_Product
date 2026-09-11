from django.apps import AppConfig


# make sure to update AppClassName and App name
class SalesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'apps.sales'
    verbose_name = 'Sales'
    label = 'sales'
