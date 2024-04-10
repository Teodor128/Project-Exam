from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Recipe, RecipeImage
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

from PROJECT_SOFTUNI_EXAM.recipes_app.forms import UserRegistrationForm, UserLoginForm, RecipeForm, ProfileForm, \
    ReviewForm, RecipeSearchForm, RecipeImageForm, RecipeImageFormSet
from PROJECT_SOFTUNI_EXAM.recipes_app.models import Recipe, Profile, Review, RecipeImage
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
    images = RecipeImage.objects.filter(recipe=recipe)

    # Define a list of rating icons based on the rating value
    for review in reviews:
        review.rating_icons = range(review.rating)

    context = {
        'recipe': recipe,
        'reviews': reviews,
        'images': images,
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
            form.save_m2m()
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

'''''
@login_required()
def update_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)  # Assuming 'id' is the primary key field

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save(commit=False)
            form.save_m2m()
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'recipes/recipe_update.html', {'form': form, 'recipe': recipe})
'''''

'''''
@login_required
def update_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, instance=recipe)
        image_formset = RecipeImageFormSet(request.POST, request.FILES, instance=recipe)

        if recipe_form.is_valid() and image_formset.is_valid():
            recipe_form.save()
            image_formset.save()

            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        recipe_form = RecipeForm(instance=recipe)
        image_formset = RecipeImageFormSet(instance=recipe)

    return render(request, 'recipes/recipe_update.html', {
        'recipe': recipe,
        'recipe_form': recipe_form,
        'image_formset': image_formset
    })
'''''


@login_required
def update_recipe(request, recipe_id):
    # Retrieve the recipe object using the provided recipe_id
    recipe = get_object_or_404(Recipe, id=recipe_id)

    # Check if the current user is the author of the recipe
    if request.user != recipe.author:
        # If the current user is not the author, render a custom message
        return render(request, 'recipes/update_access_denied.html', {
            'recipe': recipe
        })

    if request.method == 'POST':
        # Populate the forms with the submitted data and instance
        recipe_form = RecipeForm(request.POST, instance=recipe)
        image_formset = RecipeImageFormSet(request.POST, request.FILES, instance=recipe)

        # Validate the forms
        if recipe_form.is_valid() and image_formset.is_valid():
            # Save the recipe form and associated image formset
            recipe_form.save()
            image_formset.save()

            # Redirect to the recipe detail page after successful update
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        # If it's a GET request or the form data is invalid, display the update form
        recipe_form = RecipeForm(instance=recipe)
        image_formset = RecipeImageFormSet(instance=recipe)

    # Render the update form with the recipe data and formsets
    return render(request, 'recipes/recipe_update.html', {
        'recipe': recipe,
        'recipe_form': recipe_form,
        'image_formset': image_formset
    })


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

    return render(request, 'recipes/add_review.html',
                  {'form': form, 'recipe': recipe})


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

'''''
def upload_images(request):
    if request.method == 'POST':
        formset = RecipeImageFormSet(request.POST, request.FILES)
        if formset.is_valid():
            print("Formset is valid")
            for form in formset:
                if form.cleaned_data.get('image'):
                    print(f"Image uploaded: {form.cleaned_data['image']}")
                    RecipeImage.objects.create(image=form.cleaned_data['image'])
            return render(request, 'recipes/upload.html', {'form': RecipeImageForm(), 'success_message': 'Images uploaded successfully!'})
        else:
            print("Formset has errors:", formset.errors)
    else:
        formset = RecipeImageFormSet()
    return render(request, 'recipes/upload.html', {'formset': formset})
'''


def upload_images(request):
    if request.method == 'POST':
        formset = RecipeImageFormSet(request.POST, request.FILES)
        if formset.is_valid():
            main_image_id = None  # Initialize main image ID
            for form in formset:
                if form.cleaned_data.get('image'):
                    image_instance = form.save(commit=False)
                    if form.cleaned_data['is_main']:
                        main_image_id = image_instance.id
                    image_instance.save()

            # Set the main image in the recipe if specified
            if main_image_id:
                # Logic to set the main image ID in the related Recipe model
                # Example: recipe.main_image_id = main_image_id
                pass  # Replace this with your actual logic

            return render(request, 'recipes/upload.html', {'formset': RecipeImageFormSet(), 'success_message': 'Images uploaded successfully!'})
    else:
        formset = RecipeImageFormSet()
    return render(request, 'recipes/upload.html', {'formset': formset})


@permission_required('your_app.can_change_specific_data', raise_exception=True)
def limited_crud_view(request):
    # Your view logic here
    return HttpResponse("You have permission to perform this action.")


def update_profile(request):
    if request.method == 'POST':
        profile = get_object_or_404(Profile, user=request.user)
        bio = request.POST.get('bio', None)  # Allow for empty bio

        profile.bio = bio
        profile.save()

        return JsonResponse({'message': 'Profile updated successfully.'})

    return JsonResponse({'message': 'Invalid request method.'}, status=405)