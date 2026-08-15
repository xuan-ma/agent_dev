import math
import json

def calculate_math(expression: str) -> str:
    """安全的数学计算工具，支持基本运算和常用数学函数"""
    # 安全白名单：只允许数学相关的函数和运算符
    allowed_names = {
        "abs": abs, "round": round, "min": min, "max": max,
        "pow": pow, "sum": sum,
        "sqrt": math.sqrt, "log": math.log, "log10": math.log10,
        "sin": math.sin, "cos": math.cos, "tan": math.tan,
        "pi": math.pi, "e": math.e,
    }

    try:
        # 使用 eval 配合白名单，防止代码注入
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return json.dumps({
            "expression": expression,
            "result": result,
            "status": "success"
        }, ensure_ascii=False)
    except Exception as e:
        return json.dumps({
            "expression": expression,
            "error": str(e),
            "status": "failed"
        }, ensure_ascii=False)