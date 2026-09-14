from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import AuditModel, CodeGenerationModel
from apps.products.models import ProductsModel


class SupplierProfile(AuditModel):
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='supplier_profile',
        verbose_name=_('Owner'),
    )
    logo = models.ImageField(upload_to='supplier_logos/', blank=True, null=True, verbose_name=_('Supply Logo'))
    business_name = models.CharField(max_length=200, verbose_name=_('Business Name'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    phone = models.CharField(max_length=30, blank=True, verbose_name=_('Phone'))
    email = models.EmailField(blank=True, verbose_name=_('Email'))
    address = models.TextField(blank=True, verbose_name=_('Address'))
    province = models.CharField(max_length=100, blank=True, verbose_name=_('Province'))
    is_verified = models.BooleanField(default=False, verbose_name=_('Verified'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))

    class Meta:
        ordering = ['business_name']
        verbose_name = _('Supplier Profile')
        verbose_name_plural = _('Supplier Profiles')

    def __str__(self):
        return self.business_name


class SupplyListing(AuditModel, CodeGenerationModel):
    class ListingType(models.TextChoices):
        PRODUCT = 'product', _('Product')
        SERVICE = 'service', _('Service')

    class Status(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        PUBLISHED = 'published', _('Published')
        PAUSED = 'paused', _('Paused')

    supplier = models.ForeignKey(
        SupplierProfile,
        on_delete=models.CASCADE,
        related_name='listings',
        verbose_name=_('Supplier'),
    )
    product = models.ForeignKey(
        ProductsModel,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='supply_listings',
        verbose_name=_('Product'),
        help_text=_('Optional link to an existing product in the shop.'),
    )
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'))
    listing_type = models.CharField(max_length=20, choices=ListingType.choices, default=ListingType.PRODUCT)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name=_('Price'))
    unit = models.CharField(max_length=50, blank=True, verbose_name=_('Unit'))
    minimum_quantity = models.PositiveIntegerField(default=1, verbose_name=_('Minimum Quantity'))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Supply Listing')
        verbose_name_plural = _('Supply Listings')

    def __str__(self):
        return f'{self.title} ({self.supplier.business_name})'