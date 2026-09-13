from django import forms

from .models import TalentApplication, TalentOpportunity, TalentProfile


class TalentProfileForm(forms.ModelForm):
    class Meta:
        model = TalentProfile
        fields = ('headline', 'bio', 'phone', 'email', 'location', 'skills', 'experience_years', 'availability')
        widgets = {'bio': forms.Textarea(attrs={'rows': 5}), 'skills': forms.Textarea(attrs={'rows': 3})}


class TalentOpportunityForm(forms.ModelForm):
    class Meta:
        model = TalentOpportunity
        fields = ('title', 'organization_name', 'description', 'opportunity_type', 'location', 'contact_email', 'contact_phone', 'deadline')
        widgets = {'description': forms.Textarea(attrs={'rows': 5}), 'deadline': forms.DateInput(attrs={'type': 'date'})}


class TalentApplicationForm(forms.ModelForm):
    class Meta:
        model = TalentApplication
        fields = ('cover_note',)
        widgets = {'cover_note': forms.Textarea(attrs={'rows': 5})}