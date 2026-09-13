from django import forms

from .models import SupplierProfile, SupplyListing


class SupplierProfileForm(forms.ModelForm):
    class Meta:
        model = SupplierProfile
        fields = ('business_name', 'description', 'phone', 'email', 'address', 'province')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class SupplyListingForm(forms.ModelForm):
    class Meta:
        model = SupplyListing
        fields = ('product', 'title', 'description', 'listing_type', 'price', 'unit', 'minimum_quantity')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }