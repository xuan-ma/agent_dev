# Function Calling 的完整流程包括以下步骤：

1. 定义工具（tools）：告诉 AI 你有哪些函数可以调用，每个函数的参数是什么
2. 第一次调用 API：AI 分析用户输入，决定是否需要调用函数
3. 检查响应：如果 AI 返回了 `tool_calls`，说明它想调用函数
4. 执行函数：根据 AI 的请求，执行实际的函数调用
5. 第二次调用 API：将函数执行结果返回给 AI
6. AI 生成最终回复：结合函数结果，生成用户可读的回答

 应用场景 | 工具函数示例 | 用途 |
|---------|------------|------|
| **信息查询** | get_weather、search_web、query_database | 查询实时数据、搜索资料 |
| **计算任务** | calculate、solve_equation、convert_unit | 精确计算、单位转换 |
| **数据操作** | create_record、update_user、delete_item | 操作数据库、CRUD 操作 |
| **外部集成** | send_email、create_ticket、post_message | 调用第三方 API、发送通知 |
| **文件操作** | read_file、write_file、list_files | 读写文件、文件管理 |

# 通过 Function Calling，你可以让 AI 从"只会聊天"变成"能做事"的智能助手。例如：
- **客服机器人**：查询订单状态、修改地址、申请退款
- **数据分析助手**：查询数据库、生成报表、发送邮件
- **开发助手**：搜索文档、执行代码、部署应用

# function 定义三要素
## name：工具的唯一标识
## description：决定工具是否被调用
```python
# 黄金模板示例
description = (
    "获取指定城市的当前天气信息，包括气温（摄氏度）、天气状况和湿度。"   # 功能说明
    "当用户询问某个城市的天气、气温、是否需要带伞/穿外套等问题时，"     # 触发条件
    "城市名称应为中文全称，例如：北京、上海、广州。"                    # 输入格式
    "目前仅支持中国大陆主要城市，不支持历史天气和天气预报查询。"         # 能力边界
)
```

## parameters: 参数的JSON Schema定义


# Function Calling 故障问题
## 1. 参数提取错误
## 2. 工具名称注册错误
## 3. 消息拼接错误
### 3.1 tool call id 使用错误
### 3.2 必须先追加 `assistant` 的工具调用消息，再追加 `tool` 的结果消息。如果顺序颠倒，API 会直接报错
## 4. 执行层错误