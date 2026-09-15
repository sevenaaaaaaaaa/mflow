# Session History Recovery — 从 SQLite 恢复丢失文件

当文件从磁盘消失（iCloud 优化存储、误删等），内容仍保存在 Hermes 的会话历史中。

## 恢复流程

### 1. 确认文件确实不在磁盘

```bash
ls -la ~/Documents/Lovart\ Local\ Dev/自媒体样稿-*.md
ls -la ~/.Trash/*样稿*
find ~/Library/Mobile\ Documents/com~apple~CloudDocs -name "自媒体样稿*" 2>/dev/null
```

### 2. 搜索会话历史（快速路径）

```python
from hermes_tools import session_search
# 搜索包含文件名的会话
result = session_search(query="样稿-002 UI-TARS", limit=3)
# 然后用 around_message_id 滚动到 write_file 调用处
```

### 3. 直接查询 SQLite（完整路径）

如果 session_search 找不到（当前会话未索引），直接查数据库：

```python
import sqlite3, json, os

conn = sqlite3.connect(os.path.expanduser("~/.hermes/state.db"))
cursor = conn.cursor()

# 搜索包含目标文件名的 tool_calls
cursor.execute("""
    SELECT id, session_id, tool_calls FROM messages 
    WHERE tool_calls LIKE '%样稿%' 
    AND length(tool_calls) > 1000 
    ORDER BY id
""")
rows = cursor.fetchall()

articles = []
for msg_id, session_id, tc_raw in rows:
    try:
        tc = json.loads(tc_raw)
        for call in tc:
            fn = call.get("function", {})
            if fn.get("name") == "write_file":
                args = json.loads(fn.get("arguments", "{}"))
                path = args.get("path", "")
                content = args.get("content", "")
                if content and len(content) > 500:
                    articles.append({
                        "msg_id": msg_id,
                        "session_id": session_id,
                        "path": path,
                        "content": content
                    })
    except json.JSONDecodeError:
        pass

conn.close()

# 写入恢复路径
for a in articles:
    outpath = f"/recovery/dir/{os.path.basename(a['path'])}"
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(a["content"])
    print(f"✅ Restored: {a['path']} ({len(a['content'])} chars)")
```

### 4. 数据库结构

| 数据库 | 表 | 关键列 |
|--------|-----|--------|
| `~/.hermes/state.db` | `messages` | `id`, `session_id`, `role`, `content`, `tool_calls`, `tool_name` |
| | `sessions` | `id`, `title`, `started_at` |

- `tool_calls` 列存储了完整的函数调用（含 write_file 的 content 参数）
- content 在 JSON 中是 Unicode-escaped（`\uXXXX`），`json.loads()` 自动解码
- 子代理（delegate_task）创建的文件也在同一个 session 的 tool_calls 中
- FTS5 索引覆盖 `content` + `tool_name` + `tool_calls`

### 5. 注意事项

- `tool_calls` 列只在 `role=assistant` 的消息中有
- 每个 write_file 调用的 content 是完整的文件内容（不是 diff）
- 如果 JSON 解析失败（invalid escape），用正则提取：`re.findall(r'"content"\s*:\s*"(.*?)(?:"\s*})', tc_raw, re.DOTALL)`
- 恢复后**必须存到 Obsidian vault**，不要存回 `~/Documents/`

## 实战案例

2026-06-15：9 篇自媒体样稿（001-009）从 `~/Documents/Lovart Local Dev/` 消失。通过查询 `state.db` 的 `messages` 表，从 session `20260612_195624_2ad13b` 的 tool_calls 中恢复全部内容。耗时约 2 分钟。
