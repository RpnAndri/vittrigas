from django import forms

class PaymentForm(forms.Form):
    card_number = forms.CharField(max_length=19, label="Card Number")
    card_holder = forms.CharField(max_length=100, label="Card Holder")
    expiry = forms.CharField(max_length=5, label="Expiry (MM/YY)")
    cvc = forms.CharField(max_length=4, label="CVC")