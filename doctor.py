import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

print("--- 🩺 NEXORA DIAGNOSTIC TOOL ---")

# 1. Check API Key
if not api_key:
    print("❌ CRITICAL: GOOGLE_API_KEY is missing from .env file.")
    exit()
else:
    print("✅ API Key found.")

# 2. Configure Google
try:
    genai.configure(api_key=api_key)
    print("✅ Google Driver Configured.")
except Exception as e:
    print(f"❌ Driver Configuration Failed: {e}")
    exit()

# 3. Check Available Models
print("\n--- 🔍 Checking Your Available Models ---")
valid_model_found = False
recommended_model = ""

try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"  • Found: {m.name}")
            if "gemini-1.5-flash" in m.name:
                recommended_model = m.name
                valid_model_found = True
            elif "gemini-pro" in m.name and not recommended_model:
                recommended_model = m.name
                valid_model_found = True

    if valid_model_found:
        # Remove the 'models/' prefix if it exists, LangChain doesn't like it sometimes
        if recommended_model.startswith("models/"):
            recommended_model = recommended_model.replace("models/", "")
            
        print(f"\n✅ SUCCESS! We found a working model for you.")
        print(f"👉 PLEASE USE THIS EXACT NAME IN YOUR CODE:  {recommended_model}")
    else:
        print("\n❌ PROBLEM: No chat models found. Your API Key might be restricted.")

except Exception as e:
    print(f"❌ Connection Error: {e}")