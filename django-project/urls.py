# django core libs
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language

# 3rd party libs
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

# URL FOR POST CHANGE LANGUAGE
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('setlang/', set_language, name='set_language'),
]


# URL of project for Multilingual
urlpatterns += i18n_patterns(
    path('admin12321/', admin.site.urls),  # admin path
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-docs'),
    path('api/redocs/', SpectacularRedocView.as_view(url_name='api-schema'), name='api-redocs'),
    path('select2/', include('django_select2.urls')),
    path('users/', include('apps.users.urls', namespace='users')),
    path('core/', include('apps.core.urls', namespace='core')),
    path('', include('apps.sales.urls', namespace='sales')),
    path('products/', include('apps.products.urls', namespace='products')),
    path('news/', include('apps.news.urls', namespace='news')),
    # SET PREFIX_DEFAULT_LANG
    prefix_default_language=True,
)

# Static and Media files handling
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
