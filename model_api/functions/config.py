# 定义工具 schema
'''
&emsp;&emsp;这个 schema 使用 JSON Schema 格式，包含：

- **name**：函数名称（必须与实际函数名一致）

- **description**：函数的作用描述（AI 根据这个描述判断是否调用）

- **parameters**：参数定义（类型、描述、是否必填）

&emsp;&emsp;现在，让我们完整实现 Function Calling 流程：
'''

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的实时天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，例如：北京、上海、深圳"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "温度单位，celsius（摄氏度）或 fahrenheit（华氏度）"
                    }
                },
                "required": ["city"]  # city 是必填参数，unit 是可选参数
            }
        }
    }
]

print("✅ 工具 schema 已定义")