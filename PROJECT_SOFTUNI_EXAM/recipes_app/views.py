from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

from PROJECT_SOFTUNI_EXAM.recipes_app.forms import UserRegistrationForm, UserLoginForm, RecipeForm
from PROJECT_SOFTUNI_EXAM.recipes_app.models import Recipe
from django.shortcuts import render, redirect
from PROJECT_SOFTUNI_EXAM.recipes_app.forms import MyForm


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
    # Retrieve the recipe object using its id (assuming id is the primary key)
    recipe = get_object_or_404(Recipe, id=recipe_id)

    # Pass the recipe object to the template context
    context = {
        'recipe': recipe
    }

    # Render the template with the recipe detail
    return render(request, 'recipes/recipe_detail.html', context)

@login_required
def user_profile(request):
    user = request.user
    return render(request, 'recipes/user_profile.html', {'user': user})


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