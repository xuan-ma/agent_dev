# 定义工具 schema
'''
使用 JSON Schema 格式，包含：
- name：函数名称（必须与实际函数名一致）
- description：函数的作用描述（AI 根据这个描述判断是否调用）
- parameters：参数定义（类型、描述、是否必填）
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
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_math",
            "description": (
                "执行数学计算，支持加减乘除、幂运算、三角函数、对数等。"  # 功能说明
                "当用户需要精确计算数学表达式时调用此工具。"  # 触发条件
                "输入应为合法的 Python 数学表达式，例如：'2**10'、'sqrt(144)'。"  # 输入格式
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "要计算的数学表达式，使用 Python 语法"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

print("✅ 工具 schema 已定义")