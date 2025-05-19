# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Host


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class HostSignUpForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Enter your first name'
        })
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Enter your last name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Enter your email address'
        })
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Enter your phone number'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Create password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Confirm password'
        })
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Enter your address',
            'rows': 3
        })
    )
    terms_accepted = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': 'h-4 w-4 text-primary border-gray-300 rounded focus:ring-2 focus:ring-primary'
        })
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2', 'address', 'terms_accepted')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Use email as username
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Host.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number'],
                address=self.cleaned_data['address']
            )
        return user
