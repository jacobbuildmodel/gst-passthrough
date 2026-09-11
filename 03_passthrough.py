"""
03_passthrough.py - the secondary design. Each series is its own control across years.

For series s and event month m in year y:
    step(y) = 100 * ( ln P[y, m] - ln P[y-1, m-1] )     the month-on-month log change
Estimate the excess step by OLS of step(y) on a constant and a treated dummy, across
a window of years, with every GST-change year excluded from the baseline. The
coefficient on the dummy is the estimated pass-through, with HC3 robust standard
errors.

Everything is reported in LOG POINTS, so the mechanical full-pass-through targets are
converted to log points too rather than compared against percent:

    2003  1.04/1.03  = +0.9709 pct = 0.9662 log points
    2004  1.05/1.04  = +0.9615 pct = 0.9569 log points
    2007  1.07/1.05  = +1.9048 pct = 1.8868 log points
    2023  1.08/1.07  = +0.9346 pct = 0.9302 log points
    2024  1.09/1.08  = +0.9259 pct = 0.9217 log points

Reads out/analysis.csv. Writes out/event_estimates.csv.
"""
import numpy as np, pandas as pd, statsmodels.api as sm

EVENTS = {2003: (1, 0.03, 0.04), 2004: (1, 0.04, 0.05), 2007: (7, 0.05, 0.07),
          2023: (1, 0.07, 0.08), 2024: (1, 0.08, 0.09)}
GST_JAN_YEARS = {2003, 2004, 2023, 2024}
GST_JUL_YEARS = {2007}

d = pd.read_csv("out/analysis.csv")
d["index"] = pd.to_numeric(d["index"], errors="coerce")
w = d.pivot_table(index="date", columns="series", values="index", aggfunc="first").sort_index()
lvl = d.groupby("series")["level"].first()


def steps(series, month):
    """month-on-month log change into `month`, indexed by year. log points."""
    s = w[series].dropna()
    prev_m, out = (12 if month == 1 else month - 1), {}
    for dt, v in s.items():
        y, m = int(dt[:4]), int(dt[5:])
        if m != month:
            continue
        py = y - 1 if month == 1 else y
        key = f"{py}-{prev_m:02d}"
        if key in s.index:
            out[y] = 100 * (np.log(v) - np.log(s[key]))
    return pd.Series(out).sort_index()


def estimate(series, event_year, y_from, y_to):
    month = EVENTS[event_year][0]
    excluded = GST_JAN_YEARS if month == 1 else GST_JUL_YEARS
    g = steps(series, month)
    g = g[(g.index >= y_from) & (g.index <= y_to)]
    keep = [y for y in g.index if y == event_year or y not in excluded]
    g = g.loc[keep]
    if event_year not in g.index or len(g) < 6:
        return None
    treat = (g.index == event_year).astype(float)
    X = sm.add_constant(pd.DataFrame({"treated": treat}, index=g.index))
    m = sm.OLS(g.values, X.values).fit(cov_type="HC3")
    base = g[g.index != event_year]
    return dict(series=series, event=event_year, n_baseline=len(base),
                baseline_mean=base.mean(), baseline_sd=base.std(ddof=1),
                observed=g.loc[event_year], excess=m.params[1], se=m.bse[1],
                t=m.tvalues[1], p=m.pvalues[1],
                lo=m.conf_int()[1][0], hi=m.conf_int()[1][1])


def target(ev):
    _, o, n = EVENTS[ev]
    return 100 * np.log((1 + n) / (1 + o))


HEADS = ["All Items", "All Items Less Accommodation", "All Items Less Imputed Rentals For Housing"]
DIVS = sorted([s for s in lvl.index if lvl[s] == 1])

rows = []
print("=" * 96)
print("HEADLINE AGGREGATES. Baseline Januaries 2010-2026 / Julys 2005-2026, GST years excluded.")
print("=" * 96)
for ev in (2023, 2024, 2007, 2004, 2003):
    yf, yt = (2005, 2026) if ev == 2007 else (2010, 2026) if ev >= 2023 else (1995, 2015)
    print(f"\n### {ev} event, full pass-through target {target(ev):.4f} log points "
          f"(baseline years {yf}-{yt})")
    for s in HEADS + DIVS:
        if s not in w.columns:
            continue
        r = estimate(s, ev, yf, yt)
        if r is None:
            continue
        r["target"] = target(ev)
        r["gap_vs_target"] = r["excess"] - r["target"]
        rows.append(r)
        flag = ""
        if r["p"] < 0.05:
            flag = "*"
        if r["excess"] - 1.96 * r["se"] > r["target"]:
            flag = "OVER"
        elif r["excess"] + 1.96 * r["se"] < r["target"]:
            flag = "under"
        print(f"  {s[:44]:44s} obs {r['observed']:+6.3f}  base {r['baseline_mean']:+6.3f}"
              f"  excess {r['excess']:+6.3f} (se {r['se']:.3f}, p {r['p']:.3f})"
              f"  [{r['lo']:+.2f},{r['hi']:+.2f}] {flag}")

out = pd.DataFrame(rows)
out.to_csv("out/event_estimates.csv", index=False)
print(f"\nwrote out/event_estimates.csv, {len(out)} rows")
