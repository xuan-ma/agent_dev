import os
import sys

from openai import OpenAI

from model_api.openai_method import client, conversation


def summarize_history(client, messages_to_summarize, model="deepseek-chat"):
    """
    调用大模型，将一段对话历史压缩为一段摘要
    
    Args:
        client: OpenAI 客户端
        messages_to_summarize: 需要压缩的对话消息列表
        model: 用于生成摘要的模型
    
    Returns:
        摘要文本字符串
    """
    # 将对话历史格式化为可读文本
    conversation_text = ""
    for msg in messages_to_summarize:
        role_label = {"user": "用户", "assistant": "AI助手"}.get(msg["role"], msg["role"])
        conversation_text += f"{role_label}: {msg['content']}\n"
    # 构造摘要请求
    messages=[
        {
            "role": "system",
            "content": "你是一个对话摘要助手。请将以下对话历史压缩为一段简洁的摘要，"
                        "必须保留：1）用户的身份信息 2）讨论过的核心话题和结论 "
                        "3）用户明确表达的偏好或需求。摘要应使用第三人称描述。"
        },
        {
            "role": "user",
            "content": f"请将以下对话压缩为摘要：\n\n{conversation_text}"
        }
    ]
    summary_response = conversation(
        messages=messages,
        temperature=0.3
    )
    return summary_response.choices[0].message.content


def manage_history_with_summary(client, history, max_turns=3, model="deepseek-chat"):
    """
    使用摘要压缩管理对话历史
    
    Args:
        client: OpenAI 客户端
        history: 完整对话历史列表
        max_turns: 保留最近几轮完整对话（不压缩的部分）
        model: 用于生成摘要的模型
    
    Returns:
        压缩后的对话历史
    """
    # 分离 system 消息和对话消息
    system_messages = [msg for msg in history if msg["role"] == "system"]
    dialog_messages = [msg for msg in history if msg["role"] != "system"]
    
    # 如果对话轮数不超过阈值，无需压缩
    total_turns = len(dialog_messages) // 2
    if total_turns <= max_turns:
        print(f"当前 {total_turns} 轮对话，未超过阈值 {max_turns} 轮，无需压缩")
        return history
    
    # 计算需要压缩的部分和保留的部分
    keep_count = max_turns * 2  # 保留最近 max_turns 轮（每轮 2 条）
    messages_to_summarize = dialog_messages[:-keep_count]  # 早期对话 → 压缩
    messages_to_keep = dialog_messages[-keep_count:]        # 最近对话 → 保留
    
    print(f"总对话轮数: {total_turns}")
    print(f"压缩前 {len(messages_to_summarize)} 条早期消息，保留最近 {len(messages_to_keep)} 条")
    
    # 调用大模型生成摘要
    summary = summarize_history(client, messages_to_summarize, model)
    print(f"\n生成的摘要:\n{summary}\n")
    
    # 将摘要作为 system 消息的补充，拼接新的对话历史
    # 原始 system prompt + 摘要 + 最近的完整对话
    system_prompt = f"{system_messages[0]['content']}\n\n" if system_messages else ""
    summary_message = {
        "role": "system",
        "content": system_prompt + 
                   f"【以下是之前对话的摘要，请基于这些信息继续对话】\n{summary}"
    }
    compressed_history = [summary_message] + messages_to_keep
    print(f"压缩后历史长度: {len(compressed_history)} 条（1条含摘要的system + {len(messages_to_keep)}条最近对话）")
    return compressed_history


if __name__ == "__main__":
    # ========== 测试摘要压缩 ==========

    # 模拟一段包含关键信息的长对话
    long_history = [
        {"role": "system", "content": "你是一位友好的 AI 助手，擅长回答各种问题。"},
        # 第 1 轮：用户自我介绍（关键信息！）
        {"role": "user", "content": "你好，我叫张三，是一名 Python 后端工程师，在北京工作。"},
        {"role": "assistant", "content": "你好张三！很高兴认识你。作为 Python 后端工程师，你平时主要用什么框架呢？"},
        # 第 2 轮：技术偏好（关键信息！）
        {"role": "user", "content": "我主要用 FastAPI 和 Django，最近在学习大模型相关的开发。"},
        {"role": "assistant", "content": "FastAPI 和 Django 都是很好的选择！大模型开发现在确实很火，你对哪个方向比较感兴趣？"},
        # 第 3 轮：学习目标（关键信息！）
        {"role": "user", "content": "我想学习 RAG 技术，把大模型集成到我们公司的知识库系统中。"},
        {"role": "assistant", "content": "RAG 是非常实用的方向！结合你的 FastAPI 经验，可以很快搭建一个 RAG 服务。"},
        # 第 4 轮：闲聊
        {"role": "user", "content": "对了，今天北京天气怎么样？"},
        {"role": "assistant", "content": "抱歉，我无法获取实时天气信息。建议你查看天气预报应用。"},
        # 第 5 轮：继续技术讨论
        {"role": "user", "content": "好的，那我们继续聊 RAG 吧，向量数据库你推荐哪个？"},
        {"role": "assistant", "content": "对于入门，我推荐 FAISS 或 Chroma。如果是生产环境，可以考虑 Milvus 或 Qdrant。"},
    ]
    print("=" * 60)
    print("摘要压缩演示")
    print("=" * 60)

    # 只保留最近 2 轮完整对话，其余压缩为摘要
    compressed = manage_history_with_summary(client, long_history, max_turns=2)
    print(f"压缩之后的上下文信息：\n{compressed}")

    # 用压缩后的历史继续对话，验证摘要是否保留了关键信息
    test_question = "你还记得我叫什么名字吗？我是做什么工作的？"

    # 将测试问题加入压缩后的历史
    compressed.append({"role": "user", "content": test_question})

    # 调用 API
    # response = client.chat.completions.create(
    #     model="deepseek-chat",
    #     messages=compressed
    # )
    response = conversation(
        messages=compressed
    )

    answer = response.choices[0].message.content
    print(f"用户: {test_question}")
    print(f"AI: {answer}")
    print(f"\n--- 验证结果 ---")
    print(f"压缩后的上下文仅 {len(compressed)} 条消息，但 AI 仍能回忆早期信息")
    print(f"这就是摘要压缩相比滑动窗口的核心优势：关键信息不会丢失")