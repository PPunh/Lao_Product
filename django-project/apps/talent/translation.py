from modeltranslation.translator import TranslationOptions, register

from .models import TalentOpportunity, TalentProfile


@register(TalentProfile)
class TalentProfileTranslationOptions(TranslationOptions):
    fields = ('headline', 'bio', 'location', 'skills')


@register(TalentOpportunity)
class TalentOpportunityTranslationOptions(TranslationOptions):
    fields = ('title', 'organization_name', 'description', 'location')