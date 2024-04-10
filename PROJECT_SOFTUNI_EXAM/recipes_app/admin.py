from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import Recipe, Review


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'author__username')
    list_filter = ('author', 'created_at')
    ordering = ('-created_at',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user', 'rating', 'created_at')
    search_fields = ('recipe__title', 'user__username')
    list_filter = ('rating', 'created_at')
    ordering = ('-created_at',)

#SuperUser - Username: Teodor128 P_w: Password email teotodorov07@gmail.com


