# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2026-03-31

### Changed
- 技能标准化为可被 OpenClaw 直接加载的根目录结构，新增根目录 `SKILL.md`
- 技能名称统一为 `xh-seedream-gen-image`
- 新增 `scripts/seedream.py` 作为主执行入口
- 旧路径 `.claude/skills/seedream/scripts/seedream.py` 改为兼容转发入口

### Added
- 新增 `.env.example`，明确要求通过 `.env` 提供 `ARK_API_KEY`
- 新增 `requirements.txt`，统一依赖安装方式
- README 重写，补充 `npx-skill` 安装说明与完整使用文档

## [1.0.0] - 2026-03-11

### Added
- 初始版本发布
- 支持文生图、图生图、多图融合、组图生成
- 支持 Seedream 5.0 lite / 4.5 / 4.0 模型
- 支持联网搜索功能
- 提供命令行工具和 OpenClaw Skill 格式

## [1.2.0] - 2026-04-03

### Changed
- SKILL.md 文档全面升级，合并 ClawHub seedream-image-gen (v1.0.0) 的文档内容
- 新增多图融合（Multi-image to Image）示例说明
- 新增完整的命令行参数表格
- 新增模型功能对照表
- 新增图像尺寸规格说明
- 新增完整使用示例（文生图、组图、联网搜索）

### Added
- metadata 字段兼容 OpenClaw 技能规范（requires、primaryEnv、install）
- 新增 homepage 指向火山引擎官方文档
