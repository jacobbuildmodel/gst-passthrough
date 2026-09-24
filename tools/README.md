# tools

`check_figure_overflow.py` -- renders each figure SVG with DejaVu Sans (Linux's default
sans-serif, and the widest common one this repo's charts have been checked against) and fails
if any `<text>` element sits closer than 2 SVG units to either edge of the viewBox. Catches a
margin sized for one font clipping a label under a wider one -- not visible from the
coordinate math, only from rendering. Declares both a regular and a bold weight of the family,
so a chart's own `font-weight="600"` labels are measured against the real DejaVu Sans Bold
metrics, not a browser's synthetic (faux) bold applied to the regular face, which is narrower
and can pass a label that actually clips.

Not otherwise a dependency of this repo. Needs `playwright` and its Chromium browser:

```
pip install playwright
python -m playwright install chromium
python tools/check_figure_overflow.py figs/mechanism.svg figs/indexed.svg ...
```

It is wired into `run_all.sh` (and, in this repo, into `motorcycles/README.md` and
`win-rate/README.md`'s own run steps for their one figure each) so a figure change can't
silently regress this. If `playwright` isn't installed, or its Chromium build can't launch,
the check prints one line and exits 0 rather than failing the whole reproduction run -- it
only fails the run when it actually ran and found a real overflow.

`DejaVuSans.ttf` and `DejaVuSans-Bold.ttf` are bundled here so the check is reproducible
regardless of what fonts happen to be installed on the machine running it -- the same files
matplotlib ships as its own default font, under the Bitstream Vera Fonts Copyright plus the
DejaVu changes (public domain), both permitting redistribution.
