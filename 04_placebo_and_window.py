"""
04_placebo_and_window.py

T6  placebo. Apply the same estimator to non-GST event months. If placebo months
    show excess steps like the GST months, the estimator is measuring seasonality.
T4  the mid-year test, already run in 03. Here it is decomposed, because the 2007
    aggregate may be carrying the property boom rather than the tax.
Anticipation and lag. The brief names these. A step measured Dec->Jan misses any
    repricing done in December or spread over Q1.
"""
import numpy as np, pandas as pd, statsmodels.api as sm

GST_JAN = {2003, 2004, 2023, 2024}
GST_JUL = {2007}
d = pd.read_csv("out/analysis.csv")
d["index"] = pd.to_numeric(d["index"], errors="coerce")
w = d.pivot_table(index="date", columns="series", values="index", aggfunc="first").sort_index()


def steps(series, month):
    s = w[series].dropna()
    prev_m, out = (12 if month == 1 else month - 1), {}
    for dt, v in s.items():
        y, m = int(dt[:4]), int(dt[5:])
        if m != month:
            continue
        key = f"{y-1 if month==1 else y}-{prev_m:02d}"
        if key in s.index:
            out[y] = 100 * (np.log(v) - np.log(s[key]))
    return pd.Series(out).sort_index()


def excess(series, month, year, y_from, y_to, excluded):
    g = steps(series, month)
    g = g[(g.index >= y_from) & (g.index <= y_to)]
    g = g.loc[[y for y in g.index if y == year or y not in excluded]]
    if year not in g.index or len(g) < 6:
        return None
    X = sm.add_constant(pd.DataFrame({"t": (g.index == year).astype(float)}, index=g.index))
    m = sm.OLS(g.values, X.values).fit(cov_type="HC3")
    return m.params[1], m.bse[1], m.pvalues[1]


print("=" * 92)
print("T6 PLACEBO. All Items, January step, each non-GST year treated as if it were the event.")
print("Baseline Januaries 2010-2026 excluding all GST years and the year being tested.")
print("=" * 92)
hits = 0
place = []
for y in range(2010, 2027):
    if y in GST_JAN:
        continue
    r = excess("All Items", 1, y, 2010, 2026, GST_JAN | {y} - {y})
    if r is None:
        continue
    e, se, p = r
    place.append(e)
    mark = " <-- significant" if p < 0.05 else ""
    hits += p < 0.05
    print(f"  Jan {y}   excess {e:+6.3f}  se {se:.3f}  p {p:.3f}{mark}")
print(f"\n  {hits} of {len(place)} placebo Januaries significant at p<0.05. "
      f"Expected by chance at 5%: {0.05*len(place):.1f}")
print(f"  placebo excesses: mean {np.mean(place):+.3f}, sd {np.std(place, ddof=1):.3f}, "
      f"range [{min(place):+.3f}, {max(place):+.3f}]")
print(f"  For scale, the 2023 target is +0.930 and the 2023 estimate was +0.100.")
print(f"  A true 0.93 step sits at {0.93/np.std(place, ddof=1):.2f} placebo standard deviations.")

print("\n" + "=" * 92)
print("ANTICIPATION AND LAG. Excess step in each month around the event, All Items.")
print("If firms repriced early or staggered, the Dec-to-Jan step alone understates.")
print("=" * 92)
for ev, evm in [(2023, 1), (2024, 1), (2007, 7)]:
    print(f"\n  --- {ev} event ---")
    tot = 0.0
    for off in (-1, 0, 1, 2, 3):
        m = evm + off
        y = ev
        if m < 1:
            m += 12; y -= 1
        if m > 12:
            m -= 12; y += 1
        exc = GST_JAN if m == 1 else GST_JUL if m == 7 else set()
        yf, yt = (2005, 2026) if ev == 2007 else (2010, 2026)
        r = excess("All Items", m, y, yf, yt, exc)
        if r is None:
            print(f"    {y}-{m:02d}  (insufficient baseline)")
            continue
        e, se, p = r
        tot += e
        tag = "  <-- event month" if off == 0 else ""
        print(f"    {y}-{m:02d}  excess {e:+6.3f}  se {se:.3f}  p {p:.3f}  "
              f"cumulative {tot:+6.3f}{tag}")

print("\n" + "=" * 92)
print("IS THE 2007 RESULT THE TAX OR THE PROPERTY BOOM?")
print("Decomposing the All Items July 2007 excess using 2019-base division weights.")
print("The weights are from the wrong era and are used only to show which divisions")
print("carry the aggregate, not to produce a published number.")
print("=" * 92)
W2019 = {"Food": 2117, "Clothing & Footwear": 212, "Housing & Utilities": 2485,
         "Household Durables & Services": 488, "Health": 651, "Transport": 1709,
         "Information & Communication": 477, "Recreation, Sport & Culture": 714,
         "Education": 670, "Miscellaneous Goods & Services": 477}
tot = 0.0
parts = []
for s, wt in sorted(W2019.items(), key=lambda kv: -kv[1]):
    r = excess(s, 7, 2007, 2005, 2026, GST_JUL)
    if r is None:
        continue
    e, se, p = r
    c = e * wt / 10000
    tot += c
    parts.append((s, wt, e, c))
    print(f"  {s:34s} w {wt:5d}  excess {e:+7.3f}  contributes {c:+6.3f}")
print(f"\n  sum of weighted contributions      {tot:+.3f} log points")
print(f"  directly estimated All Items excess +1.815 log points")
print(f"  full pass-through target             1.887 log points")
hu = [p for p in parts if p[0] == "Housing & Utilities"][0]
print(f"\n  Housing & Utilities alone contributes {hu[3]:+.3f} of that {tot:+.3f}.")
print(f"  Excluding it, the rest of the basket contributes {tot-hu[3]:+.3f}")
print(f"  and rescaled to its own weight share "
      f"({(10000-hu[1])/10000:.3f}) that is {(tot-hu[3])/((10000-hu[1])/10000):+.3f} log points.")
