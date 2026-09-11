"""
05_verify.py - two separate jobs that must not be confused.

JOB 1 (pipeline validation). Pre-seam only. Year-on-year rates computed from this
file must reproduce the rates MTI printed contemporaneously on the 2019 base. Index
LEVELS will not match, because the bases differ. Percentage changes must, because
ip-e61 says the old series was linked in by a single scalar link factor, and a scalar
leaves percentage changes unchanged. If these fail, nothing downstream is usable.

JOB 2 (measuring the revision). Post-seam. A year-on-year rate for January 2024
spans the basket change, so the current file and the contemporaneous release SHOULD
disagree. The size of that disagreement is the reweighting effect on the published
number. It is not a pipeline error and must not be reported as one.
"""
import pandas as pd

d = pd.read_csv("out/analysis.csv")
d["index"] = pd.to_numeric(d["index"], errors="coerce")
w = d.pivot_table(index="date", columns="series", values="index", aggfunc="first").sort_index()

def yoy(series, dt):
    y, m = int(dt[:4]), int(dt[5:])
    a, b = w[series].get(dt), w[series].get(f"{y-1}-{m:02d}")
    return None if (pd.isna(a) or pd.isna(b)) else 100 * (a / b - 1)

TOL = 0.06  # MTI prints one decimal, so rounding alone permits 0.05

print("=" * 88)
print("JOB 1  PIPELINE VALIDATION, pre-seam only")
print("       source: MTI, Consumer Price Developments in January 2023, 23 Feb 2023")
print("=" * 88)
PRE = [("All Items", "2023-01", 6.6), ("Food", "2023-01", 8.1),
       ("Accommodation", "2023-01", 5.0)]
ok = True
for s, dt, pub in PRE:
    got = yoy(s, dt)
    if got is None:
        print(f"  {s:16s} {dt}  series not available"); continue
    good = abs(got - pub) < TOL
    ok &= good
    print(f"  {s:16s} {dt}  computed {got:6.3f}%  published {pub:4.1f}%  "
          f"diff {got-pub:+.3f}  {'OK' if good else 'MISMATCH'}")
print(f"\n  PIPELINE {'VALIDATED' if ok else 'BROKEN - stop here'}")

print("\n" + "=" * 88)
print("JOB 2  MEASURING THE REVISION, post-seam")
print("       source: MTI, Consumer Price Developments in January 2024, 23 Feb 2024")
print("=" * 88)
got = yoy("All Items", "2024-01")
pub = 2.9
print(f"  All Items January 2024 year-on-year")
print(f"    as published at the time, 2019 base, HES 2017/18 weights   {pub:.1f}%")
print(f"    as it stands now,         2024 base, HES 2023 weights      {got:.3f}%")
print(f"    revision                                                   {got-pub:+.3f} pp")
print(f"\n  Full statutory pass-through of the 8 to 9 per cent change is 0.926 per cent,")
print(f"  and the official GST contribution is quoted as 1.0 percentage point. The")
print(f"  rebasing alone moved this month's published inflation rate by {got-pub:+.2f} pp,")
print(f"  which is {abs(got-pub)/1.0*100:.0f} per cent of the entire official GST effect.")
print(f"\n  That is the bound. The January 2024 event cannot be estimated from this file,")
print(f"  because a revision of this size sits on top of a signal of that size.")

print("\n" + "=" * 88)
print("THE SEAM IS COMPOSITIONAL, NOT ONLY A REWEIGHTING")
print("=" * 88)
first = d.groupby("series")["date"].min()
new = sorted(first[first == "2024-01"].index)
print(f"  {len(new)} of {d.series.nunique()} series in this file begin exactly at 2024-01.")
print(f"  They did not exist in the old basket, so the January 2024 aggregate changes")
print(f"  composition as well as weights. Examples: {', '.join(new[:4])}.")
