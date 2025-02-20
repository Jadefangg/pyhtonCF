import pickle

def take_recipe():#taking input
    """Take recipe input from user and return a recipe dictionary"""
    name = input("Enter the recipe name: ")
    cooking_time = int(input("Enter cooking time (minutes): "))
    ingredients = []
    
    num_ingredients = int(input("How many ingredients would you like to enter? "))
    for i in range(num_ingredients):
        #python f string is used here. A f-string is a way to embed expressions inside string literals, 
        #using curly braces {}.
        #I have used f string as it is more easy to use.
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
#improved the try except block to handle more exceptions.
try:
    with open(filename, 'rb') as file:
        data = pickle.load(file)
except FileNotFoundError:
    print("File not found. Creating new recipe data.")
    data = {
        'recipes_list': [],
        'all_ingredients': []
    }
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    print("Creating new recipe data.")
    data = {
        'recipes_list': [],
        'all_ingredients': []
    }
else:
    # This block runs only if try succeeds
    print("Successfully loaded existing recipe data.")
finally:
    # Initialize lists from data with defaults if keys don't exist
    recipes_list = data.get('recipes_list', [])
    all_ingredients = data.get('all_ingredients', [])
    print("Data initialization completed.")# Get recipes from user
num_recipes = int(input("How many recipes would you like to enter? "))

for i in range(num_recipes):
    # The f string here is used to print the recipe number. 
    # The \n is used to print a new line.
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
with open(filename, 'wb') as file: #file output Operation<<<
    pickle.dump(data, file)