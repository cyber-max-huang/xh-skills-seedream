#!/usr/bin/env python3
"""
兼容旧路径入口：
.claude/skills/seedream/scripts/seedream.py -> scripts/seedream.py
"""
from pathlib import Path
import runpy

TARGET = Path(__file__).resolve().parents[4] / "scripts" / "seedream.py"
runpy.run_path(str(TARGET), run_name="__main__")
