def take_recipe():
    """Function to take recipe input from user and return a recipe dictionary"""
    name = input("Enter the name of the recipe: ")
    cooking_time = int(input("Enter the cooking time (in minutes): "))
    ingredients = []
    
    n = int(input("How many ingredients do you want to enter? "))
    for i in range(n):
        ingredient = input(f"Enter ingredient {i+1}: ")
        ingredients.append(ingredient)
    
    recipe = {
        'name': name,
        'cooking_time': cooking_time,
        'ingredients': ingredients
    }
    return recipe

def calc_difficulty(recipe):
    """Calculate difficulty based on cooking time and number of ingredients"""
    if recipe['cooking_time'] < 10 and len(recipe['ingredients']) < 4:
        return "Easy"
    elif recipe['cooking_time'] < 10 and len(recipe['ingredients']) >= 4:
        return "Medium"
    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) < 4:
        return "Intermediate"
    else:
        return "Hard"

recipes_list = []
ingredients_list = []

n = int(input("How many recipes would you like to enter? "))

# Main loop to take recipe inputs
for i in range(n):
    print(f"\nRecipe {i+1}")
    recipe = take_recipe()
    
    # Check and add new ingredients to ingredients_list
    for ingredient in recipe['ingredients']:
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)
    
    recipes_list.append(recipe)

# Display all recipes with their difficulty
print("YOUR RECIPES:")
print("====================")

for recipe in recipes_list:
    difficulty = calc_difficulty(recipe)
    print(f"\nRecipe: {recipe['name']}")
    print(f"Cooking Time (min): {recipe['cooking_time']}")
    print(f"Ingredients: {', '.join(recipe['ingredients'])}")
    print(f"Difficulty level: {difficulty}")

# Display all ingredients in alphabetical order
print("INGREDIENTS AVAILABLE ACROSS ALL RECIPES:")
print("====================")

ingredients_list.sort()
for ingredient in ingredients_list:
    print(ingredient)