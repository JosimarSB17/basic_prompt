from google import genai
from google.genai import types

client = genai.Client()

with open("image_understanding/monkey.jpg", "rb") as f:
    image_bytes = f.read()

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
        'What is this picture of?'      
        ]
    )

print(response.text)