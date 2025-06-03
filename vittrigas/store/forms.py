from django import forms
from django.contrib.auth.models import User
from .models import Customer

class PaymentForm(forms.Form):
    card_number = forms.CharField(max_length=19, label="Card Number")
    card_holder = forms.CharField(max_length=100, label="Card Holder")
    expiry = forms.CharField(max_length=5, label="Expiry (MM/YY)")
    cvc = forms.CharField(max_length=4, label="CVC")

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    address = forms.CharField(required=False)
    password = forms.CharField(required=False, widget=forms.PasswordInput, help_text="Leave blank if you don't want to change it.")

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        customer = kwargs.pop('customer', None)
        super().__init__(*args, **kwargs)
        if customer:
            self.fields['address'].initial = customer.address

    def save(self, user, customer):
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)

        user.save()

        customer.address = self.cleaned_data['address']
        customer.save()