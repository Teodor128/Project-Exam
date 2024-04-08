from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

from PROJECT_SOFTUNI_EXAM.recipes_app.forms import UserRegistrationForm, UserLoginForm, RecipeForm, ProfileForm, \
    ReviewForm, RecipeSearchForm
from PROJECT_SOFTUNI_EXAM.recipes_app.models import Recipe, Profile, Review
from django.shortcuts import render, redirect
from PROJECT_SOFTUNI_EXAM.recipes_app.forms import MyForm
from django.db import models
from django.contrib.auth.models import User


def my_view(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            # Process form data
            field1 = form.cleaned_data['field1']
            field2 = form.cleaned_data['field2']
            field3 = form.cleaned_data['field3']
            # Process the form data as needed
            messages.success(request, 'Form submission successful.')
            return redirect('success_page')
        else:
            # If the form is invalid, handle the errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
    else:
        form = MyForm()
    return render(request, 'recipes/my_template.html', {'form': form})


def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})

'''''
def recipe_detail(request, recipe_id)
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})
'''''


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    reviews = Review.objects.filter(recipe=recipe)

    # Define a list of rating icons based on the rating value
    for review in reviews:
        review.rating_icons = range(review.rating)

    context = {
        'recipe': recipe,
        'reviews': reviews
    }

    return render(request, 'recipes/recipe_detail.html', context)


@login_required
def user_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None  # Handle the case where profile does not exist

    return render(request, 'recipes/user_profile.html', {'profile': profile})


@login_required
def edit_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)  # Create a new Profile if it doesn't exist
        profile.save()

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')  # Redirect to user profile after editing
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'recipes/edit_profile.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('recipe_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'recipes/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('recipe_list')
    else:
        form = UserLoginForm()
    return render(request, 'recipes/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('recipe_list')


@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the new recipe to the database
            recipe = form.save(commit=False)
            recipe.author = request.user  # Assign the current user as the recipe author
            recipe.save()
            return redirect('recipe_list')  # Redirect to recipe list page after adding the recipe
    else:
        form = RecipeForm()
    return render(request, 'recipes/add_recipe.html', {'form': form})

'''''
@login_required
def update_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', recipe_id=recipe_id)
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'recipes/recipe_update.html', {'form': form})
'''


@login_required()
def update_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)  # Assuming 'id' is the primary key field

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'recipes/recipe_update.html', {'form': form, 'recipe': recipe})


def add_review(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.recipe = recipe
            review.user = request.user
            review.save()
            return redirect('recipe_detail', recipe_id=recipe_id)
    else:
        form = ReviewForm()

    return render(request, 'recipes/add_review.html', {'form': form, 'recipe': recipe})


def get_reviews_for_recipe(recipe):
    return Review.objects.filter(recipe=recipe)


def get_reviews_by_user(user):
    return Review.objects.filter(user=user)


def recipe_search(request):
    if request.method == 'GET':
        form = RecipeSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data.get('query')
            # Filter recipes based on the search query
            recipes = Recipe.objects.filter(title__icontains=query)
            context = {
                'form': form,
                'recipes': recipes,
                'query': query
            }
            return render(request, 'recipes/recipe_search_results.html', context)
    else:
        form = RecipeSearchForm()
    return render(request, 'recipes/recipe_search.html', {'form': form})
