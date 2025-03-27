from django import forms
from .models import Analytics, Invoice
from django.contrib.auth import get_user_model

User = get_user_model()

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'amount_to_pay',
            'description',
            'wallet_email_or_account',
            'recipient_user',
            'payment_method'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'recipient_user': forms.Select(attrs={'class': 'select2'}),
        }
        labels = {
            'wallet_email_or_account': 'Wallet/Email/Account Details',
        }
        help_texts = {
            'wallet_email_or_account': 'Enter recipient payment information (wallet address, email, or account number)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recipient_user'].queryset = User.objects.all()

    def clean_amount_to_pay(self):
        amount = self.cleaned_data.get('amount_to_pay')
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount

class AnalyticForm(forms.ModelForm):
    class Meta:
        model = Analytics
        fields = ['image', 'description', 'amount', 'target_user']

