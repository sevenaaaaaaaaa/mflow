#!/usr/bin/env python3
"""MFlow MCP Server — 把 MFlow 能力暴露给任意 MCP 客户端（Claude Desktop/Cursor/自研 Agent）。

纯标准库实现（stdio JSON-RPC 2.0），零依赖。
配置环境变量：
  MFLOW_URL       默认 http://127.0.0.1:8088
  MFLOW_API_TOKEN 机器 token（服务器 run/env.sh 中的 MFLOW_API_TOKEN）

用法（在 MCP 客户端里配置）：
  {
    "mcpServers": {
      "mflow": {
        "command": "python3",
        "args": ["/www/wwwroot/mflow/1-4 Dev/scripts/mcp_server.py"],
        "env": {"MFLOW_URL": "http://127.0.0.1:8088", "MFLOW_API_TOKEN": "<token>"}
      }
    }
  }
"""
import json
import os
import sys
import urllib.request

URL = (os.environ.get("MFLOW_URL") or "http://127.0.0.1:8088").rstrip("/")
TOKEN = os.environ.get("MFLOW_API_TOKEN", "")
PROTOCOL = "2024-11-05"


def _api(path, method="GET", body=None):
    req = urllib.request.Request(
        URL + path,
        data=(json.dumps(body).encode() if body is not None else None),
        method=method,
        headers={"Content-Type": "application/json", "X-MFlow-Token": TOKEN},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read() or b"{}")


def _tools():
    try:
        return (_api("/api/mcp/tools") or {}).get("tools") or []
    except Exception as e:
        print(f"[mcp] tools fetch failed: {e}", file=sys.stderr)
        return []


def _schema(t):
    props = {}
    for k, desc in (t.get("schema") or {}).items():
        props[k] = {"type": ["string", "number", "object", "boolean"], "description": str(desc)}
    return {"type": "object", "properties": props, "additionalProperties": True}


def _send(obj):
    sys.stdout.write(json.dumps(obj, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def handle(msg):
    method = msg.get("method")
    mid = msg.get("id")
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": mid, "result": {
            "protocolVersion": PROTOCOL,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": "mflow", "version": "1.0.0"}}}
    if method in ("notifications/initialized", "initialized"):
        return None
    if method == "ping":
        return {"jsonrpc": "2.0", "id": mid, "result": {}}
    if method == "tools/list":
        tools = [{"name": t["name"], "description": t.get("desc", ""), "inputSchema": _schema(t)} for t in _tools()]
        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": tools}}
    if method == "tools/call":
        params = msg.get("params") or {}
        name = params.get("name")
        args = params.get("arguments") or {}
        try:
            r = _api("/api/mcp/tool", "POST", {"name": name, "args": args})
            result = r.get("result")
            text = json.dumps(result, ensure_ascii=False, indent=1)
            is_err = isinstance(result, dict) and bool(result.get("error"))
        except Exception as e:
            text, is_err = ("调用失败：" + str(e)), True
        return {"jsonrpc": "2.0", "id": mid,
                "result": {"content": [{"type": "text", "text": text}], "isError": is_err}}
    if mid is None:
        return None
    return {"jsonrpc": "2.0", "id": mid,
            "error": {"code": -32601, "message": "Method not found: " + str(method)}}


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except Exception:
            continue
        try:
            resp = handle(msg)
        except Exception as e:
            resp = {"jsonrpc": "2.0", "id": msg.get("id"), "error": {"code": -32603, "message": str(e)}}
        if resp is not None:
            _send(resp)


if __name__ == "__main__":
    main()
