from openai import OpenAI

from config import model_info
from utils import api_key
from fee_info import token_consume

client = OpenAI(
    api_key=api_key,
    base_url=model_info["base_url"]["OpenAI"]  # "https://openrouter.ai/api/v1"  # 添加 base_url
)

response = client.chat.completions.create(
    model=model_info["model_name"],  # "openai/gpt-5",  # deepseek-v4-flash
    messages=[
        # user: 用户角色，代表人类的提问或输入
        # assitent: 助手角色，代表 AI 的回复。在构造多轮对话时，需要手动添加历史回复
        # system: 系统角色，用于设定 AI 的行为规范、角色定位、回复风格等。这是"幕后导演"，用户看不到，但会影响整个对话的基调。
        # {"role": "user", "content": "你好, 请用一句话介绍你自己"}
        {"role": "system", "content": "你是一位专业的 Python 编程导师，擅长用简洁明了的语言解释复杂概念。"},
        {"role": "user", "content": "什么是列表推导式？"}
    ]
)
# print(type(response))
token_consume(response)
print("模型回复：", response.choices[0].message.content)
print(type(response.model_dump_json()), response.model_dump_json())
'''
{
    "id":"d96b8728-b7b5-4f42-925d-ab67ec5cdbed",
    "choices":[
        {
            "finish_reason":"stop",
            "index":0,
            "logprobs":null,
            "message":{
                "content":"你好！我是DeepSeek，由深度求索公司创造的AI助手，免费提供高效、智能的对话、文件处理（支持图像、PDF、Word、Excel等）和联网搜索服务，拥有1M超长上下文，知识截止于2025年5月，致力于为你提供可靠、全面的帮助。",
                "refusal":null,
                "role":"assistant",
                "annotations":null,
                "audio":null,
                "function_call":null,
                "tool_calls":null,
                "reasoning_content":"好的，用户让我用一句话介绍自己。这是一个非常简单的请求，需要简洁明了地概括我的核心身份和功能。我是DeepSeek，由深度求索公司创造，是一个AI助手。关键信息点包括：免费、多平台支持（网页和App）、文件处理能力、长上下文（1M）、知识截止日期和联网搜索选项。需要把这些整合成一句通顺自然的话，避免啰嗦。准备回复。"
            }
        }
    ],
    "created":1782399887,
    "model":"deepseek-v4-flash",
    "object":"chat.completion",
    "moderation":null,
    "service_tier":null,
    "system_fingerprint":"fp_8b330d02d0_prod0820_fp8_kvcache_20260402",
    "usage":{
        "completion_tokens":158,
        "prompt_tokens":12,
        "total_tokens":170,
        "completion_tokens_details":{
            "accepted_prediction_tokens":null,
            "audio_tokens":null,
            "reasoning_tokens":91,
            "rejected_prediction_tokens":null
        },
        "prompt_tokens_details":{
            "audio_tokens":null,
            "cached_tokens":0
        },
        "prompt_cache_hit_tokens":0,
        "prompt_cache_miss_tokens":12
    }
}
'''