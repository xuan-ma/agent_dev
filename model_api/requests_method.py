import os

import requests
# from dotenv import load_dotenv

from config import model_platform_info
# from utils import api_key

# # 加载环境变量
# load_dotenv(override=True)
# 获取 API Key
# api_key = os.getenv("OPENROUTER_API_KEY")
headers={
    "Authorization": f"Bearer {model_platform_info['api_key']}", 
    "Content-Type": "application/json"
}


def get_platform_models():
    platform_model_url = f"{model_platform_info['base_url']['OpenAI']}/models"
    response: requests.models.Response = get(platform_model_url)
    if response.status_code == 200:
        platform_models_list = [item['id'] for item in response.json()['data']]
        print("连接成功！可用模型列表:", platform_models_list)
        return platform_models_list
    else:
        raise Exception(f"连接失败: {response.status_code}")

def get(url: str):
    print("url:", url)
    return requests.get(url, headers=headers)  # f"{base_url}/models"
    # print(f"状态码: {response.status_code}")
    

def post(url: str):
    response = requests.post(
        model_platform_info["base_url"]["OpenAI"] + "/chat/completions",
        json={
            "model": model_platform_info["model_name"],  # "openai/gpt-5", 
            "messages": [
                {"role": "user", "content": "你好, 请用一句话介绍你自己"}
            ]
        }
    )

    result = response.json()
    print("不用 SDK 的结果：", result['choices'][0]['message']['content'])


if __name__ == "__main__":
    # get(f"model_platform_info['base_url']/models")
    get_platform_models()
    # post()