"""Generic Webhook adapter — POST item JSON to a configured URL."""
import json, urllib.request

import sys as _sys  # noqa: E402
from pathlib import Path as _Path  # noqa: E402
_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "library"))
import env_guard  # noqa: E402  dev/prod separation (development: external writes become dry-run)
env_guard.install()

def publish(item, cfg):
    url = (cfg or {}).get("url")
    if not url:
        return {"ok": False, "error": "webhook url 未配置"}
    if not env_guard.require_live_write(f"Webhook 发布 → {url}"):
        return env_guard.skipped_result(f"webhook POST {url}", url="", cms_id="")
    req = urllib.request.Request(url, data=json.dumps(item, ensure_ascii=False).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
        return {"ok": True, "url": data.get("url", ""), "cms_id": data.get("id", "")}
    except Exception as e:
        return {"ok": False, "error": str(e)[:300]}
