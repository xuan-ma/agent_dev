import json

from model_api.functions.tools_config import tools
from model_api.functions.get_weather import get_weather
from model_api.openai_method import conversation

# # 创建客户端
# client = OpenAI(
#     api_key=os.getenv("DEEPSEEK_API_KEY"),
#     base_url="https://api.deepseek.com"
# )

# 用户提问
user_query = "北京现在的天气怎么样？"

# 初始化消息
messages = [
    {"role": "system", "content": "你是一个友好的天气助手，可以查询天气信息。"},
    {"role": "user", "content": user_query}
]

print(f"用户: {user_query}\n")

# 第一次调用：让 AI 决定是否需要调用工具
# response = client.chat.completions.create(
#     model="deepseek-chat",
#     messages=messages,
#     tools=tools,  # 传递工具定义
#     tool_choice="auto"  # auto: AI 自动决定是否调用；也可以设为 "none" 或强制调用某个工具
# )
response = conversation(
    history_conversations=messages,
    tools=tools
)

# 检查 AI 是否想调用函数
if response.choices[0].message.tool_calls:
    print("AI 决定调用工具：")
    
    # 提取工具调用信息, 有没有可能需要同时调用多个工具获取他们的返回结果？那估计得异步调用加速
    tool_call = response.choices[0].message.tool_calls[0]
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments)
    
    print(f"  函数名: {function_name}")
    print(f"  参数: {function_args}\n")
    
    # 执行实际的函数调用
    if function_name == "get_weather":
        function_result = get_weather(**function_args)
        print(f"函数执行结果: {function_result}\n")
        
        # 将函数结果添加到消息历史
        messages.append(response.choices[0].message)  # AI 的工具调用请求
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": function_result
        })
        
        # 第二次调用：让 AI 根据函数结果生成最终回复
        # final_response = client.chat.completions.create(
        #     model="deepseek-chat",
        #     messages=messages
        # )
        final_response = conversation(
            history_conversations=messages
        )
        
        final_answer = final_response.choices[0].message.content
        print(f"AI 最终回复: {final_answer}")
    
else:
    # AI 认为不需要调用工具，直接回复
    print(f"AI 直接回复: {response.choices[0].message.content}")