from google import genai
from pydantic import BaseModel


client = genai.Client()

class Items(BaseModel):
    product_suggestions: str
    cost: float
    reasoning: list[str]

response = client.models.generate_content(
    model='gemini-2.5-flash',
    # this is the prompt/question we are asking the model
    contents="""We are a business selling logging and monitoring products 
    What are good products to give away at our booth at PyCon?
    Last year we gave away tote bags and they were popular and met our budget 
    The year before we gave away pens and they were cheap but not popular
    the year before we gave away water bottles and they were popular but too expensive"""
)



print(response.text)

item = response.parsed  # Pydantic Items object
print("Product Suggestions:", item.product_suggestions)

for cost in item.cost:
    print(cost)
for reason in item.reasoning:
    print(reason)
