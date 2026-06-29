import os
from pathlib import Path

from dotenv import load_dotenv

from config import model_type

## 加载 apikey
env_path = Path(__file__).parent / ".env"  # 当前文件同级目录
load_dotenv(env_path, override=True)
api_key = os.getenv(f"{model_type.upper()}_API_KEY")
# api_key = os.getenv("DEEPSEEK_API_KEY")
print("api_key", api_key)