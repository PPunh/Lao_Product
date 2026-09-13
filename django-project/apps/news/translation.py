from modeltranslation.translator import register, TranslationOptions
from .models import DemandCenterModel, NewsModel

@register(NewsModel)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'subject', 'content')


@register(DemandCenterModel)
class DemandCenterTranslationOptions(TranslationOptions):
    fields = ('name', 'address')