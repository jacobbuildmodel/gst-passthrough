"""
14_staggered.py - test MAS's own account of what happened.

MAS Macroeconomic Review, October 2023, footnote 16, verbatim:
  "the impact of the GST hike this year was staggered across several months, instead
   of passing through fully at the start of the year. Several retailers such as major
   supermarket chains announced a temporary absorption of the tax increase or offered
   a token discount early this year. In the absence of similar announcements for 2024
   thus far, the upcoming GST hike is assumed to pass through fully in January under
   the current baseline."

That is a falsifiable claim and the January-only test cannot see it. If pass-through
was staggered, the cumulative change from December through month h should reach the
statutory amount at some h greater than one.

    C(y, h) = 100 * ( ln P[y, month h] - ln P[y-1, Dec] )

fitted on non-GST years with the Chinese New Year control, event year predicted out
of sample, prediction standard error. Placebo is every non-GST year at the same
horizon, so the widening of the interval with h is priced in rather than ignored.

This test was not in THESIS.md by name. Anticipation and lag were named as threats in
the brief and listed in THESIS.md's confounds, and 04 ran the month-by-month window,
but the cumulative test with placebo is new and prompted by MAS's account. Label it
as such wherever it appears.
"""
import numpy as np, pandas as pd
from scipy import stats
from lunardate import LunarDate
from datetime import timedelta

GST_JAN = {2003, 2004, 2023, 2024}
TGT = {2023: 100*np.log(1.08/1.07), 2024: 100*np.log(1.09/1.08)}
YFROM, YTO = 2010, 2026

cny = {}
for y in range(1995, 2028):
    c = LunarDate(y, 1, 1).to_solar_date()
    cny[y] = sum(1 for k in range(1, 22) if (c - timedelta(days=k)).month == 1)/21.0

d = pd.read_csv("out/analysis.csv"); d["index"] = pd.to_numeric(d["index"], errors="coerce")
w = d.pivot_table(index="date", columns="series", values="index", aggfunc="first").sort_index()


def cum(series, h):
    """cumulative log change from prior December through month h, by year."""
    s = w[series].dropna(); out = {}
    for y in range(YFROM - 1, YTO + 2):
        a, b = f"{y-1}-12", f"{y}-{h:02d}"
        if a in s.index and b in s.index:
            out[y] = 100*(np.log(s[b]) - np.log(s[a]))
    return pd.Series(out).sort_index()


def excess(series, year, h):
    g = cum(series, h)
    g = g[(g.index >= YFROM) & (g.index <= YTO)]
    base = g[~g.index.isin(GST_JAN)]
    if year not in g.index or len(base) < 8: return None
    X = np.column_stack([np.ones(len(base)), [cny[y] for y in base.index]])
    yv = base.values
    XtXi = np.linalg.pinv(X.T @ X); b = XtXi @ X.T @ yv
    r = yv - X @ b; dof = len(base) - 2; s2 = r @ r / dof
    x0 = np.array([1.0, cny[year]])
    se = np.sqrt(s2*(1 + x0 @ XtXi @ x0)); e = g.loc[year] - x0 @ b
    return dict(excess=e, se=se, dof=dof,
                lo=e - stats.t.ppf(.975, dof)*se, hi=e + stats.t.ppf(.975, dof)*se,
                base_sd=base.std(ddof=1))


for S in ["All Items", "All Items Less Accommodation"]:
    if S not in w.columns: continue
    print("=" * 104)
    print(f"{S}: cumulative excess from December, by horizon")
    print("=" * 104)
    print(f"  {'through':>9s} {'2023 excess':>26s} {'target':>8s}   {'2024 excess':>26s} {'target':>8s}")
    MON = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun"}
    for h in range(1, 7):
        line = f"  {MON[h]:>9s} "
        for ev in (2023, 2024):
            r = excess(S, ev, h)
            if r is None: line += f"{'n/a':>36s}"; continue
            hit = "*" if (r["lo"] <= TGT[ev] <= r["hi"]) else " "
            zero = "z" if (r["lo"] <= 0 <= r["hi"]) else " "
            line += f" {r['excess']:+6.3f} [{r['lo']:+6.2f},{r['hi']:+6.2f}]{hit}{zero} {TGT[ev]:7.3f}  "
        print(line)
    print("   * = interval contains full statutory pass-through;  z = interval contains zero")
    print()

print("=" * 104)
print("PLACEBO. Cumulative December-to-April excess, All Items, every year 2010-2026.")
print("=" * 104)
vals = []
for y in range(YFROM, YTO + 1):
    r = excess("All Items", y, 4)
    if r is None: continue
    tag = "  <-- GST" if y in GST_JAN else ""
    vals.append((y, r["excess"]))
    print(f"  {y}  cumulative excess through April {r['excess']:+7.3f}{tag}")
non = np.array([v for y, v in vals if y not in GST_JAN])
print(f"\n  Non-GST years: mean {non.mean():+.3f}, sd {non.std(ddof=1):.3f}, "
      f"range [{non.min():+.3f}, {non.max():+.3f}]")
for y, v in vals:
    if y in (2023, 2024):
        z = (v - non.mean())/non.std(ddof=1)
        rank = int((non < v).sum()) + 1
        print(f"  {y}: {v:+.3f}, {z:+.2f} sd from the non-GST mean, "
              f"rank {rank} of {len(non)+1}")
print(f"\n  Full statutory pass-through 2023: {TGT[2023]:.3f}   2024: {TGT[2024]:.3f}")
