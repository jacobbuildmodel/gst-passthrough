"""
10_lownoise.py - EXPLORATORY, NOT PRE-REGISTERED. Label it that way everywhere.

Test T6 failed because a 0.93 log point signal is smaller than January noise in the
aggregate. That is a statement about the aggregate. It does not have to hold for
every series. Some prices are administered and simply do not move in January for any
other reason, and in those the same signal may sit well above the noise.

This analysis was not pre-registered. It was suggested by the T5 output, where two
series produced infinite t statistics because their baseline January variance was
zero. An infinite t is not a finding, it is a degenerate standard error, and the
honest response is to look at the series descriptively rather than to report the
p-value.

Selection rule, fixed before looking at the 2023 values: keep series whose standard
deviation of January steps over 2010-2026, excluding GST years, is below half the
0.9302 target. Then report the January 2023 step against that baseline, descriptively.
"""
import numpy as np, pandas as pd
from lunardate import LunarDate
from datetime import timedelta

GST_JAN = {2003, 2004, 2023, 2024}
TGT = 100*np.log(1.08/1.07)
CUT = TGT/2

d = pd.read_csv("out/analysis.csv")
d["index"] = pd.to_numeric(d["index"], errors="coerce")
w = d.pivot_table(index="date", columns="series", values="index", aggfunc="first").sort_index()
meta = d.groupby("series").agg(level=("level","first"), parent=("parent","first"))

def jsteps(s):
    x=w[s].dropna(); o={}
    for dt,v in x.items():
        y,m=int(dt[:4]),int(dt[5:])
        if m==1 and f"{y-1}-12" in x.index: o[y]=100*(np.log(v)-np.log(x[f"{y-1}-12"]))
    return pd.Series(o).sort_index()

rows=[]
for s in w.columns:
    g=jsteps(s); g=g[(g.index>=2010)&(g.index<=2026)]
    base=g[~g.index.isin(GST_JAN)]
    if 2023 not in g.index or len(base)<8: continue
    sd=base.std(ddof=1)
    rows.append(dict(series=s, level=meta.level[s], parent=meta.parent[s],
                     base_sd=sd, base_mean=base.mean(),
                     jan2023=g.loc[2023], excess=g.loc[2023]-base.mean(),
                     jan2024=g.loc[2024] if 2024 in g.index else np.nan,
                     n_nonzero=(base.abs()>0.005).sum(), n_base=len(base)))
r=pd.DataFrame(rows)
q=r[r.base_sd<CUT].sort_values("excess", ascending=False)

print("="*104)
print("EXPLORATORY, NOT PRE-REGISTERED.")
print(f"Series whose own January noise is small: sd of January steps < {CUT:.3f} log points")
print(f"(half the {TGT:.3f} full pass-through target). {len(q)} of {len(r)} series qualify.")
print("="*104)
print(f"  {'series':50s} {'JanSD':>6s} {'base':>6s} {'Jan23':>7s} {'excess':>7s} {'Jan24':>7s}  moves")
for _,x in q.iterrows():
    print(f"  {x.series[:50]:50s} {x.base_sd:6.3f} {x.base_mean:+6.3f} {x.jan2023:+7.3f} "
          f"{x.excess:+7.3f} {x.jan2024:+7.3f}  {x.n_nonzero}/{x.n_base}")

near=q[(q.excess>0.5)&(q.excess<1.5)]
print(f"\n  Of these, {len(near)} show a January 2023 excess between 0.5 and 1.5 log points,")
print(f"  which brackets the {TGT:.3f} full pass-through figure:")
for _,x in near.iterrows():
    print(f"    {x.series[:50]:50s} excess {x.excess:+.3f}")

print("\n" + "="*104)
print("WATER SUPPLY IN DETAIL, since it is the cleanest case in the file")
print("="*104)
ws=w["Water Supply"].dropna()
print("  January steps, log points:")
g=jsteps("Water Supply")
for y in range(2015, 2027):
    if y in g.index:
        tag = "  <-- GST 7 to 8%" if y==2023 else "  <-- GST 8 to 9%" if y==2024 else ""
        print(f"    Jan {y}  {g.loc[y]:+7.3f}{tag}")
print(f"\n  target for 2023 {TGT:.3f}, for 2024 {100*np.log(1.09/1.08):.3f}")
print("""
  CAUTION before this is used for anything. Water Supply is an administered price.
  A January move in an administered price is a decision, not a market outcome, and
  Singapore has revised water prices for reasons other than GST inside this window.
  Tobacco is worse: excise duty rose in Budget 2023. Neither belongs in a claim about
  how firms respond to a tax without checking the administrative record for that
  specific price, which this analysis has not done.""")
r.to_csv("out/lownoise_2023.csv", index=False)
print(f"\nwrote out/lownoise_2023.csv")
