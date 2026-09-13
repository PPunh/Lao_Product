from django.apps import AppConfig


# make sure to update AppClassName and App name
class NewsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'apps.news'
    verbose_name = 'News'
    label = 'news'