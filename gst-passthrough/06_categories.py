"""
06_categories.py - pre-registered test T5, over-shifting by category, 2023 event only.

The 2023 event is the only one with clean identification: ip-e61 says the pre-2024
series was linked in by a scalar link factor, which preserves month-on-month changes,
so January 2023 is measured wholly inside the old basket. January 2024 sits on the
basket seam and is not estimated. Jacob's instruction, 7 September 2026.

T5: at least one, and fewer than half, of the published CPI categories show an excess
    step more than two standard errors above the mechanical figure of 0.9302 log
    points.
F5: no category over-shoots by that criterion. The answer to "which categories
    over-shifted" is then "none detectably", and that is published as the answer.

Inference is against each series' OWN placebo distribution of January steps, not
against a regression standard error, because test T6 showed the aggregate estimator
is noisier in January than a regression SE implies. 164 series are tested, so a
Benjamini-Hochberg false discovery rate control is applied at q = 0.10.
"""
import numpy as np, pandas as pd

TARGET = 100 * np.log(1.08 / 1.07)     # 0.9302 log points
GST_JAN = {2003, 2004, 2023, 2024}
YFROM, YTO = 2010, 2026

d = pd.read_csv("out/analysis.csv")
d["index"] = pd.to_numeric(d["index"], errors="coerce")
w = d.pivot_table(index="date", columns="series", values="index", aggfunc="first").sort_index()
meta = d.groupby("series").agg(level=("level", "first"), parent=("parent", "first"))


def jan_steps(series):
    s = w[series].dropna()
    out = {}
    for dt, v in s.items():
        y, m = int(dt[:4]), int(dt[5:])
        if m != 1:
            continue
        k = f"{y-1}-12"
        if k in s.index:
            out[y] = 100 * (np.log(v) - np.log(s[k]))
    return pd.Series(out).sort_index()


rows = []
for s in w.columns:
    g = jan_steps(s)
    g = g[(g.index >= YFROM) & (g.index <= YTO)]
    if 2023 not in g.index:
        continue
    base = g[~g.index.isin(GST_JAN)]
    if len(base) < 8:
        continue
    mu, sd = base.mean(), base.std(ddof=1)
    if sd == 0 or not np.isfinite(sd):
        continue
    exc = g.loc[2023] - mu
    se = sd * np.sqrt(1 + 1 / len(base))          # predictive SE for one new draw
    rows.append(dict(series=s, level=meta.level[s], n_base=len(base),
                     observed=g.loc[2023], base_mean=mu, base_sd=sd,
                     excess=exc, se=se, z_vs_zero=exc / se,
                     z_vs_target=(exc - TARGET) / se))

r = pd.DataFrame(rows)
from scipy import stats
r["p_vs_target"] = 2 * (1 - stats.norm.cdf(r.z_vs_target.abs()))
r["p_vs_zero"] = 2 * (1 - stats.norm.cdf(r.z_vs_zero.abs()))

# Benjamini-Hochberg at q=0.10 on the over-shoot test (one-sided, above target)
r["p_over"] = 1 - stats.norm.cdf(r.z_vs_target)
o = r.sort_values("p_over").reset_index(drop=True)
m, q = len(o), 0.10
o["bh_crit"] = (o.index + 1) / m * q
passing = o[o.p_over <= o.bh_crit]
k = len(passing)

print("=" * 96)
print(f"T5  OVER-SHIFTING BY CATEGORY, January 2023 event only")
print(f"    mechanical full pass-through target {TARGET:.4f} log points")
print(f"    {m} series tested, each against its own {YFROM}-{YTO} January baseline")
print("=" * 96)
print(f"\n  Series whose excess January 2023 step exceeds the target, "
      f"BH-controlled at q=0.10: {k}")
if k:
    for _, x in passing.iterrows():
        print(f"    {x.series[:52]:52s} excess {x.excess:+6.2f}  "
              f"target {TARGET:.2f}  z {x.z_vs_target:+.2f}  p {x.p_over:.4f}")
else:
    print("    none")

print(f"\n  Largest raw excesses regardless of significance, top 12:")
for _, x in r.nlargest(12, "excess").iterrows():
    print(f"    {x.series[:52]:52s} excess {x.excess:+7.2f}  "
          f"own Jan sd {x.base_sd:6.2f}  z vs zero {x.z_vs_zero:+.2f}")

print(f"\n  How noisy is a January, by series? Distribution of each series' own")
print(f"  standard deviation of January steps over {YFROM}-{YTO}:")
print(f"    median {r.base_sd.median():.2f} log points, "
      f"quartiles {r.base_sd.quantile(.25):.2f} to {r.base_sd.quantile(.75):.2f}, "
      f"max {r.base_sd.max():.2f}")
print(f"    series whose own January noise is smaller than the {TARGET:.2f} signal: "
      f"{(r.base_sd < TARGET).sum()} of {m}")

print(f"\n  Excess steps, all {m} series: mean {r.excess.mean():+.3f}, "
      f"median {r.excess.median():+.3f} log points")
print(f"  Count with excess above target: {(r.excess > TARGET).sum()}")
print(f"  Count with excess below zero:   {(r.excess < 0).sum()}")

print("\n" + "=" * 96)
if k >= 1 and k < m / 2:
    print(f"T5 PASSES on its literal terms: {k} of {m} categories over-shoot, which is")
    print(f"at least one and fewer than half.")
else:
    print(f"T5 FAILS. F5 TRIGGERED." if k == 0 else f"T5 FAILS, {k} of {m} is not fewer than half.")
print("=" * 96)
r.to_csv("out/category_2023.csv", index=False)
print(f"wrote out/category_2023.csv")
