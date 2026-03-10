#!/usr/bin/env python3
"""
Seedream 图片生成 CLI 工具
火山引擎方舟大模型服务平台 - Seedream API
"""
import os
import sys
import argparse
import time
from datetime import datetime

# 添加当前目录到路径，以便导入 seedream-api
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# 尝试导入 SDK
try:
    from volcenginesdkarkruntime import Ark
    from volcenginesdkarkruntime.types.images.images import SequentialImageGenerationOptions, ContentGenerationTool
except ImportError:
    print("错误: 请先安装 volcengine-python-sdk")
    print("运行: pip install volcengine-python-sdk[ark]")
    sys.exit(1)


# 模型映射
MODELS = {
    "5.0-lite": "doubao-seedream-5-0-260128",
    "4.5": "doubao-seedream-4-5-251128",
    "4.0": "doubao-seedream-4-0-250828",
}

# 支持的尺寸
SIZES = {
    "5.0-lite": ["2K", "3K", "1024x1024", "2048x2048", "2304x1728", "1728x2304", "2848x1600", "1600x2848"],
    "4.5": ["2K", "4K", "1024x1024", "2048x2048"],
    "4.0": ["1K", "2K", "4K", "1024x1024"],
}


def get_model_id(model_alias: str) -> str:
    """获取模型 ID"""
    return MODELS.get(model_alias, model_alias)


def generate_images(
    api_key: str,
    prompt: str,
    model: str = "5.0-lite",
    images: list = None,
    size: str = "2K",
    output_format: str = None,
    watermark: bool = False,
    sequential: bool = False,
    max_images: int = 4,
    web_search: bool = False,
    output_dir: str = "./output",
    proxy: str = None,
):
    """生成图片"""
    
    model_id = get_model_id(model)
    
    # 确定输出格式 (只有 5.0-lite 支持 png，其他默认 jpeg 且不传参数)
    if output_format is None:
        output_format = "png" if model == "5.0-lite" else "jpeg"
    
    # 创建客户端
    client_kwargs = {
        "base_url": "https://ark.cn-beijing.volces.com/api/v3",
        "api_key": api_key,
    }
    
    if proxy:
        import httpx
        client_kwargs["http_client"] = httpx.Client(proxy=proxy)
    
    client = Ark(**client_kwargs)
    
    # 构建参数
    params = {
        "model": model_id,
        "prompt": prompt,
        "size": size,
        "watermark": watermark,
        "sequential_image_generation": "auto" if sequential else "disabled",
    }
    
    # 添加图片
    if images:
        params["image"] = images if len(images) > 1 else images[0]
    
    # 添加 output_format (仅 5.0-lite 支持)
    if model == "5.0-lite" and output_format:
        params["output_format"] = output_format
    
    # 添加组图选项
    if sequential:
        params["sequential_image_generation_options"] = SequentialImageGenerationOptions(max_images=max_images)
    
    # 添加联网搜索
    if web_search:
        params["tools"] = [ContentGenerationTool(type="web_search")]
    
    print(f"[Seedream] 使用模型: {model}")
    print(f"[Seedream] 模式: {'组图' if sequential else '单图'}")
    print(f"[Seedream] 提示词: {prompt[:50]}...")
    print(f"[Seedream] 尺寸: {size}")
    print(f"[Seedream] 格式: {output_format}")
    print("[Seedream] 正在生成...")
    
    # 调用 API
    try:
        response = client.images.generate(**params)
    except Exception as e:
        print(f"[Seedream] 错误: {e}")
        sys.exit(1)
    
    # 检查错误
    if hasattr(response, 'error') and response.error:
        print(f"[Seedream] API 错误: {response.error}")
        sys.exit(1)
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 保存图片
    import requests
    timestamp = int(time.time())
    saved_files = []
    
    for i, img in enumerate(response.data):
        if hasattr(img, 'error') and img.error:
            print(f"[Seedream] 图片 {i+1} 生成失败: {img.error}")
            continue
        
        url = img.url if hasattr(img, 'url') else None
        if not url:
            continue
        
        # 生成文件名
        ext = output_format
        filename = f"seedream_{timestamp}_{i+1}.{ext}"
        filepath = os.path.join(output_dir, filename)
        
        # 下载并保存
        try:
            r = requests.get(url)
            r.raise_for_status()
            with open(filepath, 'wb') as f:
                f.write(r.content)
            saved_files.append(filepath)
            size_info = f" ({img.size})" if hasattr(img, 'size') and img.size else ""
            print(f"[Seedream] ✓ 已保存: {filename}{size_info}")
        except Exception as e:
            print(f"[Seedream] ✗ 保存失败: {filename} - {e}")
    
    # 打印使用量
    if hasattr(response, 'usage') and response.usage:
        print(f"[Seedream] 生成图片数: {response.usage.generated_images}")
    
    print(f"[Seedream] 完成! 共生成 {len(saved_files)} 张图片")
    return saved_files


def main():
    parser = argparse.ArgumentParser(
        description="Seedream 图片生成 CLI - 火山引擎方舟大模型服务平台"
    )
    parser.add_argument("--api-key", "-k", help="火山引擎 API Key", default=None)
    parser.add_argument("--prompt", "-p", help="图片描述提示词 (必填)", required=True)
    parser.add_argument(
        "--model", "-m", 
        default="5.0-lite",
        choices=["5.0-lite", "4.5", "4.0"],
        help="模型 (default: 5.0-lite)"
    )
    parser.add_argument(
        "--image", "-i",
        action="append",
        default=[],
        help="输入图片 URL (可多次使用)"
    )
    parser.add_argument(
        "--size", "-s",
        default="2K",
        help="图像尺寸 (default: 2K)"
    )
    parser.add_argument(
        "--output-format", "-f",
        choices=["png", "jpeg"],
        default=None,
        help="输出格式 (默认根据模型自动选择)"
    )
    parser.add_argument(
        "--watermark", "-w",
        action="store_true",
        help="添加水印"
    )
    parser.add_argument(
        "--sequential", "-S",
        action="store_true",
        help="启用组图模式"
    )
    parser.add_argument(
        "--max-images",
        type=int,
        default=4,
        help="最大生成图片数 (default: 4)"
    )
    parser.add_argument(
        "--web-search",
        action="store_true",
        help="启用联网搜索 (仅 5.0-lite)"
    )
    parser.add_argument(
        "--output", "-o",
        default=os.path.expanduser("~/Downloads"),
        help="输出目录 (default: ~/Downloads)"
    )
    parser.add_argument(
        "--proxy", "-x",
        help="代理地址"
    )
    
    args = parser.parse_args()
    
    # 获取 API Key
    api_key = args.api_key or os.getenv("ARK_API_KEY")
    if not api_key:
        print("错误: 请通过 --api-key 参数或设置 ARK_API_KEY 环境变量提供 API Key")
        print("\n获取 API Key: https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey")
        sys.exit(1)
    
    # 生成图片
    generate_images(
        api_key=api_key,
        prompt=args.prompt,
        model=args.model,
        images=args.image if args.image else None,
        size=args.size,
        output_format=args.output_format,
        watermark=args.watermark,
        sequential=args.sequential,
        max_images=args.max_images,
        web_search=args.web_search,
        output_dir=args.output,
        proxy=args.proxy,
    )


if __name__ == "__main__":
    main()
