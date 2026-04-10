import os
from dotenv import load_dotenv

# This loads the variables from .env into your environment
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    print("✅ Environment is set up correctly!")
    print(f"Key starts with: {api_key[:7]}...")
else:
    print("❌ Key not found. Check your .env file naming.")