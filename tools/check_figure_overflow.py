"""
check_figure_overflow.py - fail if any <text> in a figure SVG runs outside
its own viewBox once rendered in DejaVu Sans, the default sans-serif on
Linux (and so on most CI runners), which is measurably wider than the
Helvetica/Segoe UI most contributors see locally.

The bug this catches: a chart with a margin sized for one font's metrics
clips a label's text under a different one. Not visible from the coordinate
math, only from rendering. Found for real, 24 September 2026, against
mechanism.svg, decomposition.svg, gap_distribution.svg, indexed.svg,
moto_vs_car.svg and winrate.svg -- all fixed by widening a margin or
wrapping a caption, never by shrinking text below the 14px minimum.

Requires the "playwright" package and its Chromium browser
(python -m playwright install chromium), same as the rest of this repo's
rendering-based checks. Bundles tools/DejaVuSans.ttf (Bitstream Vera Fonts
License / public domain change notice, same as matplotlib and most Linux
distributions ship) so the check is reproducible without relying on
whatever fonts happen to be installed on the machine running it.

Usage:
    python tools/check_figure_overflow.py figs/mechanism.svg figs/indexed.svg ...

Exits 1 and prints every offending <text> element (its content and its
extent) if anything sits closer than 2 SVG units to either edge of the
viewBox. Exits 0, printing one PASS line per file, otherwise.
"""
import os
import sys

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(HERE, "DejaVuSans.ttf")
MARGIN = 2  # SVG units of required clearance from each edge


def check_svg(page, svg_path, tmp_html_path):
    with open(svg_path, encoding="utf-8") as f:
        svg_src = f.read()
    font_uri = "file:///" + FONT_PATH.replace(os.sep, "/")
    html = f"""<!doctype html><html><head><style>
      @font-face {{ font-family: 'DejaVu Sans'; src: url('{font_uri}') format('truetype'); }}
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
    tmp_html = os.path.join(HERE, "_overflow_check_tmp.html")
    any_fail = False
    with sync_playwright() as p:
        browser = p.chromium.launch()
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
    if os.path.exists(tmp_html):
        os.remove(tmp_html)
    sys.exit(1 if any_fail else 0)


if __name__ == "__main__":
    main()
