"""Credential path resolution for Lovart Trident scripts.

Lookup order:
1. Explicit file environment variable.
2. LOVART_TRIDENT_CREDENTIALS_DIR.
3. User-private default directory.
4. Legacy in-repo credentials directory.
5. Legacy script directory.
"""
from __future__ import annotations

import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
LEGACY_CREDENTIALS_DIR = SKILL_DIR / "credentials"
USER_CREDENTIALS_DIR = Path("~/Library/Application Support/Lovart/credentials/trident").expanduser()


def _candidate_dirs() -> list[Path]:
    dirs: list[Path] = []
    env_dir = os.environ.get("LOVART_TRIDENT_CREDENTIALS_DIR")
    if env_dir:
        dirs.append(Path(env_dir).expanduser())
    dirs.extend([USER_CREDENTIALS_DIR, LEGACY_CREDENTIALS_DIR, SCRIPT_DIR])
    return dirs


def credential_file(filename: str, env_var: str | None = None) -> Path:
    candidates: list[Path] = []
    if env_var and os.environ.get(env_var):
        candidates.append(Path(os.environ[env_var]).expanduser())
    candidates.extend(d / filename for d in _candidate_dirs())
    for path in candidates:
        if path.exists():
            return path
    checked = "\n  - ".join(str(p) for p in candidates)
    raise FileNotFoundError(f"Missing credential file {filename}. Checked:\n  - {checked}")


def credential_output_file(filename: str, env_var: str | None = None) -> Path:
    if env_var and os.environ.get(env_var):
        path = Path(os.environ[env_var]).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    env_dir = os.environ.get("LOVART_TRIDENT_CREDENTIALS_DIR")
    if env_dir:
        path = Path(env_dir).expanduser() / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    if USER_CREDENTIALS_DIR.exists():
        return USER_CREDENTIALS_DIR / filename

    return LEGACY_CREDENTIALS_DIR / filename
