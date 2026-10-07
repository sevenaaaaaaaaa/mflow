"""Generic Webhook adapter — POST item JSON to a configured URL."""
import json, urllib.request

def publish(item, cfg):
    url = (cfg or {}).get("url")
    if not url:
        return {"ok": False, "error": "webhook url 未配置"}
    req = urllib.request.Request(url, data=json.dumps(item, ensure_ascii=False).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
        return {"ok": True, "url": data.get("url", ""), "cms_id": data.get("id", "")}
    except Exception as e:
        return {"ok": False, "error": str(e)[:300]}
