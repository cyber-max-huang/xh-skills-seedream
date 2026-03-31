# xh-seedream-gen-image

适用于 OpenClaw 的 Seedream 图片生成技能，支持：

- 文生图
- 图生图（单图 / 多图）
- 组图生成（Sequential）
- 联网搜索（仅 `5.0-lite`）

技能名固定为：`xh-seedream-gen-image`。

## 1) 通过 npx-skill 安装

> 将下面地址替换为你的仓库地址（示例使用 GitHub）。

```bash
npx-skill add github:<your-org-or-user>/xh-seedream-gen-image
```

如果你的 `npx-skill` 版本使用的是 `install` 子命令，可用：

```bash
npx-skill install github:<your-org-or-user>/xh-seedream-gen-image
```

安装后应能看到技能元信息文件：`SKILL.md`（在技能根目录）。

## 2) 配置 API Key（必须在 .env 提供）

请在 `.env` 文件中提供 `ARK_API_KEY`，推荐放在技能根目录：

```bash
ARK_API_KEY=your-volcengine-ark-api-key
```

脚本读取优先级：

1. 命令行参数 `--api-key`
2. `<skill根目录>/.env`
3. `~/.openclaw/.env`
4. `~/.claude/.env`
5. 环境变量 `ARK_API_KEY`

可复制模板：

```bash
cp .env.example .env
```

## 3) 安装依赖

```bash
pip install -r requirements.txt
```

## 4) 使用方式

### 在 OpenClaw/Claude Code 中直接说

- 帮我生成一张赛博朋克城市海报
- 参考这张图，改成水彩插画风格
- 生成 4 张连贯的四季场景图

### 命令行调试

```bash
# 文生图
python3 scripts/seedream.py -p "一只可爱的橘猫"

# 图生图（支持重复 -i）
python3 scripts/seedream.py -p "改成水彩风格" -i "https://example.com/input.png"

# 组图
python3 scripts/seedream.py -p "四季风景插画" --sequential --max-images 4

# 联网搜索（仅 5.0-lite）
python3 scripts/seedream.py -p "北京今日天气信息图，扁平风格" --web-search
```

## 参数说明

| 参数 | 简写 | 说明 | 默认值 |
|---|---|---|---|
| `--prompt` | `-p` | 图片提示词（必填） | - |
| `--model` | `-m` | `5.0-lite` / `4.5` / `4.0` | `5.0-lite` |
| `--image` | `-i` | 输入图片 URL，可重复 | - |
| `--size` | `-s` | 图像尺寸 | `2K` |
| `--output-format` | `-f` | `png` / `jpeg` | 模型自动选择 |
| `--sequential` | `-S` | 启用组图 | `false` |
| `--max-images` | - | 组图最大数量 | `4` |
| `--web-search` | - | 启用联网搜索 | `false` |
| `--output` | `-o` | 输出目录 | `~/Downloads` |
| `--proxy` | `-x` | HTTP 代理 | - |

## 获取 ARK API Key

1. 打开 [火山引擎方舟 API Key 页面](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey)
2. 创建 API Key
3. 确认已开通 Seedream 对应模型

## 项目结构

```text
xh-seedream-gen-image/
├── SKILL.md
├── scripts/
│   └── seedream.py
├── .env.example
├── requirements.txt
├── README.md
└── .claude/skills/seedream/   # 旧路径兼容
```

## 许可证

MIT
