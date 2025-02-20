The code for 1.5 includes:

Full Recipe class implementation with all required methods
Property decorators for getters/setters
Class variable for tracking all ingredients
Main code with example recipes
Search functionality
Proper string representation
Docstrings for documentation
The output will show:

Details of each recipe,
Difficulty levels,
Screenshots.

# Recipe Management System (OOP Version)

An object-oriented Python program for managing cooking recipes, calculating difficulty levels, and searching recipes by ingredients.

## Features

- Recipe creation and management
- Automatic difficulty calculation
- Ingredient tracking across all recipes
- Recipe search by ingredient
- Property-based attribute management

## Class Structure

### Recipe Class
- **Attributes:**
  - `name`: Recipe name
  - `cooking_time`: Time in minutes
  - `ingredients`: List of ingredients
  - `difficulty`: Auto-calculated difficulty level
  - `all_ingredients`: Class-level list of all ingredients

- **Methods:**
  - `add_ingredients()`: Add multiple ingredients
  - `calculate_difficulty()`: Determine recipe difficulty
  - `search_ingredient()`: Check for specific ingredient
  - `recipe_search()`: Search across multiple recipes