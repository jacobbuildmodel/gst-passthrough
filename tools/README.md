# tools

`check_figure_overflow.py` -- renders each figure SVG with DejaVu Sans (Linux's default
sans-serif, and the widest common one this repo's charts have been checked against) and fails
if any `<text>` element sits closer than 2 SVG units to either edge of the viewBox. Catches a
margin sized for one font clipping a label under a wider one -- not visible from the
coordinate math, only from rendering.

Needs `playwright` and its Chromium browser, not otherwise a dependency of this repo:

```
pip install playwright
python -m playwright install chromium
python tools/check_figure_overflow.py figs/mechanism.svg figs/indexed.svg ...
```

`DejaVuSans.ttf` is bundled here so the check is reproducible regardless of what fonts happen
to be installed on the machine running it -- the same file matplotlib ships as its own default
font, under the Bitstream Vera Fonts Copyright plus the DejaVu changes (public domain), both
permitting redistribution.
