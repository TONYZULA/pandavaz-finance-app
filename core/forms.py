# core/forms.py
from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        # We only show the fields a user needs to fill out.
        # The 'created_at' field is handled automatically.
        fields = ['date', 'description', 'amount', 'transaction_type', 'partner']
        # Use a proper date picker widget for the date field
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }