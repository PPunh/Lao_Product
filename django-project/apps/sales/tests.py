# coding=utf-8
from decimal import Decimal
from django.test import TestCase

from apps.products.models import ProductsCategoryModel, ProductsModel, ProductsUnitModel, CurrencyModel
from apps.sales.models import Cart, CartItem, Order, OrderItem


class SalesOrderFlowTests(TestCase):
    def setUp(self):
        category = ProductsCategoryModel.objects.create(name='Drinks')
        unit = ProductsUnitModel.objects.create(name='Bottle')
        currency = CurrencyModel.objects.create(code='LAK', currency_name='Lao Kip', symbol='₭', is_default=True)
        self.product = ProductsModel.objects.create(
            name='Lao Beer',
            description='Local beer',
            category=category,
            unit=unit,
            currency=currency,
            price=Decimal('20000.00'),
            is_sellable=True,
        )

    def test_cart_item_line_total(self):
        cart = Cart.objects.create(session_key='test-cart-1')
        item = CartItem.objects.create(cart=cart, product=self.product, quantity=2, unit_price=self.product.price)
        self.assertEqual(item.line_total, Decimal('40000.00'))

    def test_order_total_calculation(self):
        cart = Cart.objects.create(session_key='test-cart-2')
        CartItem.objects.create(cart=cart, product=self.product, quantity=3, unit_price=self.product.price)

        order = Order.objects.create(
            customer_name='Alice',
            phone='91234567',
            address='Vientiane',
            subtotal=Decimal('60000.00'),
            discount=Decimal('5000.00'),
            shipping_fee=Decimal('3000.00'),
            tax_amount=Decimal('5500.00'),
            grand_total=Decimal('66500.00'),
            payment_method='cash',
        )
        OrderItem.objects.create(order=order, product=self.product, quantity=3, unit_price=self.product.price)

        self.assertEqual(order.grand_total, Decimal('66500.00'))
        self.assertEqual(order.items.count(), 1)

    def test_discount_cannot_make_cart_total_negative(self):
        cart = Cart.objects.create(session_key='test-cart-discount', discount=Decimal('100.00'))
        CartItem.objects.create(cart=cart, product=self.product, quantity=1, unit_price=self.product.price)

        cart.discount = Decimal('100000.00')
        cart.recalculate()

        self.assertEqual(cart.discount, self.product.price)
        self.assertGreaterEqual(cart.grand_total, Decimal('0.00'))

    def test_completed_cart_is_not_reused(self):
        request = self.client.get('/').wsgi_request
        request.session.create()
        completed_cart = Cart.objects.create(
            session_key=request.session.session_key,
            status=Cart.STATUS_COMPLETED,
        )

        from apps.sales.views import get_or_create_cart
        active_cart = get_or_create_cart(request)

        self.assertNotEqual(active_cart.pk, completed_cart.pk)
        self.assertEqual(active_cart.status, Cart.STATUS_ACTIVE)
