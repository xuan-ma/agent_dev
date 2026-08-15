# 将 ReAct 理论转换为实际可用的Prompt
react_prompt = """
你在一个由"思考、行动、观察、回答"组成的循环中运行。
在循环的最后，你输出一个答案。

使用"思考"来描述你对所提问题的思考。
使用"行动"来执行你可用的动作之一。
"观察"将是执行这些动作的结果。
"回答"将是分析"观察"结果后得出的答案。

你可用的动作包括：

calculate（计算）:
例如：calculate: 4 * 7 / 3
执行计算并返回数字

wikipedia（维基百科）:
例如：wikipedia: Django
返回从维基百科搜索的摘要

如果有机会，请始终在维基百科上查找信息。

示例会话：

问题：法国的首都是什么？

思考：我应该在维基百科上查找关于法国的信息
行动：wikipedia: France
PAUSE

你然后会收到：

观察：法国是一个国家。首都是巴黎。

思考：我已经找到了答案
回答：法国的首都是巴黎

现在轮到你了：
"""

langchain_react_prompt = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}
"""