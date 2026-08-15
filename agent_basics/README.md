# LLM 缺点
| 能力缺口 | 具体表现 | Agent 工具解法 | 对应课程章节 |
|---------|---------|---------------|-------------|
| 无法获取实时信息 | 训练数据有截止日期 | 搜索工具、API 调用工具 | 第二章 Function Calling |
| 无法精确计算 | 大数乘法、复杂公式出错 | 计算器工具、代码执行工具 | 第二章 Function Calling |
| 无法操作外部系统 | 不能读写文件、发送请求 | 文件工具、HTTP 工具 | 第二章 Function Calling、第九章 MCP |
| 无法多步推理验证 | 复杂任务信息遗漏、无法自检 | ReAct 循环、Reflection | 第三章 ReAct、第六章 Reflection |
| 无法跨系统协作 | 单一模型能力有上限 | 多 Agent 协作、A2A 协议 | 第八章 Multi-Agent、第十章 A2A |

# Agent理论模式

## 1. ReAct(TAO)
循环: 
   Thought思考 <------------------------
       |                               |
    任务是否结束 -> Action行动  -> Observation观察
       |
任务结束，输出答案


### papers
- REACT: SYNERGIZING REASONING AND ACTING IN LANGUAGE MODELS
  核心洞察：人类再解决复杂问题时，会交替进行推理和行动
  关键创新：推理追踪Reasoning Trace--让LLM在每次行动前先生成一段推理文本，解释为什么要这样做？这不仅提高了决策的可解释性，还显著提升了任务的成功率。

## 2. Plan & Execute
----
循环：
    Plan 规划

# Agent 核心四要素
## 自主性
## 感知能力
## 推理与规划
## 行动执行

### 参考资料
[LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/)


