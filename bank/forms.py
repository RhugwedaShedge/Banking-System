from django import forms

from .models import *

from django.contrib.auth import models

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    mobile_no = forms.CharField()

    # mobile_no = PhoneNumberField(
    #     widget = PhoneNumberPrefixWidget(initial = 'IN')
    # ) 

    account_no = forms.CharField()
    cif_no = forms.CharField()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 '
                    'rounded py-3 px-4 leading-tight '
                    'focus:outline-none focus:bg-white '
                    'focus:border-gray-500'
                )
            })

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            account_no = self.cleaned_data.get('account_no')
            cif_no = self.cleaned_data.get('cif_no')
            mobile_no = self.cleaned_data.get('mobile_no')

            UserBankAccount.objects.create(
                user = user,
                account_no = account_no,
                cif_no = cif_no,
                mobile_no = mobile_no,
            )
        return user
    
    
class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = [
            'userAccount', 
            'payeeAccount', 
            'amount',
            'remark',
            'transfer_type',
        ]

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')
        super().__init__(*args, **kwargs)

        self.fields['transaction_type'].disabled = True
        self.fields['transaction_type'].widget = forms.HiddenInput()

    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()
