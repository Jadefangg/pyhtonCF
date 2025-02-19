import pickle

def take_recipe():#taking input
    """Take recipe input from user and return a recipe dictionary"""
    name = input("Enter the recipe name: ")
    cooking_time = int(input("Enter cooking time (minutes): "))
    ingredients = []
    
    num_ingredients = int(input("How many ingredients would you like to enter? "))
    for i in range(num_ingredients):
        ingredient = input(f"Enter ingredient {i+1}: ").lower()
        ingredients.append(ingredient)
    
    difficulty = calc_difficulty(cooking_time, len(ingredients))
    
    return {
        'name': name,
        'cooking_time': cooking_time,
        'ingredients': ingredients,
        'difficulty': difficulty
    }

def calc_difficulty(cooking_time, num_ingredients):
    """Calculate recipe difficulty based on cooking time and number of ingredients"""
    if cooking_time < 10:
        if num_ingredients < 4:
            return "Easy"
        return "Medium"
    else:
        if num_ingredients < 4:
            return "Intermediate"
        return "Hard"

# Main code
filename = input("Enter the filename where your recipe data will be stored: ")

# Initialize data structure
try:
    with open(filename, 'rb') as file:
        data = pickle.load(file)
except FileNotFoundError:
    data = {
        'recipes_list': [],
        'all_ingredients': []
    }
except:
    print("Unexpected error occurred. Creating new recipe data.")
    data = {
        'recipes_list': [],
        'all_ingredients': []
    }
else:
    file.close()
finally:
    recipes_list = data['recipes_list']
    all_ingredients = data['all_ingredients']

# Get recipes from user
num_recipes = int(input("How many recipes would you like to enter? "))

for i in range(num_recipes):
    print(f"\nRecipe {i+1}")
    recipe = take_recipe()
    recipes_list.append(recipe)
    
    # Update all_ingredients list
    for ingredient in recipe['ingredients']:
        if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)

# Update data dictionary
data = {
    'recipes_list': recipes_list,
    'all_ingredients': all_ingredients
}

# Save to binary file
with open(filename, 'wb') as file:
    pickle.dump(data, file)