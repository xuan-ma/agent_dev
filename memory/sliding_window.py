from typing import List, Dict

from model_api.utils import print_conversation_maessages

def run(history: List[Dict], max_turns: int=5):
    """
    使用滑动窗口管理对话历史
    
    Args:
        history: 对话历史列表
        max_turns: 保留的最大对话轮数（不包括 system 消息）
    
    Returns:
        压缩后的对话历史
    """
    # 提取 system 消息（通常是第一条）
    system_messages = [msg for msg in history if msg["role"] == "system"]
    
    # 提取对话消息（user 和 assistant）
    dialog_messages = [msg for msg in history if msg["role"] != "system"]
    
    # 只保留最近 max_turns 轮对话（每轮包含 user + assistant）
    # 每轮 = 2 条消息，所以保留 max_turns * 2 条
    recent_messages = dialog_messages[-(max_turns * 2):]
    
    # 重新组合：system + 最近的对话
    return system_messages + recent_messages



if __name__ == "__main__":
    # 示例：模拟一个很长的对话历史
    long_history = [
        {"role": "system", "content": "你是 AI 助手"},
        {"role": "user", "content": "第1轮用户消息"},
        {"role": "assistant", "content": "第1轮AI回复"},
        {"role": "user", "content": "第2轮用户消息"},
        {"role": "assistant", "content": "第2轮AI回复"},
        {"role": "user", "content": "第3轮用户消息"},
        {"role": "assistant", "content": "第3轮AI回复"},
        {"role": "user", "content": "第4轮用户消息"},
        {"role": "assistant", "content": "第4轮AI回复"},
        {"role": "user", "content": "第5轮用户消息"},
        {"role": "assistant", "content": "第5轮AI回复"},
    ]

    # 只保留最近 2 轮
    compressed_history = run(long_history, max_turns=2)

    print("原始历史长度:", len(long_history))
    print("压缩后长度:", len(compressed_history))
    print("\n压缩后的内容:")
    # for msg in compressed_history:
    #     print(f"  [{msg['role']}] {msg['content']}")
    print_conversation_maessages(compressed_history)