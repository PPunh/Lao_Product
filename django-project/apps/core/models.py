# coding=utf-8
from django.db import models, transaction
from django.utils import timezone
from django.conf import settings
from decimal import Decimal
from django.core.exceptions import ValidationError
from apps.users.middleware import get_current_user
from django.utils.translation import gettext_lazy as _

# Models Here
def hero_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"hero_{instance.pk or 'new'}.{ext}"
    return os.path.join('uploads', 'hero_sliders', filename)


class HeroModel(models.Model):
    title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Title"),
        help_text=_("Main headline text on the slider")
    )
    subtitle = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Subtitle"),
        help_text=_("Short description or sub-headline")
    )
    image = models.ImageField(
        upload_to='uploads/hero_sliders/',
        verbose_name=_("Hero Image"),
        help_text=_("Recommended size: 1920x800px")
    )
    button_text = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_("Button Text"),
        help_text=_("e.g. Shop Now, Learn More")
    )
    button_url = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name=_("Button Link URL"),
        help_text=_("e.g. /products/ or https://example.com")
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Display Order"),
        help_text=_("Ordering sequence (e.g. 0, 1, 2)")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active"),
        help_text=_("Toggle to show/hide this slide on the frontend")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = _("Hero Slide")
        verbose_name_plural = _("Hero Slides")

    def __str__(self):
        return self.title or f"Hero Slide #{self.pk}"


class AddressModel(models.Model):
    village = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Village"))
    street = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Street"))
    district = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("District"))
    province = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Province"))
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Country"))

    class Meta:
        abstract = True


class PersonalInfoModel(AddressModel):
    name = models.CharField(max_length=50, verbose_name=_("Name"))
    surname = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Surname"))
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Phone"))
    email = models.EmailField(blank=True, null=True, verbose_name=_("Email"))

    def __str__(self):
        return f"{self.name} {self.surname}"

    class Meta:
        verbose_name = _("Personal Information")
        verbose_name_plural = _("Personal Information")


class AuditModel(models.Model):
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name = _("Created At")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name = _("Updated At")
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='%(class)s_created_by',
        verbose_name = _("Created By")
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='%(class)s_updated_by',
        verbose_name = _("Updated By")
    )

    class Meta:
        abstract = True


class CodeGenerationModel(models.Model):
    """
    Auto Generate a unique code for each models
    """
    code = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        verbose_name=_("Code")
    )

    class Meta:
        abstract = True

    def generate_code(self, prefix= None, start_number = 1):
        if not self.code:
            if not prefix:
                # Default prefix from class name if not provided
                prefix = self.__class__.__name__.upper()[:3]

            with transaction.atomic():
                # Lock the table to prevent race conditions
                last_obj = self.__class__.objects.select_for_update().order_by('-code').first()

                if last_obj and last_obj.code:
                    try:
                        # Assumes code format is PRE-NUMBER
                        content = last_obj.code.split('-')[-1]
                        last_number = int(content)
                        new_number = last_number + 1
                    except (ValueError, IndexError):
                        new_number = start_number
                else:
                    new_number = start_number
                self.code = f"{prefix} - {new_number}"

    def save(self, *args, **kwargs):
        if not self.code:
            self.generate_code()
        super().save(*args, **kwargs)
