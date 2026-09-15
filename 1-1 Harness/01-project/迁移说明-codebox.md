# Lovart MFlow — codebox 迁移说明

> **版本**: v1.0
> **日期**: 2026-07-23
> **目标读者**: 研发团队
> **平台**: codebox (`http://172.16.16.203:8080`)

---

## 一、前置条件

1. **内网访问**: 连接公司内网,能访问 `172.16.16.203:8080`
2. **飞书账号**: 用飞书登录 codebox 一次(账号入库)
3. **API Key**: 在 codebox 控制台生成 API Key
4. **本地环境**: 有 Python 3.9+ 和 Git

---

## 二、Step 1: 创建项目

```bash
# 设置环境变量
export CODEBOX="http://172.16.16.203:8080"
export CODEBOX_API_KEY="codebox_api_key_xxxxxxxx"
export H="Authorization: Bearer $CODEBOX_API_KEY"

# 创建项目
curl -H "$H" -X POST "$CODEBOX/api/projects" \
  -d '{"name":"lovart-mflow"}'

# 验证创建成功
curl -H "$H" "$CODEBOX/api/projects/lovart-mflow"
```

---

## 三、Step 2: 初始化项目结构

```bash
# 创建目录结构
curl -H "$H" -X POST "$CODEBOX/api/projects/lovart-mflow/exec" \
  -d '{"cmd":"mkdir -p cmd/server internal/api internal/store internal/engine scripts hooks skills config/rules config/profiles web/static"}'

# 写 go.mod
curl -H "$H" -X POST "$CODEBOX/api/projects/lovart-mflow/exec" \
  -d '{"cmd":"cat > go.mod <<'"'"'EOF'"'"'\nmodule project\n\ngo 1.21\n\nrequire (\n\tgo.mongodb.org/mongo-driver v1.13.1\n)\nEOF"}'

# 写 main.go
curl -H "$H" -X POST "$CODEBOX/api/projects/lovart-mflow/exec" \
  -d '{"cmd":"cat > cmd/server/main.go <<'"'"'EOF'"'"'\npackage main\n\nimport (\n\t\"encoding/json\"\n\t\"log\"\n\t\"net/http\"\n\t\"os\"\n)\n\nfunc main() {\n\tport := os.Getenv(\"PORT\")\n\tif port == \"\" {\n\t\tport = \"30000\"\n\t}\n\n\thttp.HandleFunc(\"/health\", func(w http.ResponseWriter, r *http.Request) {\n\t\tw.Header().Set(\"Content-Type\", \"application/json\")\n\t\tjson.NewEncoder(w).Encode(map[string]string{\"status\": \"ok\"})\n\t})\n\n\thttp.HandleFunc(\"/api/pipeline/summary\", func(w http.ResponseWriter, r *http.Request) {\n\t\tw.Header().Set(\"Content-Type\", \"application/json\")\n\t\tjson.NewEncoder(w).Encode(map[string]interface{}{\n\t\t\t\"total\": 0,\n\t\t\t\"by_phase\": map[string]int{\"QUEUE\": 0, \"CREATE\": 0, \"REVIEW\": 0, \"SHIP\": 0, \"FINAL\": 0},\n\t\t})\n\t})\n\n\tlog.Printf(\"Listening on :%s\", port)\n\tlog.Fatal(http.ListenAndServe(\":\"+port, nil))\n}\nEOF"}'

# 写 start.sh
curl -H "$H" -X POST "$CODEBOX/api/projects/lovart-mflow/exec" \
  -d '{"cmd":"cat > start.sh <<'"'"'EOF'"'"'\n#!/bin/bash\ncase \"$1\" in\n  start)\n    PORT=$3\n    go build -o run/server ./cmd/server\n    nohup ./run/server > logs/server.log 2>&1 &\n    echo $! > run/server.pid\n    sleep 1\n    if kill -0 $(cat run/server.pid) 2>/dev/null; then\n      echo \"started on port $PORT\"\n    else\n      echo \"failed to start\"\n      exit 1\n    fi\n    ;;\n  stop)\n    if [ -f run/server.pid ]; then\n      kill $(cat run/server.pid) 2>/dev/null\n      rm -f run/server.pid\n    fi\n    ;;\n  status)\n    if [ -f run/server.pid ] && kill -0 $(cat run/server.pid) 2>/dev/null; then\n      echo \"running\"\n    else\n      echo \"stopped\"\n    fi\n    ;;\nesac\nEOF\nchmod +x start.sh"}'
```

---

## 四、Step 3: 迁移 Python 脚本

```bash
# 上传 pipeline_state.py
curl -H "$H" -X POST "$CODEBOX/api/projects/lovart-mflow/exec" \
  -d '{"cmd":"cat > scripts/pipeline_state.py <<'"'"'EOF'"'"'\n# ... 内容从本地复制 ...\nEOF"}'

# 上传 router.py
curl -H "$H" -X POST "$CODEBOX/api/projects/lovart-mflow/exec" \
  -d '{"cmd":"cat > scripts/router.py <<'"'"'EOF'"'"'\n# ... 内容从本地复制 ...\nEOF"}'

# 上传 governance_check.py
curl -H "$H" -X POST "$CODEBOX/api/projects/lovart-mflow/exec" \
  -d '{"cmd":"cat > scripts/governance_check.py <<'"'"'EOF'"'"'\n# ... 内容从本地复制 ...\nEOF"}'

# 上传 hooks
for hook in pre-write-check.sh post-write-check.sh pre-import-check.sh post-generation-check.sh; do
  curl -H "$H" -X POST "$CODEBOX/api/projects/lovart-mflow/exec" \
    -d "{\"cmd\":\"cat > hooks/$hook <<'EOF'\\n# ... 内容从本地复制 ...\\nEOF\"}"
done
```

---

## 五、Step 4: 迁移 Skills

```bash
# 上传 51 个 SKILL.md (逐个)
for skill in $(ls ~/.hermes/skills/lovart/); do
  content=$(cat ~/.hermes/skills/lovart/$skill/SKILL.md | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")
  curl -H "$H" -X POST "$CODEBOX/api/projects/lovart-mflow/exec" \
    -d "{\"cmd\":\"mkdir -p skills/$skill && cat > skills/$skill/SKILL.md <<'EOF'\\n$content\\nEOF\"}"
done
```

---

## 六、Step 5: 启动项目

```bash
# 启动
curl -H "$H" -X POST "$CODEBOX/api/projects/lovart-mflow/start"

# 验证
curl -H "$H" "$CODEBOX/p/lovart-mflow/health"
# 应返回: {"status":"ok"}

# 查看日志
curl -H "$H" -X POST "$CODEBOX/api/projects/lovart-mflow/exec" \
  -d '{"cmd":"tail -20 logs/server.log"}'
```

---

## 七、Step 6: 配置权限

```bash
# 默认: 所有登录用户可访问 Dashboard
# (创建项目时自动写入 any_user + /**)

# 收窄: 只让特定人操作 API
curl -H "$H" -X POST "$CODEBOX/api/projects/lovart-mflow/grants" \
  -d '{"subject_type":"user","subject_id":"ou_xxx","path":"/api/**"}'

# 开放: 游客可访问健康检查
curl -H "$H" -X POST "$CODEBOX/api/projects/lovart-mflow/grants" \
  -d '{"subject_type":"guest","path":"/health"}'
```

---

## 八、Step 7: 给 AI Agent 用

```bash
# 生成 API Key (在 codebox 控制台操作)
# 或通过 API:
curl -H "$H" -X POST "$CODEBOX/api/user/api-keys" \
  -d '{"description":"Claude Code - Lovart MFlow"}'
# 返回: {"token":"codebox_api_key_xxxxxxxx"}

# 交给 Claude Code 的 prompt:
"""
你有一把 codebox API Key,请先 curl 读完平台使用手册,再帮我在 codebox 上维护 Lovart MFlow 项目。

平台地址: http://172.16.16.203:8080
手册: curl http://172.16.16.203:8080/api/manual
项目: lovart-mflow
API Key: codebox_api_key_xxxxxxxx

所有 API 调用都要带 header: Authorization: Bearer <API Key>
"""
```

---

## 九、验证清单

- [ ] `GET /health` 返回 `{"status":"ok"}`
- [ ] `GET /api/pipeline/summary` 返回正确统计
- [ ] `POST /api/pipeline/items` 能创建 item
- [ ] `POST /api/router/decide` 返回正确 profile
- [ ] `POST /api/hooks/pre-write` 能跑 hook
- [ ] Dashboard 页面可访问
- [ ] AI Agent 通过 API Key 调用成功
- [ ] 权限隔离生效 (不同角色看到不同内容)
