# # coding=utf-8
# from django.db import models, transaction
# from django.db.models import Sum, F, ExpressionWrapper
# from django.core.exceptions import ValidationError
# from decimal import Decimal
# from apps.core.models import AuditModel, CodeGenerationModel
# from apps.products.models import ProductsModel
# from apps.stocks.models import StocksModel
# from django.utils.translation import gettext_lazy as _
#
# class CartManager:
#     @staticmethod
#     def get_cart_items(cart_dict, event_id=None):
#         cart_items = []
#         total_price = Decimal('0')
#         cleaned_cart = {}
#
#         if not isinstance(cart_dict, dict):
#             return [], Decimal('0'), {}
#
#         from apps.events.models import EventProductItemModel
#
#         for product_id, data in cart_dict.items():
#             try:
#                 qty = data['quantity'] if isinstance(data, dict) else int(data)
#                 if qty <= 0: continue
#
#                 product = ProductsModel.objects.get(pk=product_id)
#                 sell_price = product.sell_price
#
#                 if event_id:
#                     event_item = EventProductItemModel.objects.filter(
#                         event_id=event_id,
#                         product_id=product_id
#                     ).first()
#                     if event_item:
#                         sell_price = event_item.event_sell_price
#
#                 subtotal = sell_price * qty
#                 total_price += subtotal
#
#                 cart_items.append({
#                     'product': product,
#                     'quantity': qty,
#                     'unit_price': sell_price,
#                     'subtotal': subtotal
#                 })
#                 cleaned_cart[str(product_id)] = data
#             except (ProductsModel.DoesNotExist, ValueError, TypeError):
#                 continue
#
#         return cart_items, total_price, cleaned_cart
#
#     @staticmethod
#     def calculate_totals(total_price, tax_rate, discount=Decimal('0')):
#         """Calculate tax and total for checkout/payment page"""
#         price_after_discount = max(Decimal('0'), total_price - discount)
#         tax_amount = (price_after_discount * tax_rate).quantize(Decimal('0.01'))
#         total_with_tax = price_after_discount + tax_amount
#
#         return tax_amount, total_with_tax, price_after_discount
#
#     @staticmethod
#     def get_cart_count(cart_dict):
#         if not isinstance(cart_dict, dict): return 0
#         total = 0
#         for v in cart_dict.values():
#             if isinstance(v, dict):
#                 total += int(v.get('quantity', 0))
#             else:
#                 total += int(v)
#         return total
#
#
# class SalesOrderModel(AudiCoreModel, CodeGenerationModel):
#     class Status(models.TextChoices):
#         DRAFT = 'draft', _("Draft")
#         CONFIRMED = 'confirmed', _("Confirmed")
#         CANCELLED = 'cancelled', _("Cancelled")
#
#     customer = models.ForeignKey(PartnersModel, on_delete=models.SET_NULL, related_name='sales_orders', blank=True, null=True, verbose_name=_("Customer"))
#     status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, verbose_name=_("Status"))
#
#     total_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
#     discount = models.DecimalField(max_digits=20, decimal_places=2, default=0, verbose_name=_("Discount"))
#
#     tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.10'), verbose_name=_("Tax Rate"))
#     tax_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0, verbose_name=_("Tax Amount"))
#     grand_total = models.DecimalField(max_digits=20, decimal_places=2, default=0, verbose_name=_("Grand Total"))
#
#     exchange_rate = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('750'), verbose_name=_("Exchange Rate"))
#     remark = models.TextField(blank=True, null=True, verbose_name=_("Remark"))
#     event = models.ForeignKey('events.EventsModel', on_delete=models.SET_NULL, null=True, blank=True, related_name='sales_orders', verbose_name=_("Event"))
#
#     def __str__(self):
#         return f"{self.code} - {self.customer.name}"
#
#     @property
#     def is_b2b(self):
#         # Check it's Organization customer
#         return self.customer is not None
#
#     @property
#     def customer_name_display(self):
#         # Show Customer Name or Walk-In if None
#         if self.customer:
#             return self.customer.company_name or self.customer.name
#         return "Walk-In Customer"
#
#     @classmethod
#     @transaction.atomic
#     def create_from_cart(cls, cart_dict, customer, remark="", discount=Decimal('0'), event_id=None):
#         cart_items, total_price, _ = CartManager.get_cart_items(cart_dict, event_id=event_id)
#
#         if not cart_items:
#             raise ValidationError("No items in cart")
#
#         config = SystemConfigModel.get_settings()
#         order = cls.objects.create(
#             customer=customer,
#             tax_rate=config.tax_rate,
#             exchange_rate=config.exchange_rate,
#             remark=remark,
#             discount=discount,
#             event_id=event_id
#         )
#
#         from apps.events.models import EventProductItemModel
#
#         for item in cart_items:
#             product = item['product']
#             qty = item['quantity']
#
#             if event_id:
#                 event_product = EventProductItemModel.objects.filter(
#                     event_id=event_id, product_id=product.id
#                 ).first()
#
#                 if not event_product or event_product.remaining_stock < qty:
#                     # raise ValidationError(f"Product: {product.name} in this EVENT not enough (Available: {event_product.remaining_stock if event_product else 0})")
#                     message_msg = _("Product: {product_name} in this EVENT not enough (Available: {event_product_remaining_stock})").format(
#                         product_name=product.name,
#                         event_product_remaining_stock=event_product.remaining_stock if event_product else 0
#                     )
#                     raise ValidationError(message_msg)
#
#                 event_product.sold_quantity += qty
#                 event_product.save()
#             else:
#                 stock = StocksModel.objects.filter(product=product).first()
#                 if not stock or stock.quantity < qty:
#                     # raise ValidationError(f"Product: {product.name} In Main Stock not enough")
#                     message_msg = _("Product: {product_name} In Main Stock not enough").format(
#                         product_name=product.name
#                     )
#                     raise ValidationError(message_msg)
#
#                 # stock.quantity -= qty
#                 # stock.save()
#
#             SaleItemModel.objects.create(
#                 sales_order=order,
#                 product=product,
#                 quantity=qty,
#                 unit_price=item['unit_price']
#             )
#
#         tax_amount, grand_total, _ = CartManager.calculate_totals(
#             total_price, order.tax_rate, discount
#         )
#         order.total_amount = total_price
#         order.tax_amount = tax_amount
#         order.grand_total = grand_total
#         order.status = cls.Status.CONFIRMED
#         order.save()
#
#         for item in order.items.all():
#             StockTransactionModel.objects.create(
#                 transaction_type="OUT",
#                 product=item.product,
#                 quantity=item.quantity,
#                 partner=customer,
#             )
#
#         return order
#
#     def confirm_order(self):
#         if self.status != self.Status.DRAFT:
#             raise ValidationError(_("Order has already been CONFIRMED"))
#
#         with transaction.atomic():
#             for item in self.items.all():
#                 StockTransactionModel.objects.create(
#                     transaction_type="OUT",
#                     product=item.product,
#                     quantity=item.quantity,
#                     partner=self.customer,
#                 )
#             self.status = self.Status.CONFIRMED
#             self.save()
#
#     def save(self, *args, **kwargs):
#         if not self.code:
#             self.generate_code(prefix="INV", start_number=500001)
#         super().save(*args, **kwargs)
#
# class SaleItemModel(models.Model):
#     sales_order = models.ForeignKey(SalesOrderModel, on_delete=models.CASCADE, related_name='items')
#     product = models.ForeignKey(ProductsModel, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     unit_price = models.DecimalField(max_digits=12, decimal_places=2)
#     subtotal = models.DecimalField(max_digits=20, decimal_places=2, editable=False)
#
#     def save(self, *args, **kwargs):
#         self.subtotal = Decimal(self.quantity) * self.unit_price
#         super().save(*args, **kwargs)
