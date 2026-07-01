import time

from openai import OpenAI, Stream, types

# from utils import api_key
from config import model_platform_info
from fee_info import token_consume


def chat():
    pass


def safe_chat():
    pass


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
        # types.chat.chat_completion_chunk.ChatCompletionChunk
        # print(type(chunk)) 
        # 提取增量内容
        delta_content = chunk.choices[0].delta.content
        
        if delta_content:
            print(delta_content, end="", flush=True)  # 实时打印，不换行
            full_content += delta_content
            time.sleep(0.1)  # 模拟打字机效果（可选）

    print("\n\n✅ 流式输出完成")
    return full_content

client = OpenAI(
    api_key=model_platform_info["api_key"],
    base_url=model_platform_info["base_url"]["OpenAI"]  # 添加 base_url
)

response = client.chat.completions.create(
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
        {"role": "user", "content": "什么是列表推导式？"}
    ],
    # temperature = 0：输出最确定，每次运行结果几乎相同，适合需要稳定输出的场景
    # temperature = 0.7（默认值）：平衡了创造性和稳定性，适合大多数场景
    # temperature >= 1.5：输出高度随机和创造性，适合创意写作、头脑风暴
    temperature=0.7,
    # max_tokens=500,  # 控制模型输出长度
    # max_completion_tokens=  这是控制什么输出
    stream=True  # 开启流式输出
)
stream_output(response)


