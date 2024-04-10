from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms
from django.forms import inlineformset_factory
from multiupload.fields import MultiFileField

from PROJECT_SOFTUNI_EXAM.recipes_app.models import Recipe, Profile, Review, RecipeImage


class MyForm(forms.Form):
    field1 = forms.CharField(label='Field 1', max_length=100)
    field2 = forms.IntegerField(label='Field 2')

    def clean_field2(self):
        field2_value = self.cleaned_data['field2']
        if field2_value < 0:
            raise forms.ValidationError("Field 2 must be a positive integer.")
        return field2_value


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
        fields = ['title', 'ingredients', 'instructions', 'description', 'image']
        widgets = {
            'ingredients': forms.Textarea(attrs={'rows': 3}),
            'instructions': forms.Textarea(attrs={'rows': 5}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture', ] #date of birth
        clear_profile_picture = forms.BooleanField(required=False, label='Clear Profile Picture')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']


class RecipeSearchForm(forms.Form):
    query = forms.CharField(label='Search Recipes', max_length=100)


class RecipeImageForm(forms.ModelForm):
    is_main = forms.BooleanField(label='Main Image', required=False)

    class Meta:
        model = RecipeImage
        fields = ['image', 'is_main']


RecipeImageFormSet = inlineformset_factory(
    parent_model=Recipe,
    model=RecipeImage,
    form=RecipeImageForm,
    extra=3,  # Allow up to 3 extra image upload fields
    can_delete=True  # Allow deletion of existing images if needed
)
