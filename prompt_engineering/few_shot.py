import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# ============ Few-Shot Learning 示例 ============
# 任务：情感分类（正面/负面/中性）

messages = [
    # 系统角色定义任务
    {"role": "system", "content": "你是一个情感分析助手。请根据用户输入的文本，判断情感倾向，只输出：正面、负面 或 中性。"},
    
    # ========== Few-Shot 示例开始 ==========
    # 示例 1：正面
    {"role": "user", "content": "这家餐厅的服务太棒了，菜品也很美味！"},
    {"role": "assistant", "content": "正面"},
    
    # 示例 2：负面
    {"role": "user", "content": "等了一个小时外卖还没到，客服态度也很差。"},
    {"role": "assistant", "content": "负面"},
    
    # 示例 3：中性
    {"role": "user", "content": "今天天气一般，不冷也不热。"},
    {"role": "assistant", "content": "中性"},
    # ========== Few-Shot 示例结束 ==========
    
    # 真正需要模型处理的新问题
    {"role": "user", "content": "这个产品质量不错，但是价格有点贵。"}
]

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    temperature=0  # 降低随机性，让分类更稳定
)

print("情感分析结果：", response.choices[0].message.content)