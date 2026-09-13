from modeltranslation.translator import TranslationOptions, register

from .models import SupplierProfile, SupplyListing


@register(SupplierProfile)
class SupplierProfileTranslationOptions(TranslationOptions):
    fields = ('business_name', 'description', 'address', 'province')


@register(SupplyListing)
class SupplyListingTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'unit')