#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lovart Harness Compiler & Synchronizer (harness_sync.py)
-------------------------------------------------------
This script enforces a Single Source of Truth (SSOT) for all agent rules and skills.
It reads the master rules from `1-1 Harness/02-rules/` and automatically compiles/synchronizes them to:
1. Cursor MDC Rules (.cursor/rules/*.mdc)
2. Claude Code Rules (.clauderc)
3. Codex Rules (.codexrules)
4. Hermes / OpenCode Profiles (via install-hermes-lovart-profiles.sh)

Usage:
    python3 harness_sync.py
"""

import os
import shutil
import subprocess
import sys
import json

# Define Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))

RULES_DIR = os.path.join(PROJECT_ROOT, "1-1 Harness/02-rules")
CURSOR_RULES_DIR = os.path.join(PROJECT_ROOT, ".cursor/rules")
CLAUDE_RC_PATH = os.path.join(PROJECT_ROOT, ".clauderc")
CODEX_RULES_PATH = os.path.join(PROJECT_ROOT, ".codexrules")
OPENCODE_CONFIG_PATH = os.path.join(PROJECT_ROOT, "opencode.jsonc")
HERMES_INSTALL_SCRIPT = os.path.join(PROJECT_ROOT, "1-4 Dev/automation/install-hermes-lovart-profiles.sh")
VAULT_SKILLS_ROOT = os.path.join(PROJECT_ROOT, "1-1 Harness/Skills")
HERMES_LOVART_SKILLS = os.path.join(os.path.expanduser("~"), ".hermes", "skills", "lovart")
RULE_FILES = [
    "RULES-00-iron.md",
    "RULES-10-reports.md",
    "RULES-20-creation.md",
    "RULES-30-quality.md",
    "RULES-40-ops.md",
    "RULES-50-distribution.md",
    "RULES-60-management.md",
]

# Ensure target directories exist
os.makedirs(CURSOR_RULES_DIR, exist_ok=True)

def read_rule_file(filename):
    path = os.path.join(RULES_DIR, filename)
    if not os.path.exists(path):
        print(f"Error: Master rule file {filename} not found at {path}", file=sys.stderr)
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def read_rule_bundle(filenames=RULE_FILES):
    chunks = []
    for filename in filenames:
        content = read_rule_file(filename)
        if content:
            chunks.append(content)
    return "\n\n---\n\n".join(chunks)

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ Synchronized: {os.path.relpath(path, PROJECT_ROOT)}")

def compile_cursor_rules():
    print("Compiling Cursor MDC Rules...")
    
    # 1. lovart-core.mdc (from RULES-00-iron.md)
    iron_content = read_rule_file("RULES-00-iron.md")
    core_mdc = f"""---
description: Lovart MFlow 项目基础契约：路径变量、全局铁律、产出路由、与 Hermes 技能的关系。在 Lovart 项目内做任何任务前加载。
globs: "*"
alwaysApply: true
---

{iron_content}
"""
    write_file(os.path.join(CURSOR_RULES_DIR, "lovart-core.mdc"), core_mdc)

    # 2. lovart-quality-gates.mdc (from RULES-30-quality.md)
    quality_content = read_rule_file("RULES-30-quality.md")
    # Add extra anti-slop guidelines directly into MDC
    quality_mdc = f"""---
description: Lovart 内容质量门禁：preflight、SEO/URL/i18n 检查、Anti-Slop 审计，发布前 BLOCK 验证。确保内容不缩水、不乱写、无 AI 腔调。
globs: "*"
alwaysApply: true
---

{quality_content}

## 补充：中英文禁用词库 (Anti-Slop Banned Phrases)

### 英文禁用词 (Banned Phrases in EN)
- **绝对禁用**：`leverage`, `streamline`, `unlock`, `empower`, `seamless`, `seamlessly`, `delve`, `testament`, `unprecedented`, `the future of`, `game-changer`, `revolutionize`, `elevate`, `fostering`, `tapestry`, `beacon`, `realm`, `journey`, `pave the way`
- *替代方案*：用具体的动作词代替。例如用 `use`/`utilize` 代替 `leverage`，用 `improve`/`optimize` 代替 `streamline`。

### 简中禁用词 (Banned Phrases in ZH)
- **绝对禁用**：`赋能`, `闭环`, `抓手`, `链路`, `生态位`, `底层逻辑`, `方法论`, `心智`, `对齐`, `颗粒度`, `打法`, `痛点`, `引爆`, `破局`, `维度`, `深挖`, `见证`, `颠覆性`, `前沿`
- *替代方案*：用人话和具体业务词汇代替。例如用 `支持`/`帮助` 代替 `赋能`，用 `流程`/`环节` 代替 `链路`。
"""
    write_file(os.path.join(CURSOR_RULES_DIR, "lovart-quality-gates.mdc"), quality_mdc)

    # 3. lovart-blog.mdc (from RULES-20-creation.md + Blog Specifics)
    creation_content = read_rule_file("RULES-20-creation.md")
    blog_mdc = f"""---
description: Lovart Blog 创作与优化规则。适用于所有博客生成、重写、优化与分类路由任务。强制执行 Complete Guide 和 Insight & Trend 的高标准要求。
globs: "**/*.md"
alwaysApply: false
---

{creation_content}

## Blog 创作与分类铁律

### Complete Guide (完全指南) 专属铁律
1. **字数硬门槛**：英文版必须 **≥7,500 词** (Words)；中文版必须 **≥12,000 汉字** (Characters)。
2. **第一人称叙事**：必须使用第一人称复数（`we`, `our`, `我们`）进行叙述。
3. **ASCII 对比矩阵**：正文中必须包含至少一个 ASCII 格式的对比表格/矩阵。
4. **独家公式/等式**：必须包含至少一个独特的数学公式或逻辑等式（使用 Markdown 格式，如 `\\[ ... \\]` 或 `\\( ... \\)`）。
5. **坦诚的竞品分析**：客观、坦诚地分析竞品（如 Canva, Figma 等）的优缺点。
6. **深度防御性 FAQ**：FAQ 章节必须包含 **至少 5 个** 具有深度、甚至带有挑战性的问题，并给出极其专业的解答。
7. **黄金结尾 (Golden Closing)**：结尾不能是套话，必须有启发性的总结和极具吸引力的 CTA。

### Insight & Trend (行业洞察) 专属铁律
1. **字数硬门槛**：英文版必须 **≥4,500 词** (Words)；中文版必须 **≥8,000 汉字** (Characters)。
2. **2026 真实数据引用**：必须引用至少 **3 个** 2026 年的真实、经过验证的数据点（参考 `source-pool.md`）。
3. **5 大核心剧本融合**：强制融合 Code-Native Visuals、Infinite Canvas、Enterprise Creative Ops、Hard ROI & TCO、Legal & Provenance。
4. **标准 8 章结构**：必须严格按照 8 章标准逻辑流进行写作。

### 写作防缩水规程 (Anti-Shrinkage Protocol)
1. **分段生成法**：在开始写作前，先向用户展示详细的大纲，并明确每一章的预估字数。
2. **断点续传**：每次只生成 2-3 个章节。确认无误后再生成接下来的章节。
3. **字数实时统计**：在每段生成结束时，必须在心里（或在输出中）计算当前已生成的总字数，确保最终产出 100% 达标。
4. **拒绝概括**：严禁在后半部分使用 "In summary...", "To conclude..." 等概括性词汇敷衍。
"""
    write_file(os.path.join(CURSOR_RULES_DIR, "lovart-blog.mdc"), blog_mdc)

    # 4. lovart-landing-page.mdc (from RULES-20-creation.md + Landing Page Specifics)
    landing_mdc = f"""---
description: Lovart 落地页（Tools, Features, Scenarios, Solutions）生产与刷新规则。适用于所有落地页 JSON 生成与刷新任务。
globs: "**/*.json"
alwaysApply: false
---

{creation_content}

## 落地页 JSON 生产铁律

### Composite-V2 JSON 核心规范 (Tools & Features)
1. **故事线规范**：必须严格遵循 `1-1 Harness/08-storyline/` 中的故事线定义，确保页面的叙事逻辑完整。
2. **Section 结构完整性**：必须包含所有必需的 section（如 `hero`, `features`, `pricing`, `faq`, `cta` 等），绝对禁止残留 `section_` 或 `draft_` 等临时 marker。
3. **首屏输入输出说明**：Tools 和 Features 页面首屏必须有清晰的输入输出（Input/Output）直观展示或说明。
4. **图片与媒体资源**：所有图片 URL 必须是有效的、已验证的地址，严禁使用 `IMAGE PLACEHOLDER` 或 `lorem` 图片。

### 防配置错误与防缩水机制
1. **大 JSON 分段审查**：必须使用 Read 工具分段检查，绝对不能一次性将数千行的 JSON 贴入对话。
2. **严格的键值校验**：所有的 `_id` 必须符合命名规范（如 `tools-ai-logo-maker-en`），多语言版本必须有各自独立的 JSON 文件且语言代码正确。
"""
    write_file(os.path.join(CURSOR_RULES_DIR, "lovart-landing-page.mdc"), landing_mdc)

    # 5. lovart-sanity-publish.mdc (from RULES-40-ops.md)
    ops_content = read_rule_file("RULES-40-ops.md")
    sanity_mdc = f"""---
description: Lovart Sanity 内容管道发布规则。适用于所有发布到 Sanity CMS 的任务。防止覆盖线上数据和配置错误。
globs: "1-4 Dev/lovart.sanity.studio/**/*"
alwaysApply: false
---

{ops_content}

## Sanity 内容发布管道铁律

1. **仅限增量导入**：必须使用 `npx sanity dataset import <file> --dataset production --missing`，绝对禁止在没有用户明确授权的情况下使用 `--replace`！
2. **Blog 日期双写**：所有的 Blog 文档必须同时设置 `releaseDate` 和 `publishedAt`，且两者的值必须完全一致。
3. **内链可用性**：Markdown 正文中的所有站内链接必须使用 `/blog/{{slug}}` 格式，严禁使用 `.md` 后缀、`/cluster/*` 旧路径或 `#` 占位符。
4. **发布状态控制**：所有的发布类任务在导入前，文档状态应设为 `status: ready`，等待人工审核后再进行最终 import。
"""
    write_file(os.path.join(CURSOR_RULES_DIR, "lovart-sanity-publish.mdc"), sanity_mdc)

    # 6. lovart-seo-report-iron-rules.mdc (from RULES-10-reports.md)
    reports_content = read_rule_file("RULES-10-reports.md")
    seo_mdc = f"""---
description: Lovart SEO 报告铁律 — 环比总则 + 月报结构 + OKR
globs: "*"
alwaysApply: true
---

{reports_content}
"""
    write_file(os.path.join(CURSOR_RULES_DIR, "lovart-seo-report-iron-rules.mdc"), seo_mdc)


def compile_claude_code_rules():
    print("Compiling Claude Code Rules (.clauderc)...")
    rules_content = read_rule_bundle()
    
    clauderc_content = f"""# Lovart Claude Code System Rules
# Generated automatically by harness_sync.py. DO NOT EDIT DIRECTLY.

## Lovart Full Harness Rule Bundle
{rules_content}
"""
    write_file(CLAUDE_RC_PATH, clauderc_content)


def compile_codex_rules():
    print("Compiling Codex Rules (.codexrules)...")
    rules_content = read_rule_bundle()
    
    codex_content = f"""# Lovart Codex Rules
# Generated automatically by harness_sync.py. DO NOT EDIT DIRECTLY.

{rules_content}
"""
    write_file(CODEX_RULES_PATH, codex_content)

def sync_opencode_config():
    print("Synchronizing OpenCode instructions...")
    if not os.path.exists(OPENCODE_CONFIG_PATH):
        print(f"Warning: OpenCode config not found at {OPENCODE_CONFIG_PATH}", file=sys.stderr)
        return

    try:
        with open(OPENCODE_CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Warning: opencode.jsonc is not parseable JSON; skipped instruction sync: {e}", file=sys.stderr)
        return

    rule_paths = [f"1-1 Harness/02-rules/{filename}" for filename in RULE_FILES]
    existing = config.get("instructions", [])
    rest = [item for item in existing if item not in rule_paths]
    config["instructions"] = rule_paths + rest

    with open(OPENCODE_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("✓ Synchronized: opencode.jsonc")


def sync_hermes_skills():
    """Copy vault Skills/ (SSOT) -> ~/.hermes/skills/lovart/.

    Vault dirs containing SKILL.md are the single truth; the Hermes runtime is a
    regenerated cache. Additive & idempotent: never deletes runtime-only skills
    (e.g. legacy lovart-content-generation) so nothing breaks mid-flight.
    Must run before sync_hermes_profiles() so profile builds see fresh skills.
    """
    print("Synchronizing Hermes lovart skills from vault...")
    if not os.path.isdir(VAULT_SKILLS_ROOT):
        print(f"Warning: vault skills root missing: {VAULT_SKILLS_ROOT}", file=sys.stderr)
        return
    os.makedirs(HERMES_LOVART_SKILLS, exist_ok=True)
    count = 0
    for dirpath, dirnames, filenames in os.walk(VAULT_SKILLS_ROOT):
        if "SKILL.md" not in filenames:
            continue
        name = os.path.basename(os.path.normpath(dirpath))
        if not name:
            continue
        dest = os.path.join(HERMES_LOVART_SKILLS, name)
        shutil.copytree(dirpath, dest, dirs_exist_ok=True)
        count += 1
    print(f"✓ Synchronized: {count} vault skills -> {HERMES_LOVART_SKILLS}")


def sync_hermes_profiles():
    print("Synchronizing Hermes/OpenCode Profiles...")
    if not os.path.exists(HERMES_INSTALL_SCRIPT):
        print(f"Warning: Hermes install script not found at {HERMES_INSTALL_SCRIPT}", file=sys.stderr)
        return
    
    try:
        # Run the hermes install script
        result = subprocess.run(
            ["bash", HERMES_INSTALL_SCRIPT],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True
        )
        print("✓ Hermes Profiles synchronized successfully!")
        print(result.stdout.strip().split("\n")[-1]) # Print the last line of output
    except subprocess.CalledProcessError as e:
        print(f"Error running Hermes install script: {e.stderr}", file=sys.stderr)


def main():
    print("==========================================")
    print("Lovart Harness Synchronization Started")
    print("==========================================")
    
    compile_cursor_rules()
    compile_claude_code_rules()
    compile_codex_rules()
    sync_opencode_config()
    sync_hermes_skills()
    sync_hermes_profiles()
    
    print("==========================================")
    print("🎉 All Clients Synchronized Successfully!")
    print("==========================================")

if __name__ == "__main__":
    main()
