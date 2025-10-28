from google import genai
from google.genai import types
from google.genai.types import GenerateContentConfig
from pydantic import BaseModel

client = genai.Client()

class Colors(BaseModel):
    colors: str
    stars: str
    name: str


with open("image_understanding/stardust.jpg", "rb") as f:
    image_bytes = f.read()

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
        'What colors are in this picture, identify as many stars as you can, what is the name of this star?'      
        ],
        config=GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=list[Colors] #respond with a list of Colors objects
        )
    )

print(response.parsed)  # parsed is a list of Colors objects
for color_info in response.parsed:
    print(color_info.name)  