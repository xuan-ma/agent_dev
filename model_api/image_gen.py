from openai import OpenAI

from model_api.openai_method import conversation
from model_api.image_utils import base64_decode_image

# client = OpenAI(
#   base_url="https://openrouter.ai/api/v1",
#   api_key=os.getenv("OPENROUTER_API_KEY"), # 这里替换为你的 OpenRouter API Key
# )

# # 用 Gemini 3 图像生成模型（Nano Banana Pro）
# response = client.chat.completions.create(
#   model="google/gemini-3-pro-image-preview",
#   messages=[
#           {
#             "role": "user",
#             "content": "请生成一张夕阳下群山的风景图片。"
#           }
#         ],
#   extra_body={"modalities": ["image", "text"]}
# )
response = conversation(
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
  # [
  #   {
  #     "type": "iamge_url",
  #     "image_url": f"data:image/png;base64,{base64_encode}"
  #   },
  # ]
  for image in response.images:
    base64_image_url = image['image_url']['url'] 
    # print(f"Generated image: {base64_image_url[:50]}...")
    image = base64_decode_image(base64_image_url)
    image.save("./model_api/images/gen/exercise.png")