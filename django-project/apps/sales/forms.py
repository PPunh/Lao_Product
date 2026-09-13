# coding=utf-8
from django import forms


class CartQuantityForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)


class CheckoutForm(forms.Form):
    customer_name = forms.CharField(max_length=200, label='Customer Name')
    phone = forms.CharField(max_length=30, required=False, label='Phone')
    email = forms.EmailField(required=False, label='Email')
    address = forms.CharField(widget=forms.Textarea, label='Address')
    coupon_code = forms.CharField(max_length=50, required=False, label='Coupon Code')
    shipping_fee = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0, initial=0, label='Shipping Fee')
    tax_invoice_requested = forms.BooleanField(required=False, label='Request Tax Invoice')
    tax_id = forms.CharField(max_length=100, required=False, label='Tax ID')
    company_name = forms.CharField(max_length=200, required=False, label='Company Name')
    company_address = forms.CharField(widget=forms.Textarea, required=False, label='Company Address')
    payment_method = forms.ChoiceField(
        label='Payment Method',
        choices=[
            ('cash', 'Cash'),
            ('promptpay', 'PromptPay'),
            ('icbc_laos', 'ICBC Bank (Laos)'),
            ('bcel_laos', 'BCEL (Laos)'),
            ('visa', 'Visa'),
            ('mastercard', 'Mastercard'),
            ('swift_transfer', 'SWIFT Transfer'),
            ('cod', 'Cash on Delivery'),
        ],
        initial='cash',
    )
    notes = forms.CharField(widget=forms.Textarea, required=False, label='Notes')

    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')
        notes = (cleaned_data.get('notes') or '').strip()
        if payment_method not in {'cash', 'cod'} and not notes:
            self.add_error('notes', 'Please provide the payment information.')
        return cleaned_data
