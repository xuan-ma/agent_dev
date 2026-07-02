import time
import traceback
from typing import Union, Dict, List

from openai import OpenAI, Stream, types
from openai import (
    AuthenticationError,  # 认证错误（API Key 无效）
    RateLimitError,       # 速率限制错误（请求过快）
    APIConnectionError,   # 网络连接错误
    APIError              # 通用 API 错误
)

# from utils import api_key
from config import model_platform_info
from fee_info import token_consume


client: types.chat.chat_completion.ChatCompletion = OpenAI(
    api_key=model_platform_info["api_key"],
    base_url=model_platform_info["base_url"]["OpenAI"]  # 添加 base_url
)

def convert_to_user_message(user_prompt: str) -> Dict:
    return {"role": "user", "content": user_prompt}

def convert_to__system_message(system_prompt: str) -> Dict:
    return {"role": "system", "content": system_prompt}


def call_model(
        chat_client: types.chat.chat_completion.ChatCompletion, 
        user_prompt: str,
        system_prompt: str="",
        history_conversions: List[Dict]=[],
        stream: bool=False
    ) -> types.chat.chat_completion.ChatCompletion | Stream:
    return client.chat.completions.create(
        model=model_platform_info["model_name"],  # "openai/gpt-5",  # deepseek-v4-flash
        messages=[
            # role:
            #   - user: 用户角色，代表人类的提问或输入
            #   - assitent: 助手角色，代表 AI 的回复。在构造多轮对话时，需要手动添加历史回复
            #   - system: 系统角色，用于设定 AI 的行为规范、角色定位、回复风格等。这是"幕后导演"，用户看不到，但会影响整个对话的基调。
            #   - tool: 调用工具, 需指定tool_call_id
            #   - function: 调用函数, 需指定function name
            # {"role": "user", "content": "你好, 请用一句话介绍你自己"}
            {"role": "system", "content": "你是一位专业的 Python 编程导师，擅长用简洁明了的语言解释复杂概念。"},
            {"role": "user", "content": user_prompt}  # "什么是列表推导式？"
        ],
        # temperature = 0：输出最确定，每次运行结果几乎相同，适合需要稳定输出的场景
        # temperature = 0.7（默认值）：平衡了创造性和稳定性，适合大多数场景
        # temperature >= 1.5：输出高度随机和创造性，适合创意写作、头脑风暴
        temperature=0.7,
        # max_tokens=500,  # 控制模型输出长度
        # max_completion_tokens=  这是控制什么输出
        stream=stream  # 开启流式输出
    )


def safe_call_model(
        user_prompt: str, 
        chat_client: types.chat.chat_completion.ChatCompletion, 
        max_retries: int=3
    ): 
    # 循环尝试 API 调用，最多重试 max_retries 次
    for attempt in range(max_retries):
        try:
            # 发起 API 调用
            response = chat_client.chat.completions.create(
                model=model_platform_info["model_name"],
                messages=[
                    {"role": "user", "content": user_prompt}
                ],
                timeout=30.0  # 设置超时时间（秒）
            )
            return response.choices[0].message.content
        except AuthenticationError as e:
            # 认证错误，无需重试
            return f"❌ API Key 无效或已过期，请检查环境变量配置"
        except RateLimitError as e:
            # 速率限制，等待后重试
            wait_time = 2 ** attempt  # 指数退避：1秒、2秒、4秒...
            print(f"⚠️ 请求过快，等待 {wait_time} 秒后重试...")
            time.sleep(wait_time)
            continue
        except APIConnectionError as e:
            # 网络错误，重试
            print(f"⚠️ 网络连接失败（第 {attempt+1}/{max_retries} 次），重试中...")
            time.sleep(1)
            continue
        except APIError as e:
            # 通用 API 错误
            return f"❌ API 调用失败: {str(e)}"
        except Exception as e:
            # 其他未知错误
            traceback.print_exc()
            return f"❌ 未知错误: {str(e)}"
    
    return f"❌ 重试 {max_retries} 次后仍然失败，请检查网络或稍后再试"


def stream_chat():
    pass


def normal_output(response: types.chat.chat_completion.ChatCompletion) -> str:
    token_consume(response)
    print("模型回复：", response.choices[0].message.content)
    # print(type(response.model_dump_json()), response.model_dump_json())
    finish_reason = response.choices[0].finish_reason
    # 判断是否因达到 token 上限而导致内容未生成完毕
    if finish_reason == "length":
        print("\n⚠️ 输出被截断！考虑增加 max_tokens")


def stream_output(response: Stream) -> str:
    '''
    流式输出特别适合以下场景：
        - 聊天机器人：用户看到逐字生成，体验更自然
        - 长文本生成：用户可以边看边等，不会觉得卡顿
        - 交互式应用：用户可以在生成过程中判断是否继续等待

    注意：流式模式下无法直接获取 `usage` 信息（Token 统计），如果需要统计成本，建议在非流式模式下测试，或使用第1.1节介绍的 tiktoken 本地估算。
    '''
    # 用于保存完整内容
    full_content = ""  
    # 逐块接收并打印
    for chunk in response:
        # print(type(chunk)) # types.chat.chat_completion_chunk.ChatCompletionChunk
        # 提取增量内容
        delta_content = chunk.choices[0].delta.content
        
        if delta_content:
            print(delta_content, end="", flush=True)  # 实时打印，不换行
            full_content += delta_content
            time.sleep(0.1)  # 模拟打字机效果（可选）

    print("\n\n✅ 流式输出完成")
    return full_content

def conversation(
        
    ) -> str:
    pass

def multi_conversations(chat_client):
    # 初始化对话历史
    conversation_history = [
        {"role": "system", "content": "你是一位友好的 AI 助手，擅长回答各种问题。"}
    ]

    # # 创建客户端
    # client = OpenAI(
    #     api_key=os.getenv("DEEPSEEK_API_KEY"),
    #     base_url="https://api.deepseek.com"
    # )

    # 第一轮对话
    user_message_1 = "我叫张三，今年25岁"
    conversation_history.append({"role": "user", "content": user_message_1})

    # 调用 API 获取第一轮对话回复
    response_1 = client.chat.completions.create(
        model="deepseek-chat",
        messages=conversation_history
    )

    # 提取并保存 AI 的回复内容
    assistant_message_1 = response_1.choices[0].message.content

    # 将 AI 的回复添加到对话历史中，以维持上下文连贯性
    conversation_history.append({"role": "assistant", "content": assistant_message_1})

    # 打印第一轮对话的用户输入和 AI 回复
    print(f"用户: {user_message_1}")
    print(f"AI: {assistant_message_1}\n")

    # 第二轮对话（测试是否记住了用户信息）
    user_message_2 = "我叫什么名字？"
    conversation_history.append({"role": "user", "content": user_message_2})

    # 调用 API 获取第二轮对话回复
    response_2 = client.chat.completions.create(
        model="deepseek-chat",
        messages=conversation_history
    )

    # 提取并保存 AI 的回复内容
    assistant_message_2 = response_2.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": assistant_message_2})

    print(f"用户: {user_message_2}")
    print(f"AI: {assistant_message_2}\n")

    # 查看完整的对话历史
    print("=" * 60)
    print("完整对话历史：")
    print("=" * 60)
    for i, msg in enumerate(conversation_history):
        print(f"{i}. [{msg['role']}] {msg['content']}")


if __name__ == "__main__":

    stream_output(response)


