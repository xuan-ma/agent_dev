import os

import requests
# from dotenv import load_dotenv

from config import model_info
from utils import api_key

# # 加载环境变量
# load_dotenv(override=True)
# 获取 API Key
# api_key = os.getenv("OPENROUTER_API_KEY")

# 使用 OpenRouter 的 base_url
response = requests.post(
    # "https://openrouter.ai/api/v1/chat/completions",  # OpenRouter 地址
    model_info["base_url"]["OpenAI"] + "/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}", 
        "Content-Type": "application/json"
    },
    json={
        "model": model_info["model_name"],  # "openai/gpt-5", 
        "messages": [
            {"role": "user", "content": "你好, 请用一句话介绍你自己"}
        ]
    }
)

result = response.json()
print("不用 SDK 的结果：", result['choices'][0]['message']['content'])