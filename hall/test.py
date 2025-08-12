import openai


client = openai.OpenAI(api_key="your_api_key", base_url="https://api.example.com/v1")
response = client.chat.completions.create(model="grok-3", messages=[])