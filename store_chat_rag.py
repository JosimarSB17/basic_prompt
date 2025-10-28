from google import genai
from google.genai import types
from google.genai.types import GenerateContentConfig
import rich
from rich.markdown import Markdown
import sys
import os 
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
import pandas


client = genai.Client()

class GeminiEmbeddingfunction(EmbeddingFunction):
    documnet_mode = True # true = generate embeddings for documents, false = generate embeddings for queries

    def __call__(self, input:Documents):
        if self.documnet_mode:
            embedding_task = 'retrieval_document'
        else:
            embedding_task = 'retrieval_query'
        
        response = client.models.embed_content(
            model = 'models/text-embedding-004',
            contents = input,
            config= types.EmbedContentConfig(
                task_type=embedding_task
        ))

        return [e.values for e in response.embeddings] # list comprehension
        

embed_function = GeminiEmbeddingfunction()
embed_function.documnet_mode = True #generate embeddings mode
# Initialize ChromaDB persistent client
chroma_client = chromadb.PersistentClient()
db = chroma_client.get_or_create_collection(
    name='Zoomies_clothes',
    embedding_function=embed_function
)

with open('sport_clothes.csv', 'r') as file:
    clothing_data = pandas.read_csv(file)
    ids = list(clothing_data["Style Number"])
    documents = list(clothing_data["Product Description"])

db.upsert(
    ids=ids,
    documents=documents
)

embed_function.documnet_mode = False # quering the database - finding relevant documents

#query = "can you suggest lightweight yoga pants?"
#results = db.query(query_texts=[query], n_results=5) # how many results to return
#[all_items] = results['documents'] 
#print(all_items)

chat= client.chats.create(model='gemini-2.5-flash')
try:
    with open('chat_system_instructions.txt', 'r') as f:
        system_instructions_text = f.read()
except:
    print("Error missing system instructions file.")
    sys.exit()

while True:
    question = input("Enter a question for Betty: ")
    # perform a Rag search here to find relevant documents

    results = db.query(query_texts=[question], n_results=5) # how many results to return
    [all_items] = results['documents'] 
    print(all_items)

    # creat a prompt that includes the relevant documents

    prompt_with_rag = f"""The user has the following question. 
        USER Question:{question}

        Here is the information from the product database that may help answer the users question."""
    for item in all_items:
        item_one_line = item.replace('\n', ' ') 
        prompt_with_rag += f"Product: {item_one_line}\n"
    print(prompt_with_rag)


    response = chat.send_message(
        prompt_with_rag,
        config=GenerateContentConfig(
            # giving context and instructions to the model to act as a programming tutor    
            system_instructions=system_instructions_text,
            )
    )
    

rich.print(Markdown(response.text))