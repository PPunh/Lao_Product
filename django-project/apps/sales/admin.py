# coding=utf-8
from django.contrib import admin

from .models import Cart, CartItem, InventoryReservation, Order, OrderItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_key', 'status', 'item_count', 'grand_total', 'updated_at')
    list_filter = ('status', 'updated_at')
    search_fields = ('session_key', 'user__username', 'user__email')
    readonly_fields = ('subtotal', 'tax_amount', 'grand_total', 'created_at', 'updated_at')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'variant_name', 'quantity', 'unit_price', 'line_total')
    search_fields = ('product__name', 'cart__session_key', 'variant_name')
    list_filter = ('product',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('code', 'customer_name', 'payment_method', 'payment_status', 'status', 'grand_total', 'created_at')
    list_filter = ('status', 'payment_status', 'payment_method', 'created_at')
    search_fields = ('code', 'customer_name', 'phone', 'email')
    readonly_fields = ('code', 'created_at', 'updated_at')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'variant_name', 'quantity', 'unit_price', 'line_total')
    search_fields = ('order__code', 'product__name', 'variant_name')


@admin.register(InventoryReservation)
class InventoryReservationAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'quantity', 'status', 'reserved_until', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('product__name', 'order__code')
    readonly_fields = ('created_at',)
