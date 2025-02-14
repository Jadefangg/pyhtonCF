#Defining the recipies for the different types of food
recipe_1={
    "name":"Pasta",
    "cooking_time":10,
    "ingredients":["penne","tomato sauce","onion","garlic","salt","pepper"],
}
recipe_2={
    "name":"Pizza",
    "cooking_time":20,
    "ingredients":["dough","tomato sauce","mozzarella","garlic","olives"],

}
recipe_4={
    "name":"Soup",
    "cooking_time":15,
    "ingredients":["carrot","onion","celery","potato","water","salt","pepper"],
}
recipe_5={
    "name":"Burger",
    "cooking_time":15,
    "ingredients":["bread","chicken","lettuce","tomato","onion","aoili",],
}

recipes=[recipe_1,recipe_2,recipe_4,recipe_5]
for recipe in recipes:
    print(recipe["ingredients"])
