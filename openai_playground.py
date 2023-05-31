import os
import openai
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "

def general_query(prompt):
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n{prompt}",
    temperature=0.9,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
  )
  print(f"This is response info from OPENAI: {response}")
  return response['choices'][0]['text'].replace("AI:", "").strip()
#
# prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: What is cricket\nAI: Cricket is a sport that originated in England and is played with a bat and ball. It is similar to baseball, but has some unique features to the game such as the fielding positions and the two innings.\nHuman: Which sports I asked earlier You asked me about cricket.",

# print(general_query())