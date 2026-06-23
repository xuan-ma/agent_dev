
model_type = "DeepSeek"
print("Using model type:", model_type)
models_mapping_info = {
    "DeepSeek": { # https://api-docs.deepseek.com/zh-cn/
        "base_url": {
            "OpenAI": "https://api.deepseek.com",
            "Anthropic": "https://api.deepseek.com/anthropic"
        },
        "model_name": "deepseek-v4-flash"  # deepseek-v4-pro
    },
    "OpenRouter": {
        "base_url": {
            "OpenAI": "https://openrouter.ai/api/v1",
        },
        "model_name": "openai/gpt-5"
    }
}

model_info = models_mapping_info[model_type]
print("Using model name:", model_info["model_name"])