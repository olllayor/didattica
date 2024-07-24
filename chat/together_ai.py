# together_ai.py
import os
from dotenv import load_dotenv
from together import Together

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
TOKEN = os.getenv("TOGETHER_API_KEY")

if not TOKEN:
    raise ValueError("TOGETHER_API_KEY environment variable not set")

client = Together(api_key=TOKEN)

stream = client.chat.completions.create(
    model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
    messages=[
        {"role": "user", "content": "What are some fun things to do in New York?"}
    ],
    stream=True,
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="", flush=True)
