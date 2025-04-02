from django.test import TestCase
from recipes.models import Recipe
from categories.models import Category
from ingredients.models import Ingredient

class RecipeModelTest(TestCase):
    """Tests for the Recipe model"""
    
    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods"""
        # Create a category
        test_category = Category.objects.create(
            name='Test Category',
            description='A category for testing'
        )
        
        # Create an ingredient
        test_ingredient = Ingredient.objects.create(
            name='Test Ingredient',
            notes='An ingredient for testing'
        )
        
        # Create a recipe
        test_recipe = Recipe.objects.create(
            name='Test Recipe',
            cooking_time=15,
            ingredients='Test Ingredient, Another Ingredient, Third Ingredient',
            category=test_category
        )
        
        # Add ingredient to recipe
        test_recipe.ingredient_list.add(test_ingredient)
    
    def test_recipe_name(self):
        """Test the recipe name field"""
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field('name').verbose_name
        max_length = recipe._meta.get_field('name').max_length
        self.assertEqual(field_label, 'name')
        self.assertEqual(max_length, 100)
        self.assertEqual(recipe.name, 'Test Recipe')
        
    def test_cooking_time(self):
        """Test the cooking_time field"""
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field('cooking_time').verbose_name
        self.assertEqual(field_label, 'cooking time')
        self.assertEqual(recipe.cooking_time, 15)
        
    def test_ingredients_field(self):
        """Test the ingredients text field"""
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.ingredients, 'Test Ingredient, Another Ingredient, Third Ingredient')
        
    def test_get_ingredients_list(self):
        """Test the get_ingredients_list method"""
        recipe = Recipe.objects.get(id=1)
        ingredients_list = recipe.get_ingredients_list()
        self.assertEqual(len(ingredients_list), 3)
        self.assertIn('Test Ingredient', ingredients_list)
        self.assertIn('Another Ingredient', ingredients_list)
        self.assertIn('Third Ingredient', ingredients_list)
        
    def test_calculate_difficulty_easy(self):
        """Test the calculate_difficulty method - Easy case"""
        recipe = Recipe.objects.create(
            name='Easy Recipe',
            cooking_time=5,
            ingredients='Salt, Pepper'
        )
        self.assertEqual(recipe.calculate_difficulty(), 'Easy')
        
    def test_calculate_difficulty_medium(self):
        """Test the calculate_difficulty method - Medium difficulty"""
        recipe = Recipe.objects.create(
            name='Medium Recipe',
            cooking_time=5,
            ingredients='Salt, Pepper, Sugar, Flour, Eggs'
        )
        self.assertEqual(recipe.calculate_difficulty(), 'Medium')
        
    def test_calculate_difficulty_intermediate(self):
        """Test the calculate_difficulty method - Intermediate difficulty"""
        recipe = Recipe.objects.create(
            name='Intermediate Recipe',
            cooking_time=15,
            ingredients='Salt, Pepper'
        )
        self.assertEqual(recipe.calculate_difficulty(), 'Intermediate')
        
    def test_calculate_difficulty_hard(self):
        """Test the calculate_difficulty method - Hard difficulty"""
        recipe = Recipe.objects.create(
            name='Hard Recipe',
            cooking_time=15,
            ingredients='Salt, Pepper, Sugar, Flour, Eggs'
        )
        self.assertEqual(recipe.calculate_difficulty(), 'Hard')
        
    def test_category_relationship(self):
        """Test the category foreign key relationship"""
        recipe = Recipe.objects.get(id=1)
        category = Category.objects.get(id=1)
        self.assertEqual(recipe.category, category)
        
    def test_ingredient_list_relationship(self):
        """Test the ingredient_list many-to-many relationship"""
        recipe = Recipe.objects.get(id=1)
        ingredient = Ingredient.objects.get(id=1)
        self.assertIn(ingredient, recipe.ingredient_list.all())
        
    def test_string_representation(self):
        """Test the string representation of the Recipe model"""
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(str(recipe), recipe.name)