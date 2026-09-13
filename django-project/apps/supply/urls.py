from django.urls import path

from . import views

app_name = 'supply'

urlpatterns = [
    path('', views.SupplyCenterView.as_view(), name='center'),
]