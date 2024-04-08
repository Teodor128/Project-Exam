# your_app/management/commands/import_recipes.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from PROJECT_SOFTUNI_EXAM.recipes_app.models import Recipe


class Command(BaseCommand):
    help = 'Import recipes into the database'

    def handle(self, *args, **kwargs):
        # Retrieve the User instance (e.g., first user)
        try:
            author = User.objects.first()  # You can modify this query based on your user retrieval logic
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('No users found in the database'))
            return

        # Define your recipe data (e.g., titles, ingredients, instructions)
        recipes_data = [
            {
                'title': 'Spaghetti Carbonara',
                'ingredients': '200g spaghetti, 100g pancetta or guanciale, 2 large eggs, 50g grated Pecorino Romano cheese, Freshly ground black pepper, Salt',
                'instructions': '1. Cook the spaghetti in a large pan of boiling salted water until al dente. \n2. Meanwhile, fry the pancetta or guanciale until golden and crisp. \n3. In a bowl, beat the eggs, cheese, and a generous amount of black pepper together. \n4. Drain the spaghetti and toss it in the pancetta fat. Remove from heat, and quickly stir in the egg mixture. The heat from the pasta will cook the eggs, forming a creamy sauce. Serve immediately.',
            },
            {
                'title': 'Chicken Stir-Fry',
                'ingredients': '2 chicken breasts, sliced into strips, 1 red bell pepper, sliced, 1 green bell pepper, sliced, 1 onion, sliced, 2 garlic cloves, minced, 1-inch piece of ginger, grated, 2 tbsp soy sauce, 1 tbsp oyster sauce, 1 tbsp sesame oil, Cooked rice, for serving',
                'instructions': '1. Heat oil in a large pan or wok over medium-high heat. \n2. Add chicken strips and stir-fry until golden and cooked through. Remove from pan. \n3. In the same pan, add more oil if needed, and stir-fry bell peppers, onion, garlic, and ginger until tender-crisp. \n4. Return chicken to the pan, add soy sauce, oyster sauce, and sesame oil. Stir well to combine. \n5. Serve hot over cooked rice.',
            },
            # Add more recipe data as needed
        ]

        # Create recipes and associate with the retrieved User instance
        for recipe_data in recipes_data:
            recipe = Recipe.objects.create(
                title=recipe_data['title'],
                author=author,  # Assign the User instance to the author field
                ingredients=recipe_data['ingredients'],
                instructions=recipe_data['instructions']
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully imported recipe: {recipe.title}'))
