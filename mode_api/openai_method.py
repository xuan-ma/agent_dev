from openai import OpenAI

from config import model_info
from utils import api_key

client = OpenAI(
    api_key=api_key,
    base_url=model_info["base_url"]["OpenAI"]  # "https://openrouter.ai/api/v1"  # 添加 base_url
)

response = client.chat.completions.create(
    model=model_info["model_name"],  # "openai/gpt-5",  # deepseek-v4-flash
    messages=[
        {"role": "user", "content": "你好, 请用一句话介绍你自己"}
    ]
)
print("使用 SDK 的结果：", response.choices[0].message.content)