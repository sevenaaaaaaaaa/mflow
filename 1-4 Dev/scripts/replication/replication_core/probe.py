"""probe — 源探测：可达性 / SSR 判定 / 资源形态。"""
import re
import urllib.request
import urllib.error
from . import DEFAULT_UA


def fetch(url, timeout=30, ua=DEFAULT_UA):
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "ignore")


def probe_source(url, timeout=30):
    """探测源页：可达性、SSR 判定、样式表清单。

    SSR 判定（实战启发：composite-page-all 752KB body 全量 SSR；
    CSR 站 body 是空壳 + JS bundle）：body 内可见文本密度 > 阈值即判 SSR。
    """
    result = {"url": url, "reachable": False, "status": None, "ssr": None,
              "title": None, "size": 0, "stylesheets": [], "error": None}
    try:
        html = fetch(url, timeout=timeout)
    except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
        result["error"] = repr(e)[:200]
        return result
    result.update({"reachable": True, "size": len(html)})
    m = re.search(r"<title>([^<]*)</title>", html)
    if m:
        result["title"] = m.group(1)
    result["stylesheets"] = re.findall(
        r'<link[^>]+rel="stylesheet"[^>]+href="([^"]+)"', html)
    body = re.search(r"<body[^>]*>(.*)</body>", html, re.S)
    body_html = body.group(1) if body else html
    result["bodySize"] = len(body_html)
    text = re.sub(r"<script\b.*?</script>|<style\b.*?</style>|<[^>]+>", " ",
                  body_html, flags=re.S)
    text_density = len(re.sub(r"\s+", "", text))
    result["textDensity"] = text_density
    result["ssr"] = text_density > 2000 and len(body_html) > 50000
    scripts = len(re.findall(r"<script\b", body_html))
    result["scriptTags"] = scripts
    return result
