class Recipe:
    """the class to represent a cooking recipe."""
    
                            # Class variable to store all ingredients across recipes
    all_ingredients = []    #stores all the ingredients across all the recipes.

    def __init__(self, name):
        """Initialize recipe with name and empty values."""
        self.name = name
        self.ingredients = []
        self.cooking_time = 0
        self.difficulty = None

    # Getter and setter for name
    @property
    def name(self):
        """Get recipe name."""
        return self._name

    @name.setter
    def name(self, value):
        """Set recipe name."""
        self._name = value

    # Getter and setter for cooking_time
    @property
    def cooking_time(self):
        """Get cooking time."""
        return self._cooking_time
    
    @cooking_time.setter
    def cooking_time(self, value):
        """Set cooking time and recalculate difficulty."""
        self._cooking_time = value
        self.difficulty = None  # Reset difficulty when cooking time changes

    def add_ingredients(self, *ingredients):
        """Add ingredients to recipe and update all_ingredients."""
        self.ingredients.extend(ingredients)
        self.difficulty = None  # Reset difficulty when ingredients change
        self.update_all_ingredients()

    def get_ingredients(self):
        """Get list of ingredients."""
        return self.ingredients

    def calculate_difficulty(self):
        """Calculate recipe difficulty based on cooking time and ingredients."""
        if not self.cooking_time or not self.ingredients:
            self.difficulty = None
            return
        # Calculate difficulty based on cooking time and number of ingredients
        num_ingredients = len(self.ingredients)
        
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

    #property is a decorator that is an inbuilt function in python, 
    # it is used to access the class variable.
    #a decorator is a design pattern in python that allows a user to add new functionality 
    # to an object without modifying its structure.

    @property
    def difficulty(self):
        """Get difficulty, calculating it if not set."""
        if self._difficulty is None:
            self.calculate_difficulty()
        return self._difficulty
    
    #setter is a decorator that is an inbuilt function in python,
    #it is used to set the class variable
    #here it is being used to set the difficulty of the recipe.

    @difficulty.setter
    def difficulty(self, value):
        """Set difficulty."""
        self._difficulty = value

    def search_ingredient(self, ingredient):
        """Search for an ingredient in the recipe."""
        return ingredient in self.ingredients

    def update_all_ingredients(self):
        """Update class's all_ingredients list."""
        for ingredient in self.ingredients:
            if ingredient not in Recipe.all_ingredients:
                Recipe.all_ingredients.append(ingredient)

    def __str__(self):
        """Return string representation of recipe."""
        return (
            f"\nRecipe: {self.name}\n"
            f"Cooking Time: {self.cooking_time} minutes\n"
            f"Ingredients: {', '.join(self.ingredients)}\n"
            f"Difficulty: {self.difficulty}"
        )
    
    #classmethod is a decorator that is an inbuilt function in python,
    # it is used to define a method that is bound to the class rather than its object.
    #here it is used to search for recipes containing an ingredient.

    @classmethod
    def recipe_search(cls, data, search_term):#cls is used to access the class variable. 
        """Search for recipes containing an ingredient."""
        print(f"\nResults for recipes containing {search_term}:")
        found = False
        for recipe in data:
            if recipe.search_ingredient(search_term):
                print(recipe)
                found = True
        if not found:
            print("No recipes found.")

# The main code begins here

def main():
    # Create Tea recipe
    tea = Recipe("Tea")
    tea.add_ingredients("Tea Leaves", "Sugar", "Water")
    tea.cooking_time = 5
    print(tea)

    # Create Coffee recipe
    coffee = Recipe("Coffee")
    coffee.add_ingredients("Coffee Powder", "Sugar", "Water")
    coffee.cooking_time = 5
    print(coffee)

    # Create Cake recipe
    cake = Recipe("Cake")
    cake.add_ingredients("Sugar", "Butter", "Eggs", "Vanilla Essence", 
                        "Flour", "Baking Powder", "Milk")
    cake.cooking_time = 50
    print(cake)

    # Create Banana Smoothie recipe
    smoothie = Recipe("Banana Smoothie")
    smoothie.add_ingredients("Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes")
    smoothie.cooking_time = 5
    print(smoothie)

    # Create recipe list
    recipes_list = [tea, coffee, cake, smoothie]

    # Search for recipes here
    print("\nRecipe Search Results:")
    print("=====================")
    for ingredient in ["Water", "Sugar", "Bananas"]:
        Recipe.recipe_search(recipes_list, ingredient)

                           #__name__ is a built-in variable that is used to check if the code is being run as the main program.
if __name__ == "__main__": #this is used to check if the code is being run as the main program.
    main()                 #calling the main function.