"""
12_figures.py - generate the three SVG figures from out/analysis.csv.

Figures are generated, never hand-edited, so they regenerate byte-identically.
Theme-aware via CSS custom properties with literal fallbacks. Responsive via
viewBox with no fixed width. Every figure carries a full aria-label describing what
it shows and what the numbers are, so it is readable without sight of it.
Titles live in the article caption, not inside the image, per Part E.
"""
import numpy as np, pandas as pd, pathlib

OUT = pathlib.Path("figs"); OUT.mkdir(exist_ok=True)
GST_JAN = {2003, 2004, 2023, 2024}
TGT23 = 100*(1.08/1.07 - 1)

d = pd.read_csv("out/analysis.csv"); d["index"] = pd.to_numeric(d["index"], errors="coerce")
w = d.pivot_table(index="date", columns="series", values="index", aggfunc="first").sort_index()

def jan_pct(s):
    """January month-on-month change in PERCENT. Used for figure 1, which the
    reader reads as a price change."""
    x = w[s].dropna(); o = {}
    for dt, v in x.items():
        y, m = int(dt[:4]), int(dt[5:])
        if m == 1 and f"{y-1}-12" in x.index: o[y] = 100*(v/x[f"{y-1}-12"] - 1)
    return pd.Series(o).sort_index()


def jan_log(s):
    """January month-on-month change in LOG POINTS. Used for figure 3, because the
    analysis in 08 to 11 is in log points and a figure must not use a different
    basis from the prose it sits next to."""
    x = w[s].dropna(); o = {}
    for dt, v in x.items():
        y, m = int(dt[:4]), int(dt[5:])
        if m == 1 and f"{y-1}-12" in x.index: o[y] = 100*(np.log(v) - np.log(x[f"{y-1}-12"]))
    return pd.Series(o).sort_index()

STYLE = """<style>
    :root{--fg:#1c1c1c;--muted:#767676;--faint:#c8c8c8;--grid:#e6e6e6;--accent:#0b6bcb;}
    @media (prefers-color-scheme: dark){
      :root{--fg:#ececec;--muted:#9a9a9a;--faint:#565656;--grid:#3a3a3a;--accent:#5aa9f0;}
    }
    .fg{fill:var(--fg,#1c1c1c)} .mut{fill:var(--muted,#767676)}
    .lbl{font:11px system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
    .lbl-b{font:600 11px system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
    .grid{stroke:var(--grid,#e6e6e6);stroke-width:1;fill:none}
    .axis{stroke:var(--muted,#767676);stroke-width:1;fill:none}
    .ctx{fill:var(--faint,#c8c8c8)} .ctxs{stroke:var(--faint,#c8c8c8)}
    .acc{fill:var(--accent,#0b6bcb)} .accs{stroke:var(--accent,#0b6bcb)}
  </style>"""

def svg(vb_w, vb_h, aria, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb_w} {vb_h}" '
            f'role="img" aria-label="{aria}" style="max-width:100%;height:auto">\n'
            f'  {STYLE}\n{body}\n</svg>\n')

# ---------- Figure 1: the tax against ordinary January variation ----------
g = jan_pct("All Items"); g = g[(g.index >= 2010) & (g.index <= 2026)]
W, H = 640, 300; L, R, T = 46, 24, 34
x0, x1 = -1.0, 1.8
sx = lambda v: L + (v - x0)/(x1 - x0)*(W - L - R)
rows = []
rows.append(f'  <line class="axis" stroke="#767676" x1="{L}" y1="200" x2="{W-R}" y2="200"/>')
for t in np.arange(-1.0, 1.81, 0.5):
    X = sx(t)
    rows.append(f'  <line class="grid" stroke="#e6e6e6" x1="{X:.1f}" y1="{T}" x2="{X:.1f}" y2="200"/>')
    rows.append(f'  <text class="lbl mut" fill="#767676" x="{X:.1f}" y="216" text-anchor="middle">{t:+.1f}%</text>')
placed = {}
for y, v in g.items():
    X = sx(v); band = round(X/16)
    k = placed.get(band, 0); placed[band] = k + 1
    Y = 190 - k*15
    gst = y in GST_JAN
    cls = "acc" if gst else "ctx"
    rows.append(f'  <circle class="{cls}" fill="{"#0b6bcb" if gst else "#c8c8c8"}" cx="{X:.1f}" cy="{Y}" r="{4.5 if gst else 3.5}"/>')
    if gst:
        rows.append(f'  <text class="lbl-b acc" fill="#0b6bcb" x="{X:.1f}" y="{Y-9}" text-anchor="middle">{y}</text>')
bx0, bx1 = sx(0), sx(TGT23)
rows.append(f'  <line class="accs" stroke="#0b6bcb" x1="{bx0:.1f}" y1="246" x2="{bx1:.1f}" y2="246" stroke-width="7"/>')
rows.append(f'  <text class="lbl-b acc" fill="#0b6bcb" x="{bx1+8:.1f}" y="250">the whole 2023 tax rise, {TGT23:.2f}%</text>')
rows.append(f'  <text class="lbl mut" fill="#767676" x="{L}" y="{T-14}">each dot is one January, All Items index, 2010 to 2026</text>')
rows.append(f'  <text class="lbl mut" fill="#767676" x="{L}" y="272">month-on-month change into January</text>')
aria1 = (f"Dot plot of the month-on-month change in Singapore's All Items consumer price index "
         f"into each January from 2010 to 2026. The values range from minus 0.75 per cent in 2025 "
         f"to plus 1.63 per cent in 2011, with a standard deviation of 0.61 per cent across the "
         f"non-GST years. The two GST years are highlighted: January 2023 at plus 0.19 per cent and "
         f"January 2024 at minus 0.43 per cent, both sitting well inside the ordinary spread. "
         f"A bar beneath shows that full pass-through of the 2023 GST rise would be 0.93 per cent, "
         f"which is smaller than the ordinary year-to-year variation in the dots above it.")
(OUT/"fig1-signal-vs-noise.svg").write_text(svg(W, H, aria1, "\n".join(rows)), newline="\n")

# ---------- Figure 2: water supply, the January reveal ----------
# Redesigned after rendering the first version: an index line spanning 70 to 112 makes
# a 1 per cent step invisible, and the two GST labels collided. Stripping the series to
# its January changes only is the residual reveal from INSPIRATION.md source 2: remove
# everything the tax did not cause and see what is left.
wj = jan_pct("Water Supply")
wj = wj[(wj.index >= 2016) & (wj.index <= 2026)]
W, H = 640, 300; L, R, T, B = 54, 22, 40, 218
ylo, yhi = -0.12, 1.25
syw = lambda v: B - (v - ylo)/(yhi - ylo)*(B - T)
bw = (W - L - R)/len(wj) * 0.5
rows = []
for t in [0.0, 0.25, 0.5, 0.75, 1.0, 1.25]:
    Y = syw(t)
    rows.append(f'  <line class="grid" stroke="#e6e6e6" x1="{L}" y1="{Y:.1f}" x2="{W-R}" y2="{Y:.1f}"/>')
    rows.append(f'  <text class="lbl mut" fill="#767676" x="{L-8}" y="{Y+4:.1f}" text-anchor="end">{t:.2f}%</text>')
YT = syw(TGT23)
rows.append(f'  <line class="accs" stroke="#0b6bcb" x1="{L}" y1="{YT:.1f}" x2="{W-R}" y2="{YT:.1f}" stroke-width="1.5"/>')
rows.append(f'  <text class="lbl-b acc" fill="#0b6bcb" x="{L}" y="{YT-7:.1f}">what the tax alone should add, 0.93%</text>')
rows.append(f'  <line class="axis" stroke="#767676" x1="{L}" y1="{syw(0):.1f}" x2="{W-R}" y2="{syw(0):.1f}"/>')
for i, (y, v) in enumerate(wj.items()):
    X = L + (i + 0.5)*(W - L - R)/len(wj)
    gst = y in GST_JAN
    if abs(v) < 1e-9:
        rows.append(f'  <line class="ctxs" stroke="#c8c8c8" x1="{X-bw/2:.1f}" y1="{syw(0):.1f}" '
                    f'x2="{X+bw/2:.1f}" y2="{syw(0):.1f}" stroke-width="2.5"/>')
    else:
        rows.append(f'  <rect class="{"acc" if gst else "ctx"}" fill="{"#0b6bcb" if gst else "#c8c8c8"}" '
                    f'x="{X-bw/2:.1f}" y="{syw(v):.1f}" width="{bw:.1f}" height="{syw(0)-syw(v):.1f}"/>')
        rows.append(f'  <text class="lbl-b acc" fill="#0b6bcb" x="{X:.1f}" y="{syw(v)-7:.1f}" '
                    f'text-anchor="middle">{v:.2f}%</text>')
    rows.append(f'  <text class="lbl mut" fill="#767676" x="{X:.1f}" y="{B+18}" text-anchor="middle">{str(y)[2:]}</text>')
rows.append(f'  <text class="lbl mut" fill="#767676" x="{L}" y="{T-18}">water supply price, change into each January</text>')
rows.append(f'  <text class="lbl mut" fill="#767676" x="{L}" y="{B+48}">Nine Januaries at exactly zero. Two at the size of the tax.</text>')
rows.append(f'  <text class="lbl mut" fill="#767676" x="{L}" y="{B+64}">PUB last revised the price in 2017, then in April 2024 and April 2025.</text>')
aria2 = ("Bar chart of the month-on-month change in Singapore's water supply consumer price index "
         "into each January from 2016 to 2026. Nine of the eleven Januaries show a change of exactly "
         "zero and are drawn as flat ticks on the baseline. The two exceptions are January 2023 at "
         "plus 1.02 per cent and January 2024 at plus 0.97 per cent, the two months the GST rate rose. "
         "A reference line marks 0.93 per cent, the amount the tax rise alone should add, and both "
         "bars sit just above it. PUB last revised the water price in 2017 and next in April 2024 and "
         "April 2025, so no January in this chart contains a tariff decision.")
(OUT/"fig2-water-supply.svg").write_text(svg(W, H, aria2, "\n".join(rows)), newline="\n")

# ---------- Figure 3: the still prices, every January ----------
ALL = {s: jan_log(s) for s in w.columns}
CUT = 100*np.log(1.08/1.07)/2   # half the target, in log points
med = {}
for y in range(2010, 2027):
    e = []
    for s, gg in ALL.items():
        gg = gg[(gg.index >= 2010) & (gg.index <= 2026)]
        if y not in gg.index: continue
        base = gg[~gg.index.isin(GST_JAN | {y})]
        if len(base) < 8 or base.std(ddof=1) >= CUT: continue
        e.append(gg.loc[y] - base.mean())
    if e: med[y] = float(np.median(e))
W, H = 640, 300; L, R, T, B = 52, 20, 34, 232
mlo, mhi = -0.35, 0.80
syb = lambda v: B - (v - mlo)/(mhi - mlo)*(B - T)
bw = (W - L - R)/len(med) * 0.62
rows = []
for t in [-0.2, 0.0, 0.2, 0.4, 0.6, 0.8]:
    Y = syb(t)
    rows.append(f'  <line class="grid" stroke="#e6e6e6" x1="{L}" y1="{Y:.1f}" x2="{W-R}" y2="{Y:.1f}"/>')
    rows.append(f'  <text class="lbl mut" fill="#767676" x="{L-8}" y="{Y+4:.1f}" text-anchor="end">{t:+.1f}</text>')
rows.append(f'  <line class="axis" stroke="#767676" x1="{L}" y1="{syb(0):.1f}" x2="{W-R}" y2="{syb(0):.1f}"/>')
for i, (y, v) in enumerate(sorted(med.items())):
    X = L + (i + 0.5)*(W - L - R)/len(med)
    Y0, Y1 = syb(0), syb(v)
    gst = y in GST_JAN
    rows.append(f'  <rect class="{"acc" if gst else "ctx"}" fill="{"#0b6bcb" if gst else "#c8c8c8"}" '
                f'x="{X-bw/2:.1f}" y="{min(Y0,Y1):.1f}" width="{bw:.1f}" height="{abs(Y1-Y0):.1f}"/>')
    if gst:
        rows.append(f'  <text class="lbl-b acc" fill="#0b6bcb" x="{X:.1f}" y="{Y1-6:.1f}" text-anchor="middle">{y}</text>')
    if y % 2 == 0:
        rows.append(f'  <text class="lbl mut" fill="#767676" x="{X:.1f}" y="{B+18}" text-anchor="middle">{str(y)[2:]}</text>')
rows.append(f'  <text class="lbl mut" fill="#767676" x="{L}" y="{T-14}">median excess January move in log points, the 32 prices that otherwise hold still</text>')
rows.append(f'  <text class="lbl mut" fill="#767676" x="{L}" y="{B+50}">Every other January averages -0.01. The two GST years are +0.68 and +0.45.</text>')
aria3 = ("Bar chart of the median excess January price move, in log points, among the 32 consumer "
         "price index series whose January movement is otherwise very small, for each year from 2010 "
         "to 2026. Every non-GST year lies between minus 0.19 and plus 0.16, averaging minus 0.01 with "
         "a standard deviation across years of 0.08. The two GST years stand far above the rest: "
         "January 2023 at plus 0.68 and January 2024 at plus 0.45, which are 8.2 and 5.5 standard "
         "deviations above the non-GST average and the two largest values in the seventeen years shown.")
(OUT/"fig3-still-prices.svg").write_text(svg(W, H, aria3, "\n".join(rows)), newline="\n")

print("wrote:")
for f in sorted(OUT.glob("*.svg")):
    print(f"  {f}  {f.stat().st_size} bytes")
print("\nmedian excess by year, the still prices:")
for y, v in sorted(med.items()): print(f"  {y} {v:+.4f}")
