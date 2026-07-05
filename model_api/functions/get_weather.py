import json

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

if __name__ == "__main__":
    # 测试函数
    print("测试天气查询函数：")
    print(get_weather("北京"))
    print(get_weather("上海", "fahrenheit"))