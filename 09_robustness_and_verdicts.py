"""
09_robustness_and_verdicts.py

Three jobs.
1. Match the baseline windows. "All Items Less Accommodation" starts in 2015, so its
   estimate used a shorter and calmer baseline than "All Items". Comparing the two on
   different windows is not a comparison. Rerun both on 2015-2026.
2. Redo T5 with the Chinese New Year control and prediction-interval inference.
3. Record the pre-registered verdicts, pass or fail, as committed in THESIS.md.
"""
import numpy as np, pandas as pd
from scipy import stats
from lunardate import LunarDate
from datetime import timedelta

GST_JAN = {2003, 2004, 2023, 2024}
TGT23 = 100*np.log(1.08/1.07)
cny = {}
for y in range(1995, 2028):
    c = LunarDate(y,1,1).to_solar_date()
    cny[y] = sum(1 for k in range(1,22) if (c-timedelta(days=k)).month == 1)/21.0

d = pd.read_csv("out/analysis.csv")
d["index"] = pd.to_numeric(d["index"], errors="coerce")
w = d.pivot_table(index="date", columns="series", values="index", aggfunc="first").sort_index()

def jsteps(s):
    x = w[s].dropna(); out = {}
    for dt, v in x.items():
        y, m = int(dt[:4]), int(dt[5:])
        if m == 1 and f"{y-1}-12" in x.index: out[y] = 100*(np.log(v)-np.log(x[f"{y-1}-12"]))
    return pd.Series(out).sort_index()

def pex(s, year, yf, yt, use_cny=True, minbase=8):
    g = jsteps(s); g = g[(g.index>=yf)&(g.index<=yt)]
    base = g[~g.index.isin(GST_JAN)]
    if year not in g.index or len(base) < minbase: return None
    cols=[np.ones(len(base))]
    if use_cny: cols.append(np.array([cny[y] for y in base.index]))
    X=np.column_stack(cols); yv=base.values
    XtXi=np.linalg.pinv(X.T@X); b=XtXi@X.T@yv; r=yv-X@b
    dof=len(base)-X.shape[1]; s2=r@r/dof
    x0=np.array([1.0]+([cny[year]] if use_cny else []))
    se=np.sqrt(s2*(1+x0@XtXi@x0)); exc=g.loc[year]-x0@b
    return dict(excess=exc, se=se, dof=dof, n=len(base),
                lo=exc-stats.t.ppf(.975,dof)*se, hi=exc+stats.t.ppf(.975,dof)*se,
                p=2*(1-stats.t.cdf(abs(exc/se),dof)))

print("="*100); print("1. MATCHED BASELINE WINDOWS, 2015-2026, January 2023 event")
print("   target %.4f log points" % TGT23); print("="*100)
for s in ["All Items","All Items Less Accommodation","All Items Less Imputed Rentals For Housing"]:
    for yf in (2010, 2015):
        r = pex(s, 2023, yf, 2026)
        if r is None: print(f"  {s[:42]:42s} baseline {yf}-2026  (insufficient)"); continue
        v = "EXCLUDES target" if (r['hi']<TGT23 or r['lo']>TGT23) else "includes target"
        print(f"  {s[:42]:42s} baseline {yf}-2026 n={r['n']:2d}  excess {r['excess']:+6.3f}"
              f"  se {r['se']:.3f}  CI [{r['lo']:+.2f},{r['hi']:+.2f}]  {v}")
print("\n  On the matched 2015-2026 window the two aggregates agree, and the earlier")
print("  apparent precision of All Items Less Accommodation was the shorter, calmer")
print("  baseline window rather than a property of the series.")

print("\n"+"="*100); print("2. T5 REDONE. Category over-shifting, January 2023, CNY controlled,")
print("   prediction-interval inference, Benjamini-Hochberg at q=0.10"); print("="*100)
rows=[]
for s in w.columns:
    r = pex(s, 2023, 2010, 2026)
    if r is None: continue
    z=(r['excess']-TGT23)/r['se']
    rows.append(dict(series=s, excess=r['excess'], se=r['se'], dof=r['dof'],
                     p_over=1-stats.t.cdf(z, r['dof']), p_zero=r['p']))
t=pd.DataFrame(rows).sort_values('p_over').reset_index(drop=True)
m=len(t); t['bh']=(t.index+1)/m*0.10
pas=t[t.p_over<=t.bh]
print(f"  {m} series tested. Over-shooting the target at FDR q=0.10: {len(pas)}")
for _,x in pas.iterrows():
    print(f"    {x.series[:56]:56s} excess {x.excess:+6.2f}  se {x.se:.2f}  p {x.p_over:.4f}")
uncorrected=(t.p_over<0.05).sum()
print(f"\n  Uncorrected, {uncorrected} of {m} would clear p<0.05; {0.05*m:.1f} expected by chance.")
print(f"  Median excess across all series {t.excess.median():+.3f} log points, target {TGT23:.3f}.")
print(f"  Series with excess above target: {(t.excess>TGT23).sum()} of {m}.")
t.to_csv("out/category_2023_cny.csv", index=False)

print("\n"+"="*100); print("3. PRE-REGISTERED VERDICTS, as committed in THESIS.md on 4 September 2026")
print("="*100)
V=[("T1","parallel trends hold for 2023 and 2024","FAIL",
    "slope +0.159 log pts/month, p=7.0e-05 for 2023. F1 TRIGGERED, DiD declared invalid."),
   ("T2","excess step within 0.2pp of mechanical, both events","FAIL",
    "2023 excess -0.017 [-1.42,+1.39]; 2024 -0.470 [-1.84,+0.90]. Neither lands in [0.73,1.13]."),
   ("F2","excess below 0.4pp or above 1.5pp in BOTH events","TRIGGERED",
    "both point estimates below 0.4. Full pass-through not confirmed in the aggregate."),
   ("T3","2023 and 2024 agree within 0.3pp","FAIL",
    "difference 0.453pp on the CNY-controlled estimates."),
   ("F3","events differ by more than 0.5pp","NOT TRIGGERED",
    "difference 0.453pp, just inside. Reported rather than averaged regardless, since 2024 sits on the seam."),
   ("T4","July 2007 shows excess of at least 1.4","PASS on its terms",
    "+1.815 [+0.47,+3.16]. But 63 per cent of it is Housing & Utilities during the 2007 property boom."),
   ("F4","July 2007 shows no step","NOT TRIGGERED","a step is present; its attribution is the problem, not its existence."),
   ("T5","at least one and fewer than half of categories over-shoot","see above",
    f"{len(pas)} of {m} at FDR q=0.10 after controlling for Chinese New Year."),
   ("T6","placebo Januaries not distinguishable from zero","FAIL",
    "2 of 15 significant at p<0.05 against 0.8 expected; placebo sd 0.59, range 2.4 log pts wide."),
   ("F6","placebo excesses of similar magnitude to 2023 and 2024","TRIGGERED",
    "the 2023 estimate sits inside the placebo distribution. Pre-registered consequence: NO PASS-THROUGH NUMBER IS PUBLISHABLE.")]
for k,desc,verd,note in V:
    print(f"  {k:3s} {verd:18s} {desc}")
    print(f"      {note}")
print("\n"+"="*100)
print("BINDING CONSEQUENCE")
print("="*100)
print("""  F6 fired. THESIS.md committed in advance that if placebo Januaries showed
  excess steps of similar magnitude to the event years, the estimator is measuring
  January seasonality rather than tax and no pass-through number is publishable.

  So the piece publishes no estimate of Singapore's GST pass-through. It publishes
  the null, the reason for it, and the power calculation that shows the reason is
  structural: at 0.59 log points of January noise, detecting a 0.93 log point step
  at 5 per cent with 80 per cent power needs 4 events. Singapore has had 2 in the
  era with usable data, and one of those sits on a basket revision.

  What must NOT be written: that the GST rise did not pass through. The data cannot
  say that either. It says the question is not answerable this way.""")
