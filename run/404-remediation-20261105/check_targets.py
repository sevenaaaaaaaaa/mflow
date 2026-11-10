#!/usr/bin/env python3
"""Verify every 301 target in redirect-map.csv is live (final status 200).
Follows up to 6 hops; records status chain, final URL, and any error.
"""
import csv, json, time, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import Request, build_opener, HTTPRedirectHandler
from urllib.error import HTTPError, URLError

BASE = "/Users/seveno/MFlow Dev/mflow/run/404-remediation-20261105"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

opener = build_opener(NoRedirect)

def trace(url, max_hops=6):
    chain = []
    cur = url
    for _ in range(max_hops):
        try:
            req = Request(cur, headers={"User-Agent": UA, "Accept": "text/html"})
            resp = opener.open(req, timeout=20)
            chain.append((resp.status, cur))
            return resp.status, cur, chain
        except HTTPError as e:
            chain.append((e.code, cur))
            loc = e.headers.get("Location")
            if e.code in (301, 302, 303, 307, 308) and loc:
                from urllib.parse import urljoin
                cur = urljoin(cur, loc)
                continue
            return e.code, cur, chain
        except Exception as e:
            chain.append(("ERR:" + type(e).__name__, cur))
            return "ERR", cur, chain
    return "LOOP", cur, chain

rows = list(csv.DictReader(open(BASE + "/redirect-map.csv")))
print("targets", len(rows), flush=True)
out = []
done = 0
t0 = time.time()
with ThreadPoolExecutor(max_workers=16) as ex:
    futs = {ex.submit(trace, r["target_url"]): r for r in rows}
    for f in as_completed(futs):
        r = futs[f]
        code, final, chain = f.result()
        out.append({
            "source_url": r["source_url"], "target_url": r["target_url"],
            "rule": r["rule"], "final_code": code, "final_url": final,
            "chain": " -> ".join(f"{c} {u}" for c, u in chain),
        })
        done += 1
        if done % 100 == 0:
            print(f"progress {done}/{len(rows)} elapsed {time.time()-t0:.0f}s bad={sum(1 for x in out if x['final_code']!=200)}", flush=True)

with open(BASE + "/target-check.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0]))
    w.writeheader(); w.writerows(out)
bad = [x for x in out if x["final_code"] != 200]
summary = {
    "total": len(out),
    "ok_200": sum(1 for x in out if x["final_code"] == 200),
    "bad": len(bad),
    "by_code": {},
}
for x in out:
    summary["by_code"][str(x["final_code"])] = summary["by_code"].get(str(x["final_code"]), 0) + 1
json.dump({"summary": summary, "bad": bad}, open(BASE + "/target-check-summary.json", "w"), ensure_ascii=False, indent=2)
print("DONE", json.dumps(summary, ensure_ascii=False), flush=True)
