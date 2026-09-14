from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from apps.core.models import AuditModel
from apps.news.models import DemandCenterModel
from apps.products.models import ProductsModel


class MarketCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Name'))
    slug = models.SlugField(max_length=120, unique=True, blank=True, verbose_name=_('Slug'), help_text=_("Automatically generated from the name if left blank."))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))

    class Meta:
        ordering = ['name']
        verbose_name = _('Market Category')
        verbose_name_plural = _('Market Categories')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class MarketUpdate(AuditModel):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='market_updates',
        verbose_name=_('Author'),
    )
    category = models.ForeignKey(
        MarketCategory,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='updates',
        verbose_name=_('Category'),
    )
    product = models.ForeignKey(
        ProductsModel,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='market_updates',
        verbose_name=_('Related Product'),
    )
    demand_center = models.ForeignKey(
        DemandCenterModel,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='market_updates',
        verbose_name=_('Related Demand Center'),
    )
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    summary = models.TextField(verbose_name=_('Summary'))
    content = models.TextField(verbose_name=_('Content'))
    image = models.ImageField(upload_to='market_updates/', blank=True, null=True, verbose_name=_('Image'))
    source_url = models.URLField(blank=True, verbose_name=_('Source URL', ), help_text=_('Optional link to the original source of the update.'))
    is_featured = models.BooleanField(default=False, verbose_name=_('Featured'))
    is_published = models.BooleanField(default=False, verbose_name=_('Published'))
    published_at = models.DateTimeField(blank=True, null=True, verbose_name=_('Published At'))

    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = _('Market Update')
        verbose_name_plural = _('Market Updates')

    def __str__(self):
        return self.title