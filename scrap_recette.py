import scrape_schema_recipe
import re

url = 'https://www.marmiton.org/recettes/recette-hasard.aspx'
recipe_list = scrape_schema_recipe.scrape_url(url, python_objects=True)
recipe = recipe_list[0]

ingredient_list = recipe['recipeIngredient']
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

for ingredient in clean_ingredient_list :
  splitted_ingredient = ingredient.split()
  if re.match('\d+(\/\d+)?',splitted_ingredient[0]) != None :
    if "de" in splitted_ingredient :
      index = splitted_ingredient.index("de")
      assumed_amount = " ".join(splitted_ingredient[:index])
      assumed_ingredient = " ".join(splitted_ingredient[index+1:])
    else :
      assumed_amount = splitted_ingredient[0]
      assumed_ingredient = " ".join(splitted_ingredient[1:])
  else :
    assumed_amount = ""
    assumed_ingredient = " ".join(splitted_ingredient)
  print(assumed_amount)
  print(assumed_ingredient)


