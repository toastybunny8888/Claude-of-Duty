import re, json, glob, hashlib, os, base64, sys

BOOT = '<script>try{if(typeof Game==="undefined")throw new Error("game scripts failed to load");'
PLACEHOLDER = "/*ZBA_SOUNDS*/[]"

parts = sorted(glob.glob("src/part_*.html"))
text = ""
for p in parts:
    with open(p, encoding="utf-8", newline="") as f:
        text += f.read()

with open("assets.json", encoding="utf-8") as f:
    assets = json.load(f)

out = re.sub(r"__ASSET_(\d+)__", lambda m: assets[int(m.group(1))], text)

# ---- add-ons: self-contained <script> blocks (addons/*.html) injected just before the boot script.
# zombie_behind_audio.html gets the base64 of addons/sounds/behind*.wav in place of its placeholder.
addons = sorted(glob.glob("addons/*.html"))
inject = ""
for a in addons:
    with open(a, encoding="utf-8", newline="") as f:
        s = f.read()
    if PLACEHOLDER in s:
        wavs = sorted(glob.glob("addons/sounds/behind*.wav"))
        if not wavs:
            print("WARNING: no addons/sounds/behind*.wav found, zombies will stay silent. Add behind1.wav ... behind5.wav and rebuild.")
        blobs = []
        for w in wavs:
            with open(w, "rb") as f:
                blobs.append(base64.b64encode(f.read()).decode("ascii"))
        s = s.replace(PLACEHOLDER, json.dumps(blobs))
        print(f"embedded {len(wavs)} zombie sound(s) from addons/sounds")
    inject += s + "\n"

if inject:
    if out.count(BOOT) != 1:
        sys.exit("could not find the boot script to inject the add-ons before, stop here")
    out = out.replace(BOOT, inject + BOOT, 1)
    print(f"injected {len(addons)} add-on(s)")

with open("omni-ops_built.html", "w", encoding="utf-8", newline="") as f:
    f.write(out)
print(f"built omni-ops_built.html from {len(parts)} parts")

orig = "omni-ops_v116_wallbuys (1).html"
if os.path.exists(orig):
    h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
    print("matches original exactly" if h(orig) == h("omni-ops_built.html")
          else "differs from original (expected once edits have been made)")
