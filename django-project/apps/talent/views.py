from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView


class TalentCenterView(TemplateView):
    template_name = 'talent/talent_center.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('Talent Center'),
            'talent_actions': [
                {'icon': 'fa-user-plus', 'title': _('Create your profile'), 'text': _('Present your skills, experience, and interests to local opportunities.')},
                {'icon': 'fa-magnifying-glass', 'title': _('Find opportunities'), 'text': _('Explore practical work and collaboration opportunities as they become available.')},
                {'icon': 'fa-comments', 'title': _('Build connections'), 'text': _('Start conversations with organizations looking for capable people.')},
            ],
        })
        return context