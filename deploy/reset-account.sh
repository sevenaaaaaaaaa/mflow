#!/usr/bin/env bash
# reset-account.sh — root CLI 密码重置（无需登录工作台）
# Usage: bash reset-account.sh <username> <new-password>
set -euo pipefail
U="${1:-}"; P="${2:-}"
[[ -z "$U" || -z "$P" ]] && { echo "Usage: bash $0 <username> <new-password(>=6)>"; exit 1; }
[[ ${#P} -lt 6 ]] && { echo "密码至少 6 位"; exit 1; }
PYTHON="${LOVART_PYTHON:-/www/wwwroot/mflow/.venv/bin/python}"
"$PYTHON" - "$U" "$P" <<'PY'
import bcrypt, json, sys, os, datetime
u, pw = sys.argv[1], sys.argv[2]
f = "/www/wwwroot/mflow/run/auth.json"
users = json.load(open(f))
rec = next((x for x in users if x["username"] == u), None)
if not rec:
    print("账号不存在:", u); sys.exit(1)
rec["hash"] = bcrypt.hashpw(pw.encode(), bcrypt.gensalt(rounds=10)).decode()
os.chmod(f, 0o600)
open(f, "w").write(json.dumps(users, ensure_ascii=False, indent=1))
with open("/www/wwwroot/mflow/run/approvals.log", "a") as log:
    log.write(f"{datetime.datetime.now().isoformat(timespec='seconds')} RESET {u} by root-CLI\n")
print("已重置:", u)
PY
systemctl restart mflow-console 2>/dev/null || true
