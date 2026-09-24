"""
check_figure_overflow.py - fail if any <text> in a figure SVG runs outside
its own viewBox once rendered in DejaVu Sans, the default sans-serif on
Linux (and so on most CI runners), which is measurably wider than the
Helvetica/Segoe UI most contributors see locally.

The bug this catches: a chart with a margin sized for one font's metrics
clips a label's text under a different one. Not visible from the coordinate
math, only from rendering. Found for real, 24 September 2026, against
mechanism.svg, decomposition.svg, gap_distribution.svg, moto_vs_car.svg and
winrate.svg (regular-weight labels) and indexed.svg (a font-weight="600"
label, "premium 387" -- missed on the first pass of this tool, which
declared only the regular face under the 'DejaVu Sans' family name, so
every bold label was measured in faux-bold regular instead of the real,
wider Bold face). Fixed by widening a margin or wrapping a caption, never
by shrinking text below the 14px minimum.

Bundles both tools/DejaVuSans.ttf and tools/DejaVuSans-Bold.ttf (Bitstream
Vera Fonts License / public domain change notice, same as matplotlib and
most Linux distributions ship), declared as two @font-face weights of one
'DejaVu Sans' family so a chart's own font-weight="600"/"700" text picks up
the real bold metrics instead of the browser's synthetic (faux) bold.

Needs the "playwright" package and its Chromium browser
(python -m playwright install chromium) -- see tools/README.md. Neither is
a dependency of the rest of this repo, so if they aren't available this
script prints one line and exits 0 rather than failing the whole
reproduction run; it only exits nonzero when it actually ran and found a
real overflow.

Usage:
    python tools/check_figure_overflow.py figs/mechanism.svg figs/indexed.svg ...

Exits 1 and prints every offending <text> element (its content and its
extent) if anything sits closer than 2 SVG units to either edge of the
viewBox. Exits 0, printing one PASS line per file, otherwise. Exits 0 and
prints one SKIP line if playwright or Chromium isn't available.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(HERE, "DejaVuSans.ttf")
FONT_BOLD_PATH = os.path.join(HERE, "DejaVuSans-Bold.ttf")
MARGIN = 2  # SVG units of required clearance from each edge
SKIP_MSG = ("figure overflow check skipped: playwright not installed, "
            "see tools/README.md")

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None


def check_svg(page, svg_path, tmp_html_path):
    with open(svg_path, encoding="utf-8") as f:
        svg_src = f.read()
    font_uri = "file:///" + FONT_PATH.replace(os.sep, "/")
    font_bold_uri = "file:///" + FONT_BOLD_PATH.replace(os.sep, "/")
    html = f"""<!doctype html><html><head><style>
      @font-face {{ font-family: 'DejaVu Sans'; font-weight: 100 599;
                    src: url('{font_uri}') format('truetype'); }}
      @font-face {{ font-family: 'DejaVu Sans'; font-weight: 600 900;
                    src: url('{font_bold_uri}') format('truetype'); }}
      svg text {{ font-family: 'DejaVu Sans' !important; }}
      body {{ margin: 0; }}
    </style></head><body>
    {svg_src}
    </body></html>"""
    with open(tmp_html_path, "w", encoding="utf-8") as f:
        f.write(html)
    page.goto("file:///" + tmp_html_path.replace(os.sep, "/"))
    page.evaluate("document.fonts.ready")
    page.wait_for_timeout(80)
    return page.evaluate(f"""() => {{
        const svg = document.querySelector('svg');
        const vb = svg.viewBox.baseVal;
        const texts = Array.from(document.querySelectorAll('text'));
        return texts.map(t => {{
            const b = t.getBBox();
            const ok = (b.x >= vb.x + {MARGIN}) && ((b.x + b.width) <= (vb.x + vb.width - {MARGIN}));
            return {{ text: t.textContent, x: b.x, right: b.x + b.width,
                      vb_x: vb.x, vb_w: vb.width, ok }};
        }});
    }}""")


def main():
    svg_paths = sys.argv[1:]
    if not svg_paths:
        print("usage: check_figure_overflow.py <svg> [<svg> ...]")
        sys.exit(2)

    if sync_playwright is None:
        print(SKIP_MSG)
        sys.exit(0)

    tmp_html = os.path.join(HERE, "_overflow_check_tmp.html")
    any_fail = False
    try:
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch()
            except Exception:
                print(SKIP_MSG)
                sys.exit(0)
            page = browser.new_page()
            for svg_path in svg_paths:
                results = check_svg(page, svg_path, tmp_html)
                fails = [r for r in results if not r["ok"]]
                if fails:
                    any_fail = True
                    print(f"FAIL {svg_path}")
                    for r in fails:
                        print(f"  x={r['x']:.1f} right={r['right']:.1f} "
                              f"viewBox=[{r['vb_x']:.1f},{r['vb_x']+r['vb_w']:.1f}]  "
                              f"text={r['text']!r}")
                else:
                    print(f"PASS {svg_path} ({len(results)} text elements)")
            browser.close()
    finally:
        if os.path.exists(tmp_html):
            os.remove(tmp_html)
    sys.exit(1 if any_fail else 0)


if __name__ == "__main__":
    main()
