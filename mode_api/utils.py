import os

from dotenv import laod_dotenv


load_dotenv(override=True)

api_key = os.getenv("DEEPSEEK_API_KEY")
