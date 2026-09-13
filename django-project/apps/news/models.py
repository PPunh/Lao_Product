# coding=utf-8
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import AuditModel

class NewsModel(AuditModel):
    title = models.CharField(
        max_length=255,
        verbose_name = _("Title")
    )
    subject = models.TextField(
        verbose_name = _("Subject")
    )
    images = models.ImageField(
        upload_to='news_images/',
        verbose_name = _("Images")
    )
    content = models.TextField(
        verbose_name = _("Content")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name = _("Is active")
    )


    class Meta:
        verbose_name = _("News")
        verbose_name_plural = _("News")
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)



class DemandCenterModel(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_("Demand Center Name")
    )
    address = models.TextField(
        verbose_name=_("Address")
    )
    contact_number = models.CharField(
        max_length=20,
        verbose_name=_("Contact Number")
    )
    email = models.EmailField(
        verbose_name=_("Email")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active")
    )

    class Meta:
        verbose_name = _("Demand Center")
        verbose_name_plural = _("Demand Centers")
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)