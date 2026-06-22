from openai import OpenAI

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"  # 添加 base_url
)

response = client.chat.completions.create(
    model="openai/gpt-5",  # deepseek-v4-flash
    messages=[{"role": "user", "content": "你好"}]
)
print("使用 SDK 的结果：", response.choices[0].message.content)