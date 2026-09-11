"""
02_parallel_trends.py - pre-registered test T1, and its fail condition F1.

T1: over the 24 months before each of the 2023 and 2024 events, an OLS slope fitted
to the monthly log difference between the GST-liable aggregate and the
exempt-or-absorbed control aggregate is not distinguishable from zero at p < 0.05,
for both events.

F1: the pre-trend slope is significant at p < 0.05 for either event. The two-group
DiD is then declared invalid and the secondary design is used.

Treatment  All Items Less Accommodation   (published by SingStat, GST-liable heavy)
Control    Accommodation                  (actual + imputed residential rentals plus
                                           housing maintenance; rentals are exempt
                                           supplies under the Fourth Schedule)

Reads out/analysis.csv. Prints its working. Writes nothing.
"""
import numpy as np, pandas as pd, statsmodels.api as sm

d = pd.read_csv("out/analysis.csv")
d["index"] = pd.to_numeric(d["index"], errors="coerce")
w = d.pivot_table(index="date", columns="series", values="index", aggfunc="first").sort_index()

TREAT, CONTROL = "All Items Less Accommodation", "Accommodation"
print(f"treatment: {TREAT}\ncontrol:   {CONTROL}\n")

lg = np.log(w[[TREAT, CONTROL]].dropna())
gap = 100 * (lg[TREAT] - lg[CONTROL])
print(f"gap series runs {gap.index[0]} to {gap.index[-1]}, {len(gap)} months\n")

verdict = {}
for ev, label in [("2023-01", "7% to 8%"), ("2024-01", "8% to 9%")]:
    pre = gap[gap.index < ev].tail(24)
    y = pre.values
    x = sm.add_constant(np.arange(len(y), dtype=float))
    m = sm.OLS(y, x).fit()
    slope, se, p = m.params[1], m.bse[1], m.pvalues[1]
    ok = p >= 0.05
    verdict[ev] = ok
    print(f"--- {ev} ({label}) ---")
    print(f"  window {pre.index[0]} to {pre.index[-1]}, n={len(y)}")
    print(f"  gap moved from {y[0]:.3f} to {y[-1]:.3f} log points ({y[-1]-y[0]:+.3f})")
    print(f"  slope {slope:+.4f} log points per month, se {se:.4f}, t {m.tvalues[1]:+.2f}, p {p:.2e}")
    print(f"  implied drift over the 24 months: {slope*24:+.2f} log points")
    print(f"  T1 {'PASSES' if ok else 'FAILS'} for this event\n")

allpass = all(verdict.values())
print("=" * 68)
print(f"T1 {'PASSES' if allpass else 'FAILS'} overall.")
print(f"F1 {'not triggered' if allpass else 'TRIGGERED'}.")
if not allpass:
    print("""
The briefed difference-in-differences design is declared INVALID and is not used to
produce any published estimate. This was pre-registered in THESIS.md before the data
was downloaded, with the reason stated: the only exempt category with meaningful CPI
weight is accommodation, and Singapore accommodation was in an extraordinary rental
cycle across the pre-period.

The analysis proceeds to the secondary design, in which each series is its own
control across years.""")
