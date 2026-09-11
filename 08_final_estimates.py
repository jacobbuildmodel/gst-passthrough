"""
08_final_estimates.py - correct inference, then the pre-registered verdicts.

WHY THIS SUPERSEDES THE SE'S IN 03 AND 07. With a single treated observation, the
treated dummy fits that point exactly: its residual is zero and its leverage is one.
HC3 divides by (1 - leverage) squared, so it is undefined there, and statsmodels
warned about a divide by zero. Any robust standard error on a singleton dummy is
unreliable.

The correct question is not "how precisely is a coefficient estimated" but "how far
is the event year from what the baseline years predict, relative to how well the
baseline predicts a year it has not seen". So: fit on baseline years only, predict
the event year, and use the prediction standard error

    se = s * sqrt( 1 + x0' (X'X)^-1 x0 )

which includes both parameter uncertainty and the irreducible one-year noise. This is
wider than a regression SE, correctly.
"""
import numpy as np, pandas as pd
from scipy import stats
from lunardate import LunarDate
from datetime import timedelta

GST_JAN, GST_JUL = {2003, 2004, 2023, 2024}, {2007}
YFROM, YTO = 2010, 2026
TGT = {2003: 100*np.log(1.04/1.03), 2004: 100*np.log(1.05/1.04),
       2007: 100*np.log(1.07/1.05), 2023: 100*np.log(1.08/1.07),
       2024: 100*np.log(1.09/1.08)}

cny = {}
for y in range(1995, 2028):
    c = LunarDate(y, 1, 1).to_solar_date()
    cny[y] = sum(1 for k in range(1, 22) if (c - timedelta(days=k)).month == 1) / 21.0

d = pd.read_csv("out/analysis.csv")
d["index"] = pd.to_numeric(d["index"], errors="coerce")
w = d.pivot_table(index="date", columns="series", values="index", aggfunc="first").sort_index()


def steps(series, month):
    s = w[series].dropna(); pm = 12 if month == 1 else month - 1; out = {}
    for dt, v in s.items():
        y, m = int(dt[:4]), int(dt[5:])
        if m != month: continue
        k = f"{y-1 if month==1 else y}-{pm:02d}"
        if k in s.index: out[y] = 100*(np.log(v) - np.log(s[k]))
    return pd.Series(out).sort_index()


def predict_excess(series, year, month, y_from, y_to, use_cny):
    g = steps(series, month)
    g = g[(g.index >= y_from) & (g.index <= y_to)]
    excl = GST_JAN if month == 1 else GST_JUL
    base = g[~g.index.isin(excl)]
    if year not in g.index or len(base) < 8: return None
    cols = [np.ones(len(base))]
    if use_cny: cols.append(np.array([cny[y] for y in base.index]))
    X = np.column_stack(cols); y = base.values
    XtXi = np.linalg.pinv(X.T @ X); beta = XtXi @ X.T @ y
    resid = y - X @ beta; dof = len(base) - X.shape[1]
    s2 = resid @ resid / dof
    x0 = np.array([1.0] + ([cny[year]] if use_cny else []))
    pred = x0 @ beta
    se = np.sqrt(s2 * (1 + x0 @ XtXi @ x0))
    exc = g.loc[year] - pred
    t = exc / se
    return dict(series=series, year=year, observed=g.loc[year], predicted=pred,
                excess=exc, se=se, dof=dof, n_base=len(base),
                p_vs_zero=2*(1-stats.t.cdf(abs(t), dof)),
                lo=exc - stats.t.ppf(.975, dof)*se, hi=exc + stats.t.ppf(.975, dof)*se)


print("=" * 102)
print("HEADLINE ESTIMATES, prediction-interval inference, Chinese New Year controlled")
print("=" * 102)
res = {}
for ev, mth, yf, yt in [(2023, 1, 2010, 2026), (2024, 1, 2010, 2026), (2007, 7, 2005, 2026)]:
    tgt = TGT[ev]
    note = "clean" if ev != 2024 else "SEAM - basket revision in this month"
    print(f"\n### {ev}  target {tgt:.4f} log points   [{note}]")
    for s in ["All Items", "All Items Less Accommodation"]:
        if s not in w.columns: continue
        r = predict_excess(s, ev, mth, yf, yt, use_cny=(mth == 1))
        if r is None: continue
        res[(ev, s)] = r
        v = ("EXCLUDES target" if (r['hi'] < tgt or r['lo'] > tgt) else "includes target")
        print(f"  {s:30s} observed {r['observed']:+6.3f}  predicted {r['predicted']:+6.3f}"
              f"  excess {r['excess']:+6.3f}  se {r['se']:.3f}"
              f"  95% CI [{r['lo']:+.2f},{r['hi']:+.2f}]  {v}")

print("\n" + "=" * 102)
print("POWER. Can this design detect full pass-through at all?")
print("=" * 102)
plac = [predict_excess("All Items", y, 1, 2010, 2026, True) for y in range(2010, 2027)
        if y not in GST_JAN]
plac = [p for p in plac if p]
sd = np.std([p["excess"] for p in plac], ddof=1)
tgt23 = TGT[2023]
print(f"  Placebo January excesses, All Items, CNY controlled: n={len(plac)}, sd={sd:.3f} log points")
print(f"  range [{min(p['excess'] for p in plac):+.3f}, {max(p['excess'] for p in plac):+.3f}]")
print(f"  Signal to be detected: {tgt23:.3f} log points, which is {tgt23/sd:.2f} sd.")
ncp = tgt23 / sd
power = 1 - stats.norm.cdf(1.96 - ncp) + stats.norm.cdf(-1.96 - ncp)
print(f"  Power of a two-sided 5% test with ONE event: {power*100:.0f} per cent.")
need = (( (1.96 + 0.842) * sd / tgt23 ) ** 2)
print(f"  Events needed for 80 per cent power: {np.ceil(need):.0f}.")
print(f"  January GST events in the era with usable data: 2 (2023 and 2024), and one")
print(f"  of those sits on a basket revision. So the design has {need:.1f} times fewer")
print(f"  events than it needs, and this is a property of the world, not of the code.")

print("\n" + "=" * 102)
print("IS THE 2007 RESULT THE TAX? Contribution of Housing & Utilities.")
print("=" * 102)
W = {"Food":2117,"Clothing & Footwear":212,"Housing & Utilities":2485,
     "Household Durables & Services":488,"Health":651,"Transport":1709,
     "Information & Communication":477,"Recreation, Sport & Culture":714,
     "Education":670,"Miscellaneous Goods & Services":477}
tot = hu = 0.0
for s, wt in W.items():
    r = predict_excess(s, 2007, 7, 2005, 2026, False)
    if r is None: continue
    c = r["excess"] * wt / 10000; tot += c
    if s == "Housing & Utilities": hu = c
r07 = predict_excess("All Items", 2007, 7, 2005, 2026, False)
print(f"  All Items July 2007 excess           {r07['excess']:+.3f}  se {r07['se']:.3f}"
      f"  95% CI [{r07['lo']:+.2f},{r07['hi']:+.2f}]")
print(f"  full pass-through target              {TGT[2007]:+.3f}")
print(f"  sum of weighted division excesses    {tot:+.3f}")
print(f"  of which Housing & Utilities alone   {hu:+.3f}  ({100*hu/tot:.0f} per cent of it)")
rest = (tot - hu) / ((10000 - W['Housing & Utilities']) / 10000)
print(f"  the rest of the basket, rescaled     {rest:+.3f}  against a target of {TGT[2007]:.3f}")
print(f"\n  Singapore private residential prices were in a boom in 2007. The single")
print(f"  largest contributor to the one GST event big enough to detect is the division")
print(f"  that boom sits in, so the aggregate step cannot be attributed to the tax.")
