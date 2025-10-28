from google import genai
import rich
from rich.markdown import Markdown


client = genai.Client()
chat = client.chats.create(model='gemini-2.5-flash')

while True:
    question = input("Enter a message: ")
    response = chat.send_message(question + ' Answer in a short sentence.')

    rich.print(Markdown(response.text))
    print(response.usage_metadata.total_token_count)


rich.print(Markdown(response.text))
print(response.usage_metadata)