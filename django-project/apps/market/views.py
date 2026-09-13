from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView

from .models import MarketCategory, MarketUpdate


class MarketUpdatesView(ListView):
    template_name = 'market/market_updates.html'
    context_object_name = 'updates'
    paginate_by = 12

    def get_queryset(self):
        updates = MarketUpdate.objects.filter(is_published=True).select_related('category', 'product', 'demand_center')
        category = self.request.GET.get('category')
        if category:
            updates = updates.filter(category__slug=category)
        return updates

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('Market Updates'),
            'categories': MarketCategory.objects.filter(is_active=True),
            'selected_category': self.request.GET.get('category', ''),
        })
        return context


class MarketUpdateDetailView(DetailView):
    model = MarketUpdate
    template_name = 'market/market_update_detail.html'
    context_object_name = 'update'

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True).select_related('category', 'product', 'demand_center')