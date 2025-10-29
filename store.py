from google import genai
from google.genai.types import GenerateContentConfig
import rich
from rich.markdown import Markdown
import sys



client = genai.Client()
chat= client.chats.create(model='gemini-2.5-flash')
try:
    with open('chat_system_instructions.txt', 'r') as f:
        system_instructions_text = f.read()
except:
    print("Error missing system instructions file.")
    sys.exit()

while True:
    question = input("Enter a question for Betty: ")
    response = chat.send_message(
        question,
        config=GenerateContentConfig(
            # giving context and instructions to the model to act as a programming tutor    
            system_instructions=system_instructions_text,
            )
    )
    

rich.print(Markdown(response.text))