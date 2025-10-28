from google import genai
from google.genai.types import GenerateContentConfig
import rich
from rich.markdown import Markdown



client = genai.Client()
chat= client.chats.create(model='gemini-2.5-flash')

while True:
    question = input("Enter a question for the tutor: ")
    response = chat.send_message(
        question,
        config=GenerateContentConfig(
            # giving context and instructions to the model to act as a programming tutor    
            system_instructions="""You are a helpful programming tutor for Java programming students
            You can explain concepts and programs but don't give the user the answer. If the user
            asks for code, ask them questions and explain concepts to help them write it themselves.""",
            )
    )
    

rich.print(Markdown(response.text))