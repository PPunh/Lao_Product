from django.urls import path

from . import views

app_name = 'talent'

urlpatterns = [
    path('', views.TalentCenterView.as_view(), name='center'),
    path('opportunity/<int:pk>/', views.TalentOpportunityDetailView.as_view(), name='opportunity-detail'),
    path('profile/create/', views.TalentProfileCreateView.as_view(), name='profile-create'),
    path('profile/edit/', views.TalentProfileUpdateView.as_view(), name='profile-edit'),
    path('opportunity/create/', views.TalentOpportunityCreateView.as_view(), name='opportunity-create'),
    path('opportunity/<int:pk>/edit/', views.TalentOpportunityUpdateView.as_view(), name='opportunity-edit'),
    path('opportunity/<int:pk>/delete/', views.TalentOpportunityDeleteView.as_view(), name='opportunity-delete'),
    path('opportunity/<int:pk>/apply/', views.TalentApplicationCreateView.as_view(), name='application-create'),
]