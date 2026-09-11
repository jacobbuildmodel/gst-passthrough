"""
07_cny_controlled.py - redo the January estimates controlling for Chinese New Year.

Why this is necessary. MTI's own January 2023 release attributes that month's price
movement to "the one-off effect of the 1%-point GST increase as well as seasonal
effects associated with the Chinese New Year". Chinese New Year moves between
22 January and 19 February, and the pre-festival buying period moves with it. In the
2010-2026 window, 2023 has the EARLIEST New Year (22 January) and therefore the most
January pre-festival pressure, while 2024 has a late one (10 February) and much less.
That biases the 2023 estimate up and the 2024 estimate down, in exactly the pattern
the uncontrolled results showed.

Control: the share of the 21 days before Chinese New Year that fall in January.
    2023  New Year 22 Jan, window 1-21 Jan, share 1.000  (maximum in the window)
    2024  New Year 10 Feb, window 20 Jan-9 Feb, share 0.571
Dates computed with the lunardate package and cross-checked against five known years.

Model, per series:  jan_step(y) = a + b * cny_share(y) + c * treated(y) + e
HC3 robust standard errors. Every GST year is excluded from the baseline.
"""
import numpy as np, pandas as pd, statsmodels.api as sm
from lunardate import LunarDate
from datetime import date, timedelta

GST_JAN = {2003, 2004, 2023, 2024}
YFROM, YTO = 2010, 2026
TARGETS = {2023: 100 * np.log(1.08 / 1.07), 2024: 100 * np.log(1.09 / 1.08)}

cny_share = {}
for y in range(YFROM - 1, YTO + 2):
    c = LunarDate(y, 1, 1).to_solar_date()
    days = [c - timedelta(days=k) for k in range(1, 22)]
    cny_share[y] = sum(1 for dd in days if dd.month == 1) / 21.0

print("Chinese New Year and the share of its 21-day run-up falling in January")
for y in range(YFROM, YTO + 1):
    c = LunarDate(y, 1, 1).to_solar_date()
    mark = "   <-- GST event" if y in (2023, 2024) else ""
    print(f"  {y}  {c.isoformat()}   share {cny_share[y]:.3f}{mark}")

d = pd.read_csv("out/analysis.csv")
d["index"] = pd.to_numeric(d["index"], errors="coerce")
w = d.pivot_table(index="date", columns="series", values="index", aggfunc="first").sort_index()


def jan_steps(series):
    s = w[series].dropna()
    out = {}
    for dt, v in s.items():
        y, m = int(dt[:4]), int(dt[5:])
        if m == 1 and f"{y-1}-12" in s.index:
            out[y] = 100 * (np.log(v) - np.log(s[f"{y-1}-12"]))
    return pd.Series(out).sort_index()


def fit(series, year, with_cny):
    g = jan_steps(series)
    g = g[(g.index >= YFROM) & (g.index <= YTO)]
    g = g.loc[[y for y in g.index if y == year or y not in GST_JAN]]
    if year not in g.index or len(g) < 8:
        return None
    X = pd.DataFrame({"treated": (g.index == year).astype(float)}, index=g.index)
    if with_cny:
        X["cny"] = [cny_share[y] for y in g.index]
    X = sm.add_constant(X)
    m = sm.OLS(g.values, X.values).fit(cov_type="HC3")
    i = list(X.columns).index("treated")
    return dict(excess=m.params[i], se=m.bse[i], p=m.pvalues[i],
                lo=m.conf_int()[i][0], hi=m.conf_int()[i][1],
                cny_coef=(m.params[list(X.columns).index("cny")] if with_cny else np.nan),
                resid_sd=np.sqrt(m.scale))


AGGS = ["All Items", "All Items Less Accommodation",
        "All Items Less Imputed Rentals For Housing", "Food",
        "Food & Beverage Serving Services", "Food Excl Food & Beverage Serving Services"]

for ev in (2023, 2024):
    tgt = TARGETS[ev]
    print("\n" + "=" * 100)
    print(f"JANUARY {ev} EVENT.  full pass-through target {tgt:.4f} log points"
          + ("   [SEAM: basket revision in this month, not an estimate]" if ev == 2024 else "   [clean]"))
    print("=" * 100)
    print(f"  {'series':44s} {'no control':>22s}   {'CNY controlled':>26s}")
    for s in AGGS:
        if s not in w.columns:
            continue
        a, b = fit(s, ev, False), fit(s, ev, True)
        if a is None or b is None:
            continue
        excl = "excludes target" if (b["hi"] < tgt or b["lo"] > tgt) else "includes target"
        print(f"  {s[:44]:44s} {a['excess']:+6.3f} (se {a['se']:.3f})   "
              f"{b['excess']:+6.3f} (se {b['se']:.3f}) [{b['lo']:+.2f},{b['hi']:+.2f}] {excl}")

print("\n" + "=" * 100)
print("T6 PLACEBO, REDONE WITH THE CNY CONTROL. All Items.")
print("=" * 100)
place = []
for y in range(YFROM, YTO + 1):
    if y in GST_JAN:
        continue
    r = fit("All Items", y, True)
    if r:
        place.append((y, r["excess"], r["p"]))
sig = [x for x in place if x[2] < 0.05]
es = np.array([x[1] for x in place])
for y, e, p in place:
    print(f"  Jan {y}  excess {e:+6.3f}  p {p:.3f}{'  <-- significant' if p < 0.05 else ''}")
print(f"\n  {len(sig)} of {len(place)} significant at p<0.05, {0.05*len(place):.1f} expected by chance")
print(f"  placebo sd {es.std(ddof=1):.3f} log points, range [{es.min():+.3f}, {es.max():+.3f}]")
print(f"  A true 0.930 step is {0.930/es.std(ddof=1):.2f} placebo standard deviations.")
r23 = fit("All Items", 2023, True)
print(f"\n  2023 estimate {r23['excess']:+.3f} sits at the "
      f"{100*(es < r23['excess']).mean():.0f}th percentile of the placebo distribution.")
