# gst-passthrough

Did Singapore's GST increases pass through to consumer prices in full?

Analysis directory for a piece on jacobbuildmodel.github.io. Companion to
`coe-analysis`, and it follows the same conventions: numbered scripts in run order,
a fixed raw snapshot rather than a live mirror, published MD5 checksums, and a
pre-registered thesis written before any data was read.

## Status as of 8 September 2026

ANALYSIS COMPLETE. Article drafted, `draft: true`. See `RESULTS.md` for the findings
and `2026-09-08.md` for the piece.

Headline result: the aggregate index cannot detect a rate change this small. The
signal is 0.93 log points against 0.59 of January noise, giving 35 per cent power
where four events would be needed for 80. In the 32 series that barely move in an
ordinary January, both GST years stand out at 8.2 and 5.5 standard deviations, and
water supply, whose every price change in eleven years traces to a dated PUB decision,
rose 1.02 and 0.97 per cent in the two GST Januaries against statutory amounts of 0.93
and 0.93, having moved zero in the nine others.

## The question

GST rose from 7 to 8 per cent on 1 January 2023 and from 8 to 9 per cent on
1 January 2024. Did prices rise by the full amount of the tax, more, or less, and
which categories over-shifted?

Full pass-through is not the change in the rate. It is the change in the
tax-inclusive multiplier:

    2003  3% to 4%   1.04/1.03 - 1 = 0.9709%
    2004  4% to 5%   1.05/1.04 - 1 = 0.9615%
    2007  5% to 7%   1.07/1.05 - 1 = 1.9048%
    2023  7% to 8%   1.08/1.07 - 1 = 0.9346%
    2024  8% to 9%   1.09/1.08 - 1 = 0.9259%

The analysis covers all five increases, not only the two recent ones. The July 2007
change matters most for method: it is the only one that does not land in January, so
it separates the tax effect from January seasonality and from every January-specific
confound.

## Install

    pip install -r requirements.txt

Python 3.11.15. Versions are pinned in `requirements.txt` to the ones the published
figures were produced with. `lunardate` is required by scripts 07, 08, 09 and 14,
which compute Chinese New Year dates; without it those four fail on a clean machine.

## Run order

    ./run_all.sh                     runs 01 to 14 in order, then verifies checksums

or by hand:

    python 00_download.py            fetch raw/ (or download by hand, see DATA_REQUEST.md)
    python 01_clean.py               raw -> out/analysis.csv, out/series_index.csv
    python 02_parallel_trends.py     test T1 and fail condition F1
    python 03_passthrough.py         first-pass event estimates, all five events
    python 04_placebo_and_window.py  placebo, anticipation and lag, 2007 decomposition
    python 05_verify.py              pipeline validation, and measuring the 2024 revision
    python 06_categories.py          test T5, first pass
    python 07_cny_controlled.py      Chinese New Year control
    python 08_final_estimates.py     CORRECT inference, power calculation
    python 09_robustness_and_verdicts.py  matched windows, T5 redone, verdict table
    python 10_lownoise.py            exploratory low-variance series
    python 11_lownoise_placebo.py    does the selection manufacture the result
    python 12_figures.py             figs/*.svg
    python 13_crosscheck_export.py   raw file vs SingStat's own TableBuilder export
    python 14_staggered.py           tests MAS's staggered pass-through account

02 through 14 depend only on out/analysis.csv, so 01 must run first. After that they
can run in any order. 13 additionally needs the second raw export and is skipped by
`run_all.sh` if that file is absent, because it is a cross-check rather than an input
to anything.

IMPORTANT: 03 and 07 report standard errors that 08 supersedes. With a single treated
observation the treatment dummy fits that point exactly and HC3 is undefined, which
statsmodels warns about. 08 replaces every published standard error with a prediction
interval. 03 and 07 are kept because they show the working that led to the correction;
no number in the article comes from them.

## Files

    THESIS.md                     pre-registration, sealed 4 September 2026, not edited
    THESIS_ADDENDUM.md            everything learned after the seal, per A2
    RESULTS.md                    the findings, and what may and may not be claimed
    2026-09-08.md                 the article, draft: true
    HANDOVER.md                   brief for the website chat
    INSPIRATION.md                the Part F technique pass
    number_manifest.csv           every figure in the prose, its source and its script
    CHECKSUMS.md5                 md5 of every tracked file
    DATA_REQUEST.md               exactly what to download and from where
    SOURCES.md                    every source, marked PRIMARY or SECONDARY, with dates
    policy_timeline.csv           what else changed at each event, with evidence status
    cpi_weights.csv               CPI weights, both bases, from ip-e61 Appendix III
    figs/                         three generated SVGs
    notes/01_mas_implied_estimate.md   an early lead, and how it could be wrong
    requirements.txt              pinned dependency versions
    run_all.sh                    runs the pipeline end to end and verifies checksums
    LICENSE                       MIT
    00_download.py                fetches the raw CPI file and writes raw/RETRIEVED.txt
    raw/cpi_2024base_monthly.csv  the analysis input, from data.gov.sg
    raw/cpi_2024base_monthly_tablebuilder.csv  same table from SingStat, used as a check
    raw/RETRIEVED.txt             provenance and checksums for both
    out/                          generated, gitignored

## What the checksums cover, and how to use them

`CHECKSUMS.md5` has two parts, marked with comment lines.

INPUTS are the raw data, the scripts, and the prose. They are what this repository
ships. If one of these fails `md5sum -c`, you have a different copy of the repository
from the one the article was written against.

OUTPUTS are everything under `out/` and `figs/`. These are generated, and they are
listed so that you can confirm your rebuild produced the same numbers and the same
figures as mine, byte for byte. They are gitignored, so on a fresh clone they will be
missing until you run the pipeline. That is the expected order: run `run_all.sh`,
which builds them and then checks every line.

A passing OUTPUT checksum is the real reproducibility claim. It says your machine,
from the same raw file, produced identical analysis output and identical SVGs.

## Reproducibility

`raw/` is a fixed snapshot, not a live mirror. SingStat revises CPI and rebases it
periodically, and it rebased to 2024 = 100 during the period this analysis covers.
Re-downloading later will not reproduce the published figures and is not meant to.
`raw/RETRIEVED.txt` records the URL, the retrieval timestamp, the byte count and the
MD5 of the file as downloaded.

All text files are written with LF line endings. A repository whose checksums are
published cannot let git rewrite line endings on checkout, so `.gitattributes` sets
`* -text` before anything is committed.

## A note on the data source

The series that was actually published during the 2023 and 2024 rate changes was the
2019-base index. data.gov.sg has since unpublished it: dataset
`d_ba8a05c8908b5e1dc13540286d585f8a` returns "dataset not found" as of
4 September 2026. The current 2024-base series re-links history using weights from
the 2023 Household Expenditure Survey.

Whether that reweighting took effect in January 2024, the same month as the second
rate change, or in January 2025, a year clear of it, is unresolved and is the single
biggest threat to the 2024 estimate. It is listed as conditional request C2.
