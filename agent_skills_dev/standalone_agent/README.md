简化版 LangChain Agent + Skills 系统
适合在 Jupyter Notebook 中使用

使用示例:
    from standalone_agent import scan_skills, initialize_agent, chat

    # 1. 扫描 Skills
    skills_snapshot = scan_skills(Path("./skills"))

    # 2. 初始化 Agent
    agent = initialize_agent(
        api_key="sk-xxx",
        base_url="https://api.deepseek.com",
        model="deepseek-chat",
        skills_dir=Path("./skills")
    )

    # 3. 对话
    response = chat(agent, "查询北京的天气")
    print(response)

    # 4. 流式对话
    async for chunk in chat_stream(agent, "查询北京的天气"):
        print(chunk, end="", flush=True)

依赖版本:
    langchain==1.2.12
    langchain-core==1.2.19
    langchain-deepseek==1.0.1
    pyyaml
    requests
    html2text