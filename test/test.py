from google import genai

client = genai.Client(api_key="GEMINI_API_KEY")

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="Hello! Who are you?"
)

print(response.text)