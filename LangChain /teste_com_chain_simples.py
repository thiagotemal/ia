import os

from dotenv import load_dotenv
from groq import Groq

# Carrega as variáveis do arquivo .env para o sistema
load_dotenv()

client = Groq(os.getenv("GROK_API_KEY"))

completion = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
      {
        "role": "user",
        "content": "DeepLearing é machibe learning ?"
      }
    ],

)

print(completion.choices[0].message.content)
