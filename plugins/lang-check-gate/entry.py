import subprocess as sp, os
def check(file_path, lang="en", config=None):
    hook_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "1-4 Dev", "scripts", "hooks")
    r = sp.run(["bash", os.path.join(hook_dir, "lang-check.sh"), "--file", file_path, "--lang", lang], capture_output=True, text=True, timeout=120)
    return {"rc": r.returncode, "out": (r.stdout + r.stderr)[-3000:]}
