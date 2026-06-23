import os

from dotenv import load_dotenv

from config import model_type


load_dotenv(override=True)
api_key = os.getenv(f"{model_type.upper()}_API_KEY")
print("api_key", api_key)