"""
URL configuration for PROJECT_SOFTUNI_EXAM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from PROJECT_SOFTUNI_EXAM.recipes_app import views
from PROJECT_SOFTUNI_EXAM.recipes_app.views import recipe_search

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('profile/', views.user_profile, name='user_profile'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('add/', views.add_recipe, name='add_recipe'),

    path('', views.recipe_list, name='recipe_list'),
    #path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('add/', views.add_recipe, name='add_recipe'),

    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/<int:recipe_id>/update/', views.update_recipe, name='update_recipe'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('recipe/<int:recipe_id>/add_review/', views.add_review, name='add_review'),
    path('recipe/search/', recipe_search, name='recipe_search'),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

