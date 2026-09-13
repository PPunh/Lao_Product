# coding=utf-8
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'sales'
router = DefaultRouter()

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.SalePage.as_view(), name='sale_page'),
    path('cart/', views.CartPage.as_view(), name='cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('order/<str:order_code>/success/', views.OrderSuccessView.as_view(), name='order_success'),
]

urlpatterns += router.urls
