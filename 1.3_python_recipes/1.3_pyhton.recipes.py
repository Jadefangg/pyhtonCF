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
    # this code below is a docstring and is part of python documentation, 
    # a docstring can be accessed by typing help(calc_difficulty) in the python shell,
    # or via print(calc_difficulty.__doc__).
    """
    Calculate recipe difficulty based on cooking time and ingredient count using binary decisions
    
    Parameters:
    - recipe (dict): Recipe dictionary containing 'cooking_time' and 'ingredients'
    
    Returns:
    - str: Difficulty level (Easy, Medium, Intermediate, or Hard)
    """
    cooking_time = recipe['cooking_time']
    num_ingredients = len(recipe['ingredients'])
    
    # Define thresholds
    TIME_THRESHOLD = 10
    INGREDIENT_THRESHOLD = 4
    
    # 2 condition if else based on thresholds
    if cooking_time < TIME_THRESHOLD:
        if num_ingredients < INGREDIENT_THRESHOLD:
            return "Easy"
        else:
            return "Medium"
    else:
        if num_ingredients < INGREDIENT_THRESHOLD:
            return "Intermediate"
        else:
            return "Hard"
recipes_list = []
ingredients_list = []
#while true loop to keep asking for recipes <<< This is the main loop
while True:
    # Ask to add recipe here
    choice = input("\nWould you like to add a recipe? (yes/no): ").lower()
    
    if choice != 'yes':
        break
        
    print("\nNew Recipe:")
    recipe = take_recipe()
    
    # Check and add new ingredients to ingredients_list
    for ingredient in recipe['ingredients']:
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)
    
    recipes_list.append(recipe)

# Check if added
if not recipes_list:
    print("\nNo recipes added.")
else:
    # Display all recipes and also display their difficulty
    print("\nYOUR RECIPES:")
    print("====================")

    for recipe in recipes_list:
        difficulty = calc_difficulty(recipe)
        print(f"\nRecipe: {recipe['name']}")
        print(f"Cooking Time (min): {recipe['cooking_time']}")
        print(f"Ingredients: {', '.join(recipe['ingredients'])}")
        print(f"Difficulty level: {difficulty}")

    # Display all ingredients entered in analphabetical order
    print("\nINGREDIENTS AVAILABLE ACROSS ALL RECIPES:")
    print("====================")

    ingredients_list.sort()
    for ingredient in ingredients_list:
        print(ingredient)