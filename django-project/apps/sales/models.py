# coding=utf-8
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import CodeGenerationModel
from apps.products.models import ProductsModel


class Cart(models.Model):
    STATUS_ACTIVE = 'active'
    STATUS_CHECKOUT = 'checkout'
    STATUS_COMPLETED = 'completed'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, _('Active')),
        (STATUS_CHECKOUT, _('Checkout')),
        (STATUS_COMPLETED, _('Completed')),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='carts',
        blank=True,
        null=True,
    )
    session_key = models.CharField(max_length=64, blank=True, null=True, db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    coupon_code = models.CharField(max_length=50, blank=True, null=True, default='')
    discount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.07'))
    subtotal = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    shipping_fee = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    tax_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    grand_total = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

    @property
    def item_count(self):
        return sum(item.quantity for item in self.items.all())

    def recalculate(self):
        subtotal = sum((item.line_total for item in self.items.all()), Decimal('0.00'))
        taxable_total = max(subtotal - self.discount, Decimal('0.00'))
        tax_amount = (taxable_total * self.tax_rate).quantize(Decimal('0.01'))
        self.subtotal = subtotal
        self.tax_amount = tax_amount
        self.grand_total = subtotal - self.discount + self.shipping_fee + tax_amount
        self.save(update_fields=['coupon_code', 'discount', 'tax_rate', 'subtotal', 'shipping_fee', 'tax_amount', 'grand_total', 'updated_at'])

    def apply_coupon(self, code):
        normalized_code = (code or '').strip().upper()
        discount_map = {
            'SAVE10': Decimal('10.00'),
            'WELCOME5': Decimal('5.00'),
            'FREESHIP': Decimal('0.00'),
        }
        self.coupon_code = normalized_code
        if normalized_code in discount_map:
            self.discount = discount_map[normalized_code]
        else:
            self.discount = Decimal('0.00')
        self.recalculate()

    def __str__(self):
        return f"Cart #{self.pk or 'new'} ({self.item_count})"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(ProductsModel, on_delete=models.CASCADE, related_name='cart_items')
    variant_name = models.CharField(max_length=200, blank=True, default='', verbose_name=_('Variant'))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('Quantity'))
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    line_total = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        unique_together = ('cart', 'product', 'variant_name')
        verbose_name = _('Cart Item')
        verbose_name_plural = _('Cart Items')

    def save(self, *args, **kwargs):
        self.line_total = Decimal(self.quantity) * self.unit_price
        super().save(*args, **kwargs)
        if self.cart_id:
            self.cart.recalculate()

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class Order(CodeGenerationModel):
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        PAID = 'paid', _('Paid')
        COMPLETED = 'completed', _('Completed')
        CANCELLED = 'cancelled', _('Cancelled')

    class PaymentMethod(models.TextChoices):
        CASH = 'cash', _('Cash')
        PROMPTPAY = 'promptpay', _('PromptPay')
        ICBC_LAOS = 'icbc_laos', _('ICBC Bank (Laos)')
        BCEL_LAOS = 'bcel_laos', _('BCEL (Laos)')
        VISA = 'visa', _('Visa')
        MASTERCARD = 'mastercard', _('Mastercard')
        SWIFT_TRANSFER = 'swift_transfer', _('SWIFT Transfer')
        COD = 'cod', _('Cash on Delivery')

    customer_name = models.CharField(max_length=200, verbose_name=_('Customer Name'))
    phone = models.CharField(max_length=30, blank=True, null=True, verbose_name=_('Phone'))
    email = models.EmailField(blank=True, null=True, verbose_name=_('Email'))
    address = models.TextField(blank=True, null=True, verbose_name=_('Address'))
    tax_invoice_requested = models.BooleanField(default=False, verbose_name=_('Request Tax Invoice'))
    tax_id = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Tax ID'))
    company_name = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Company Name'))
    company_address = models.TextField(blank=True, null=True, verbose_name=_('Company Address'))
    payment_method = models.CharField(max_length=30, choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    payment_status = models.CharField(max_length=30, default='pending', verbose_name=_('Payment Status'))
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PENDING)
    subtotal = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    discount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    shipping_fee = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    tax_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    grand_total = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    notes = models.TextField(blank=True, null=True, verbose_name=_('Notes'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def save(self, *args, **kwargs):
        if not self.code:
            self.generate_code(prefix='ORD', start_number=100001)
        super().save(*args, **kwargs)

    @classmethod
    def create_from_cart(cls, cart, **order_data):
        if not cart.items.exists():
            raise ValueError('Cart is empty.')

        order = cls.objects.create(
            customer_name=order_data.get('customer_name', 'Walk-in Customer'),
            phone=order_data.get('phone'),
            email=order_data.get('email'),
            address=order_data.get('address'),
            tax_invoice_requested=order_data.get('tax_invoice_requested', False),
            tax_id=order_data.get('tax_id'),
            company_name=order_data.get('company_name'),
            company_address=order_data.get('company_address'),
            payment_method=order_data.get('payment_method', cls.PaymentMethod.CASH),
            notes=order_data.get('notes'),
            subtotal=cart.subtotal,
            discount=cart.discount,
            shipping_fee=cart.shipping_fee,
            tax_amount=cart.tax_amount,
            grand_total=cart.grand_total,
        )

        for item in cart.items.select_related('product'):
            OrderItem.objects.create(
                order=order,
                product=item.product,
                variant_name=item.variant_name,
                quantity=item.quantity,
                unit_price=item.unit_price,
            )

        return order

    def __str__(self):
        return f"{self.code} - {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(ProductsModel, on_delete=models.PROTECT, related_name='order_items')
    variant_name = models.CharField(max_length=200, blank=True, default='', verbose_name=_('Variant'))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('Quantity'))
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    line_total = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')

    def save(self, *args, **kwargs):
        self.line_total = Decimal(self.quantity) * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class InventoryReservation(models.Model):
    STATUS_ACTIVE = 'active'
    STATUS_RELEASED = 'released'
    STATUS_CONSUMED = 'consumed'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, _('Active')),
        (STATUS_RELEASED, _('Released')),
        (STATUS_CONSUMED, _('Consumed')),
    ]

    product = models.ForeignKey(ProductsModel, on_delete=models.CASCADE, related_name='reservations')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='reservations', blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    reserved_until = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Inventory Reservation')
        verbose_name_plural = _('Inventory Reservations')

    def __str__(self):
        return f"{self.product.name} reserved {self.quantity}"
