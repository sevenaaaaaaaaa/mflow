"""WordPress REST adapter (Application Passwords). Requires requests."""
def publish(item, cfg):
    try:
        import requests
    except ImportError:
        return {"ok": False, "error": "pip install requests"}
    base, user, pw = (cfg or {}).get("base", "").rstrip("/"), (cfg or {}).get("user", ""), (cfg or {}).get("app_password", "")
    if not base or not pw:
        return {"ok": False, "error": "wordpress base/user/app_password 未配置"}
    r = requests.post(f"{base}/wp-json/wp/v2/posts",
                      json={"title": item.get("title"), "content": item.get("body_md"), "status": "draft"},
                      auth=(user, pw), timeout=60)
    if r.status_code in (200, 201):
        d = r.json()
        return {"ok": True, "url": d.get("link", ""), "cms_id": str(d.get("id", ""))}
    return {"ok": False, "error": f"HTTP {r.status_code}: {r.text[:200]}"}
