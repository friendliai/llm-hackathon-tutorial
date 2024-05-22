import os
import gradio as gr
from friendli import Friendli

FRIENDLI_TOKEN = os.getenv("FRIENDLI_TOKEN")
client = Friendli(token=FRIENDLI_TOKEN)

def chat_function(message, history):
  new_messages = []
  for user, chatbot in history:
    new_messages.append({"role" : "user", "content": user})
    new_messages.append({"role" : "assistant", "content": chatbot})
  new_messages.append({"role": "user", "content": message})

  stream = client.chat.completions.create(
    model="meta-llama-3-70b-instruct",
    messages=new_messages,
    stream=True
  )
  res = ""
  for chunk in stream:
    res += chunk.choices[0].delta.content or ""
    yield res

gr.ChatInterface(chat_function).launch()
