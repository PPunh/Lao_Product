from modeltranslation.translator import register, TranslationOptions
from .models import NewsModel

@register(NewsModel)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'subject', 'content')