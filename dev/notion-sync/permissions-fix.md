# notion-sync 目录 Permission Denied 诊断与修复

> 更新时间：2026-06-07  
> 状态：已定位根因，待执行修复

## 现象

Cursor 终端、ApplyPatch/Write 覆盖、Delete 对部分 `notion-sync` 文件返回 `Operation not permitted` / `Permission denied`，但：

- Cursor **Read** 工具仍可读取这些文件
- **新建**文件（如 `relations-map.json`）可正常读写
- 普通 iCloud Drive（`CloudDocs`）与 Desktop 不受此问题影响

## 根因

Obsidian 专用 iCloud 容器路径：

`~/Library/Mobile Documents/iCloud~md~obsidian/...`

其中 **早期创建** 的 6 个文件缺少 macOS 文件提供器所需的 `com.apple.macl` 扩展属性，导致 **Cursor 子进程** 无法读/写/删/改名。这不是 Unix `chmod` 问题（权限位均为 `644 seveno:staff`）。

| 文件 | Shell 读写 | 有 `com.apple.macl` |
|---|---|---|
| `README.md` | 否 | 否 |
| `official-records.json` | 否 | 否 |
| `backfill-queue.csv` | 否 | 否 |
| `notion-databases.schema.json` | 否 | 否 |
| `sync-manifest.json` | 否 | 否 |
| `notion-targets.json` | 否 | 否 |
| `relations-map.json` | **是** | **是** |

## 修复方案（任选其一）

### 方案 A：授予 Cursor「完全磁盘访问权限」（推荐，一劳永逸）

1. 打开 **系统设置 → 隐私与安全性 → 完全磁盘访问权限**
2. 点击 `+`，添加 **Cursor.app**（通常在 `/Applications/Cursor.app`）
3. 若仍无效，一并添加 **Cursor Helper** / **Cursor Helper (Plugin)**
4. **完全退出并重启 Cursor**
5. 回到本对话，让 Agent 继续更新被锁文件

### 方案 B：在系统终端删除锁文件后由 Agent 重建

1. 打开 **Terminal.app**（不是 Cursor 内置终端）
2. 运行桌面上的脚本：

```bash
bash ~/Desktop/fix-notion-sync-locks.sh
```

3. 脚本会备份到 `~/Desktop/notion-sync-backup-YYYYMMDD-HHMMSS/` 并删除 6 个锁文件
4. 回到 Cursor，让 Agent **重建**这些文件（内容已在备份中）

### 方案 C：在 Obsidian / Finder 中手动删除

在 Obsidian 文件列表或 Finder 中，将上述 6 个文件移入废纸篓，然后让 Agent 重建。

## 验证标准

修复后，在 Cursor 内置终端执行：

```bash
BASE="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project/1-1 GEO Readme/notion-sync"
test -r "$BASE/README.md" && test -w "$BASE/README.md" && echo OK || echo FAIL
```

应输出 `OK`。

## 预防

- 在 Obsidian iCloud vault 内，优先让 Cursor **新建**文件，或对已有文件通过 Obsidian 保存一次后再编辑
- 若长期依赖 Agent 自动化，建议为 Cursor 开启「完全磁盘访问权限」
- 可考虑将 `notion-sync/` 迁到非 iCloud 路径（如 Git 仓库内独立目录），Obsidian vault 内只保留链接
