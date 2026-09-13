from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import TalentApplicationForm, TalentOpportunityForm, TalentProfileForm
from .models import TalentApplication, TalentOpportunity, TalentProfile


class TalentCenterView(ListView):
    template_name = 'talent/talent_center.html'
    context_object_name = 'opportunities'
    paginate_by = 12

    def get_queryset(self):
        return TalentOpportunity.objects.filter(status=TalentOpportunity.Status.OPEN).select_related('owner')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': _('Talent Center'),
            'talent_profile': TalentProfile.objects.filter(owner=self.request.user).first() if self.request.user.is_authenticated else None,
        })
        return context


class TalentOpportunityDetailView(DetailView):
    model = TalentOpportunity
    template_name = 'talent/opportunity_detail.html'
    context_object_name = 'opportunity'

    def get_queryset(self):
        return super().get_queryset().filter(status=TalentOpportunity.Status.OPEN)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['application_form'] = TalentApplicationForm()
        context['has_profile'] = self.request.user.is_authenticated and TalentProfile.objects.filter(owner=self.request.user).exists()
        context['has_applied'] = self.request.user.is_authenticated and TalentApplication.objects.filter(opportunity=self.object, talent__owner=self.request.user).exists()
        return context


class TalentProfileCreateView(LoginRequiredMixin, CreateView):
    form_class = TalentProfileForm
    template_name = 'talent/profile_form.html'
    success_url = reverse_lazy('talent:center')

    def dispatch(self, request, *args, **kwargs):
        if TalentProfile.objects.filter(owner=request.user).exists():
            return redirect('talent:center')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TalentProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = TalentProfileForm
    template_name = 'talent/profile_form.html'
    success_url = reverse_lazy('talent:center')

    def get_object(self, queryset=None):
        return TalentProfile.objects.get(owner=self.request.user)


class TalentOpportunityCreateView(LoginRequiredMixin, CreateView):
    form_class = TalentOpportunityForm
    template_name = 'talent/opportunity_form.html'
    success_url = reverse_lazy('talent:center')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.status = TalentOpportunity.Status.DRAFT
        return super().form_valid(form)


class TalentOpportunityUpdateView(LoginRequiredMixin, UpdateView):
    model = TalentOpportunity
    form_class = TalentOpportunityForm
    template_name = 'talent/opportunity_form.html'
    success_url = reverse_lazy('talent:center')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class TalentOpportunityDeleteView(LoginRequiredMixin, DeleteView):
    model = TalentOpportunity
    template_name = 'talent/confirm_delete.html'
    success_url = reverse_lazy('talent:center')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class TalentApplicationCreateView(LoginRequiredMixin, CreateView):
    form_class = TalentApplicationForm
    template_name = 'talent/application_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.opportunity = get_object_or_404(TalentOpportunity, pk=kwargs['pk'], status=TalentOpportunity.Status.OPEN)
        if request.user.is_authenticated and not TalentProfile.objects.filter(owner=request.user).exists():
            return redirect('talent:profile-create')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        profile = get_object_or_404(TalentProfile, owner=self.request.user)
        if TalentApplication.objects.filter(opportunity=self.opportunity, talent=profile).exists():
            return redirect('talent:opportunity-detail', pk=self.opportunity.pk)
        form.instance.opportunity = self.opportunity
        form.instance.talent = profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('talent:opportunity-detail', kwargs={'pk': self.opportunity.pk})