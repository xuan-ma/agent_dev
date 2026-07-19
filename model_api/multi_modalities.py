import io
import base64
from typing import List, Dict

from PIL import Image

from model_api.openai_method import client, conversation

def compress_image(image_path, max_size=(800, 800)):
    """压缩图片到合适大小"""
    with Image.open(image_path) as img:
        # 保持宽高比缩放
        img.thumbnail(max_size)
        
        # 保存为JPEG并压缩
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=85)
        
        # 编码为base64
        return base64.b64encode(buffer.getvalue()).decode('utf-8')

def build_image_url(image_url: str):
    if image_url.startswith("http://") or image_url.startswith("https://"):
        return image_url
    # 处理本地图片
    image_base64 = compress_image(image_url)
    return f"data:image/jpeg;base64,{image_base64}"

def build_messages_with_image(role: str, prompt: str, image_url: str, history_messages:List[Dict]=[]):
    history_messages.append({
        "role": role,  # "user"
        "content": [
            {
                "type": "text", 
                "text": prompt},  # "这张图片里有什么？请详细描述。"
            {
                "type": "image_url",
                "image_url": {"url": image_url}
            }
        ]
    }) 
    return history_messages


# 构造包含图片的消息
# response = client.chat.completions.create(
#     model="openai/gpt-4o",  # 使用支持视觉的模型
#     messages=[
#         {
#             "role": "user",
#             "content": [
#                 {"type": "text", "text": "这张图片里有什么？请详细描述。"},
#                 {
#                     "type": "image_url",
#                     "image_url": {"url": image_url}
#                 }
#             ]
#         }
#     ],
#     max_tokens=500
# )

# print("AI 对图片的描述：")
# print(response.choices[0].message.content)


# # 方法2：使用base64编码本地图片
# print("=" * 60)
# print("方法2：通过base64编码传递本地图片")
# print("=" * 60)


# def compress_image(image_path, max_size=(800, 800)):
#     """压缩图片到合适大小"""
#     with Image.open(image_path) as img:
#         # 保持宽高比缩放
#         img.thumbnail(max_size)
        
#         # 保存为JPEG并压缩
#         buffer = io.BytesIO()
#         img.save(buffer, format='JPEG', quality=85)
        
#         # 编码为base64
#         return base64.b64encode(buffer.getvalue()).decode('utf-8')

# # 使用压缩后的图片
# b64_image = compress_image("/Users/mac/大模型资料/大模型基础入门/images/zhipu_model_plaza.png")
# print(f"压缩后大小: {len(b64_image)/1024:.2f} KB")  # 确保 <500KB

# # ✅ 这样更有可能成功
# messages=[{
#     "role": "user",
#     "content": [
#         {"type": "text", "text": "描述图片"},
#         {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}}
#     ]
# }]

# response = client.chat.completions.create(
#     model="openai/gpt-4o",
#     messages=messages,
#     max_tokens=100
# )

# print(f"AI回复：{response.choices[0].message.content}")

if __name__ == "__main__":
    # 一张公开的图片 URL（示例）
    image_url = "https://upload.wikimedia.org/wikipedia/commons/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
    messages = build_messages_with_image(
        "user",
        "这张图片里有什么？请详细描述。",
        image_url
    )
    response = conversation(
        messages=messages
    )
    print("AI 对图片的描述：")
    print(response.choices[0].message.content)