"""
11_lownoise_placebo.py - does selecting on low January noise manufacture the result?

The low-noise finding is post-hoc. The obvious failure mode: selecting series on a
small standard deviation, then declaring any movement large. If that were happening,
the same procedure applied to a year with no GST change would also throw up a cluster
of series moving by about a percent. This checks that directly.

Procedure, identical for every candidate year Y:
  1. compute each series' January steps 2010-2026, drop all GST years and drop Y
  2. keep series whose sd over what remains is below 0.465 log points
  3. record the January-Y excess for the kept series
A GST year should stand out. If it does not, the finding is selection.
"""
import numpy as np, pandas as pd
GST_JAN = {2003, 2004, 2023, 2024}
TGT = 100*np.log(1.08/1.07); CUT = TGT/2

d = pd.read_csv("out/analysis.csv"); d["index"]=pd.to_numeric(d["index"],errors="coerce")
w = d.pivot_table(index="date",columns="series",values="index",aggfunc="first").sort_index()

def jsteps(s):
    x=w[s].dropna(); o={}
    for dt,v in x.items():
        y,m=int(dt[:4]),int(dt[5:])
        if m==1 and f"{y-1}-12" in x.index: o[y]=100*(np.log(v)-np.log(x[f"{y-1}-12"]))
    return pd.Series(o).sort_index()

ALL={s:jsteps(s) for s in w.columns}

def run(year):
    exc=[]
    for s,g in ALL.items():
        g=g[(g.index>=2010)&(g.index<=2026)]
        if year not in g.index: continue
        base=g[~g.index.isin(GST_JAN|{year})]
        if len(base)<8: continue
        if base.std(ddof=1) >= CUT: continue
        exc.append(g.loc[year]-base.mean())
    e=np.array(exc)
    if len(e)==0: return None
    return dict(year=year, n=len(e), median=np.median(e), mean=e.mean(),
                frac_above_half=(e>TGT/2).mean(), frac_above_tgt=(e>TGT).mean(),
                q25=np.percentile(e,25), q75=np.percentile(e,75))

print("="*100)
print("Same low-noise selection applied to every January. GST years marked.")
print(f"Selection: own January sd < {CUT:.3f} log points. Full pass-through target {TGT:.3f}.")
print("="*100)
print(f"  {'year':6s} {'n kept':>7s} {'median':>8s} {'mean':>8s} {'IQR':>18s} "
      f"{'>0.47':>7s} {'>0.93':>7s}")
rows=[]
for y in range(2010,2027):
    r=run(y)
    if not r: continue
    rows.append(r)
    tag = "  <-- GST" if y in (2023,2024) else ""
    print(f"  {y:6d} {r['n']:7d} {r['median']:+8.3f} {r['mean']:+8.3f} "
          f"[{r['q25']:+6.2f},{r['q75']:+6.2f}] {r['frac_above_half']*100:6.0f}% "
          f"{r['frac_above_tgt']*100:6.0f}%{tag}")

t=pd.DataFrame(rows).set_index("year")
non=t.drop(index=[y for y in (2023,2024) if y in t.index])
print(f"\n  Non-GST Januaries: median excess averages {non['median'].mean():+.3f}, "
      f"sd across years {non['median'].std(ddof=1):.3f}")
for y in (2023,2024):
    if y in t.index:
        z=(t.loc[y,'median']-non['median'].mean())/non['median'].std(ddof=1)
        print(f"  {y}: median excess {t.loc[y,'median']:+.3f}, "
              f"{z:+.2f} sd from the non-GST average, "
              f"rank {int((non['median']<t.loc[y,'median']).sum())+1} of {len(non)+1}")

print("\n" + "="*100)
print("WATER SUPPLY, every January step in the file")
print("="*100)
g=ALL["Water Supply"]; g=g[g.index>=2010]
for y in g.index:
    tag=" <-- GST 7->8%" if y==2023 else " <-- GST 8->9%" if y==2024 else ""
    print(f"    Jan {y}  {g.loc[y]:+7.4f}{tag}")
print(f"\n    2023 target {TGT:.4f}   observed {g.loc[2023]:+.4f}   gap {g.loc[2023]-TGT:+.4f}")
t24=100*np.log(1.09/1.08)
print(f"    2024 target {t24:.4f}   observed {g.loc[2024]:+.4f}   gap {g.loc[2024]-t24:+.4f}")
print("\n    Index precision check, Water Supply values around each event:")
for dt in ["2022-12","2023-01","2023-12","2024-01"]:
    print(f"      {dt}  {w['Water Supply'].get(dt)}")
print("\n" + "="*100)
print("POLYTECHNIC EDUCATION, the government-absorption prediction")
print("="*100)
g=ALL["Polytechnic Education"]; g=g[g.index>=2015]
for y in g.index:
    tag=" <-- GST 7->8%" if y==2023 else " <-- GST 8->9%" if y==2024 else ""
    print(f"    Jan {y}  {g.loc[y]:+7.4f}{tag}")
print("\n    MOF states the government absorbs GST on publicly subsidised education.")
print("    A zero step in 2023 is what that policy predicts.")
