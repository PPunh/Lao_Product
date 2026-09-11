# coding=utf-8
from django.views.generic import TemplateView, ListView
from django.utils.translation import gettext_lazy as _
from apps.products.models import ProductsCategoryModel, ProductsModel
from apps.core.models import HeroModel
from apps.core.mixins import SearchFilterMixin

class SalePage(SearchFilterMixin, TemplateView):
    template_name = "sales/sale_product.html"
    pagination = 20
    search_fields = [
        "name",
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Products")
        
        context['hero_sliders'] = HeroModel.objects.filter(is_active=True).order_by('order', '-created_at')

        context['product_category'] = ProductsCategoryModel.objects.all().order_by('name')

        products = ProductsModel.objects.filter(is_sellable=True).select_related('category', 'unit')
        
        selected_category = self.request.GET.get('category')
        if selected_category:
            products = products.filter(category_id=selected_category)
            
        context['products'] = products
        context['selected_category'] = selected_category
        return context