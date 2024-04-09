from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

from django.db import models


class MyModel(models.Model):
    field1 = models.CharField(max_length=100)
    field2 = models.IntegerField()
'''
    def save(self, *args, **kwargs):
        # Custom save method to enforce business rules
        if self.field2 > 0:
            super().save(*args, **kwargs)

'''


class Recipe(models.Model):

    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.TextField()
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_first_image_url(self):
        first_image = self.recipeimage_set.first()
        if first_image:
            return first_image.image.url
        else:
            return '/path/to/default_image.jpg'

    def __str__(self):
        return self.title


class Review(models.Model):
    RATING_CHOICES = (
        (1, 'One'),
        (2, 'Two'),
        (3, 'Three'),
        (4, 'Four'),
        (5, 'Five'),
    )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.recipe.title} by {self.user.username}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class RecipeImage(models.Model):
    recipe = models.ForeignKey('recipes_app.Recipe', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='recipe_images/', default='default_image.jpg')  # Set default image filename
