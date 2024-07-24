from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "You are world class Professor"},
        {
          "type": "image_url",
          "image_url": {
            "url": "https://telegra.ph/file/43b2a90a5d1e168d68718.png",
          },
        },
      ],
    }
  ],
  stream=True,
  max_tokens=300,
)
for chunk in response:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")


