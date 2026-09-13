from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import SupplierProfileForm, SupplyListingForm
from .models import SupplierProfile, SupplyListing


class SupplyCenterView(ListView):
    template_name = 'supply/supply_center.html'
    context_object_name = 'listings'
    paginate_by = 12

    def get_queryset(self):
        return SupplyListing.objects.filter(
            status=SupplyListing.Status.PUBLISHED,
            is_active=True,
            supplier__is_active=True,
        ).select_related('supplier', 'product')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('Supply Center'),
            'supplier_profile': SupplierProfile.objects.filter(owner=self.request.user).first() if self.request.user.is_authenticated else None,
        })
        return context


class SupplyListingDetailView(DetailView):
    model = SupplyListing
    template_name = 'supply/supply_listing_detail.html'
    context_object_name = 'listing'

    def get_queryset(self):
        return super().get_queryset().filter(
            status=SupplyListing.Status.PUBLISHED,
            is_active=True,
            supplier__is_active=True,
        ).select_related('supplier', 'product')


class SupplierProfileCreateView(LoginRequiredMixin, CreateView):
    model = SupplierProfile
    form_class = SupplierProfileForm
    template_name = 'supply/supplier_form.html'
    success_url = reverse_lazy('supply:center')

    def dispatch(self, request, *args, **kwargs):
        if SupplierProfile.objects.filter(owner=request.user).exists():
            return redirect('supply:profile-edit')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class SupplierProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = SupplierProfile
    form_class = SupplierProfileForm
    template_name = 'supply/supplier_form.html'
    success_url = reverse_lazy('supply:center')

    def get_object(self, queryset=None):
        return SupplierProfile.objects.get(owner=self.request.user)


class SupplyListingCreateView(LoginRequiredMixin, CreateView):
    model = SupplyListing
    form_class = SupplyListingForm
    template_name = 'supply/supply_listing_form.html'
    success_url = reverse_lazy('supply:center')

    def dispatch(self, request, *args, **kwargs):
        if not SupplierProfile.objects.filter(owner=request.user).exists():
            return redirect('supply:profile-create')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.supplier = SupplierProfile.objects.get(owner=self.request.user)
        form.instance.status = SupplyListing.Status.DRAFT
        return super().form_valid(form)


class SupplyListingUpdateView(LoginRequiredMixin, UpdateView):
    model = SupplyListing
    form_class = SupplyListingForm
    template_name = 'supply/supply_listing_form.html'
    success_url = reverse_lazy('supply:center')

    def get_queryset(self):
        return super().get_queryset().filter(supplier__owner=self.request.user)


class SupplyListingDeleteView(LoginRequiredMixin, DeleteView):
    model = SupplyListing
    template_name = 'supply/confirm_delete.html'
    success_url = reverse_lazy('supply:center')

    def get_queryset(self):
        return super().get_queryset().filter(supplier__owner=self.request.user)