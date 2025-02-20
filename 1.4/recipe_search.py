import pickle

def display_recipe(recipe):
    """Display a recipe with all its attributes"""
    #f strings
    print(f"\nRecipe: {recipe['name']}")
    print(f"Cooking Time: {recipe['cooking_time']} minutes")
    print(f"Ingredients: {', '.join(recipe['ingredients'])}")
    print(f"Difficulty: {recipe['difficulty']}")

def search_ingredient(data): # This function is used to search for a specific ingredient in the recipe
    """Search for recipes containing a specific ingredient"""
    try:
        print("\nAvailable ingredients:")
        for index, ingredient in enumerate(data['all_ingredients']):
            print(f"{index}. {ingredient}")
        
        #here the choice is taken from the user and is the ingredient that the user wants to search for.
        choice = int(input("\nEnter the number of the ingredient: "))
        ingredient_searched = data['all_ingredients'][choice]
        #this is the search operation
        print(f"\nRecipes containing {ingredient_searched}:")
        found_recipes = False
        for recipe in data['recipes_list']:
            if ingredient_searched in recipe['ingredients']:
                display_recipe(recipe)
                found_recipes = True
        #if no recipes are found with the ingredient
        if not found_recipes:
            print("No recipes found with this ingredient.")
            
    # I have Combined the two exceptions/error cases into one.        
    except (ValueError, IndexError) as e:  
        if isinstance(e, ValueError):
            print("Invalid input! Please enter a valid number.")
        else:
            print("Option number out of range! Please choose a valid ingredient number.")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return
    finally:
        print("\nSearch operation completed.")
# this is the main code
filename = input("Enter the filename containing your recipe data: ")

try:
    with open(filename, 'rb') as file:
        data = pickle.load(file)
except FileNotFoundError:
    print("File not found! Please make sure you've entered the correct filename.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
else:
    search_ingredient(data)