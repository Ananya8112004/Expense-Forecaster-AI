import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
env_path = Path(__file__).parent / '.env'
print(f"Loading .env from: {env_path}")
print(f".env file exists: {env_path.exists()}")

load_dotenv(dotenv_path=env_path)

# Check the API key
api_key = os.getenv('GEMINI_API_KEY')
print(f"GEMINI_API_KEY loaded: {api_key is not None}")
if api_key:
    print(f"API Key starts with: {api_key[:10]}...")
else:
    print("ERROR: API key is None or empty")

# Print all environment variables that start with GEMINI
print("\nAll GEMINI environment variables:")
for key, value in os.environ.items():
    if 'GEMINI' in key:
        print(f"{key} = {value[:20] if value else 'None'}...")
