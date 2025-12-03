import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

print("Available Gemini models:")
print("-" * 60)
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"Name: {model.name}")
        print(f"  Display Name: {model.display_name}")
        print(f"  Methods: {model.supported_generation_methods}")
        print()
