from django.urls import path

from . import views

app_name = 'supply'

urlpatterns = [
    path('', views.SupplyCenterView.as_view(), name='center'),
    path('listing/<int:pk>/', views.SupplyListingDetailView.as_view(), name='listing-detail'),
    path('profile/create/', views.SupplierProfileCreateView.as_view(), name='profile-create'),
    path('profile/edit/', views.SupplierProfileUpdateView.as_view(), name='profile-edit'),
    path('listing/create/', views.SupplyListingCreateView.as_view(), name='listing-create'),
    path('listing/<int:pk>/edit/', views.SupplyListingUpdateView.as_view(), name='listing-edit'),
    path('listing/<int:pk>/delete/', views.SupplyListingDeleteView.as_view(), name='listing-delete'),
]