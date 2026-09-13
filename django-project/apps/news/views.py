# coding=utf-8
from django.views.generic import ListView, DetailView
from apps.core.mixins import SearchFilterMixin
from django.utils.translation import gettext_lazy as _
from .models import DemandCenterModel, NewsModel

class NewsListView(SearchFilterMixin, ListView):
    model = NewsModel
    template_name = 'news/news.html'
    context_object_name = 'news_list'
    paginate_by = 10
    search_fields = ['title', 'subject', 'content']

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("News")
        return context


class NewsDetailView(DetailView):
    model = NewsModel
    template_name = 'news/news_detail.html'
    context_object_name = 'news'

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context


class DemandCenterListView(ListView):
    model = DemandCenterModel
    template_name = 'news/demand_center.html'
    context_object_name = 'demand_centers'
    paginate_by = 12

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Demand Center')
        return context


class DemandCenterDetailView(DetailView):
    model = DemandCenterModel
    template_name = 'news/demand_center_detail.html'
    context_object_name = 'demand_center'

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context

    