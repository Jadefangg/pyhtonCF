from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q  # Import Q for complex queries
from recipes.models import Recipe
from categories.models import Category
from ingredients.models import Ingredient
# Create your views here.

#IMPORTANT - In django some views ar defined as functions and some as classes.
# FBVs and CBVs

def home(request):
    """homepage view"""
    num_recipes = Recipe.objects.count()
    num_categories = Category.objects.count()
    num_ingredients = Ingredient.objects.count()

    # The order_by() method is used to sort the results of a query.
    # In this case, we are sorting the recipes by their id in descending order.
    latest_recipes = Recipe.objects.all().order_by('-id')[:5]

    # dictionary is a Python dictionary that serves as a container for all the data you want to make available 
    # to your template. When you call the render() function, Django passes this dictionary to the template engine, 
    # which then makes the dictionary's keys available as variables in your template.

    context = { #declaring keys and values in the dictionary
        # Key-value pairs for the context dictionary:
        'number_of_recipes': num_recipes,
        'number_of_categories': num_categories,
        'number_of_ingredients': num_ingredients,
        'latest_recipes': latest_recipes,
    }
    return render(request, 'recipes/home.html', context) #rendering the template with the context dictionary

def about(request):
    """The about page"""
    return render(request, 'recipes/about.html') #rendering the about page template
#This is a CBV - specifically a ListView!
# After your about() function and before the get_queryset() method
class RecipeListView(ListView):
    """View for listing all recipes"""
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 8
    
    def get_queryset(self):
        """get all the recipes as a list"""
        queryset = Recipe.objects.all().order_by('-id')

        # Get search query from URL parameter
        # this is the usage of Q objects of django,
        # if I didn't want to use these I would use the filter() method
        # and chain the filters together with the & operator
        # but that would require that the user match both the name and ingredients to
        # get a match, which is not what we want.
        
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | 
                Q(ingredients__icontains=query)
            )
        
        # Get category filter from URL parameter
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category__id=category_id)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        """Add categories to context for filtering"""
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_category'] = self.request.GET.get('category', '')
        return context
class RecipeDetailView(DetailView):
    """View for displaying a single recipe's details"""
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'
    
    def get_context_data(self, **kwargs):
        """Add additional context for the template"""
        context = super().get_context_data(**kwargs)
        recipe = self.get_object()
        context['ingredients_list'] = recipe.get_ingredients_list()
        context['difficulty'] = recipe.calculate_difficulty()
        context['related_recipes'] = Recipe.objects.filter(
            category=recipe.category
        ).exclude(id=recipe.id)[:3]  # 3 related recipes
        return context

def category_view(request, category_id):
    """View for displaying recipes in a specific category"""
    category = get_object_or_404(Category, id=category_id)
    recipes = Recipe.objects.filter(category=category)
    
    context = {
        'category': category,
        'recipes': recipes,
    }
    
    return render(request, 'recipes/category.html', context)

def ingredient_view(request, ingredient_id):
    """View for displaying recipes that use a specific ingredient"""
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    
    # Get all recipes that have this ingredient in their ingredient_list
    recipes_with_ingredient = ingredient.used_in.all()
    
    # Also find recipes that mention this ingredient in their text field
    recipes_with_text_mention = Recipe.objects.filter(
        ingredients__icontains=ingredient.name
    )
    
    # Combine the querysets and remove duplicates
    recipes = (recipes_with_ingredient | recipes_with_text_mention).distinct()
    
    context = {
        'ingredient': ingredient,
        'recipes': recipes,
    }
    
    return render(request, 'recipes/ingredient.html', context)

def search_view(request):
    """View for searching recipes"""
    query = request.GET.get('q', '')
    
    if query:
        # Search in name and ingredients
        recipes = Recipe.objects.filter(
            Q(name__icontains=query) | 
            Q(ingredients__icontains=query)
        )
    else:
        recipes = Recipe.objects.none()  # Empty queryset if no search term
    
    context = {
        'query': query,
        'recipes': recipes,
    }
    
    return render(request, 'recipes/search_results.html', context)

def difficulty_view(request, difficulty):
    """View for filtering recipes by difficulty"""
    # Normalize the difficulty parameter
    difficulty = difficulty.lower()
    
    # Get all recipes
    recipes = Recipe.objects.all()
    
    # Filter recipes by calculated difficulty
    filtered_recipes = []
    for recipe in recipes:
        if recipe.calculate_difficulty().lower() == difficulty:
            filtered_recipes.append(recipe)
    
    context = {
        'difficulty': difficulty.capitalize(),
        'recipes': filtered_recipes,
    }
    
    return render(request, 'recipes/difficulty.html', context)