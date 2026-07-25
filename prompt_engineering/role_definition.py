import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# ❌ 糟糕的提示词
bad_prompt = {"role": "user", "content": "解释一下装饰器"}

# ✅ 优秀的提示词（明确角色）
good_system = """你是一个专业的Python技术导师。
特点：
- 解释简洁易懂，避免术语堆砌
- 提供可运行的代码示例
- 指出常见错误和注意事项
- 语气友好，鼓励学习"""

good_prompt = {"role": "user", "content": "请解释Python装饰器的原理"}

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": good_system},
        good_prompt
    ]
)

print(response.choices[0].message.content)