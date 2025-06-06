from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django_countries.widgets import CountrySelectWidget
import re

from store.models import Customer


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise ValidationError("Enter a valid email address.")
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email


class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'country',
            'company_name',
            'address',
            'address2',
            'state_or_country',
            'postal_code',
            'phone',
        ]
        labels = {
            'country': 'Country',
            'company_name': 'Company name',
            'address': 'Street address',
            'address2': 'Apartment / suite (optional)',
            'state_or_country': 'State / Region',
            'postal_code': 'Postal / ZIP code',
            'phone': 'Phone number',
        }
        widgets = {
            'country': CountrySelectWidget(attrs={'class': 'form-select'}),
        }

    def clean_country(self):
        value = self.cleaned_data.get('country')
        if not value or len(str(value).strip()) < 2:
            raise ValidationError("Country must be at least 2 characters.")
        return value

    def clean_postal_code(self):
        value = self.cleaned_data.get('postal_code')
        if not re.fullmatch(r'\d{5,6}', value or ''):
            raise ValidationError("Postal code must be 5 or 6 digits.")
        return value

    def clean_phone(self):
        value = self.cleaned_data.get('phone')
        if not re.fullmatch(r'\+?\d{7,15}', value or ''):
            raise ValidationError("Enter a valid phone number (7–15 digits, optional +).")
        return value
