import os

import requests
import json
from openai import types

# from utils import api_key
from model_api.config import model_platform_info

def token_consume(response: types.chat.chat_completion.ChatCompletion):
    # 查看 Token 消耗，中文约 1.5-1.8 字 ≈ 1 token
    ##### 通过API直接获取
    print(f"\n[Token 消耗] 输入: {response.usage.prompt_tokens}, "
          f"输出: {response.usage.completion_tokens}, "
          f"总计: {response.usage.total_tokens}")
    ######################################
    ##### 使用 Hugging Face transformers
    ######################################
    # from transformers import AutoTokenizer
    # # DeepSeek
    # tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-V3.2")
    # text = "你好,世界!Hello World!"
    # tokens = tokenizer.encode(text)
    # print(f"Token 数量: {len(tokens)}")

    # # Qwen (通义千问)
    # tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-7B")
    # tokens = tokenizer.encode(text)
    # print(f"Token 数量: {len(tokens)}")

    ######################################
    # 仅适用于 OpenAI / GPT 系列模型
    ######################################
    # import tiktoken

    # encoding = tiktoken.encoding_for_model("gpt-5")
    # text = "你好,世界!Hello World!"

    # tokens = encoding.encode(text)
    # print(f"Token 数量: {len(tokens)}")
    

def get_account_balance():
    # requests方式查询账户余额信息
    response = requests.get(
        # "https://openrouter.ai/api/v1/auth/key",
        model_platform_info["balance_url"],
        # headers={"Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}"}
        headers={"Authorization": f"Bearer {model_platform_info['api_key']}"}
    )
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

# response = requests.get(
#     "https://api.deepseek.com/user/balance",
#     headers={"Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}"}
# )

# print(json.dumps(response.json(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    get_account_balance()