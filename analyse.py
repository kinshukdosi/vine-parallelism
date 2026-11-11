"""Turns results.csv into speedup.png and breadth.png using Brent's upper bound"""
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

matplotlib.use("Agg")

df = pd.read_csv("results.csv")
P = [2**k for k in range(13)]  # 1 to 4,096 cores

def speedup(total: float, depth: float, p: int) -> float:
    """W / T_P, using Brent's upper bound T_P = W/P + D."""
    return total / (total / p + depth)

def largest(g: pd.DataFrame) -> pd.Series:
    """The row with the largest n for one program."""
    return g.sort_values("n").iloc[-1]

# estimated speedup vs cores, at each program's largest n
fig, ax = plt.subplots(figsize=(6, 4.5))
for program, g in df.groupby("program"):
    row = largest(g)
    total, depth, n = float(row["total"]), float(row["depth"]), int(row["n"])
    ax.loglog(P, [speedup(total, depth, p) for p in P],
              marker="o", label=f"{program} (n={n:,})")
ax.loglog(P, P, "k--", lw=1, label="ideal (linear)")
ax.set(xlabel="cores (P)", ylabel="estimated speedup",
       title="Estimated speedup vs core count")
ax.legend()
fig.tight_layout()
fig.savefig("speedup.png", dpi=150)

# breadth vs input size
fig, ax = plt.subplots(figsize=(6, 4.5))
for program, g in df.groupby("program"):
    g = g.sort_values("n")
    ax.loglog(g["n"], g["breadth"], marker="o", label=str(program))
ax.set(xlabel="input size (n)", ylabel="breadth",
       title="Available parallelism vs input size")
ax.legend()
fig.tight_layout()
fig.savefig("breadth.png", dpi=150)

for program, g in df.groupby("program"):
    row = largest(g)
    total, depth, n = float(row["total"]), float(row["depth"]), int(row["n"])
    print(f"{program}: breadth {total / depth:,.1f} at n={n:,}; "
          f"estimated speedup on 1,024 cores ~{speedup(total, depth, 1024):,.0f}x")