from openai import OpenAI

from config import model_info
from utils import api_key

# TODO
# 配置阿里云DashScope客户端
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"), # 确保 .env 文件中有 DASHSCOPE_API_KEY
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

def get_embedding(text, model="text-embedding-v3"):
    """
    获取文本的 Embedding 向量
    Args:
        text: 输入文本
        model: 模型名称，默认使用 Qwen 的 text-embedding-v3
    """
    response = client.embeddings.create(
        model=model,
        input=text,
        dimensions=1024, # 可选参数：指定输出维度 (64, 512, 768, 1024)
        encoding_format="float"
    )
    return response.data[0].embedding

# 测试文本
text = "通义千问是阿里云推出的一个超大规模语言模型。"

# 获取向量
embedding = get_embedding(text)

# 打印结果信息
print(f"模型: text-embedding-v3 (Qwen系列)")
print(f"文本: {text}")
print(f"向量维度: {len(embedding)}")
print(f"前10位数值: {embedding[:10]}")