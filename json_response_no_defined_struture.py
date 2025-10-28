from google import genai
from google.genai.types import GenerateContentConfig




client = genai.Client()
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents="""I have leftover chicken, cheese, and broccoli. Suggest one recipe""",
    config=GenerateContentConfig(
        response_mime_type="application/json"
)
)


    

print(response.text)    