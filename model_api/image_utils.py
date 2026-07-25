import base64
import io

from PIL import Image

def base64_encode_image(image_path, max_size=(800, 800)) -> str:
    """压缩图片到合适大小"""
    with Image.open(image_path) as img:
        # 保持宽高比缩放
        img.thumbnail(max_size)
        
        # 保存为JPEG并压缩
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=85)
        
        # 编码为base64
        return base64.b64encode(buffer.getvalue()).decode('utf-8')
    
def base64_decode_image(base64_str: str) -> Image:
    # 去掉前缀
    if base64_str.startswith("data:image"):
        base64_str = base64_str.split(",")[1]
    # 解码为二进制数据
    image_data = base64.b64decode(base64_str)
    # 用 BytesIO 包装成文件流，然后打开为 PIL Image
    image = Image.open(io.BytesIO(image_data))
    print(f"✅ 图像尺寸: {image.size}, 格式: {image.format}")
    return image
