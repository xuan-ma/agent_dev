import os
from pathlib import Path

from dotenv import load_dotenv

# from config import model_type

model_platform = "OpenRouter"

## 加载环境变量
env_path = Path(__file__).parent / ".env"  # 当前文件同级目录
load_dotenv(env_path, override=True)
# api_key = os.getenv(f"{model_type.upper()}_API_KEY")
# api_key = os.getenv("DEEPSEEK_API_KEY")
# print("api_key", api_key)

print("Using model platform:", model_platform)
PLATFORMS_CONFIG = {
    "DeepSeek": { # https://api-docs.deepseek.com/zh-cn/
        "base_url": {
            "OpenAI": "https://api.deepseek.com",
            "Anthropic": "https://api.deepseek.com/anthropic"
        },
        "api_key": os.getenv("DEEPSEEK_API_KEY"),
        "balance_url": "https://api.deepseek.com/user/balance",
        "model_name": "deepseek-v4-flash"  # deepseek-v4-pro
    },
    "OpenRouter": {
        "base_url": {
            "OpenAI": "https://openrouter.ai/api/v1",
        },
        "api_key": os.getenv("OPENROUTER_API_KEY"),
        "balance_url": "https://openrouter.ai/api/v1/auth/key",
        # 智谱: z-ai/glm-5.2
        # deepseek: deepseek/deepseek-v4-pro
        # OpenAI: openai/gpt-4o, 
        "model_name": "openai/gpt-5"  
    },
    "DashScope": {  # 阿里百炼
        "base_url": {
            "OpenAI": "https://dashscope.aliyuncs.com/compatible-mode/v1"
        },
        "api_key": os.getenv("DASHSCOPE_API_KEY"),
        "model_name": "text-embedding-v3"
    },
    "ZhiPu": {
        "base_url": {
            "OpenAI": "https://open.bigmodel.cn/api/paas/v4/"
        },
        "api_key": os.getenv("ZHIPU_API_KEY"),
        "model_name": "GLM-4.7"  # GLM-4.6V
    },
    "OpenAI": {
        "base_url": {
            "OpenAI": "https://api.openai.com/v1"
        },
        "api_key": os.getenv("OPENAI_API_KEY"),
        "model_name": "gpt-5"
    }
}

model_platform_info = PLATFORMS_CONFIG[model_platform]
print("Using model name:", model_platform_info["model_name"])