#!/usr/bin/env python3
"""
xh-seedream-gen-image CLI
火山引擎方舟 Seedream 图片生成工具
"""
import argparse
import os
import sys
import time
from pathlib import Path

try:
    from volcenginesdkarkruntime import Ark
    from volcenginesdkarkruntime.types.images.images import (
        ContentGenerationTool,
        SequentialImageGenerationOptions,
    )
except ImportError:
    print("错误: 缺少依赖 volcengine-python-sdk[ark]")
    print("请先执行: pip install -r requirements.txt")
    sys.exit(1)


MODELS = {
    "5.0-lite": "doubao-seedream-5-0-260128",
    "4.5": "doubao-seedream-4-5-251128",
    "4.0": "doubao-seedream-4-0-250828",
}

ROOT_DIR = Path(__file__).resolve().parents[1]
ENV_FILES = [
    ROOT_DIR / ".env",
    Path.home() / ".openclaw" / ".env",
    Path.home() / ".claude" / ".env",
]


def load_env_file(path: Path) -> dict:
    env_vars = {}
    if not path.exists():
        return env_vars
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                env_vars[key.strip()] = value.strip().strip('"').strip("'")
    except Exception:
        pass
    return env_vars


def resolve_api_key(cli_api_key: str | None) -> str | None:
    if cli_api_key:
        return cli_api_key
    for env_file in ENV_FILES:
        env_vars = load_env_file(env_file)
        if env_vars.get("ARK_API_KEY"):
            return env_vars["ARK_API_KEY"]
    return os.getenv("ARK_API_KEY")


def get_model_id(model_alias: str) -> str:
    return MODELS.get(model_alias, model_alias)


def generate_images(
    api_key: str,
    prompt: str,
    model: str = "5.0-lite",
    images: list | None = None,
    size: str = "2K",
    output_format: str | None = None,
    watermark: bool = False,
    sequential: bool = False,
    max_images: int = 4,
    web_search: bool = False,
    output_dir: str = str(Path.home() / "Downloads"),
    proxy: str | None = None,
):
    model_id = get_model_id(model)
    if output_format is None:
        output_format = "png" if model == "5.0-lite" else "jpeg"

    client_kwargs = {
        "base_url": "https://ark.cn-beijing.volces.com/api/v3",
        "api_key": api_key,
    }
    if proxy:
        import httpx

        client_kwargs["http_client"] = httpx.Client(proxy=proxy)

    client = Ark(**client_kwargs)
    params = {
        "model": model_id,
        "prompt": prompt,
        "size": size,
        "watermark": watermark,
        "sequential_image_generation": "auto" if sequential else "disabled",
    }

    if images:
        params["image"] = images if len(images) > 1 else images[0]
    if model == "5.0-lite" and output_format:
        params["output_format"] = output_format
    if sequential:
        params["sequential_image_generation_options"] = SequentialImageGenerationOptions(
            max_images=max_images
        )
    if web_search:
        params["tools"] = [ContentGenerationTool(type="web_search")]

    print(f"[xh-seedream-gen-image] 模型: {model}")
    print(f"[xh-seedream-gen-image] 提示词: {prompt[:60]}...")
    print("[xh-seedream-gen-image] 正在生成...")

    try:
        response = client.images.generate(**params)
    except Exception as e:
        print(f"[xh-seedream-gen-image] 请求失败: {e}")
        sys.exit(1)

    if hasattr(response, "error") and response.error:
        print(f"[xh-seedream-gen-image] API 错误: {response.error}")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    import requests

    timestamp = int(time.time())
    saved_files = []
    for i, img in enumerate(response.data):
        if hasattr(img, "error") and img.error:
            print(f"[xh-seedream-gen-image] 图片 {i + 1} 生成失败: {img.error}")
            continue
        url = img.url if hasattr(img, "url") else None
        if not url:
            continue
        filename = f"seedream_{timestamp}_{i + 1}.{output_format}"
        filepath = os.path.join(output_dir, filename)
        try:
            r = requests.get(url, timeout=120)
            r.raise_for_status()
            with open(filepath, "wb") as f:
                f.write(r.content)
            saved_files.append(filepath)
            print(f"[xh-seedream-gen-image] 已保存: {filepath}")
        except Exception as e:
            print(f"[xh-seedream-gen-image] 保存失败: {filename} - {e}")

    print(f"[xh-seedream-gen-image] 完成，共 {len(saved_files)} 张图片")
    return saved_files


def main():
    parser = argparse.ArgumentParser(description="xh-seedream-gen-image CLI")
    parser.add_argument("--api-key", "-k", default=None, help="火山引擎 ARK API Key")
    parser.add_argument("--prompt", "-p", required=True, help="图片提示词")
    parser.add_argument(
        "--model",
        "-m",
        default="5.0-lite",
        choices=["5.0-lite", "4.5", "4.0"],
        help="模型版本",
    )
    parser.add_argument("--image", "-i", action="append", default=[], help="输入图片 URL")
    parser.add_argument("--size", "-s", default="2K", help="图像尺寸")
    parser.add_argument(
        "--output-format",
        "-f",
        choices=["png", "jpeg"],
        default=None,
        help="输出格式",
    )
    parser.add_argument("--watermark", "-w", action="store_true", help="添加水印")
    parser.add_argument("--sequential", "-S", action="store_true", help="启用组图模式")
    parser.add_argument("--max-images", type=int, default=4, help="组图最大数量")
    parser.add_argument("--web-search", action="store_true", help="启用联网搜索")
    parser.add_argument(
        "--output",
        "-o",
        default=str(Path.home() / "Downloads"),
        help="输出目录",
    )
    parser.add_argument("--proxy", "-x", default=None, help="HTTP 代理地址")
    args = parser.parse_args()

    api_key = resolve_api_key(args.api_key)
    if not api_key:
        print("错误: 未找到 ARK_API_KEY。")
        print("请在以下任一位置配置：")
        print(f"1) {ROOT_DIR / '.env'}")
        print(f"2) {Path.home() / '.openclaw' / '.env'}")
        print(f"3) {Path.home() / '.claude' / '.env'}")
        print("或通过 --api-key 传入。")
        sys.exit(1)

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
