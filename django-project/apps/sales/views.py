# coding=utf-8
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import modelform_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from apps.core.mixins import SearchFilterMixin
from apps.core.models import HeroModel
from apps.products.models import ProductsCategoryModel, ProductsModel

from .forms import CheckoutForm
from .models import Cart, CartItem, Order


def get_or_create_cart(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart, created = Cart.objects.get_or_create(session_key=session_key)
    if request.user.is_authenticated and (cart.user is None or cart.user != request.user):
        cart.user = request.user
        cart.save(update_fields=['user'])
    return cart


@require_POST
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1) or 1)

    if not product_id:
        messages.error(request, _('Product was not selected.'))
        return redirect('sales:sale_page')

    product = get_object_or_404(ProductsModel, pk=product_id)
    cart = get_or_create_cart(request)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'unit_price': product.price, 'quantity': 0, 'variant_name': ''},
    )
    item.unit_price = product.price
    item.quantity += quantity
    item.save()
    cart.recalculate()

    messages.success(request, _('%(product)s added to cart.') % {'product': product.name})
    return redirect('sales:cart')


@require_POST
def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart=get_or_create_cart(request))
    quantity = int(request.POST.get('quantity', 1) or 1)
    if quantity <= 0:
        item.delete()
        messages.info(request, _('Item removed from cart.'))
    else:
        item.quantity = quantity
        item.save()
        messages.success(request, _('Cart updated.'))
    return redirect('sales:cart')


@require_POST
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart=get_or_create_cart(request))
    item.delete()
    messages.info(request, _('Item removed from cart.'))
    return redirect('sales:cart')


@require_POST
def apply_coupon(request):
    cart = get_or_create_cart(request)
    code = request.POST.get('coupon_code', '').strip()
    cart.apply_coupon(code)
    if cart.discount > 0:
        messages.success(request, _('Coupon applied successfully.'))
    else:
        messages.info(request, _('Coupon code was not recognized.'))
    return redirect('sales:cart')


class SalePage(SearchFilterMixin, TemplateView):
    template_name = 'sales/sale_product.html'
    pagination = 20
    search_fields = ['name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Products')
        context['hero_sliders'] = HeroModel.objects.filter(is_active=True).order_by('order', '-created_at')
        context['product_category'] = ProductsCategoryModel.objects.all().order_by('name')

        products = ProductsModel.objects.filter(is_sellable=True).select_related('category', 'unit')
        selected_category = self.request.GET.get('category')
        if selected_category:
            products = products.filter(category_id=selected_category)

        context['products'] = products
        context['selected_category'] = selected_category
        cart = get_or_create_cart(self.request)
        context['cart_count'] = cart.item_count
        return context


class CartPage(TemplateView):
    template_name = 'sales/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_or_create_cart(self.request)
        cart.recalculate()
        context['cart'] = cart
        context['items'] = cart.items.select_related('product').order_by('product__name')
        context['title'] = _('Shopping Cart')
        return context


class CheckoutView(FormView):
    template_name = 'sales/checkout.html'
    form_class = CheckoutForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_or_create_cart(self.request)
        cart.recalculate()
        context['cart'] = cart
        context['items'] = cart.items.select_related('product').order_by('product__name')
        return context

    def form_valid(self, form):
        cart = get_or_create_cart(self.request)
        if not cart.items.exists():
            messages.error(self.request, _('Your cart is empty.'))
            return redirect('sales:cart')

        coupon_code = (form.cleaned_data.get('coupon_code') or '').strip()
        if coupon_code:
            cart.apply_coupon(coupon_code)

        cart.shipping_fee = form.cleaned_data.get('shipping_fee') or Decimal('0.00')
        cart.recalculate()

        order = Order.create_from_cart(
            cart,
            customer_name=form.cleaned_data['customer_name'],
            phone=form.cleaned_data.get('phone'),
            email=form.cleaned_data.get('email'),
            address=form.cleaned_data.get('address'),
            tax_invoice_requested=form.cleaned_data.get('tax_invoice_requested', False),
            tax_id=form.cleaned_data.get('tax_id'),
            company_name=form.cleaned_data.get('company_name'),
            company_address=form.cleaned_data.get('company_address'),
            payment_method=form.cleaned_data.get('payment_method', Order.PaymentMethod.CASH),
            notes=form.cleaned_data.get('notes'),
        )

        cart.status = Cart.STATUS_COMPLETED
        cart.save(update_fields=['status', 'updated_at'])
        messages.success(self.request, _('Order created successfully.'))
        return redirect('sales:order_success', order_code=order.code)


class OrderSuccessView(TemplateView):
    template_name = 'sales/order_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = get_object_or_404(Order, code=kwargs.get('order_code'))
        context['order'] = order
        context['title'] = _('Order Confirmed')
        return context
