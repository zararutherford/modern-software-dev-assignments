from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'visa_type', 'current_status', 'country_of_origin',
            'case_number', 'filing_date', 'priority_date', 'notes'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1234567890'}),
            'visa_type': forms.Select(attrs={'class': 'form-control'}),
            'current_status': forms.Select(attrs={'class': 'form-control'}),
            'country_of_origin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'case_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CASE-XXX-XXXX'}),
            'filing_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'priority_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Additional notes...'}),
        }
