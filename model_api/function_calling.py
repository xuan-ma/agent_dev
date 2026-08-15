import json
import sys

from openai

sys.path.append(".")
# from model_api.functions.tools_config import tools
# from model_api.functions.get_weather import get_weather
from model_api.functions import tools, TOOL_REGISTRY
# from model_api.functions import get_weather
from model_api.openai_method import conversation

def execte_tools_serial(tools):
    pass


if __name__ == "__main__":
    # 用户提问
    user_query = "北京现在的天气怎么样？查询完之后帮我计算 111 x 22345 的结果"

    # 初始化消息
    messages = [
        {"role": "system", "content": "你是一个友好的天气助手，可以查询天气信息。"},
        {"role": "user", "content": user_query}
    ]

    print(f"用户: {user_query}\n")

    response = conversation(
        messages=messages,
        tools=tools,
        # auto: AI 自动决定是否调用
        # required: 必须调用至少一个工具，不能直接回答
        # none: 不允许调用任何工具，只能生成文本
        # {type: function, function: ...}：强制调用某个工具
        tool_choice="auto"  # auto/required/none/
    )

    # # 检查 AI 是否想调用函数
    if response.choices[0].message.tool_calls:
        print("AI 决定调用工具：")
        # # 必须先追加 `assistant` 的工具调用消息，再追加 `tool` 的结果消息。如果顺序颠倒，API 会直接报错: 
        # '''
        # Exception: ❌ API 调用失败: Error code: 400 - {'error': {'message': "Messages with role 'tool' must be a response to a preceding message with 'tool_calls'", 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_request_error'}}
        # '''
        # # messages.append(response.choices[0].message.model_dump())  # AI 的工具调用请求
        # print("response.choices[0].message.model_dump()", response.choices[0].message.model_dump())
        # print("response.choices[0].message", response.choices[0].message)
        messages.append(response.choices[0].message)
        # '''
        #     {'content': '', 'refusal': None, 'role': 'assistant', 'annotations': None, 'audio': None, 
        #     'function_call': None, 
        #     'tool_calls': [
        #         {'id': 'call_00_MwxcicUwsq3zASpgZT8i0411', 'function': {'arguments': '{"city": "北京"}', 'name': 'get_weather'}, 'type': 'function', 'index': 0}
        #     ], 
        #     'reasoning_content': "The user asks about Beijing's weather. I'll call get_weather for Beijing."}
        # '''
        for tool_call in response.choices[0].message.tool_calls:
            # 提取工具调用信息, 有没有可能需要同时调用多个工具获取他们的返回结果？那估计得异步调用加速
            # tool_call = response.choices[0].message.tool_calls[0]
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            print(f"  函数名: {function_name}")
            print(f"  参数: {function_args}\n")
            
            # 执行实际的函数调用
            # if function_name in TOOL_REGISTRY:
            function_result = TOOL_REGISTRY[function_name](**function_args)
            print(f"  函数执行结果: {function_result}\n")
            
            # 将函数结果添加到消息历史
            # messages.append(response.choices[0].message)  # AI 的工具调用请求
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": function_result
            })
            
        # 第二次调用：让 AI 根据函数结果生成最终回复
        final_response = conversation(
            messages=messages
        )
        
        final_answer = final_response.choices[0].message.content
        print(f"AI 最终回复: {final_answer}")
        
    else:
        # AI 认为不需要调用工具，直接回复
        print(f"AI 直接回复: {response.choices[0].message.content}")