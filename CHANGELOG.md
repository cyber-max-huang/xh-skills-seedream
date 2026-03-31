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
