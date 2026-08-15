import json
import os

import requests

def get_weather(city: str, unit: str = "celsius") -> str:
    """
    获取指定城市的天气信息（Mock 函数，实际应调用天气 API）
    
    Args:
        city: 城市名称
        unit: 温度单位（celsius 或 fahrenheit）
    
    Returns:
        天气信息的 JSON 字符串
    """
    # 模拟天气数据
    weather_data = {
        "北京": {"temperature": 15, "condition": "晴天", "humidity": 45},
        "上海": {"temperature": 20, "condition": "多云", "humidity": 60},
        "深圳": {"temperature": 28, "condition": "小雨", "humidity": 75},
    }
    
    # 检查城市是否存在于模拟数据中
    if city in weather_data:
        data = weather_data[city]
        # 如果单位为华氏度，则进行温度单位转换
        if unit == "fahrenheit":
            data["temperature"] = int(data["temperature"] * 9/5 + 32)
        
        # 返回包含详细天气信息的 JSON 字符串
        return json.dumps({
            "city": city,
            "temperature": data["temperature"],
            "unit": unit,
            "condition": data["condition"],
            "humidity": data["humidity"]
        }, ensure_ascii=False)
    else:
        # 若城市未在数据中定义，返回错误信息
        return json.dumps({"error": f"未找到 {city} 的天气数据"}, ensure_ascii=False)

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "你的_tavily_api_key")

# ==========================================
# 1. 本地真正的工具函数执行逻辑：调用 Tavily API
# ==========================================
def get_weather_v2(query: str) -> str:
    """
    使用 Tavily 搜索天气信息的底层真实函数
    """
    print(f"\n🌍 [Tool 执行中] 正在通过 Tavily 搜索: {query} ...")
    
    url = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "basic",     # 基础搜索速度更快
        "include_answer": True,      # 让 Tavily 尝试直接提取简短回答
        "max_results": 3             # 只要前 3 个最相关的网页结果
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        # 提取有价值的信息返回给大模型（优先返回 Tavily 的总结内容）
        result_text = data.get("answer", "")
        if not result_text:
            # 如果没有直接 answer，就把搜索到的 snippet 组装起来
            snippets = [result["content"] for result in data.get("results", [])]
            result_text = "\n".join(snippets)
        return json.dumps({"status": "success", "search_result": result_text},ensure_ascii=False)
    else:
        return json.dumps({"status": "error", "message": f"Tavily API 请求失败: {response.text}"})


if __name__ == "__main__":
    # 测试函数
    print("测试天气查询函数：")
    print(get_weather("北京"))
    print(get_weather("上海", "fahrenheit"))