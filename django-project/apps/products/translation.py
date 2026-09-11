# translation.py
from modeltranslation.translator import register, TranslationOptions
from .models import (
    ProductsCategoryModel,
    ProductsUnitModel,
    CurrencyModel,
    ProductsModel
)

@register(CurrencyModel)
class CurrencyTranslationOption(TranslationOptions):
    fields = ('code', 'currency_name', 'symbol')

@register(ProductsCategoryModel)
class ProductsCategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(ProductsUnitModel)
class ProductsUnitTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(ProductsModel)
class ProductsTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'price')
