from django import forms
from .models import User, Spouse, Dependant, Payment, Case
from .utils import get_members_and_dependants
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'phone_number', 'id_number', 'username', 'email', 'age', 'is_deceased']

class SpouseForm(forms.ModelForm):
    class Meta:
        model = Spouse
        fields = ['user', 'name', 'phone_number', 'id_number', 'age', 'is_deceased']

class DependantForm(forms.ModelForm):
    class Meta:
        model = Dependant
        fields = ['user', 'name', 'phone_number', 'relationship', 'age', 'is_deceased']

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['case', 'user', 'amount', 'is_registration']

class CaseForm(forms.ModelForm):
    deceased_member_name = forms.ChoiceField()  # Add a choice field for deceased member

    def __init__(self, *args, **kwargs):
        super(CaseForm, self).__init__(*args, **kwargs)
        self.fields['deceased_member_name'].choices = [(member['name'], member['name']) for member in get_members_and_dependants()]

    class Meta:
        model = Case
        fields = ['case_number', 'deceased_member_name', 'date_of_death', 'is_closed']

