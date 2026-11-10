#!/usr/bin/env python3
"""gsc-submit.py — 部署完成后把新 sitemap 交给 GSC，并清掉该退休的旧登记。

默认 dry-run；--apply 才真正调用 API。
"""
import json, sys, time, urllib.parse, urllib.request, urllib.error
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOKEN = Path("/Users/seveno/MFlow Dev/mflow/dev/scripts/sentinel/gsc_credentials/gsc-token.json")
SITE = "https://www.lovart.ai/"
RETIRE = ["all-urls.txt", "sitemap.xml", "sitemap-scenarios.xml"]


def get_token():
    tok = json.loads(TOKEN.read_text())
    data = urllib.parse.urlencode({"client_id": tok["client_id"], "client_secret": tok["client_secret"],
                                   "refresh_token": tok["refresh_token"], "grant_type": "refresh_token"}).encode()
    req = urllib.request.Request(tok["token_uri"], data=data)
    return json.loads(urllib.request.urlopen(req, timeout=30).read().decode())["access_token"]


def api(token, path, method="GET"):
    url = "https://searchconsole.googleapis.com/webmasters/v3/" + path
    req = urllib.request.Request(url, method=method, headers={"Authorization": "Bearer " + token})
    try:
        body = urllib.request.urlopen(req, timeout=30).read().decode()
        return json.loads(body) if body.strip() else {"ok": True}
    except urllib.error.HTTPError as e:
        return {"http_error": e.code, "body": e.read().decode()[:200]}


def main():
    apply = "--apply" in sys.argv
    idx = (HERE / "sitemap-index.xml").read_text(encoding="utf-8")
    import re
    feeds = re.findall(r"<loc>([^<]+)</loc>", idx)
    print("index 子项:", len(feeds))
    token = get_token()
    sc = urllib.parse.quote(SITE, safe="")
    if not apply:
        print("[dry] 将提交:", len(feeds), "条")
        print("[dry] 将删除登记:", RETIRE)
        return
    cur = api(token, "sites/" + sc + "/sitemaps")
    print("提交前 GSC 已登记:", len(cur.get("sitemap") or []))
    ok = 0
    for feed in feeds:
        q = urllib.parse.quote(feed, safe="")
        r = api(token, "sites/" + sc + "/sitemaps/" + q, method="PUT")
        if r.get("http_error"):
            print("  X", feed, r["http_error"])
        else:
            ok += 1
        time.sleep(0.35)
    print("提交成功:", ok, "/", len(feeds))
    for name in RETIRE:
        q = urllib.parse.quote(SITE + name, safe="")
        r = api(token, "sites/" + sc + "/sitemaps/" + q, method="DELETE")
        print(("  removed " if not r.get("http_error") else "  skip/failed ") + name, r.get("http_error") or "")
        time.sleep(0.35)
    after = api(token, "sites/" + sc + "/sitemaps")
    print("提交后 GSC 已登记:", len(after.get("sitemap") or []))


if __name__ == "__main__":
    main()
