# Addendum to THESIS.md

Invariant A2 forbids editing THESIS.md after it is sealed. Everything learned after
4 September 2026 goes here instead.

Still no CPI file. `raw/` remains empty. Nothing below is measured from data. It is
all either quoted from a primary document or arithmetic on quoted figures.

## 1. C2 is resolved, and the access route that resolved it

Opened 7 September 2026. Jacob supplied the answer; I then confirmed it against the
primary source and it holds.

SingStat's PDF paths return 403 from this environment. Its `.ashx` paths do not. The
Information Paper is readable at

  https://www.singstat.gov.sg/-/media/files/publications/economy/ip-e61.ashx

where the same document at `/ip-e61.pdf` is refused. Every SingStat document written
off as blocked on 4 September should be retried on `.ashx` before anyone asks Jacob
to fetch it.

## 2. What the Information Paper actually says

Quoted from ip-e61, retrieved 7 September 2026:

- Release: the rebased series "will be released on 24 February 2025".
- Start of the new basket: the new series begins "with indices commencing from
  January 2024."
- Linking: "the 2019-based CPI data series are linked to the 2024-based CPI data
  series by re-scaling them to the new base year of 2024 via a link factor. The link
  factor is the ratio of the annual 2024-based index in 2024 to the annual
  2019-based index in 2024."
- Classification: reclassified to S-COICOP 2022. Ten main divisions. Two renamed:
  Information & Communication, formerly Communication; Recreation, Sport & Culture,
  formerly Recreation & Culture.

## 3. Jacob is right about 2023, and the link factor is the reason

The linking is a single scalar applied to the whole pre-2024 series. Multiplying an
index series by a constant leaves every month-on-month percentage change in that
series unchanged. So the January 2023 step measured in the published 2024-based file
is arithmetically identical to the January 2023 step in the 2019-based file.

The 2023 event is clean identification. Confirmed, and now for a stated reason
rather than an assumption.

This is checkable rather than merely argued, and it should be checked: if the two
files are ever both in hand, every pre-2024 monthly change must agree to floating
point. Any disagreement means the link is not the pure rescaling the paper
describes, and the 2023 estimate would need revisiting.

## 4. Jacob is right that the current series confounds 2024

December 2023 comes from the rescaled old basket. January 2024 comes from the new
basket, with HES 2023 weights and a changed classification. The link factor is an
annual ratio for 2024, so nothing forces the December-to-January step to be
continuous. The measured step contains the tax change and the basket change
together.

The weight shifts across that seam are not small, per 10,000:

    HOUSING & UTILITIES              +453
    HEALTH                           +357
    TRANSPORT                        -402
    RECREATION, SPORT & CULTURE      -119
    INFORMATION & COMMUNICATION       -96
    EDUCATION                         -91
    FOOD                              -75
    HOUSEHOLD DURABLES & SERVICES     +59
    CLOTHING & FOOTWEAR               -47
    MISCELLANEOUS GOODS & SERVICES    -39

Transport falling 402 while Housing rises 453 is a large reshuffle to land in the
same month as a tax change, in a year when private transport prices were moving
violently.

## 5. Where I correct Jacob: 2024 is separable, and the open-data finding is why

Jacob's instruction was to bound the reweighting if possible and otherwise say
plainly that the two cannot be separated. There is a third option, and it is better
than both.

The rebasing was released on 24 February 2025. Every CPI release through the whole
of 2024, including the January 2024 release, was published on the 2019 base. So the
2019-based series contains a December 2023 to January 2024 change computed entirely
within the old basket, with no reweighting anywhere near it. That measurement
identifies the January 2024 step cleanly.

That series is the one data.gov.sg has unpublished. Dataset
`d_ba8a05c8908b5e1dc13540286d585f8a` returned "dataset not found" on 4 September
2026.

So the open-data finding is not a closing aside about portal hygiene. It is
load-bearing. The only public series that can identify the second of the two rate
changes without confounding it against a basket revision is the series that was
removed from the open portal. It survives in TableBuilder, which is not machine
readable from here, and the reader who wants to check the number has to know it
exists.

CONSEQUENCE FOR THE DATA REQUEST: conditional item C1 is promoted from robustness
check to essential for the 2024 event.

## 6. The bound, for if C1 cannot be obtained

If only the 2024-based file is available, the cross-category part of the reweighting
is computable exactly rather than bounded. The contribution of the weight change to
the aggregate January 2024 step is

    sum over divisions of (w_2024 - w_2019) x r_i

with r_i the division's January 2024 change and the weight vectors above. Subtract
it and what remains is the aggregate step net of cross-category reweighting.

What that does NOT remove is reweighting within divisions, and the reclassification
to S-COICOP 2022, which can move items between divisions rather than merely
reweighting them. So this is a partial correction and would have to be published as
one. It is second best. C1 is first best.

## 7. New, and it changes the shape of the piece: the liable share is now known

The Information Paper's Appendix III gives group-level weights. Every division and
group total reconciles exactly, which is a decent check that the table was read
correctly.

2019-based basket, per 10,000, the basket in force for the January 2023 event:

    Imputed Rentals for Housing                      1,750
    Actual Rentals for Housing                         228
    Housing Maintenance & Repairs                      220
    Utilities & Other Fuels                            287
    Medicines & Health Products                        116
    Outpatient Care Services                           274
    Inpatient Care Services                            151
    Other Health Services                               28
    Health Insurance                                    82
    General, Vocational & Higher Education             466
    Private Tuition & Other Educational Courses        196
    School Textbooks & Study Guides                      8

Lease of residential property is exempt under the Fourth Schedule, so actual and
imputed rentals, 1,978 per 10,000, carry no GST. MOF states the government absorbs
GST on publicly subsidised education and healthcare, which reaches at most the care
services, health insurance and subsidised education lines, 1,001 per 10,000.

    GST-liable share of the basket, upper bound   80.22 per cent
    GST-liable share of the basket, lower bound   70.21 per cent

Full statutory pass-through of the 2023 change is 0.9346 per cent, so the expected
effect on the whole index is

    at 80.22 per cent liable    0.9346 x 0.8022 = 0.7497 pp
    at 70.21 per cent liable    0.9346 x 0.7021 = 0.6562 pp

MAS's forecasts imply 1.0 pp. That is 1.33 to 1.52 times the mechanical expectation.

## 8. What that does and does not establish

It does not establish over-shifting. It establishes that a gap exists between the
central bank's implied figure and full statutory pass-through on the taxable base,
and that the gap is large enough to be worth explaining. Four explanations, and the
piece has to say which one the data supports rather than assuming the flattering one:

1. Firms over-shifted. The interesting case.
2. MAS's bands are rounded. Both are exactly 1.0 wide and exactly 1.0 apart. If MAS
   shifted a band by a round number rather than publishing a computed estimate, the
   entire gap is an artefact. This remains the biggest single threat and I have not
   been able to read the MAS chapter PDFs, which are still 403.
3. MAS means direct plus second-round effects. Suppliers of exempt services cannot
   reclaim input GST, so a GST rise raises their costs and can push even exempt
   prices up. If "effects of the GST increase" includes that, 1.0 against 0.75 is
   not over-shifting, it is the sum of two channels, and the comparison is invalid.
4. My liable share is wrong, most likely because I have guessed how much of health
   and education is publicly subsidised. The bounds are wide for that reason and the
   piece should publish both, not a midpoint.

Explanation 3 is the one I currently find most plausible and it is the one that
would kill the headline. It should be tested before the headline is written, not
after.

## 9. Revised headline candidates

The sealed thesis preferred "The GST rise was under 1%. Prices rose 4.8%." That
still works if the measurement lands near the mechanical figure. Added, pending data:

- "The clean test of the 2024 GST rise was deleted" (46)
- "Singapore withdrew the data that answers this" (45)
- "The GST rise cost more than the GST" (36), only if explanation 1 survives

## 10. Standing corrections to the sealed thesis

- THESIS.md lists as an open confound "the rebasing to 2024 = 100. If the weights
  changed in January 2024 this is fatal to that year's aggregate estimate. Open
  until C2." C2 is now closed. The weights did change in January 2024. It is fatal
  to that year's aggregate estimate IN THE CURRENT SERIES ONLY, and the 2019-based
  series escapes it.
- THESIS.md says the CPI weights are needed. They are now in hand at division and
  group level from ip-e61, for both bases. The CPI file is still required for the
  price series, but the denominator question is answered.

## 11. The official figure is the same round number twice, and it should not be

Added 7 September 2026, after retrieving the MTI monthly releases.

MTI publishes "Consumer Price Developments" every month, and mti.gov.sg is reachable
from this environment where singstat.gov.sg mostly is not. These releases are
PRIMARY, contemporaneous, and on the 2019 base.

Consumer Price Developments in January 2024, released 23 February 2024:

  "For 2024 as a whole, both headline and core inflation are projected to average
  2.5-3.5%. Excluding the transitory effects of the 1%-point increase in the GST
  rate to 9%, headline and core inflation are expected to come in at 1.5-2.5%."

MAS Monetary Policy Statement, 14 April 2023, for the previous event:

  including GST, core 3.5-4.5% and headline 5.5-6.5%; excluding GST, core 2.5-3.5%
  and headline 4.5-5.5%.

Both events imply exactly 1.0 percentage point. On four separate measures.

They should not be equal. Full statutory pass-through differs between the two
events, because the base differs:

    2023   1.08/1.07 - 1 = 0.9346 per cent
    2024   1.09/1.08 - 1 = 0.9259 per cent

and the baskets differ too, since the 2024 basket carries more weight in exempt
accommodation than the 2019 basket did: rentals rise from 1,978 to 2,432 per 10,000.
A genuinely computed estimate would move between the two years. This one does not
move at all.

Every band is also exactly 1.0 wide and shifted by exactly 1.0.

## 12. What that does to the argument, and it is an improvement

The sealed thesis and section 7 above set up an over-shifting story: the official
1.0 exceeds the 0.66 to 0.75 that full statutory pass-through on the taxable base
implies, therefore firms took more than the tax. That reading is now much weaker.
The likelier explanation is that 1.0 is a round-number convention, not a
measurement: one percentage point of GST is treated as one percentage point of
inflation, and the arithmetic of the tax-inclusive multiplier and of the exempt
share of the basket is not applied.

I cannot prove that. It is an inference from three things: the figure is identical
across two events whose mechanical effects differ; the bands are exactly 1.0 wide
and exactly 1.0 apart; and I have found no published methodology behind it. The MAS
chapter PDFs, which might contain one, are still 403. What would settle it is a MAS
or MTI statement of how the figure is derived. Until then the piece says "consistent
with a convention" and not "is a convention".

This is a better piece than the one I expected to write on 4 September, and the
change came from the evidence rather than from preference, which is invariant A1
working as intended. The frame is now:

  The official line is that the GST rise added one percentage point to inflation.
  That number is the same for both rate changes although the arithmetic says it
  should not be, it is larger than full pass-through on the part of the basket that
  actually carries GST, and nobody has published a measurement. Here is one.

The headline candidate "The GST rise cost more than the GST" is withdrawn. It
asserts the over-shifting reading that this section has just weakened. New
candidates:

- "One percentage point is not a measurement" (39)
- "The same GST number, twice, wrongly" (35)
- "Nobody measured what the GST rise did" (37)

None is settled. The measurement decides.

## 13. A second route to the clean 2024 measurement

The MTI monthly releases carry Table A.1, CPI index levels on the 2019 base, and
Table A.2, year-on-year rates, by MAS's own grouping: All Items, MAS Core, Food,
Services, Retail & Other Goods, Electricity & Gas, Private Transport, Accommodation.
That grouping is better suited to this question than the ten COICOP divisions,
because it separates Accommodation, which is exempt, and Private Transport, which
was moving violently on COE prices, into their own lines.

Verified accessible: Consumer Price Developments in January 2023 (released
23 February 2023) and in January 2024 (released 23 February 2024). January 2023
index levels on the 2019 base, quoted from the release: All Items 111.397, MAS Core
108.195, Food 113.743, Services 106.669, Retail & Other Goods 100.861, Electricity &
Gas 115.037, Private Transport 134.513, Accommodation 108.142.

So if TableBuilder proves impossible, the January 2024 step can still be measured on
the old basket from contemporaneous primary releases. That is second best, because
it means hand-entering published tables rather than deriving everything from one
downloaded file, and invariant A3 wants the latter. It would have to be labelled as
what it is. But it means the 2024 event is not lost even in the worst case.

Also quoted, and a useful independent check on any estimate produced later:
"On a month-on-month basis, core CPI rose by 0.6%, due in part to the 1%-point GST
rate increase." Core excludes accommodation and private transport, so its GST-liable
share is higher than headline's, and it should show a larger step than headline. That
is a prediction the data can test.

## 14. Note on this file's own header, and everything after 8 September 2026

The line at the top of this file, "Still no CPI file, raw/ remains empty", was true
when it was written on 7 September and is left standing as a record of that. The data
arrived on 7 September and was analysed on 8 September. Findings live in RESULTS.md.

## 15. The MAS Reviews close the biggest open question

Jacob supplied the April 2023 and October 2023 Macroeconomic Reviews as PDFs on
8 September, because MAS PDF paths return 403 from this environment.

Section 8 above listed four ways the over-shifting reading could evaporate. Number two
was that MAS's bands might be rounded rather than computed. That is now settled, and
more precisely than "rounded".

MAS October 2023, footnote 16: the 2023 pass-through "was staggered across several
months, instead of passing through fully at the start of the year", retailers
"announced a temporary absorption of the tax increase", and for 2024 "the upcoming GST
hike is assumed to pass through fully in January under the current baseline".

MAS April 2023, Chapter 4 footnote 1: "a full pass-through of the GST rate hike will
occur over the course of 2023", "subject to significant uncertainty".

So the one percentage point is an assumption of full pass-through, not a measurement,
and MAS says so in its own words. Explanation three from section 8, that MAS might
mean direct plus second-round effects, is also ruled out: the figure is the direct
mechanical effect under an assumption of completeness.

CONSEQUENCE. The article says "assumed" and quotes MAS. The hedge "consistent with a
round-number convention rather than a measurement" is withdrawn. It was the right
thing to write on 7 September without the source, and the wrong thing to keep once the
source existed.

## 16. MAS corroborates the null

Two further statements matter because they point the same way as the data.

"Notably, the extent of GST hike pass-through in January was relatively modest
compared to that seen during the previous GST increase in 2007." April 2023.

"some local supermarket and pharmacy chains, as well as other retailers, absorbed the
GST increase for some items, albeit temporarily for three to six months." April 2023.

The January 2023 aggregate step is undetectable in the index. MAS's own account is
that it was modest and that pass-through was spread over months. Those agree. The
piece says so rather than presenting the null as a discovery MAS would dispute.

## 17. The staggered version was tested and fails for the same reason

14_staggered.py cumulates from December through each month to June. The 2023 estimates
drift upward toward the target, which is the shape MAS describes, but every interval
contains both the target and zero, and by April the placebo range on non-GST years is
-1.903 to +1.974 with 2023 ranking 12 of 16. Cumulating adds noise faster than signal.

This test was prompted by MAS's account and is not pre-registered by name. Anticipation
and lag were named as threats in the brief and in THESIS.md's confounds, and 04 ran the
month-by-month window, so it is not wholly post-hoc either. The article's aside says
which it is.
