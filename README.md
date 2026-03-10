# Seedream 图片生成 Skill

基于火山引擎方舟大模型服务平台的 Seedream 图片生成 API 的 OpenClaw/Claude Code Skill。

## 功能

- ✅ 文生图 (Text to Image)
- ✅ 图生图 (Image to Image) - 单图输入
- ✅ 多图融合 (Multi-image to Image) - 多图输入
- ✅ 组图生成 (Sequential Image Generation)
- ✅ 联网搜索 (Web Search) - 仅 5.0 lite

## 安装

### 方式一：使用 npx skills add（推荐）

```bash
npx skills add cyber-max-huang/openclaw-skill-seedream
```

### 方式二：手动安装

```bash
# 1. 克隆仓库
git clone https://github.com/cyber-max-huang/openclaw-skill-seedream.git ~/openclaw-skill-seedream

# 2. 配置 OpenClaw
# 编辑 ~/.openclaw/openclaw.json，添加：
```

```json
{
  "skills": {
    "load": {
      "extraDirs": ["~/openclaw-skill-seedream"]
    }
  }
}
```

### 方式三：作为插件安装

在 Claude Code / OpenClaw 中告诉 AI：

> 请帮我安装 github.com/cyber-max-huang/openclaw-skill-seedream

## 使用

### 直接告诉 AI

只需告诉 AI 你想生成什么图片，例如：
- "帮我生成一只可爱的橘猫图片"
- "生成一张科技感的城市夜景"
- "制作一张北京天气预报图"

AI 会自动调用 Seedream API 生成图片。

### 命令行使用

```bash
# 设置 API Key
export ARK_API_KEY="your-api-key"

# 文生图
python3 ~/openclaw-skill-seedream/.claude/skills/seedream/scripts/seedream.py -p "一只可爱的猫"

# 图生图
python3 ~/openclaw-skill-seedream/.claude/skills/seedream/scripts/seedream.py -p "转为水彩画" -i "input.png"

# 组图
python3 ~/openclaw-skill-seedream/.claude/skills/seedream/scripts/seedream.py -p "四季风景" --sequential --max-images 4
```

## 前置要求

- Python 3.9+
- 火山引擎 API Key
- 安装依赖：`pip3 install volcengine-python-sdk[ark]`

## 获取 API Key

1. 访问[火山引擎控制台](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey)
2. 创建 API Key
3. 开通 Seedream 模型服务

## 支持的模型

| 模型 | 别名 | 支持功能 |
|------|------|----------|
| Seedream 5.0 lite | 5.0-lite | 文生图、图生图、组图、联网搜索、png输出 |
| Seedream 4.5 | 4.5 | 文生图、图生图、组图、jpeg输出 |
| Seedream 4.0 | 4.0 | 文生图、图生图、组图、jpeg输出 |

## 项目结构

```
openclaw-skill-seedream/
├── .claude/
│   └── skills/
│       └── seedream/
│           ├── SKILL.md      # Skill 定义文件
│           └── scripts/
│               └── seedream.py  # CLI 工具
├── README.md
└── CHANGELOG.md
```

## 版本历史

See [CHANGELOG.md](./CHANGELOG.md)

## 许可证

MIT License
