#!/usr/bin/env python3
"""Regenerate version.json from ario.apk (version, size, date, sha256)."""
import glob, hashlib, json, os, re, subprocess, datetime

APK = "ario.apk"
OUT = "version.json"

def find_aapt2():
    root = os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT") or ""
    c = sorted(glob.glob(os.path.join(root, "build-tools", "*", "aapt2")))
    return c[-1] if c else None

def apk_version():
    tool = find_aapt2()
    if not tool:
        return None
    try:
        out = subprocess.run([tool, "dump", "badging", APK], capture_output=True, text=True, check=True).stdout
        m = re.search(r"versionName='([^']*)'", out)
        return m.group(1) if m else None
    except Exception:
        return None

old = {}
if os.path.exists(OUT):
    old = json.load(open(OUT, encoding="utf8"))

# The newest entry (first item) of changelog.json decides the version shown on
# the site. The APK's own versionName is only used if the changelog is empty.
CL = "changelog.json"
log = json.load(open(CL, encoding="utf8")) if os.path.exists(CL) else []
top = log[0].get("version") if log else None

data = {
    "version": top or apk_version() or old.get("version", "1.0"),
    "size": os.path.getsize(APK),
    "date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
    "sha256": hashlib.sha256(open(APK, "rb").read()).hexdigest(),
    "file": APK,
}
json.dump(data, open(OUT, "w", encoding="utf8"), indent=2)
print(data)

# --- changelog.json: make sure the current version has an entry ---------------
# Edit changelog.json by hand to write nice notes per language. If you forget,
# an entry is added automatically from the last commit message so the site never
# shows a version without notes.
if not any(e.get("version") == data["version"] for e in log):
    try:
        msg = subprocess.run(["git", "log", "-1", "--pretty=%s"], capture_output=True, text=True).stdout.strip()
    except Exception:
        msg = ""
    msg = msg or "Update"
    log.insert(0, {"version": data["version"], "date": data["date"], "notes": {"fa": [msg], "ar": [msg], "en": [msg]}})
    json.dump(log, open(CL, "w", encoding="utf8"), indent=2, ensure_ascii=False)
    print("changelog entry added for", data["version"])
