import openai
import os
import json

dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(dir_path, 'conversation.json')


# Load in the conversation json file
with open(file_path) as json_file:
  conversation = json.load(json_file)


functions=[
      {
        "name": "send_money",
        "description": "Send someone money to someone else",
        "parameters": {
            "type": "object",
            "properties": {
                "name":{
                    "type": "string",
                    "description": "The name of the person to send the tip to"
                },
                "amount":{
                    "type": "number",
                    "description": "The amount of money to send to the user",
                },
                "currency":{
                    "type": "string",
                    "description": "The currency to send the money in",
                },
            }
        },
        "required": ["name", "amount"]
      },
      {
        "name": "create_wallet",
        "description": "Create a wallet for the user",
        "parameters": {
            "type": "object",
            "properties": {
                "name":{
                    "type": "string",
                    "description": "The name of the wallet to create"
                },
            }
        },
      },
      {
        "name": "check_balance",
        "description": "Check the balance of a requested contact or wallet",
        "parameters": {
            "type": "object",
            "properties": {
                "name":{
                    "type": "string",
                    "description": "The name of the contact or wallet to check the transactions of",
                },
            }
        }
      },
            {
        "name": "check_transactions",
        "description": "Check the transactions of a requested contact or wallet",
        "parameters": {
            "type": "object",
            "properties": {
                "name":{
                    "type": "string",
                    "description": "The name of the contact or wallet to check the transactions of",
                },
            }
        }
      },
]


def generate_response(prompt):
  # Add the prompt to the conversation
  conversation.append({'role': 'user', 'name':'Awera', 'content':prompt+'.'})
  openai.api_key = os.environ["OPEN_AI_KEY"]
  response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=conversation,
    functions=functions,
    temperature=1.1,
  )
  # Save the conversation back to the json file, adding correct indentation

  
  if response.choices[0].finish_reason == 'function_call':
    retuend_response = response['choices'][0]['message']['function_call']
    return retuend_response
  else:
    conversation.append(response['choices'][0]['message'])
    with open(file_path, 'w') as outfile:
      json.dump(conversation, outfile, indent=4)
  return response['choices'][0]['message']['content']

def generate_text(prompt):
  openai.api_key = os.environ["OPEN_AI_KEY"]
  conversation.append({'role': 'user', 'name':'Awera', 'content':prompt+'.'})
  response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=conversation,
  )
  conversation.append(response['choices'][0]['message'])
  with open(file_path, 'w') as outfile:
    json.dump(conversation, outfile, indent=4)
  return response['choices'][0]['message']['content']
