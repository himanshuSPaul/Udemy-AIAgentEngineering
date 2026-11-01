# API_KEY=ollama
# BASE_URL= http://localhost:11434/v1
# MODEL=qwen3:1.7b

"""
Added perspective To AI Assitance by adding system message
"""



import os
from dotenv import load_dotenv
from openai import OpenAI

conversation = []
# Load Env from .env file
load_dotenv()
api_key = os.getenv("API_KEY")
base_url =os.getenv("BASE_URL")
model = os.getenv("MODEL")
print("API KEy From .env File :",api_key)
print("Base URL From .env File :",base_url)
print("Model From .env File :",model)

role_list = [
  {"role_id" :0, "role_name":"Teacher","role_prompt":"Consider your self as Teacher. Explain politely in 20 words"},
  {"role_id" :1, "role_name":"Science Expert","role_prompt":"Consider your self as Science Expert. Explain politely in 15 words"},
  {"role_id" :2, "role_name":"Philosopher","role_prompt":"Consider your self as Philosopher. Explain politely in 10 words"},
  
]


# Create Moodel Connection 
client = OpenAI(base_url=base_url,api_key=base_url)
print("Client :",client)

user_message = """
Choose Your Assitance !
0. Teacher
1. Science Expert
2. Shop owner
"""
user_input = eval(input(user_message))
print("User Input:",user_input)
print("User Input:",role_list[user_input])


print("Selected Assitance :",role_list[user_input]['role_name'])
conversation.append({'role':'system','content':role_list[user_input]['role_prompt']})



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
  
  
  print("\n\n=====>>>>>>Conversion Stack Trace<<<<<<<<===***")
  for message in  conversation :
   print(message)
  print("==================>>>>>><<<<<<<<=============\n\n***")
   
        
