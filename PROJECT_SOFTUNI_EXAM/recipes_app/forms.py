from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms

from PROJECT_SOFTUNI_EXAM.recipes_app.models import Recipe


class MyForm(forms.Form):
    field1 = forms.CharField(label='Field 1', max_length=100)
    field2 = forms.IntegerField(label='Field 2')
    field3 = forms.BooleanField(label='Field 3', required=False)


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'instructions', 'image']