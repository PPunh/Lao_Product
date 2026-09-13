from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView


class SupplyCenterView(TemplateView):
    template_name = 'supply/supply_center.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('Supply Center'),
            'supply_actions': [
                {'icon': 'fa-truck', 'title': _('Offer products'), 'text': _('Share products and services with buyers across Lao Product.')},
                {'icon': 'fa-clipboard-list', 'title': _('Manage listings'), 'text': _('Keep your supply information organized and easy to discover.')},
                {'icon': 'fa-handshake', 'title': _('Connect with demand'), 'text': _('Respond to active demand from local businesses and communities.')},
            ],
        })
        return context