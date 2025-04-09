from django.urls import path
from . import views

urlpatterns = [
    # Basic pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    
    # Recipe views
    path('recipes/', views.RecipeListView.as_view(), name='recipe-list'),
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe-detail'),
    
    # Filtering views
    path('categories/<int:category_id>/', views.category_view, name='category-detail'),
    path('ingredients/<int:ingredient_id>/', views.ingredient_view, name='ingredient-detail'),
    path('difficulty/<str:difficulty>/', views.difficulty_view, name='difficulty'),
    path('recipe/add/', views.add_recipe, name='add-recipe'),#2.5
    path('recipe/<int:pk>/edit/', views.edit_recipe, name='edit-recipe'), #2.5,
    path('logout/success/', views.logout_success, name='logout-success'),
    path('logout/', views.custom_logout, name='logout'),
    # Search
    path('search/', views.search_view, name='search'),

]