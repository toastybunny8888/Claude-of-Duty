import re, json

SRC = "omni-ops_v116_wallbuys (1).html"
MIN_LEN = 5000

with open(SRC, encoding="utf-8", newline="") as f:
    text = f.read()
print(f"original size: {len(text)/1e6:.1f} MB")

assert "__ASSET_" not in text, "placeholder text already exists in the file"

assets = []
def repl(m):
    assets.append(m.group(0))
    return f"__ASSET_{len(assets)-1}__"

stripped = re.sub(r"[A-Za-z0-9+/=]{%d,}" % MIN_LEN, repl, text)

# Prove the process is lossless before writing anything
rebuilt = re.sub(r"__ASSET_(\d+)__", lambda m: assets[int(m.group(1))], stripped)
assert rebuilt == text, "round trip failed, stop here and tell Claude"

# Show what kinds of blobs were found
print(f"blobs extracted: {len(assets)}")
for i, a in enumerate(assets[:8]):
    idx = text.find(a)
    print(f"  blob {i}: {len(a)/1e6:.2f} MB, preceded by: {text[max(0, idx-50):idx]!r}")

with open("game.src.html", "w", encoding="utf-8", newline="") as f:
    f.write(stripped)
with open("assets.json", "w", encoding="utf-8") as f:
    json.dump(assets, f)

print(f"game.src.html size: {len(stripped)/1024:.0f} KB")
