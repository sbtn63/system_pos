from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

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
    email = forms.EmailField()
    current_password = forms.CharField(
        widget=forms.PasswordInput()
    )
    password_new = forms.CharField(
        widget=forms.PasswordInput(),
        required=False
    )
    confirm_password_new = forms.CharField(
        widget=forms.PasswordInput(), 
        required=False
    )
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password_new','confirm_password_new', 'current_password']
    
    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and email != self.current_user.email:
            if User.objects.exclude(pk=self.current_user.pk).filter(email=email).exists():
                raise ValidationError("El email de usuario ya está en uso.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password_new = cleaned_data.get('password_new')
        confirm_password_new = cleaned_data.get('confirm_password_new')
        if password_new or confirm_password_new:
            if not password_new:
                self.add_error('password_new', 'Debes proporcionar la nueva contraseña.')
            if not confirm_password_new:
                self.add_error('confirm_password_new', 'Debes confirmar la nueva contraseña.')
            if password_new and confirm_password_new and password_new != confirm_password_new:
                self.add_error('confirm_password_new', 'Las contraseñas no coinciden.')
            if password_new:
                try:
                    validate_password(password_new)
                except ValidationError as e:
                    self.add_error('password_new', e)
        return cleaned_data
    
class LoginUserForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class DashboardForm(forms.ModelForm):
    logo_company = forms.ImageField(widget=forms.FileInput)
    class Meta:
        model = Dashboard
        fields = ['name_company', 'logo_company']