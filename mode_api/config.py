
model_type = "DeepSeek"
print("Using model type:", model_type)
models_mapping_info = {
    "DeepSeek": { # https://api-docs.deepseek.com/zh-cn/
        "base_url": {
            "OpenAI": "https://api.deepseek.com",
            "Anthropic": "https://api.deepseek.com/anthropic"
        },
        "balance_url": "https://api.deepseek.com/user/balance",
        "model_name": "deepseek-v4-flash"  # deepseek-v4-pro
    },
    "OpenRouter": {
        "base_url": {
            "OpenAI": "https://openrouter.ai/api/v1",
        },
        "balance_url": "https://openrouter.ai/api/v1/auth/key",
        "model_name": "openai/gpt-5"
    },
    "DashScope": {  # 阿里百炼
        "base_url": {
            "OpenAI": "https://dashscope.aliyuncs.com/compatible-mode/v1"
        },
        "model_name": "text-embedding-v3"
    },
    "ZhiPu": {
        "base_url": {
            "OpenAI": "https://open.bigmodel.cn/api/paas/v4/"
        },
        "model_name": "GLM-4.7"  # GLM-4.6V
    },
    "OpenAI": {
        "base_url": {
            "OpenAI": "https://api.openai.com/v1"
        },
        "model_name": "gpt-5"
    }
}

model_info = models_mapping_info[model_type]
print("Using model name:", model_info["model_name"])