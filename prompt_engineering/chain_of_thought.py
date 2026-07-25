# 让AI展示推理过程
prompt = """请一步步分析以下问题：
问题：一个班级有30名学生，其中60%是女生。如果再加入5名男生，女生占比是多少？

请按以下格式作答：
1. 理解题意：...
2. 计算原始数据：...
3. 计算新数据：...
4. 得出结论：...
"""

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": prompt}],
    temperature=0
)

print(response.choices[0].message.content)