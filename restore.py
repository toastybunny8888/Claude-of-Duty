import re, json, os, hashlib

with open("game.src.html", encoding="utf-8", newline="") as f:
    src = f.read()
with open("assets.json", encoding="utf-8") as f:
    assets = json.load(f)

out = re.sub(r"__ASSET_(\d+)__", lambda m: assets[int(m.group(1))], src)
with open("omni-ops_built.html", "w", encoding="utf-8", newline="") as f:
    f.write(out)
print("built omni-ops_built.html")

orig = "omni-ops_v116_wallbuys (1).html"
if os.path.exists(orig):
    h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
    print("matches original exactly" if h(orig) == h("omni-ops_built.html")
          else "differs from original (expected once edits have been made)")