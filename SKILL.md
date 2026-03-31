---
name: xh-seedream-gen-image
description: 使用火山引擎方舟 Seedream 生成图片，支持文生图、图生图、组图与联网搜索（5.0-lite）。
emoji: 🎨
tags:
  - image-generation
  - seedream
  - volcengine
  - openclaw
---

# xh-seedream-gen-image

面向 OpenClaw 的 Seedream 图片生成技能。  
你只需要描述想要的图片内容，我会调用脚本完成生成并保存到本地目录。

## 你可以这样说

- 生成一张赛博朋克城市夜景，霓虹灯风格
- 把这张参考图改成水彩风格（并附上图片 URL）
- 生成 4 张连贯的四季海报
- 生成今日北京天气信息图（开启联网搜索）

## API Key 配置（必须）

将 `ARK_API_KEY` 写入 `.env` 文件，推荐顺序如下：

1. `<skill根目录>/.env`（推荐）
2. `~/.openclaw/.env`
3. `~/.claude/.env`

示例：

```bash
ARK_API_KEY=your-volcengine-ark-api-key
```

## 运行方式（供 Agent 调用）

```bash
python3 scripts/seedream.py -p "一只可爱的橘猫"
```

常用参数：

- `-p, --prompt`：提示词（必填）
- `-m, --model`：`5.0-lite` / `4.5` / `4.0`
- `-i, --image`：输入图片 URL（可重复传入多张）
- `--sequential --max-images 4`：启用组图
- `--web-search`：启用联网搜索（推荐用于实时信息图）
- `-o, --output`：输出目录（默认 `~/Downloads`）

## 依赖

```bash
pip install -r requirements.txt
```

> 说明：该技能默认使用 `scripts/seedream.py` 作为执行入口。
