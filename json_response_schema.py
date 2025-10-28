from google import genai
from google.genai.types import GenerateContentConfig
from pydantic import BaseModel

#this is formatting the response into a defined structure
class Recipe(BaseModel):
    recipe_name: str
    ingredients: list[str]
    instructions: list[str]

client = genai.Client()
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents="""I have leftover chicken, cheese, and broccoli. Suggest one recipe""",
    config=GenerateContentConfig(
        # This gives the model additional instructions on how to respond
        system_instruction='include US and metric units',
        # this tells the model to respond in json format and follow the structure defined in the Recipe class
        response_mime_type="application/json",
        response_schema=Recipe
)
)


    

print(response.text)
recipe = response.parsed # a recipe object 
print("Recipe Name:", recipe.recipe_name)

#looping through ingredients and instructions
for ingredient in recipe.ingredients:
    print(ingredient)
for step in recipe.instructions:
    print(step)