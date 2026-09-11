from django.apps import AppConfig


# make sure to update AppClassName and App name
class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'apps.products'
    verbose_name = 'Products'
    label = 'products'
