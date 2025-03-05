import mysql.connector  # Import the MySQL connector

conn = mysql.connector.connect(
    host='localhost',
    user='cf-python',
    passwd='password')  # Establish a connection to the MySQL server
cursor = conn.cursor() # Create a cursor object using the cursor() method

# Initial test to verify connection
print("MySQL connection established successfully!")

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
cursor.execute("USE task_database")
print("using the task database test")

# 3 ' are given to write the query in multiple lines. A single one can also be used.
cursor.execute(''' 
CREATE TABLE IF NOT EXISTS Recipes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    ingredients VARCHAR(255), 
    cooking_time INT,
    difficulty VARCHAR(20)
)
''')
print("Recipes table created successfully!")

#   MAIN MENU CODE
def main_menu(conn, cursor):
    """Display main menu and handle user choices."""
    while True:
        print("\n==== Recipe Management System ====") # Display the main menu
        print("1. Create a new recipe")
        print("2. Search for a recipe by ingredient")
        print("3. Update an existing recipe")
        print("4. Delete a recipe")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ") # Get user input
        
        if choice == '1':                             # Call the appropriate function based on user choice
            create_recipe(conn, cursor)
        elif choice == '2':
            search_recipe(conn, cursor)
        elif choice == '3':
            update_recipe(conn, cursor)
        elif choice == '4':
            delete_recipe(conn, cursor)
        elif choice == '5':                           # Exit the program
            print("Saving changes and exiting...")    # Display a message before exiting
            conn.commit()  # Commit any pending changes
            cursor.close()  # Close the cursor
            conn.close()   # Close the connection
            print("Goodbye!")
            break
        else:                                        # Handle invalid choices
            print("Invalid choice. Please enter a number between 1 and 5.") 

def calculate_difficulty(cooking_time, ingredients_list):
    """
    Calculate recipe difficulty based on cooking time and number of ingredients.
    
    Parameters:
        cooking_time (int): Cooking time in minutes
        ingredients_list (list): List of ingredients or comma-separated string
    
    Returns:
        str: Difficulty level (Easy, Medium, Intermediate, or Hard)
    """
    # If ingredients_list is a string, count items by splitting on commas
    if isinstance(ingredients_list, str):
        num_ingredients = len(ingredients_list.split(','))
    else:
        num_ingredients = len(ingredients_list)
    
    # Logic for determining difficulty
    if cooking_time < 10:
        if num_ingredients < 4:
            return "Easy"
        else:
            return "Medium"
    else:
        if num_ingredients < 4:
            return "Intermediate"
        else:
            return "Hard"

def create_recipe(conn, cursor):
    """Create a new recipe and add it to the database."""
    print("\n-- Create a New Recipe --")
    
    # Get recipe details from user
    name = input("Enter recipe name: ")
    
    cooking_time = 0
    while True:
        try:
            cooking_time = int(input("Enter cooking time in minutes: "))
            if cooking_time <= 0:
                print("Cooking time must be a positive number.")
                continue
            break
        except ValueError:                      #this makes sure that the input is a number which is positive
            print("Please enter a valid number.")
    
    # Get ingredients as a list
    print("Enter ingredients (type 'done' on a new line when finished):")
    ingredients = []
    while True:
        ingredient = input("- ")
        if ingredient.lower() == 'done':
            break
        ingredients.append(ingredient)
    
    if not ingredients:
        print("Recipe must have at least one ingredient.")
        return
    
    # Convert ingredients list to comma-separated string
    ingredients_str = ", ".join(ingredients)
    
    # Calculate difficulty
    difficulty = calculate_difficulty(cooking_time, ingredients)
    
    try:
        # Build and execute query to insert recipe
        insert_query = """
        INSERT INTO Recipes (name, ingredients, cooking_time, difficulty)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (name, ingredients_str, cooking_time, difficulty))
        conn.commit()
        print(f"Recipe '{name}' added successfully!")
    except mysql.connector.Error as err:
        print(f"Error adding recipe: {err}")

def search_recipe(conn, cursor):
    """Search for recipes by ingredient."""
    print("\n-- Search for a Recipe --")
    
    # Get all ingredients from the database
    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()
    
    if not results:
        print("No recipes found in the database.")
        return
    
    # Create a list of unique ingredients
    all_ingredients = set()
    for row in results:
        # Each row contains a single-element tuple with ingredients string
        ingredients_str = row[0]
        # Split the comma-separated string into individual ingredients
        ingredient_list = [ing.strip() for ing in ingredients_str.split(',')]
        # Add each ingredient to our set (avoiding duplicates)
        all_ingredients.update(ingredient_list)
    
    # Convert set to sorted list for display
    all_ingredients = sorted(all_ingredients)
    
    # Display all unique ingredients
    print("\nAvailable ingredients:")
    for idx, ingredient in enumerate(all_ingredients, 1):
        print(f"{idx}. {ingredient}")
    
    # Get user's choice
    while True:
        try:
            choice = int(input("\nEnter the number of the ingredient to search for: "))
            if 1 <= choice <= len(all_ingredients):
                break
            else:
                print(f"Please enter a number between 1 and {len(all_ingredients)}.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Get the selected ingredient
    search_ingredient = all_ingredients[choice - 1]
    print(f"\nSearching for recipes containing '{search_ingredient}'...")
    
    # Build the search query with LIKE and wildcard %
    search_query = "SELECT * FROM Recipes WHERE ingredients LIKE %s"
    cursor.execute(search_query, (f"%{search_ingredient}%",))
    
    # Fetch and display results
    recipes = cursor.fetchall()
    
    if not recipes:
        print(f"No recipes found containing '{search_ingredient}'.")
    else:
        print(f"\nFound {len(recipes)} recipe(s) containing '{search_ingredient}':")
        for recipe in recipes:
            print(f"\nID: {recipe[0]}")
            print(f"Name: {recipe[1]}")
            print(f"Ingredients: {recipe[2]}")
            print(f"Cooking Time: {recipe[3]} minutes")
            print(f"Difficulty: {recipe[4]}")

def update_recipe(conn, cursor):
    """Update an existing recipe."""
    print("\n-- Update a Recipe --")
    
    # Fetch all recipes to show the user
    cursor.execute("SELECT id, name FROM Recipes")
    recipes = cursor.fetchall()
    
    if not recipes:
        print("No recipes found in the database.")
        return
    
    # Display available recipes
    print("\nAvailable recipes:")
    for recipe in recipes:
        print(f"ID: {recipe[0]} - Name: {recipe[1]}")
    
    # Get recipe ID to update
    recipe_id = 0
    while True:
        try:
            recipe_id = int(input("\nEnter the ID of the recipe to update: "))
            # Check if the ID exists
            cursor.execute("SELECT * FROM Recipes WHERE id = %s", (recipe_id,))
            recipe = cursor.fetchone()
            if recipe:
                break
            else:
                print("Recipe not found. Please enter a valid ID.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Display current recipe details
    print(f"\nCurrent recipe details:")
    print(f"Name: {recipe[1]}")
    print(f"Ingredients: {recipe[2]}")
    print(f"Cooking Time: {recipe[3]} minutes")
    print(f"Difficulty: {recipe[4]}")
    
    # Ask which column to update
    print("\nWhich attribute would you like to update?")
    print("1. Name")
    print("2. Ingredients")
    print("3. Cooking Time")
    
    column_choice = 0
    while True:
        try:
            column_choice = int(input("Enter your choice (1-3): "))
            if 1 <= column_choice <= 3:
                break
            else:
                print("Please enter a number between 1 and 3.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Update based on user's choice
    if column_choice == 1:
        # Update name
        new_name = input("Enter the new name: ")
        cursor.execute("UPDATE Recipes SET name = %s WHERE id = %s", (new_name, recipe_id))
        print(f"Name updated successfully to '{new_name}'.")
        
    elif column_choice == 2:
        # Update ingredients
        print("Enter new ingredients (type 'done' on a new line when finished):")
        ingredients = []
        while True:
            ingredient = input("- ")
            if ingredient.lower() == 'done':
                break
            ingredients.append(ingredient)
        
        if not ingredients:
            print("Recipe must have at least one ingredient.")
            return
        
        # Convert ingredients list to comma-separated string
        ingredients_str = ", ".join(ingredients)
        
        cursor.execute("UPDATE Recipes SET ingredients = %s WHERE id = %s", (ingredients_str, recipe_id))
        print("Ingredients updated successfully.")
        
        # Need to recalculate difficulty
        cursor.execute("SELECT cooking_time FROM Recipes WHERE id = %s", (recipe_id,))
        cooking_time = cursor.fetchone()[0]
        new_difficulty = calculate_difficulty(cooking_time, ingredients)
        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (new_difficulty, recipe_id))
        print(f"Difficulty recalculated and updated to '{new_difficulty}'.")
        
    elif column_choice == 3:
        # Update cooking time
        new_cooking_time = 0
        while True:
            try:
                new_cooking_time = int(input("Enter the new cooking time in minutes: "))
                if new_cooking_time <= 0:
                    print("Cooking time must be a positive number.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")
        
        cursor.execute("UPDATE Recipes SET cooking_time = %s WHERE id = %s", (new_cooking_time, recipe_id))
        print(f"Cooking time updated successfully to {new_cooking_time} minutes.")
        
        # Need to recalculate difficulty
        cursor.execute("SELECT ingredients FROM Recipes WHERE id = %s", (recipe_id,))
        ingredients_str = cursor.fetchone()[0]
        new_difficulty = calculate_difficulty(new_cooking_time, ingredients_str)
        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (new_difficulty, recipe_id))
        print(f"Difficulty recalculated and updated to '{new_difficulty}'.")
    
    # Commit changes
    conn.commit()

def delete_recipe(conn, cursor):
    """Delete a recipe from the database."""
    print("\n-- Delete a Recipe --")
    
    # Fetch all recipes to show the user
    cursor.execute("SELECT id, name FROM Recipes")
    recipes = cursor.fetchall()
    
    if not recipes:
        print("No recipes found in the database.")
        return
    
    # Display available recipes
    print("\nAvailable recipes:")
    for recipe in recipes:
        print(f"ID: {recipe[0]} - Name: {recipe[1]}")
    
    # Get recipe ID to delete
    recipe_id = 0
    while True:
        try:
            recipe_id = int(input("\nEnter the ID of the recipe to delete: "))
            # Check if the ID exists
            cursor.execute("SELECT name FROM Recipes WHERE id = %s", (recipe_id,))
            recipe = cursor.fetchone()
            if recipe:
                break
            else:
                print("Recipe not found. Please enter a valid ID.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Confirm deletion
    confirm = input(f"Are you sure you want to delete recipe '{recipe[0]}'? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Deletion cancelled.")
        return
    
    # Delete the recipe
    cursor.execute("DELETE FROM Recipes WHERE id = %s", (recipe_id,))
    conn.commit()
    print(f"Recipe '{recipe[0]}' has been deleted.")

# This is used to actually call the main menu function to start the program!
if __name__ == "__main__":
    main_menu(conn, cursor)