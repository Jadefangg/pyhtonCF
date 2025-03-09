#OBJECT REALTIONAL MAPPER - 1.7 
#SQLALCHEMY installed

from sqlalchemy import create_engine #importing the create_engine function from the sqlalchemy module
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, or_ 



# Create a connection string using the existing credentials which connects to the task_database
connection_string = "mysql+mysqlconnector://cf-python:password@localhost/task_database" #this has my username(cf-python) and password(password) for the database(task_database)

# Create the engine
engine = create_engine(connection_string, echo=True)

#import - create - use

Base = declarative_base()            #creating a base class for the ORM  
Session = sessionmaker(bind=engine)  #creating a session class for the ORM
session = Session()                  #creating a session object for the ORM   

# Create a Recipe class that inherits from the Base class allowing it to be mapped to the database.

class Recipe(Base):
    """This is the model representing a recipe in the database."""
    
    __tablename__ = 'final_recipes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)                    #nullable=False means that the column cannot be empty
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))
    
    def __repr__(self):
        """Return the sructure of the recipe."""
        return f"Recipe(id={self.id}, name={self.name}, difficulty={self.difficulty})"
    
    def __str__(self):
        """Return a organised version of the recipe."""
        return(#f string is used here to format the string in a more organised way.
            f"\n{'-' * 40}", 
            f"\n{self.name.upper():^40}",
            f"\n{'-' * 40}",
            f"\nCooking Time: {self.cooking_time} minutes",
            f"\nDifficulty: {self.difficulty}",
            f"\n\nIngredients:",
            f"\n{'-' * 15}",
            f"\n" + "\n".join([f"• {ingredient.strip()}" for ingredient in self.return_ingredients_as_list()]),
            f"\n{'-' * 40}\n"
            )
    
    def calculate_difficulty(self):
        """
        This will calculate the difficulty of the recipe based on cooking time and ingredients.
        Will also update the difficulty attribute directly.
        """
        ingredients_list = self.return_ingredients_as_list()
        num_ingredients = len(ingredients_list)
        
        if self.cooking_time < 10:
            if num_ingredients < 4:
                self.difficulty = "Easy"
            else:
                self.difficulty = "Medium"
        else:
            if num_ingredients < 4:
                self.difficulty = "Intermediate"
            else:
                self.difficulty = "Hard"
    
    def return_ingredients_as_list(self):
        """Convert the ingredients string to a list."""
        if not self.ingredients:
            return []
        return self.ingredients.split(', ')

# Create all tables defined in the Base metadata
# this also creates the table in the database.
Base.metadata.create_all(engine)

#Above code is to create the table in the database

#All applications functions start here <<<

def create_recipe():
    """Create a new recipe and add it to the database."""
    print("\n------ Create a New Recipe ------")
    
    # Get recipe name (ensure it's not empty and within length limit)
    while True:
        name = input("\nEnter recipe name: ")
        if not name:
            print("Recipe name cannot be empty.")
            continue
        if len(name) > 50:
            print("Recipe name must be less than 50 characters.")
            continue
        break
    
    # Get cooking time (ensure it's a positive integer)
    while True:
        try:
            cooking_time = input("\nPlease enter the cooking time (minutes): ")
            if not cooking_time.isnumeric():                        #not is used to check if the value is not a number, isnumeric() is a function that will return true if the string is a number.
                print("Cooking time must be a positive number.")
                continue
            cooking_time = int(cooking_time)                        #int is provided in sqlalchemy to convert the string to an integer.
            if cooking_time <= 0:
                print("Cooking time must be a positive number.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    # Get ingredients
    ingredients = []
    while True:
        try:
            num_ingredients = input("\nHow many ingredients would you like to enter? ")
            if not num_ingredients.isnumeric():
                print("Please enter a valid number.")
                continue
            num_ingredients = int(num_ingredients)
            if num_ingredients <= 0:
                print("You must enter at least one ingredient.")
                continue
            break
        except ValueError:                      #value error is provided in sqlalchemy to catch any errors that occur when a value is not valid.
            print("Please enter a valid number.")
    
    print("\nEnter each ingredient:")
    for i in range(num_ingredients):       #this loop runs in every element of range, range is a function that will create a list of numbers from 0 to the number specified in the function.
        while True:
            ingredient = input(f"{i+1}. ") 
            if not ingredient:
                print("Ingredient cannot be empty.")
                continue
            ingredients.append(ingredient)
            break
    
    # Convert ingredients list to string
    ingredients_str = ", ".join(ingredients)
    
    # Create new recipe object
    recipe_entry = Recipe(
        name=name,
        ingredients=ingredients_str,
        cooking_time=cooking_time
    )
    
    # Calculate difficulty
    recipe_entry.calculate_difficulty()
    
    # Add to database
    try:
        session.add(recipe_entry)
        session.commit()
        print(f"\nRecipe '{name}' added successfully!")
    except Exception as e:                 #this is an exception handling block where e is assigned to the error message   
        session.rollback()                 #this will rollback the session if there is an error - start again.
        print(f"Error adding recipe: {e}") #the e is the error message that will now be printed if there is an error

def view_all_recipes():
    """Display all recipes from the database."""
    print("\n------ All Recipes ------")
    
    # Get all recipes from database
    recipes = session.query(Recipe).all()
    
    # Check if any recipes exist
    if not recipes:
        print("\nSorry,no recipes have been found in the database.")
        return None
    
    # Display recipes
    print(f"\nFound {len(recipes)} recipes:")
    for recipe in recipes:
        print(recipe)                       #this will print the recipe object in a formatted way.

def search_by_ingredients():
    """Search for recipes containing specific ingredients."""
    print("\n---Search by Ingredients---")
    
    # Check if there are any recipes
    recipe_count = session.query(Recipe).count()
    if recipe_count == 0:
        print("\nNo recipes found in the database.")
        return None
    
    # Get every ingredients from all the recipes.
    results = session.query(Recipe.ingredients).all()
    
    # Create list of unique ingredients
    all_ingredients = []
    for result in results:
        ingredient_list = result[0].split(', ')            #this code will split the ingredients by the comma and create a list of ingredients which will be stored in the ingredient_list variable.
        for ingredient in ingredient_list:
            if ingredient.strip() not in all_ingredients:
                all_ingredients.append(ingredient.strip()) #this code will strip the ingredient of any white spaces and then add it to the all_ingredients list.
    
    # Sort ingredients alphabetically
    all_ingredients.sort()
    
    # Display ingredients
    print("\nAvailable ingredients:")
    for index, ingredient in enumerate(all_ingredients, 1):  #enumerate will be used to add a counter to the list of ingredients. The counter starts at 1.
        print(f"{index}- {ingredient}")                      #index will be the index of the ingredient in the list and the ingredient is the name of the ingredient.
    
    # Get user's ingredient selection
    while True:
        try:
            selection = input("\nEnter the numbers of ingredients to search for (separated by spaces): ")
            selected_numbers = [int(num) for num in selection.split()]
            
            # Validate all selections
            valid_selection = True
            for num in selected_numbers:
                if num < 1 or num > len(all_ingredients):
                    valid_selection = False
                    break
            
            if not valid_selection:
                print(f"Please enter valid numbers between 1 and {len(all_ingredients)}.")
                continue
            
            break
        except ValueError:
            print("Please enter valid numbers separated by spaces.")
    
    # Create list of ingredients to search for
    search_ingredients = [all_ingredients[num-1] for num in selected_numbers]
    print(f"\nSearching for recipes containing: {', '.join(search_ingredients)}")
    
    # Create search condition
    # the or_ function is used to combine multiple conditions in a query. The differece between or_ and and_ is that or_ will return true if any of the conditions are true.
    conditions = []
    # search condition is created here
    for ingredient in search_ingredients:
        like_term = f"%{ingredient}%"                         # % is a wildcard character that will match any sequence of characters. Its purpose is to match any ingredient that contains the selected ingredient.
        conditions.append(Recipe.ingredients.like(like_term)) # .like is used to search for a pattern in a column. In this case, it will search for the ingredient in the ingredients column.
    # by using % wildcards, it can find ingredients even if they're part of a longer ingredient name



    # Search for recipes with any of the selected ingredients
    found_recipes = session.query(Recipe).filter(or_(*conditions)).all() 
    # The *conditions syntax unpacks the list of conditions and passes them as separate arguments to the or_() function.
    # This creates a combined filter that will match any recipe that contains ANY of the selected ingredients.
    
    # display results
    if not found_recipes:
        print("\nNo recipes found with the selected ingredients.")
    else:
        print(f"\nFound {len(found_recipes)} recipe(s):")
        for recipe in found_recipes:
            print(recipe)

def edit_recipe():
    """Edit an existing recipe."""
    print("\n------ Edit a Recipe ------")
    
    # check if there are any recipes
    recipe_count = session.query(Recipe).count()
    if recipe_count == 0:
        print("\nNo recipes found in the database.")
        return None
    
    # get all recipes (id and name)
    recipes = session.query(Recipe.id, Recipe.name).all()
    
    # display available recipes
    print("\nAvailable recipes:")
    for recipe in recipes:
        print(f"ID: {recipe.id} - {recipe.name}")
    
    # get recipe ID to edit
    while True:
        try:
            recipe_id = input("\nEnter the ID of the recipe to edit: ")
            if not recipe_id.isnumeric():
                print("Please enter a valid ID.")
                continue
            
            recipe_id = int(recipe_id)
            recipe_to_edit = session.query(Recipe).filter(Recipe.id == recipe_id).first()
            
            if not recipe_to_edit:
                print("Recipe not found. Please enter a valid ID.")
                continue
            
            break
        except ValueError:
            print("Please enter a valid number.")
    
    # display editable attributes
    print("\nRecipe details:")
    print(f"1. Name: {recipe_to_edit.name}")
    print(f"2. Ingredients: {recipe_to_edit.ingredients}")
    print(f"3. Cooking Time: {recipe_to_edit.cooking_time} minutes")
    
    # get attribute to edit
    while True:
        try:
            attribute_choice = input("\nWhich attribute would you like to edit (1-3)? ")
            if not attribute_choice.isnumeric():
                print("Please enter a number between 1 and 3.")
                continue
            
            attribute_choice = int(attribute_choice)
            if attribute_choice < 1 or attribute_choice > 3:
                print("Please enter a number between 1 and 3.")
                continue
            
            break
        except ValueError:
            print("Please enter a valid number.")
    
    # edit the chosen attribute
    if attribute_choice == 1:
        # Edit name
        while True:
            new_name = input("\nEnter new name: ")
            if not new_name:
                print("Recipe name cannot be empty.")
                continue
            if len(new_name) > 50:
                print("Recipe name must be less than 50 characters.")
                continue
            
            recipe_to_edit.name = new_name
            print(f"Name updated to: {new_name}")
            break
    
    elif attribute_choice == 2:
        # Edit ingredients
        ingredients = []
        while True:
            try:
                num_ingredients = input("\nHow many ingredients would you like to enter? ")
                if not num_ingredients.isnumeric():
                    print("Please enter a valid number.")
                    continue
                
                num_ingredients = int(num_ingredients)
                if num_ingredients <= 0:
                    print("You must enter at least one ingredient.")
                    continue
                
                break
            except ValueError:
                print("Please enter a valid number.")
        
        print("\nEnter each ingredient:")
        for i in range(num_ingredients):
            while True:
                ingredient = input(f"{i+1}. ")
                if not ingredient:
                    print("Ingredient cannot be empty.")
                    continue
                ingredients.append(ingredient)
                break
        
        # Update ingredients
        recipe_to_edit.ingredients = ", ".join(ingredients)
        print("Ingredients updated successfully.")
        
        # Recalculate difficulty
        recipe_to_edit.calculate_difficulty()
    
    elif attribute_choice == 3:
        # Edit cooking time
        while True:
            try:
                new_cooking_time = input("\nEnter new cooking time (minutes): ")
                if not new_cooking_time.isnumeric():
                    print("Cooking time must be a positive number.")
                    continue
                
                new_cooking_time = int(new_cooking_time)
                if new_cooking_time <= 0:
                    print("Cooking time must be a positive number.")
                    continue
                
                recipe_to_edit.cooking_time = new_cooking_time
                print(f"Cooking time updated to: {new_cooking_time} minutes")
                break
            except ValueError:
                print("Please enter a valid number.")
        
        # Recalculate difficulty
        recipe_to_edit.calculate_difficulty()
    
    # Commit changes to database
    try:
        session.commit()
        print("\nRecipe updated successfully!")
    except Exception as e:
        session.rollback()
        print(f"Error updating recipe: {e}")

def delete_recipe():
    """Delete a recipe from the database."""
    print("\n------ Delete a Recipe ------")
    
    # Check if there are any recipes
    recipe_count = session.query(Recipe).count()
    if recipe_count == 0:
        print("\nNo recipes found in the database.")
        return None
    
    # Get all recipes (id and name)
    recipes = session.query(Recipe.id, Recipe.name).all()
    
    # Display available recipes
    print("\nAvailable recipes:")
    for recipe in recipes:
        print(f"ID: {recipe.id} - {recipe.name}")
    
    # Get recipe ID to delete
    while True:                     #the while loop has the purpose of ensuring that the user enters a valid ID. If the user enters an invalid ID, the loop will continue to ask for a valid ID.
        try:
            recipe_id = input("\nEnter the ID of the recipe to delete: ")
            if not recipe_id.isnumeric():
                print("Please enter a valid ID.")
                continue
            
            recipe_id = int(recipe_id)
            recipe_to_delete = session.query(Recipe).filter(Recipe.id == recipe_id).first()
            
            if not recipe_to_delete:
                print("Recipe not found. Please enter a valid ID.")
                continue
            
            break
        except ValueError:
            print("Please enter a valid number.")
    
    # Confirm deletion
    confirm = input(f"\nAre you sure you want to delete '{recipe_to_delete.name}'? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Deletion cancelled.")
        return None
    
    # Delete recipe
    try:
        session.delete(recipe_to_delete)
        session.commit()
        print(f"\nRecipe '{recipe_to_delete.name}' deleted successfully!")
    except Exception as e:                     #except as is a way to catch an exception and assign it to a variable. This variable can then be used to display the error message. 
        session.rollback()
        print(f"Error deleting recipe: {e}")   #e is here again for the error message

# >>> the main menu begins here <<<
def main_menu():
    """Display the main menu and handle user choices."""
    while True:
        print("\n====== Recipe Management System ======")
        print("1. Create a new recipe")
        print("2. View all recipes")
        print("3. Search for recipes by ingredients")
        print("4. Edit a recipe")
        print("5. Delete a recipe")
        print("Type 'quit' to exit the application")
        
        choice = input("\nEnter your choice: ").lower()     #.lower() is used to convert the user's input to lowercase.
        
        if choice == '1':
            create_recipe()
        elif choice == '2':
            view_all_recipes()
        elif choice == '3':
            search_by_ingredients()
        elif choice == '4':
            edit_recipe()
        elif choice == '5':
            delete_recipe()
        elif choice == 'quit':
            print("\nSaving changes and closing the application...")
            session.close()
            engine.dispose()
            print("Goodbye!")
            break
        else:
            print("\nYour choice is wrong. Please enter a number between 1 and 5, or 'quit'.")

# run the main menu!
if __name__ == "__main__":
    main_menu()