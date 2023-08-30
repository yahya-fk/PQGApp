from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=True, help_text='Required. Your first name.',
        widget=forms.TextInput(attrs={'placeholder':'Votre Prenom','class': 'form-control text-dark', 'style': 'background-color: #f0f0f0; border:none; border-bottom: 3px solid grey'})
    )
    last_name = forms.CharField(
        max_length=30, required=True, help_text='Required. Your last name.',
        widget=forms.TextInput(attrs={'placeholder':'Votre Nom','class': 'form-control text-dark', 'style': 'background-color: #f0f0f0; border:none; border-bottom: 3px solid grey'})
    )
    email = forms.EmailField(
        max_length=254, required=True, help_text='Required. Enter a valid email address.',
        widget=forms.EmailInput(attrs={'placeholder':'Votre Email','class': 'form-control text-dark', 'style': 'background-color: #f0f0f0; border:none; border-bottom: 3px solid grey'})
    )
    username = forms.CharField(
        max_length=30, required=True, help_text='Required. Your username.',
        widget=forms.TextInput(attrs={'placeholder':'Votre username','class': 'form-control text-dark', 'style': 'background-color: #f0f0f0; border:none; border-bottom: 3px solid grey'})
    )
    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={'placeholder':'Votre Mot de Passe','class': 'form-control text-dark', 'style': 'background-color: #f0f0f0; border:none; border-bottom: 3px solid grey'})
    )
    password2 = forms.CharField(
        label="Confirm Password", widget=forms.PasswordInput(attrs={'placeholder':'Confimer votre mot de passe','class': 'form-control text-dark', 'style': 'background-color: #f0f0f0; border:none; border-bottom: 3px solid grey'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class SignInForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder':'username','class': 'form-control text-dark', 'style': 'background-color: #f0f0f0; border:none; border-bottom: 3px solid grey'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'password','class': 'form-control text-dark', 'style': 'background-color: #f0f0f0; border:none; border-bottom: 3px solid grey'}),
    )