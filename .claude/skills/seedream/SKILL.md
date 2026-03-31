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

# xh-seedream-gen-image（兼容路径）

这是兼容旧目录的 Skill 入口。  
请优先使用仓库根目录的 `SKILL.md` 与 `scripts/seedream.py`。

## 配置 API Key

在 `.env` 中提供 `ARK_API_KEY`：

```bash
ARK_API_KEY=your-volcengine-ark-api-key
```

建议放在仓库根目录 `.env`，并确保该文件不提交到仓库。

## 执行入口

```bash
python3 .claude/skills/seedream/scripts/seedream.py -p "一只可爱的橘猫"
```
