"""
File         : hello_ai.py
Author       : hi_paul
Created      : 2026-10-21
Last Updated : 2026-10-21
Version      : 1.0.0

Description  :
    My first AI Assistance that uses the Ollama API to answer questions about Artificial Intelligence.

Usage:
    cd DAY-01
    python hello_ai.py

Arguments / Inputs:
    None


Outputs:
    Writes the AI response to the console.

Dependencies:
    - Python 3.10+


Notes:
    - 

Change Log:

"""















from openai import OpenAI
from dotenv import load_dotenv
import os

# Load configuration from the .env file
load_dotenv()

# Create a client that communicates with Ollama
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

# Send a question to the AI model
response = client.chat.completions.create(
    model=os.getenv("MODEL"),
    messages=[
        {
            "role": "user",
            "content": "What is Artificial Intelligence?"
        }
    ]
)

# Display the response
print(response.choices[0].message.content)
