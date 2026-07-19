from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY"), # 这里替换为你的 OpenRouter API Key
)

# 用 Gemini 3 图像生成模型（Nano Banana Pro）
response = client.chat.completions.create(
  model="google/gemini-3-pro-image-preview",
  messages=[
          {
            "role": "user",
            "content": "请生成一张夕阳下群山的风景图片。"
          }
        ],
  extra_body={"modalities": ["image", "text"]}
)

# 提取返回的图像数据（Base64 编码）
response = response.choices[0].message
if response.images:
  for image in response.images:
    image_url = image['image_url']['url'] 
    print(f"Generated image: {image_url[:50]}...")