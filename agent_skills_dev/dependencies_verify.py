# 验证核心依赖包
try:
    import langchain
    import dotenv
    import openai
    print(" 所有依赖包安装成功")
    print(f"LangChain 版本: {langchain.__version__}")
except ImportError as e:
    print(f" 依赖包导入失败: {e}")