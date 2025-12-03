import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load your API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Error: GOOGLE_API_KEY not found in .env file")
else:
    genai.configure(api_key=api_key)
    print("--- 🔍 Checking Available Models for your API Key ---")
    try:
        count = 0
        for m in genai.list_models():
            # We only care about models that can Chat (generateContent)
            if 'generateContent' in m.supported_generation_methods:
                print(f"✅ Found: {m.name}")
                count += 1
        
        if count == 0:
            print("❌ No chat models found! Your API key might be restricted or invalid.")
            
    except Exception as e:
        print(f"Error connecting to Google: {e}")