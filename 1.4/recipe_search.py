import pickle

def display_recipe(recipe):
    """Display a recipe with all its attributes"""
    print(f"\nRecipe: {recipe['name']}")
    print(f"Cooking Time: {recipe['cooking_time']} minutes")
    print(f"Ingredients: {', '.join(recipe['ingredients'])}")
    print(f"Difficulty: {recipe['difficulty']}")

def search_ingredient(data):
    """Search for recipes containing a specific ingredient"""
    print("\nAvailable ingredients:")
    for index, ingredient in enumerate(data['all_ingredients']):
        print(f"{index}. {ingredient}")
    
    try:
        choice = int(input("\nEnter the number of the ingredient you want to search for: "))
        ingredient_searched = data['all_ingredients'][choice]
    except (ValueError, IndexError):
        print("Invalid input! Please enter a number from the list.")
        return
    else:
        print(f"\nRecipes containing {ingredient_searched}:")
        found_recipes = False
        for recipe in data['recipes_list']:
            if ingredient_searched in recipe['ingredients']:
                display_recipe(recipe)
                found_recipes = True
        
        if not found_recipes:
            print("No recipes found with this ingredient.")

# this is the main code
filename = input("Enter the filename containing your recipe data: ")

try:
    with open(filename, 'rb') as file:
        data = pickle.load(file)
except FileNotFoundError:
    print("File not found! Please make sure you've entered the correct filename.")
else:
    search_ingredient(data)