import os

from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("AVALAI_API_KEY")

if api_key:
    print("AVALAI_API_KEY is loaded successfully.")
    print(f"Key length: {len(api_key)}")
else:
    print("AVALAI_API_KEY was not found.")
