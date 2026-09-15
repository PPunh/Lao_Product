# translation.py ในแอปของคุณ
from modeltranslation.translator import register, TranslationOptions
from .models import HeroModel, PersonalInfoModel

@register(HeroModel)
class HeroTranslationOptions(TranslationOptions):
    fields = ('title', 'image', 'subtitle', 'button_text')


@register(PersonalInfoModel)
class PersonalInfoTranslationOptions(TranslationOptions):
    fields = ('name', 'surname', 'village', 'street', 'district', 'province', 'country')
