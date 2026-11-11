"""Runs each program at each size with --breadth-first and writes results.csv."""
import csv
import re
import subprocess
import sys

PROGRAMS = ["sum_seq", "sum_dc"]
SIZES = [1024, 4096, 16384, 65536]


def grab(label, text):
    """Finds a number like 2_993_893 after a label in Vine's output."""
    m = re.search(rf"{label}\s+([\d_]+)", text)
    if not m:
        sys.exit(f"Couldn't find '{label}' in Vine's output:\n{text}")
    return int(m.group(1).replace("_", ""))


def run(program, n):
    proc = subprocess.run(
        ["vine", "run", f"programs/{program}.vi", "--breadth-first", "--lib", "programs/common.vi"],
        input=f"{n}\n",
        capture_output=True,
        text=True,
        check=True,
    )
    out = proc.stdout + proc.stderr
    total, depth = grab("Total", out), grab("Depth", out)
    return {
        "program": program,
        "n": n,
        "result": grab("result:", out),
        "total": total,
        "depth": depth,
        "breadth": round(total / depth, 1),
    }


rows = []
for n in SIZES:
    results = {}
    for program in PROGRAMS:
        r = run(program, n)
        rows.append(r)
        results[program] = r["result"]
        print(f"{program:8} n={n:>6}  total={r['total']:>12,}  "
              f"depth={r['depth']:>9,}  breadth={r['breadth']:>9,}")
    if len(set(results.values())) != 1:
        sys.exit(f"Programs disagree at n={n}: {results}")

with open("results.csv", "w", newline="") as fh:
    writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
print("Wrote results.csv")