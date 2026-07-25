# 要求JSON格式输出
system_prompt = """请以JSON格式返回结果，严格遵循以下格式：
{
    "summary": "核心要点（一句话）",
    "steps": ["步骤1", "步骤2", "步骤3"],
    "code_example": "代码示例",
    "common_mistakes": ["常见错误1", "常见错误2"]
}"""

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "如何使用Python读取CSV文件？"}
    ],
    temperature=0  # 确定性输出
)

print(response.choices[0].message.content)