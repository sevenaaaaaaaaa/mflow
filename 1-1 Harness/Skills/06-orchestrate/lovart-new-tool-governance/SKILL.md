---
description: 新工具治理 skill。注册新工具到 TOOLS-REGISTRY。
---
# lovart-new-tool-governance — tool creation gate

> **Why this exists**: When the agent encounters a new problem and creates a script,
> it often bypasses all constraints — wrong paths, bad naming, no documentation,
> no smoke test, no registry entry. This accumulates noise. This skill is the
> **mandatory first step** before creating any new script/tool/file.

## When this skill loads

加载条件：
- Agent 想创建新脚本 (write_file / terminal python3 -c > /path/to/script.py)
- Agent 想创建新 skill (skill_manage create)
- Agent 想创建新 hook / cron job / automation script
- 用户说"写个脚本" / "做个工具" / "加个检查" / "创建一个..."

不加载：
- 修改现有脚本 (用 patch)
- 一次性临时脚本 (写到 /tmp/ 不入 vault)
- 读取/查询现有脚本

## 5 步强制流程

### Step 1: 搜索已有

```bash
# 在创建前，先搜有没有已经做这个的脚本
search_files(pattern="关键词", target="content", path="1-4 Dev/scripts/")
search_files(pattern="关键词", target="content", path="1-1 Harness/Skills/")
```

如果搜到 0 结果 → 继续 Step 2
如果搜到结果 → **读一下现有的是否已经满足需求**，满足则不创建新脚本

### Step 2: 确定位置和命名

| 类型 | 位置 | 命名 |
|------|------|------|
| Python 脚本 | `1-4 Dev/scripts/` | `snake_case.py` |
| Shell 脚本 | `1-4 Dev/scripts/` | `kebab-case.sh` |
| Skill 脚本 | `1-1 Harness/Skills/06-orchestrate/<skill-name>/` | 按 skill 目录结构 |
| Hook 脚本 | `1-4 Dev/scripts/hooks/` | `kebab-case.sh` |

**禁止**：
- 任意路径写脚本 (如 ~/tmp/test.py)
- CamelCase 命名
- 无扩展名的脚本
- 直接在 vault 根目录写文件

### Step 3: 写脚本

写完后，在脚本内嵌入：
- `#!/usr/bin/env python3` 或 `#!/usr/bin/env bash` (shebang)
- 第一行注释说明用途
- docstring 或 README 说明

### Step 4: 运行 governance check

```bash
python3 $HARNESS_ROOT/Skills/06-orchestrate/lovart-new-tool-governance/governance_check.py /path/to/new/script.py
```

6 个 gate:
- G1 命名: snake_case.py / kebab-case.sh
- G2 shebang: #!/usr/bin/env python3|bash
- G3 位置: 必须在 ALLOWED_ROOTS 下
- G4 docstring: 有注释说明用途
- G5 无违规: 无 sanity deploy / --replace / schemaTypes / rm -rf /
- G6 smoke: --help 不 crash (Python) / bash -n 不报错 (Shell)

**全部 PASS 才能注册**。有 FAIL → 修完重跑。

### Step 5: 注册到 TOOLS-REGISTRY.md

在 `1-1 Harness/09-scripts/TOOLS-REGISTRY.md` 末尾追加一行：

```
| path | purpose | created | owner | status | smoke |
```

注册后脚本才算"正式进入项目"。

## 反模式

- **❌ 没搜就创建**: 50% 的"新脚本"其实已经有类似实现
- **❌ 没 check 就用**: governance check 是物理约束，不是建议
- **❌ 没注册就结束**: 未注册的脚本 = 噪音，下次会被当成垃圾清理
- **❌ 绕过 ALLOWED_ROOTS**: 任意路径写脚本 = 无法追踪 = 定时炸弹

## 文件 map

```
1-1 Harness/Skills/06-orchestrate/lovart-new-tool-governance/
├── SKILL.md                ← 本文件
├── governance_check.py     ← 6-gate 校验器
└── tests/smoketest.sh      ← 校验器自身测试
```

## 与 pipeline-state / router 的关系

- pipeline-state: 管"内容在哪个阶段"
- router: 管"该去哪个 profile / 装哪些 skill"
- governance: 管"创建新工具时是否合规"

三者互不替代：governance 不关心内容流程，只关心工具创建是否合规。
