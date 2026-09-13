from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView


class MarketUpdatesView(TemplateView):
    template_name = 'market/market_updates.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('Market Updates'),
            'market_sections': [
                {'icon': 'fa-chart-line', 'title': _('Local signals'), 'text': _('Follow useful changes in products, services, and local business activity.')},
                {'icon': 'fa-arrow-trend-up', 'title': _('Opportunities'), 'text': _('Keep an eye on emerging categories and areas of growing demand.')},
                {'icon': 'fa-newspaper', 'title': _('Latest news'), 'text': _('Read the latest updates published by the Lao Product community.'), 'url': 'news:news-list'},
            ],
        })
        return context