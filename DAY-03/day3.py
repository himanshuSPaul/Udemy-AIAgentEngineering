# API_KEY=ollama
# BASE_URL= http://localhost:11434/v1
# MODEL=qwen3:1.7b

"""
Added perspective To AI Assitance by adding system message
"""



import os
from dotenv import load_dotenv
from openai import OpenAI

conversation = [
              {"role":"system",
              "content":"Consider yourself as AI teacher. Explain every concept in simple language with on 50 words with real-life examples.Keep the resoponse more natural"}
              ]
# Load Env from .env file
load_dotenv()
api_key = os.getenv("API_KEY")
base_url =os.getenv("BASE_URL")
model = os.getenv("MODEL")
print("API KEy From .env File :",api_key)
print("Base URL From .env File :",base_url)
print("Model From .env File :",model)


# Create Moodel Connection 
client = OpenAI(base_url=base_url,api_key=base_url)
print("Client :",client)


print("\n\n\n",40*'=')
while True:
  user_message = {}
  user_input = input("User :> ")
  user_message ['role']='user'
  user_message ['content'] =user_input
  conversation.append(user_message)
  
  #print("\n\n*** conversation :",conversation)
  if user_input.lower() == 'quit':
    break
  # Send request to Model
  response = client.chat.completions.create(model=model,messages=conversation 
                                           )
  # print AI response
  print("AI   :> ",response.choices[0].message.content, "\n")
  agent_message = {}
  agent_message['role'] ='assitance'
  agent_message['content'] = response.choices[0].message.content
  conversation.append(agent_message)
  
  
  #print("\n\n=====>>>>>>Conversion Stack Trace<<<<<<<<===***")
  #for message in  conversation :
  #  print(message)
  #print("==================>>>>>><<<<<<<<=============\n\n***")
   
        
