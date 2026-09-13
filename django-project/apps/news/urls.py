# coding=utf-8
# django libs
from django.urls import path, include

# 3rd party libs
from rest_framework.routers import DefaultRouter

# custom import
from . import views

# Namespace for URLs in this users app
app_name = 'news'
router = DefaultRouter()
# router.register('', views.ViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.NewsListView.as_view(), name='news-list'),
    path('demand-center/', views.DemandCenterListView.as_view(), name='demand-center'),
    path('demand-center/<int:pk>/', views.DemandCenterDetailView.as_view(), name='demand-center-detail'),
    path('<int:pk>/', views.NewsDetailView.as_view(), name='news-detail'),
]

# when user go to path /app_name/ it will show api root page (endpoints list)
urlpatterns += router.urls
