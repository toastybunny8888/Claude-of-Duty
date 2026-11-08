import re, os, glob
from collections import Counter

LIMIT = 100_000  # characters per chunk

with open("game.src.html", encoding="utf-8", newline="") as f:
    text = f.read()

lines = text.splitlines(True)

chunks, cur, size = [], [], 0
for line in lines:
    if len(line) > LIMIT:
        if cur:
            chunks.append("".join(cur)); cur, size = [], 0
        chunks.append(line)
        continue
    if size + len(line) > LIMIT and cur:
        chunks.append("".join(cur)); cur, size = [], 0
    cur.append(line); size += len(line)
if cur:
    chunks.append("".join(cur))

assert "".join(chunks) == text, "split check failed, stop and tell Claude"

os.makedirs("src", exist_ok=True)
for old in glob.glob("src/part_*.html"):
    os.remove(old)
for i, c in enumerate(chunks, 1):
    with open(f"src/part_{i:03d}.html", "w", encoding="utf-8", newline="") as f:
        f.write(c)

report = [f"total {len(text)/1024:.0f} KB, {len(lines)} lines, {len(chunks)} chunks", "", "CHUNKS"]
for i, c in enumerate(chunks, 1):
    flag = "  <-- oversized (likely a library)" if len(c) > LIMIT * 1.5 else ""
    report.append(f"part_{i:03d}.html  {len(c)/1024:.0f} KB  starts: {c[:60]!r}{flag}")

KEYWORDS = ["grenade", "stim", "tomahawk", "knife", "killcam", "replay",
            "best ?play", "third.?person", "throw"]
report += ["", "KEYWORD HITS"]
for k in KEYWORDS:
    pat = re.compile(k, re.I)
    report.append(f"\n## {k}")
    total, per_part = 0, Counter()
    for i, c in enumerate(chunks, 1):
        for ln in c.splitlines():
            if len(ln) < 400 and pat.search(ln):
                total += 1
                per_part[i] += 1
                if total <= 25:
                    report.append(f"part_{i:03d}: {ln.strip()[:140]}")
    top = ", ".join(f"part_{p:03d}={n}" for p, n in per_part.most_common(8))
    report.append(f"(total {total} lines; most hits in: {top})")

with open("report.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(report))

print(f"wrote {len(chunks)} parts into src/ and report.txt")