

from openai import OpenAI

from model_api.openai_method import client
from model_api.config import model_platform_info


'''
和Chat Completions API 主要差异点：
    1. 服务端状态管理 - 通过 previous_response_id 自动维护对话历史
    2. 内置工具支持 - Web搜索、文件搜索、计算机操作等
    3. 事件驱动架构 - 更可预测的流式响应
    4. 简化的 agentic 工作流 - 专为 AI Agent 设计
'''


# 初始化客户端
client = OpenAI()  # 确保设置了 OPENAI_API_KEY 环境变量

# ============================================================
# 示例2: Responses API (新方式)
# 服务端自动管理对话状态，通过 previous_response_id 引用
# ============================================================
print("\n" + "=" * 60)
print("【Responses API - 新方式】")
print("=" * 60)

# 第一轮对话 - 开启服务端存储
response1 = client.responses.create(
    model=model_platform_info["model_name"],  # "gpt-5-nano",
    input="我叫小红，请记住我的名字",
    store=True  # 🔑 关键: 启用服务端状态存储
)
print(f"用户: 我叫小红，请记住我的名字")
print(f"助手: {response1.output_text}")
print(f"📦 Response ID: {response1.id}")  # 用于后续引用

# 第二轮对话 - 使用 previous_response_id 自动关联上下文
response2 = client.responses.create(
    model=model_platform_info["model_name"],
    input="你还记得我叫什么名字吗？",
    previous_response_id=response1.id,  # 🔑 关键: 引用之前的响应
    store=True
)
print(f"\n用户: 你还记得我叫什么名字吗？")
print(f"助手: {response2.output_text}")
print(f"\n✅ 无需手动管理消息历史，服务端自动维护!")


# ============================================================
# 示例3: Responses API 内置工具 (Web Search)
# Chat Completions API 不支持此功能
# ============================================================
print("\n" + "=" * 60)
print("【Responses API - 内置 Web Search 工具】")
print("=" * 60)

response_search = client.responses.create(
    model="gpt-5-nano",
    input="今天的比特币价格是多少？",
    tools=[{"type": "web_search_preview"}]  # 🔑 内置工具
)
print(f"用户: 今天的比特币价格是多少？")
print(f"助手: {response_search.output_text}")
print(f"\n🔍 Chat Completions API 需要手动实现搜索功能，")
print(f"   Responses API 直接内置 web_search_preview 工具!")


