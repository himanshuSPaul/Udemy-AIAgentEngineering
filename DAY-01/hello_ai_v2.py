"""
File         : hello_ai_v2.py
Author       : hi_paul
Created      : 2026-10-21
Last Updated : 2026-10-21
Version      : 1.0.0

Description  :
    My first AI agent that uses the Ollama API to answer questions about Artificial Intelligence.
    - This version includes a simple interactive chat interface using conversation loops
    - Lets the user end the session at any time by typing quit.

Usage:
    cd DAY-01
    python hello_ai_v2.py

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

# Load configuration
load_dotenv()

# Create AI client
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

print("=" * 40)
print("      My AI Assistant")
print("=" * 40)

while True:

    user_input = input("\nYou : ")

    if user_input.lower() == "quit":
        print("\nAI  : Goodbye! Have a great day.")
        break

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    print("\nAI :", response.choices[0].message.content)

