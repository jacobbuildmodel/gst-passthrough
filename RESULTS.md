# Results

Analysis run 8 September 2026 on raw/cpi_2024base_monthly.csv, md5
a48b09388082c3545e461d5c58bb6b90, downloaded 7 September 2026 from data.gov.sg
dataset d_bdaff844e3ef89d39fceb962ff8f0791.

Pipeline validated first: year-on-year rates computed from this file reproduce the
rates MTI printed contemporaneously on the 2019 base, for January 2023 All Items
(6.638 against 6.6), Food (8.137 against 8.1) and Accommodation (5.028 against 5.0).
Index levels differ because the bases differ. Percentage changes match, which is what
ip-e61's scalar link factor predicts.

## The short version

The aggregate index cannot answer the question. The individual prices can.

## 1. The pre-registered design failed, in the way it was predicted to fail

T1, parallel trends, FAILS. Over the 24 months before January 2023 the gap between
All Items Less Accommodation and Accommodation trended at +0.159 log points a month,
p = 7.0e-05. F1 triggered. The difference-in-differences design is declared invalid
and produces no published number.

THESIS.md predicted this on 4 September, before the file was downloaded, and gave the
reason: the only exempt category with meaningful CPI weight is accommodation, and
Singapore accommodation was in an extraordinary rental cycle. The prediction was
right. The design died for the stated reason.

## 2. The aggregate estimate is a null, and an underpowered one

Secondary design: each series is its own control across years. January step, measured
Dec to Jan in log points, against that series' own January baseline over 2010-2026
with all GST years excluded, controlling for Chinese New Year.

Inference is by prediction interval, not by a regression standard error on a treated
dummy. With one treated observation that dummy has leverage 1, its residual is zero,
and HC3 divides by zero. Fitting on the baseline years and predicting the event year
is the correct construction and gives wider, honest intervals.

    January 2023, All Items      excess -0.017 log points, 95% CI [-1.42, +1.39]
    full pass-through target      0.930 log points

The interval contains the target and contains zero. It is uninformative.

Why it is uninformative is the point. The placebo distribution of January excesses
across the 15 non-GST Januaries has a standard deviation of 0.590 log points and a
range 2.4 log points wide. The signal is 0.930. So:

    power of a two-sided 5% test with one event    35 per cent
    events needed for 80 per cent power            4
    January GST events with usable data            2, one of them on a basket seam

T6 fails and F6 triggers. THESIS.md committed in advance that if placebo Januaries
showed excess steps like the event years, no pass-through number would be publishable
from this estimator. The 2023 estimate sits at the 73rd percentile of the placebo
distribution. That commitment binds and is honoured: the piece publishes no aggregate
estimate of Singapore's GST pass-through.

What this does NOT say is that the tax failed to pass through. The data cannot say
that either. It says the aggregate index is the wrong instrument.

## 3. The one event big enough to see is confounded

July 2007, 5 to 7 per cent, target 1.887 log points. All Items excess +1.815, CI
[+0.47, +3.16]. On its literal terms T4 passes: a step is there, and it brackets full
pass-through, in a month with no January seasonality.

Decomposing it by division kills the attribution. Housing & Utilities alone
contributes +1.340 of the +2.133 weighted total, 63 per cent of it. Singapore private
residential prices were in a boom in mid-2007. Excluding housing and rescaling, the
rest of the basket gives +1.055 against a target of 1.887.

The one event with enough signal to clear the noise sits on top of a property boom.

## 4. Where the tax IS visible, and this is the finding

EXPLORATORY, NOT PRE-REGISTERED. It was suggested by two degenerate standard errors
in the T5 output and must be labelled as post-hoc wherever it appears.

Most CPI series move in January for reasons that have nothing to do with tax. Some do
not. Selecting series whose own standard deviation of January steps over 2010-2026 is
below half the target, 0.465 log points, keeps 32 of 162 series.

In those 32 series:

    year   median excess     year   median excess
    2010        -0.191       2019        +0.134
    2011        +0.040       2020        -0.027
    2012        -0.012       2021        +0.000
    2013        -0.018       2022        +0.000
    2014        +0.158       2023        +0.675   GST 7 to 8
    2015        +0.005       2024        +0.447   GST 8 to 9
    2016        -0.023       2025        -0.034
    2017        -0.111       2026        -0.009
    2018        -0.041

Across the 15 non-GST Januaries the median excess averages -0.009 with a standard
deviation across years of 0.083. The two GST Januaries rank 1 and 2 of 17, at +8.2
and +5.5 standard deviations.

The selection is not manufacturing this. The identical procedure applied to any
non-GST January, with that year excluded from its own baseline, returns approximately
zero. It returns something only in the two years the tax changed.

## 5. Water supply is the cleanest natural experiment in the file

Every change in the Water Supply index since 2015, and its administrative cause:

    2017-07   70.555 ->  81.208   +15.10%   PUB water price revision, phase 1
    2018-07   81.208 ->  93.149   +14.70%   PUB water price revision, phase 2
    2023-01   93.149 ->  94.102    +1.02%   GST 7 to 8 per cent
    2024-01   94.102 ->  95.018    +0.97%   GST 8 to 9 per cent
    2024-04   95.018 -> 101.661    +6.99%   PUB +20 cents per cubic metre
    2025-04  101.661 -> 112.292   +10.46%   PUB +30 cents per cubic metre

Six changes in eleven years and every one traces to a dated administrative decision.
PUB's press release of 27 September 2023 states the previous revision was in 2017 and
the next were 1 April 2024 and 1 April 2025. No water price changed on either
1 January. It also states "All figures are before GST", so the consumer price is the
tariff multiplied by one plus the rate.

    Jan 2023   observed +1.0231%   statutory +0.9346%   gap +0.0885 pp
    Jan 2024   observed +0.9734%   statutory +0.9259%   gap +0.0475 pp

Full pass-through, twice, in a price that moved zero in the nine other Januaries.

The small excess over statutory is consistent with rounding to the cent in billing.
That explanation has NOT been verified against PUB's billing rules and must not be
asserted. State the gap; do not explain it.

## 6. The absorption policy is confirmed in 2023 and not in 2024

MOF states the government absorbs GST on publicly subsidised education, so a zero step
in a GST month is what the policy predicts.

Polytechnic Education moves once a year, in April, with the academic year. Every
change in the series from 2015 to 2026:

    2015-04  +1.5330%     2021-04  +0.9477%
    2016-04  +4.0181%     2022-04  +1.0844%
    2017-04  +4.0073%     2023-04  +1.0932%
    2018-04  +3.7404%     2024-01  +0.1374%   <-- the only January move of any size
    2019-01  -0.0011%     2024-04  +1.2313%
    2019-04  +3.6521%     2025-04  +3.7595%
    2020-04  +2.3824%     2026-04  +1.1405%

January 2023 is exactly zero, as predicted.

January 2024 is +0.1374 per cent. That is 0.15 of the 0.9259 statutory figure, so it
is nowhere near full pass-through, but it is not zero either. Two facts about it, and
neither is an explanation:

- Apart from a rounding-sized -0.0011 in January 2019, it is the only January this
  series has moved in eleven years. Every other move is an April fee revision.
- It falls in the month SingStat began the 2024 basket, which is the same reason the
  aggregate January 2024 estimate is set aside in section 7.

The other subsidised-education series move the same way in that month and by similar
small amounts: Primary +0.1442, Secondary +0.0430, Post-Secondary (Non-Tertiary)
+0.1011. In January 2023 the same three moved -0.7415, -1.1462 and -0.6547, so their
Januaries are not reliably still either.

I cannot separate the basket revision from a genuine small movement, and I am not
going to pretend otherwise. The article reports the prediction as confirmed once and
not twice, and gives the 2024 number.

## 7. The 2024 event cannot be estimated from this file, and the size of the problem

ip-e61: the 2024-based indices commence from January 2024. So the December to January
step spans the basket revision.

Measured directly: All Items year-on-year for January 2024 was published at the time
as 2.9 per cent on the 2019 base. The same month in the current file computes to
3.112 per cent. The revision moved that month's published inflation rate by
+0.212 percentage points, which is 21 per cent of the entire official 1.0 point GST
effect. A revision that size sits on top of a signal that size.

43 of 207 series in the file begin exactly at 2024-01, so the seam changes
composition, not only weights.

The series that would settle it, the 2019-base monthly index published throughout
2024, has been unpublished from data.gov.sg. Dataset
d_ba8a05c8908b5e1dc13540286d585f8a returns "dataset not found".

Water Supply escapes all of this, because a single item's index does not depend on
how items are weighted together.

## 8. The official figure is not a measurement

MAS, April 2023: 2023 core inflation 3.5-4.5 per cent including GST, 2.5-3.5 per cent
excluding. MTI, February 2024: 2024 headline and core 2.5-3.5 per cent including GST,
1.5-2.5 per cent excluding. Both imply exactly 1.0 percentage point.

The two should differ. Statutory pass-through is 0.9346 per cent in 2023 and 0.9259
in 2024, and the 2024 basket carries more exempt accommodation than the 2019 basket
did, rentals rising from 1,978 to 2,432 per 10,000. Full pass-through on the liable
share of the 2019 basket is 0.66 to 0.75 percentage points, not 1.0.

No published methodology for the 1.0 has been found. The MAS chapter PDFs are 403
from this environment. The piece says "consistent with a round-number convention" and
not "is a convention".

## Pre-registered verdicts

    T1  FAIL           F1 TRIGGERED, DiD invalid
    T2  FAIL           neither event lands in [0.73, 1.13]
    F2  TRIGGERED      both point estimates below 0.4
    T3  FAIL           events differ by 0.453 pp
    F3  not triggered  0.453 is inside the 0.5 threshold
    T4  PASS on terms  but 63 per cent of it is the 2007 property boom
    F4  not triggered
    T5  6 of 162 over-shoot at FDR q=0.10 after the CNY control
    T6  FAIL           F6 TRIGGERED, no aggregate pass-through number publishable

## What the piece can and cannot claim

CAN: that the aggregate index cannot detect a rate change of this size, with the
power calculation showing why. That in prices which move for no other reason in
January, both rate changes are visible at 8.2 and 5.5 standard deviations. That water
supply shows full pass-through twice, against a verified administrative record. That
publicly subsidised education shows zero, as the absorption policy predicts. That the
official 1.0 percentage point is the same for two events whose arithmetic differs.
That the series needed to check January 2024 has been withdrawn from the open portal.

CANNOT: any aggregate pass-through estimate. That the GST rise did not pass through.
That firms over-shifted in general. That the low-noise result generalises to the 80
per cent of the basket that does move in January, since those are exactly the prices
where the method has no power.

---

# Added 8 September 2026, after Jacob supplied the MAS Reviews and a TableBuilder export

## 9. The pipeline is now checked against SingStat's own export

Jacob supplied a direct TableBuilder export of the same table, TS/M213751. All 37,881
observations agree exactly with the data.gov.sg download: zero value mismatches, zero
observations present in one file and absent from the other. See 13_crosscheck_export.py.
The data.gov.sg copy is a faithful reproduction and 01_clean.py reads it correctly.

## 10. MAS explains the null rather than contradicting it

The two Macroeconomic Reviews close the question the piece previously hedged.

October 2023, footnote 16, verbatim:
  "The increase in the GST will still add to core inflation next year, albeit
   marginally, as the impact of the GST hike this year was staggered across several
   months, instead of passing through fully at the start of the year. Several
   retailers such as major supermarket chains announced a temporary absorption of the
   tax increase or offered a token discount early this year. In the absence of similar
   announcements for 2024 thus far, the upcoming GST hike is assumed to pass through
   fully in January under the current baseline."

April 2023, Chapter 4, footnote 1, verbatim:
  "Although subject to significant uncertainty, MAS estimates' indicate that a full
   pass-through of the GST rate hike will occur over the course of 2023."

April 2023, Chapter 4:
  "Notably, the extent of GST hike pass-through in January was relatively modest
   compared to that seen during the previous GST increase in 2007."

April 2023, Section 3.2:
  "some local supermarket and pharmacy chains, as well as other retailers, absorbed
   the GST increase for some items, albeit temporarily for three to six months."

Three consequences.

First, the one percentage point is an ASSUMPTION of full pass-through, stated as one
by MAS in both Reviews. The piece can now say "assumed" rather than "consistent with a
round-number convention". That hedge is removed.

Second, MAS itself says the January 2023 step was modest, and modest by comparison
with 2007. That corroborates the null rather than contradicting it.

Third, MAS gives a mechanism the water result then confirms from the other side:
retailers absorbed temporarily, and an administered price cannot.

## 11. The staggered version was tested and does not rescue the aggregate

See 14_staggered.py. Cumulative excess from December through month h, All Items, CNY
controlled, prediction intervals, non-GST years as placebo.

    through   2023 excess        95% interval         target
    Jan       -0.017             [-1.42, +1.39]       0.930
    Feb       +0.300             [-1.04, +1.64]       0.930
    Mar       +0.579             [-1.19, +2.35]       0.930
    Apr       +0.857             [-1.87, +3.59]       0.930
    Jun       +1.124             [-1.94, +4.19]       0.930

The 2023 point estimates drift upward toward the target, which is the shape MAS
describes. Every interval still contains both the target and zero. By April the same
calculation on non-GST years ranges from -1.903 to +1.974 with sd 1.146, and 2023
ranks 12 of 16.

Cumulating adds noise faster than signal. The aggregate cannot see a staggered
pass-through any more than a concentrated one. The 2024 path does not drift upward at
all, which is consistent with MAS expecting no absorption that year and equally
consistent with the basket revision sitting in that month.

NOTE ON PROVENANCE: this test was not in THESIS.md by name. Anticipation and lag were
named as threats in the brief and listed in THESIS.md's confounds, and 04 ran the
month-by-month window, but the cumulative test with placebo was prompted by MAS's
account. Labelled as such in the article's aside.

## 12. What changed in the article

- Section 3 gains MAS's staggering account and a one-line summary of the test above,
  with the detail in the aside.
- Section 5 gains the mechanism: a supermarket can absorb, PUB cannot.
- Section 7 is rewritten. The hedge is gone; MAS is quoted saying "assumed".
- Nothing else changed. No figure was regenerated. No number was revised.
