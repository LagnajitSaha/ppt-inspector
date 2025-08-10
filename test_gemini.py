from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ No GEMINI_API_KEY found in .env file")
    exit()

print("✅ Loaded API key:", api_key[:10] + "...")

# Configure Gemini API
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

# Test request
try:
    response = model.generate_content("Say hello in one sentence.")
    print("🤖 Gemini says:", response.text)
except Exception as e:
    print("❌ Error:", e)
