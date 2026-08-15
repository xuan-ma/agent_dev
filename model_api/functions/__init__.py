from .get_weather import get_weather
from .basics import calculate_math
from .tools_config import tools

# 自动从工具定义生成注册表
def build_tool_registry(tools: list, func_map: dict) -> dict:
    """
    根据工具定义自动构建注册表，确保名称一致

    参数：
        tools: 工具定义列表（JSON Schema）
        func_map: 函数名到函数对象的映射

    返回：
        工具注册表（工具名 -> 函数对象）
    """
    registry = {}
    for tool in tools:
        name = tool["function"]["name"]
        if name in func_map:
            registry[name] = func_map[name]
        else:
            raise ValueError(f"工具 '{name}' 没有对应的函数实现，请检查 func_map")
    return registry

# 函数映射（函数名 -> 函数对象）
FUNC_MAP = {
    "get_weather": get_weather,
    "calculate_math": calculate_math
}

# 自动生成注册表
TOOL_REGISTRY = build_tool_registry(tools, FUNC_MAP)

print(f"✅ 自动生成的注册表：{list(TOOL_REGISTRY.keys())}")