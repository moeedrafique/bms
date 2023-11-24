from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *
from allauth.account.forms import LoginForm


class ProductForm(forms.ModelForm):
    unit = forms.ModelChoiceField(queryset=Unit.objects.all(), to_field_name='name', empty_label="Select unit")
    category = forms.ModelChoiceField(queryset=Category.objects.all(), to_field_name='name', empty_label="Select category")
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), to_field_name='name', empty_label="Select supplier")
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['name']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2')

class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ['recipient_email', 'branch', 'role']
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Add additional widgets or choices if needed
    #     self.fields['branch'].widget = forms.TextInput(attrs={'placeholder': 'Branch'})
    #     self.fields['role'].widget = forms.TextInput(attrs={'placeholder': 'Role'})