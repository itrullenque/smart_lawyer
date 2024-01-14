import os
import time
from openai import OpenAI

#extracting the api key
filename = 'api_key.txt'
with open(filename, 'r') as file: 
    api_key = file.read().strip() #apikey
    
filename = 'api_org.txt'
with open(filename, 'r') as file:
    api_key2 = file.read().strip() #organization

#instantiate the openai client
myclient = OpenAI(api_key = api_key, 
                  organization=api_key2)


#create the assistance
assistant = myclient.beta.assistants.create(
    name="smart lawyer",
    instructions="You are an expert assistance on developing smart contract in solidity. The user will be provide information to issue a contract.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-1106-preview"
)

# Upload a file with an "assistants" purpose

file_1 = myclient.files.create(
  file=open("Digital assets.pdf", "rb"),
  purpose='assistants'
)

file_2 = myclient.files.create(
  file=open("Investment Company Act of 1940.pdf", "rb"),
  purpose='assistants'
)

file_3 = myclient.files.create(
  file=open("solidity_example.txt", "rb"),
  purpose='assistants'
)

#Create a thread
thread = myclient.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": "",
      "file_ids": [file_1.id,file_2.id,file_3.id]
    }
  ]
)

#create the message
message = myclient.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=
    """
    Please follow the next instructions:
    1. Extract the text from the pdf.
    2. Process the information of the pdf's and find the key points.
    3. Write Solidity code for a smart contract of a bond token that satisfies the legal requirements extracted from the pdf's. As an example use the template bond token in the txt file. Make the smart contract as advanced as possible.
    4. Your answer should be structured in the following way:
        a. The solidity code of the smart contract.
        b. The proof that the smart contract complies with the regulations.
    """
)

#Run the assistance
run = myclient.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
)

#Check run status
while run.status != "completed":
    run = myclient.beta.threads.runs.retrieve(
  thread_id=thread.id,
  run_id=run.id
)
    time.sleep(1)

#Display the message
messages = myclient.beta.threads.messages.list(
  thread_id=thread.id
)
new_message = messages.data[0].content[0].text.value

print(messages)