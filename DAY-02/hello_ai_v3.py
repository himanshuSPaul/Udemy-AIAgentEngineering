"""
File         : hello_ai_v3.py
Author       : hi_paul
Created      : 2026-10-24
Last Updated : 2026-10-24
Version      : 1.0.2

Description  :
    AI assistance with memory for maintaining context in conversations.
    Enhanced version of previous interactive AI assistant that adds conversation memory using a list to store messages, allowing the assistant to remember earlier messages and respond in context.
    So , all it does is :
    - Keeps the interactive chat loop from the previous version, letting the user ask multiple questions in one session.
    - Maintains a conversation history by storing both user messages and AI replies in a messages list.
    - Sends the full conversation history with each request, so the AI can understand follow-up questions (e.g. “Can you explain that in simpler words?”).
    

Usage:
    cd DAY-02
    python hello_ai_v3.py

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
messages = []
while True:

    user_input = input("\nYou : ")
    # Save the user's message
    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    if user_input.lower() == "quit":
        print("\nAI  : Goodbye! Have a great day.")
        break

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=messages
    )

    ai_reply = response.choices[0].message.content

    print("\nAI :", ai_reply)

    # Save the AI's reply
    messages.append(
        {
            "role": "assistant",
            "content": ai_reply
        }
    )

    
