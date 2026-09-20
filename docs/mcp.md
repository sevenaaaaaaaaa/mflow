# MFlow × MCP（Model Context Protocol）

把 MFlow 的能力开放给**任意 MCP 客户端**（Claude Desktop、Cursor、自研 Agent、IDE 插件），
让 AI 直接驱动你的内容运营：检索内容库/知识库、查任务、跑预设（强制 dry-run）、看执行画布。

## 1. 需要什么
- 服务器地址（默认 `http://127.0.0.1:8088`，MCP 服务与 console 同机运行）
- 机器 token：服务器 `run/env.sh` 里的 `MFLOW_API_TOKEN`

## 2. 客户端配置
```json
{
  "mcpServers": {
    "mflow": {
      "command": "python3",
      "args": ["/www/wwwroot/mflow/1-4 Dev/scripts/mcp_server.py"],
      "env": {
        "MFLOW_URL": "http://127.0.0.1:8088",
        "MFLOW_API_TOKEN": "<你的 token>"
      }
    }
  }
}
```

## 3. 可用工具（17 个）
只读：`mflow_health` `mflow_selfcheck` `mflow_inbox` `mflow_search_content` `mflow_search_kb`
`mflow_semantic_search` `mflow_recall` `mflow_list_tasks` `mflow_get_task` `mflow_list_runs`
`mflow_run_detail` `mflow_list_automations` `mflow_list_playbooks` `mflow_check_url` `mflow_list_reports`

**动作（强制 dry-run，不写生产库）**：`mflow_run_preset` `mflow_run_playbook`

## 4. 安全边界
- 机器 token 走 `/api/mcp/tool` 白名单；写生产库的动作（发布/真实修复）**不开放**，必须真人会话 + 确认。
- `run_preset` / `run_playbook` 一律强制 `dry_run=true`。

## 5. 自测
```bash
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | MFLOW_API_TOKEN=<token> python3 "1-4 Dev/scripts/mcp_server.py"
```

## 6. 与 OpenFlow / 其他系统
- 除 MCP 外，MFlow 还有 REST 机器接口：`GET /api/*` + `X-MFlow-Token`（只读）。
- 出站事件：设置 → 出站 Webhook（task/run/playbook/audit 事件，可选 HMAC 签名）。
