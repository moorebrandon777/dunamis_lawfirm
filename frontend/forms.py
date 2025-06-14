from django import forms
from captcha.fields import CaptchaField

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your Name',
            'class': 'form-control'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Your Email',
            'class': 'form-control'
        })
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your Phone Number',
            'class': 'form-control'
        })
    )
    address = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your Address',
            'class': 'form-control'
        })
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': 'Your Message',
            'class': 'form-control',
            'rows': 5
        })
    )
    captcha = CaptchaField()