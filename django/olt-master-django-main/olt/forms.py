from django import forms
from django.contrib.auth.models import User
from .models import Perfil

class LoginForm(forms.Form):
    email = forms.CharField(label='Email', max_length=100)
    senha = forms.CharField(label='Senha', widget=forms.PasswordInput)

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError('Este email já está sendo utilizado.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "A confirmação de senha não corresponde."
            )
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data['email']
        username = email.split('@')[0]
        user.username = username
        user.is_active = False  # O usuário será criado como inativo
        user.set_password(self.cleaned_data['password'])

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Um usuário com este nome já existe.')

        if commit:
            user.save()
        return user
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['foto_perfil']