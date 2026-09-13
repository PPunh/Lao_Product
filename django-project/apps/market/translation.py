from modeltranslation.translator import TranslationOptions, register

from .models import MarketCategory, MarketUpdate


@register(MarketCategory)
class MarketCategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(MarketUpdate)
class MarketUpdateTranslationOptions(TranslationOptions):
    fields = ('title', 'summary', 'content')