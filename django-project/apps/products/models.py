# coding=utf-8
from django.db import models
from decimal import Decimal
from apps.core.models import AuditModel, CodeGenerationModel
from django.utils.translation import gettext_lazy as _

class ProductsCategoryModel(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Category"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))


    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("Products Category")
        verbose_name_plural = _("Products Categories")
        ordering = ["name"]


class ProductsUnitModel(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Unit"))

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("Products Unit")
        verbose_name_plural = _("Products Units")
        ordering = ["name"]

class CurrencyModel(models.Model):
    code = models.CharField(
        max_length=3,
        blank=True, null=True,
        verbose_name=_("Currency Code"),
        help_text=_("e.g. LAK, USD, CNY, THB")
    )
    currency_name = models.CharField(
        max_length=50,
        blank=True, null=True,
        verbose_name=_("Currency Name")
    )
    symbol = models.CharField(
        max_length=10,
        blank=True, null=True,
        verbose_name=_("Symbol / Icon"),
        help_text=_("e.g. ₭, $, ¥, ฿")
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name=_("Is Default Currency")
    )

    def __str__(self):
        return f"{self.code} ({self.symbol})"

    class Meta:
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")


class ProductsModel(AuditModel, CodeGenerationModel):
    name = models.CharField(max_length=200, verbose_name=_("Name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    category = models.ForeignKey(ProductsCategoryModel, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("Category"))
    unit = models.ForeignKey(ProductsUnitModel, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("Unit"))
    currency = models.ForeignKey(
        CurrencyModel,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name=_("Currency")
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        verbose_name=_("Price")
    )
    is_sellable = models.BooleanField(default=True, verbose_name=_("Is Sellable"))
    product_img = models.ImageField(
        upload_to='products/images',
        blank=True,
        null=True,
        verbose_name=_("Product Image")
    )

    def __str__(self):
        stock = self.stocks.first()
        quantity = stock.quantity if stock else 0
        return f"SKU: {self.code} | {self.name} | Instock: {quantity}"

    class Meta:
        verbose_name = _("Products")
        verbose_name_plural = _("Products")
        ordering = ["-code"]

    def save(self, *args, **kwargs):
        if not self.code:
            self.generate_code(prefix="PRD", start_number=251354)

        super().save(*args, **kwargs)


class StocksModel(models.Model):
    product = models.ForeignKey(
        ProductsModel,
        on_delete=models.CASCADE,
        verbose_name=_("Product"),
        related_name="stocks",
    )
    quantity = models.IntegerField(
        verbose_name=_("Quantity"),
        default=0
    )

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = _("Stock")
        verbose_name_plural = _("Stocks")
        ordering = ["product"]
