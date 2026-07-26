import os
import time
import asyncio

from openai import OpenAI, AsyncOpenAI
from dotenv import load_dotenv

from model_api.config import model_platform_info
from model_api.openai_method import conversation as sync_conversation


# 异步客户端
async_client = AsyncOpenAI(
    api_key=model_platform_info["api_key"],
    base_url=model_platform_info["base_url"]["OpenAI"]
)

# 方法1：同步调用（逐个执行）
def sync_batch(questions: list[str]):
    print("=" * 60)
    print("同步调用（逐个执行）")
    print("=" * 60)
    
    start_time = time.time()
    results = []
    
    for question in questions:
        response = sync_conversation(
            messages=[{"role": "user", "content": question}],
            max_tokens=50
        )
        results.append(response.choices[0].message.content)
    
    elapsed = time.time() - start_time
    print(f"完成 {len(questions)} 个请求")
    print(f"耗时：{elapsed:.2f} 秒\n")
    
    return results, elapsed

# 方法2：异步并发调用
async def ask_question_async(question):
    """异步调用单个问题"""
    response = await async_client.chat.completions.create(
        model=model_platform_info["model_name"],
        messages=[{"role": "user", "content": question}],
        max_tokens=50
    )
    return response.choices[0].message.content

async def async_batch(questions: list[str]):
    '''
    **最佳实践**：对于 100 个以上的大批量任务，建议分批执行（如每批 20 个），避免内存占用过高和网络不稳定的影响。
    '''
    print("=" * 60)
    print("异步并发调用")
    print("=" * 60)
    
    start_time = time.time()
    
    # 使用 asyncio.gather 并发执行所有请求
    results = await asyncio.gather(*[ask_question_async(q) for q in questions])
    
    elapsed = time.time() - start_time
    print(f"完成 {len(questions)} 个请求")
    print(f"耗时：{elapsed:.2f} 秒\n")
    
    return results, elapsed


if __name__ == "__main__":
    # 测试问题列表
    questions = [
        "什么是Python？",
        "什么是JavaScript？",
        "什么是Go语言？",
        "什么是Rust？",
        "什么是TypeScript？"
    ]
    # 性能对比
    print("开始性能测试...\n")

    # 同步测试
    sync_results, sync_time = sync_batch(questions)

    # # 异步测试,Jupyter 专用
    # async_results, async_time = await async_batch(questions)

    # 普通python环境使用
    async_results, async_time = asyncio.run(async_batch(questions))

    # 性能提升
    improvement = (sync_time - async_time) / sync_time * 100

    print("=" * 60)
    print("性能对比")
    print("=" * 60)
    print(f"同步调用耗时：{sync_time:.2f} 秒")
    print(f"异步调用耗时：{async_time:.2f} 秒")
    print(f"性能提升：{improvement:.1f}%")
    print(f"\n异步调用使耗时减少了 {sync_time - async_time:.2f} 秒！")