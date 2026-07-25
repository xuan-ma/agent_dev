# import io
from typing import List, Dict

from model_api.openai_method import client, conversation
from model_api.image_utils import base64_encode_image


def build_image_url(image_url: str):
    if image_url.startswith("http://") or image_url.startswith("https://"):
        return image_url
    # 处理本地图片
    image_base64 = base64_encode_image(image_url)
    return f"data:image/jpeg;base64,{image_base64}"

def build_messages_with_image(role: str, prompt: str, image_url: str, history_messages:List[Dict]=[]):
    history_messages.append({
        "role": role,  # "user"
        "content": [
            {
                "type": "text", 
                "text": prompt  # "这张图片里有什么？请详细描述。"
            },  
            {
                "type": "image_url",
                "image_url": {"url": build_image_url(image_url)}
            }
        ]
    }) 
    return history_messages


if __name__ == "__main__":
    # 一张公开的图片 URL（示例）
    # image_url = "https://res.cloudinary.com/demo/image/upload/sample.jpg"
    # 本地图像
    image_url = "./model_api/images/sample.jpg"
    messages = build_messages_with_image(
        role="user",
        prompt="这张图片里有什么？请详细描述。",
        image_url=image_url
    )
    print('messages', messages)
    response = conversation(
        messages=messages
    )
    print("AI 对图片的描述：")
    print(response.choices[0].message.content)