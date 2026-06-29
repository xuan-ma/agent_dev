from openai import OpenAI

from utils import api_key
from config import model_info

from fee_info import token_consume

client = OpenAI(
    api_key=api_key,
    base_url=model_info["base_url"]["OpenAI"]  # "https://openrouter.ai/api/v1"  # 添加 base_url
)

response = client.chat.completions.create(
    model=model_info["model_name"],  # "openai/gpt-5",  # deepseek-v4-flash
    messages=[
        # role:
        #   - user: 用户角色，代表人类的提问或输入
        #   - assitent: 助手角色，代表 AI 的回复。在构造多轮对话时，需要手动添加历史回复
        #   - system: 系统角色，用于设定 AI 的行为规范、角色定位、回复风格等。这是"幕后导演"，用户看不到，但会影响整个对话的基调。
        #   - tool: 调用工具, 需指定tool_call_id
        #   - function: 调用函数, 需指定function name
        # {"role": "user", "content": "你好, 请用一句话介绍你自己"}
        {"role": "system", "content": "你是一位专业的 Python 编程导师，擅长用简洁明了的语言解释复杂概念。"},
        {"role": "user", "content": "什么是列表推导式？"}
    ],
    temperature=0.7,
    max_tokens=500,  # 控制模型输出长度
    # max_completion_tokens=  这是控制什么输出
)
# print(type(response))
token_consume(response)
print("模型回复：", response.choices[0].message.content)
print(type(response.model_dump_json()), response.model_dump_json())