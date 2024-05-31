from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm

from .models import User , Dashboard

class UserAdminRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


class UserEmployeeRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

class UserEditForm(UserChangeForm):
    current_password = forms.CharField(widget=forms.PasswordInput())
    password_new = forms.CharField(widget=forms.PasswordInput(), required=False)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password_new', 'current_password']
    

class LoginUserForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password']

class DashboardForm(forms.ModelForm):
    logo_company = forms.ImageField(widget=forms.FileInput)
    class Meta:
        model = Dashboard
        fields = ['name_company', 'logo_company']