#!/usr/bin/env python3
"""Active site profile: which public site / brand this MFlow instance manages.

Brand- and customer-specific values never live in the public repo. They are resolved at
runtime, first hit wins:

  1. environment variables
       MFLOW_MAIN_SITE_URL   public origin of the managed site, e.g. https://www.acme.example
       MFLOW_BRAND_NAME      display name, e.g. "Acme"
       MFLOW_BRAND_SLUG      directory name under ops/brands/, e.g. "acme"
       MFLOW_BLOCK_PREFIX    Gutenberg block namespace for replicated components, e.g. "acme"
       MFLOW_GSC_SITE        Search Console property (defaults to main_site_url + "/")
  2. ops/site.json         gitignored; deploy/sync.sh ships ops/ to the server
                           keys: main_site_url, brand_name, brand_slug, block_prefix, gsc_site,
                           brand_terms (list), ga4_property, ga4_stream,
                           sanity_project, sanity_dataset, own_hosts (list)
  3. run/sites/main.json   "domain" / "name"
  4. neutral defaults      https://www.example.com / "Example" / "mflow"

Brand-specific helper code lives in ops/brands/<brand_slug>/code/ and is imported via
load_brand_module() only when present.

CLI: python3 site_profile.py [key]   → prints the whole profile as JSON, or one value.
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path

ROOT = Path(os.environ.get("MFLOW_ROOT") or Path(__file__).resolve().parents[3])
OPS_DIR = ROOT / "ops"
SITE_FILE = OPS_DIR / "site.json"

DEFAULTS = {
    "main_site_url": "https://www.example.com",
    "brand_name": "Example",
    "brand_slug": "",
    "block_prefix": "mflow",
    "gsc_site": "",
    "brand_terms": [],
    "ga4_property": "",
    "ga4_stream": "",
    "sanity_project": "",
    "sanity_dataset": "production",
    "own_hosts": [],
}

_ENV = {
    "main_site_url": "MFLOW_MAIN_SITE_URL",
    "brand_name": "MFLOW_BRAND_NAME",
    "brand_slug": "MFLOW_BRAND_SLUG",
    "block_prefix": "MFLOW_BLOCK_PREFIX",
    "gsc_site": "MFLOW_GSC_SITE",
    "ga4_property": "MFLOW_GA4_PROPERTY",
    "ga4_stream": "MFLOW_GA4_STREAM",
    "sanity_project": "MFLOW_SANITY_PROJECT",
    "sanity_dataset": "MFLOW_SANITY_DATASET",
}


def _read_json(p: Path) -> dict:
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def profile() -> dict:
    """Merged profile (env > ops/site.json > run/sites/main.json > defaults)."""
    out = dict(DEFAULTS)
    run_dir = Path(os.environ.get("MFLOW_RUN_DIR") or (ROOT / "run"))
    main = _read_json(run_dir / "sites" / "main.json")
    if main.get("domain"):
        out["main_site_url"] = "https://" + str(main["domain"]).strip("/")
    if main.get("name"):
        out["brand_name"] = str(main["name"])
    for k, v in _read_json(SITE_FILE).items():
        if v not in (None, ""):
            out[k] = v
    for k, env in _ENV.items():
        if os.environ.get(env):
            out[k] = os.environ[env]
    out["main_site_url"] = str(out["main_site_url"]).rstrip("/")
    if not out.get("gsc_site"):
        out["gsc_site"] = out["main_site_url"] + "/"
    if not out.get("own_hosts"):
        host = out["main_site_url"].split("://", 1)[-1].split("/", 1)[0]
        out["own_hosts"] = [host] if host and host != "www.example.com" else []
    if not out.get("brand_terms"):
        out["brand_terms"] = [str(out["brand_name"]).lower()] if out.get("brand_name") else []
    return out


def get(key: str, default=None):
    return profile().get(key, default)


def main_site_url() -> str:
    return profile()["main_site_url"]


def block_prefix() -> str:
    return str(profile()["block_prefix"] or "mflow")


def brand_dir() -> Path | None:
    slug = str(profile().get("brand_slug") or "").strip()
    if not slug or "/" in slug or slug.startswith("."):
        return None
    d = OPS_DIR / "brands" / slug
    return d if d.is_dir() else None


def load_brand_module(name: str):
    """Import ops/brands/<slug>/code/<name>.py if it exists, else return None."""
    d = brand_dir()
    if d is None:
        return None
    f = d / "code" / f"{name}.py"
    if not f.is_file():
        return None
    spec = importlib.util.spec_from_file_location(f"mflow_brand_{name}", f)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as e:  # a broken brand module must not take the pipeline down
        print(f"[site_profile] brand module {f} failed to load: {e}", file=sys.stderr)
        return None
    return mod


if __name__ == "__main__":
    p = profile()
    if len(sys.argv) > 1 and sys.argv[1] == "own_hosts_regex":
        # grep -E alternation of the site's own hosts (for "external link" counting in hooks)
        print("|".join(h.replace(".", "\\.") for h in p.get("own_hosts") or []))
    elif len(sys.argv) > 1:
        v = p.get(sys.argv[1], "")
        print(json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v)
    else:
        print(json.dumps(p, ensure_ascii=False, indent=2))
