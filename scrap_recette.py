import scrape_schema_recipe
import re

class Recipe :

  totalRecipes = 0

  def __init__(self, scrape, classified_ingredient_list):
    Recipe.totalRecipes += 1
    self.name = scrape['name']
    self.prepTime = scrape['prepTime']
    self.cookTime = scrape['cookTime']
    self.image = scrape['image']
    self.recipeYield = scrape['recipeYield']
    self.ingredients = classified_ingredient_list
    self.recipeInstructions = scrape['recipeInstructions']

  def getTotalNumber(cls):
    return cls.totalRecipes
  getTotalNumber = classmethod(getTotalNumber)

class Ingredient :
  def __init__(self, typeIngredient, amount, ingredient) :
    self.typeIngredient = typeIngredient
    self.amount = amount
    self.ingredient = ingredient

  def format(self):
    if self.typeIngredient == "vagueAmount" :
      return self.ingredient
    elif self.typeIngredient == "amount" :
      return self.amount + " de " + self.ingredient
    else :
      return self.amount + " " + self.ingredient

url = 'https://www.marmiton.org/recettes/recette-hasard.aspx'
recipe_list = scrape_schema_recipe.scrape_url(url, python_objects=True)

ingredient_list = recipe_list[0]['recipeIngredient']
clean_ingredient_list = []

for ingredient in ingredient_list :
  if " et " in ingredient :
    ingredient1 = ingredient.split(" et ")[0].replace(" d'"," de ",1)
    ingredient2 = ingredient.split(" et ")[1].replace(" d'"," de ",1)
    clean_ingredient_list.append(ingredient1)
    clean_ingredient_list.append(ingredient2)
  elif " ou " in ingredient :
    ingredient1 = ingredient.split(" ou ")[0].replace(" d'"," de ",1)
    ingredient2 = ingredient.split(" ou ")[1].replace(" d'"," de ",1)
    clean_ingredient_list.append(ingredient1)
    clean_ingredient_list.append(ingredient2)
  else :
    clean_ingredient_list.append(ingredient)

classified_ingredient_list = []

for ingredient in clean_ingredient_list :
  splitted_ingredient = ingredient.split()
  if re.match('\d+(\/\d+)?',splitted_ingredient[0]) != None :
    if "de" in splitted_ingredient :
      typeIngredient = "amount"
      index = splitted_ingredient.index("de")
      assumed_amount = " ".join(splitted_ingredient[:index])
      assumed_ingredient = " ".join(splitted_ingredient[index+1:])
    else :
      typeIngredient = "piece"
      assumed_amount = splitted_ingredient[0]
      assumed_ingredient = " ".join(splitted_ingredient[1:])
  else :
    typeIngredient = "vagueAmount"
    assumed_amount = ""
    assumed_ingredient = " ".join(splitted_ingredient)
  ingredient = Ingredient(typeIngredient, assumed_amount, assumed_ingredient)
  classified_ingredient_list.append(ingredient)

recipe = Recipe(recipe_list[0], classified_ingredient_list)

print(recipe.recipeInstructions)



