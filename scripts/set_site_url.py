#!/usr/bin/env python3
"""Point canonical/og:url/og:image at the real site address (runs in GitHub Actions)."""
import os, re
repo = os.environ.get("GITHUB_REPOSITORY", "")
owner, _, name = repo.partition("/")
if os.path.exists("CNAME"):
    base = "https://" + open("CNAME").read().strip() + "/"
elif name.lower() == f"{owner.lower()}.github.io":
    base = f"https://{owner.lower()}.github.io/"
elif repo:
    base = f"https://{owner.lower()}.github.io/{name}/"
else:
    raise SystemExit("GITHUB_REPOSITORY not set")
s = open("index.html", encoding="utf8").read()
s = re.sub(r'(rel="canonical" href=")[^"]*', r"\g<1>" + base, s)
s = re.sub(r'(property="og:url" content=")[^"]*', r"\g<1>" + base, s)
s = re.sub(r'(property="og:image" content=")[^"]*', r"\g<1>" + base + "assets/og.jpg", s)
open("index.html", "w", encoding="utf8").write(s)
print("site url:", base)
