# GST pass-through: thesis and pre-registered tests

Committed 4 September 2026, before any data file was downloaded. Invariant A2 says
this file is not edited afterwards. Corrections and additions go in
THESIS_ADDENDUM.md.

At the time of writing, raw/ is empty. No CPI file has been read. Every number below
is either arithmetic on the statutory tax rates, or a threshold I am committing to
in advance.

## The question

Singapore raised GST from 7 to 8 per cent on 1 January 2023 and from 8 to 9 per cent
on 1 January 2024. Did consumer prices rise by the full amount of the tax, more, or
less, and which categories over-shifted?

## The arithmetic that defines "full"

A GST rise does not raise prices by the change in the rate. It raises them by the
change in the tax-inclusive multiplier. Full pass-through of the 2023 change is
1.08/1.07 - 1, which is 0.9346 per cent, not 1 per cent.

    Event          Rate change    Full pass-through
    1 Jan 2003     3% to 4%       0.9709%
    1 Jan 2004     4% to 5%       0.9615%
    1 Jul 2007     5% to 7%       1.9048%
    1 Jan 2023     7% to 8%       0.9346%
    1 Jan 2024     8% to 9%       0.9259%
    2023 and 2024 combined        1.8692%

Over-shifting means an estimated step above these figures. Under-shifting means
below. Both are ordinary results in tax incidence: the split depends on relative
elasticities, so full pass-through is a hypothesis, not an accounting identity.

## Thesis

Prices absorbed close to the full statutory amount within one month of each change,
the aggregate step was too small for a consumer to notice against ordinary monthly
inflation, and the widespread belief that the GST rise "caused" the 2023 cost of
living squeeze confuses a one-off level step of under 1 per cent with an inflation
rate that was running several times larger for reasons that had nothing to do with
tax.

I expect over-shifting to be concentrated in categories priced in round numbers,
where a 0.93 per cent increase on a 1.40 dollar item cannot be charged and the
smallest feasible increase is 10 cents, which is 7 per cent.

## Expected headline

Preferred: "The GST rise was under 1%. Prices rose 4.8%." (44 characters)

Fallbacks, in order, depending on what the data does:
- "Most categories took the GST rise in full" (41)
- "The GST rise landed in one month, not two" (41)
- "Nobody can separate the 2024 GST rise from the reweighting" (58), if C2 shows the
  HES 2023 weights took effect in January 2024

## Design, and the order in which it is allowed to fail

Primary design, as briefed: difference-in-differences, GST-liable categories as
treatment, GST-exempt and GST-absorbed categories as control.

I record now, before seeing data, that I expect this design to fail, and why. The
only large exempt category in the CPI is accommodation, because residential rent is
an exempt supply. Singapore rents rose at an unprecedented rate through 2022 and
2023. A control group whose price path is dominated by the largest rental boom in
the country's recent history cannot be assumed to be moving in parallel with
anything. The other candidate controls, publicly subsidised healthcare and
education, have GST absorbed by the government, but they are administered prices
reviewed on their own annual cycle rather than market prices.

If the pre-registered parallel-trends test fails, the failure is published as a
result and the analysis falls back to the secondary design. It does not get quietly
repaired until it passes.

Secondary design: each category is its own control across years. The counterfactual
for January 2023 in a given category is that category's own distribution of January
month-on-month changes in years with no rate change. The estimate of pass-through is
the excess January step. The 1 July 2007 change tests the method itself, because it
falls in a month with no January seasonality and no January confounds.

## Tests, committed in advance

Survives if:

T1. Parallel trends. Over the 24 months before each of the 2023 and 2024 events, an
OLS slope fitted to the monthly log difference between the GST-liable aggregate and
the exempt-or-absorbed control aggregate is not distinguishable from zero at p below
0.05, for both events.

T2. Aggregate pass-through. The excess January step in the GST-liable aggregate lies
within 0.2 percentage points of the mechanical figure: within [0.73, 1.13] for 2023
and within [0.73, 1.13] for 2024.

T3. Replication. The 2023 and 2024 point estimates agree with each other within 0.3
percentage points.

T4. The mid-year test. The July 2007 event shows an excess July step of at least 1.4
per cent, against a July baseline from non-GST years.

T5. Over-shifting exists but is not general. At least one, and fewer than half, of
the published CPI categories show an excess step more than two standard errors above
the mechanical figure.

T6. Placebo. Applying the same estimator to January 2019, 2020, 2022, 2025 and 2026
yields excess steps not distinguishable from zero at p below 0.05.

Fails if:

F1. The pre-trend slope is significant at p below 0.05 for either 2023 or 2024. The
two-group DiD is then declared invalid in the piece, by name, and the secondary
design is used.

F2. The excess step is below 0.4 percentage points or above 1.5 percentage points in
both 2023 and 2024. Full pass-through is then rejected and the piece reports the
direction.

F3. The two events differ by more than 0.5 percentage points. The piece then reports
the discrepancy as the finding and does not average them.

F4. July 2007 shows no step distinguishable from zero. The estimator is then
suspect, and the January numbers are published only with that stated.

F5. No category over-shifts by the T5 criterion. The answer to "which categories
over-shifted" is then "none detectably", and that is published as the answer.

F6. Placebo Januaries show excess steps of similar magnitude to 2023 and 2024. The
estimator is then measuring January seasonality rather than tax, and no
pass-through number is publishable at all.

## Confounds named in advance

These are threats I know about before looking. Anything I find later goes in the
addendum, flagged as found later.

- January 2024: carbon tax rose from 5 to 25 dollars per tonne on 1 January 2024.
  Hits electricity and gas, which are GST-liable, and does not hit the control.
- Q1 2024: SP Group raised the household electricity tariff 4.1 per cent from
  1 January 2024. The release attributes this to energy costs and, on the text I
  have retrieved so far, does not mention carbon tax. To be checked in full.
- December 2023: public transport fares rose. A fare change one month before the
  January event contaminates the December baseline as well as the January step.
- February 2023: tobacco excise rose in Budget 2023, one month after the first
  event.
- 2022 and 2023: the rental boom, which is the reason I expect the control group to
  fail.
- January 2023 and January 2024: CDC vouchers were issued to every household. A
  demand-side shock landing in the same month as the tax change, pushing the same
  way, and impossible to separate with aggregate CPI.
- The rebasing to 2024 = 100 with HES 2023 weights. If the weights changed in
  January 2024 this is fatal to that year's aggregate estimate. Open until C2.
- 2003 and 2004: those events sit inside the SARS shock and its recovery.

## What this piece will not do

It will not say whether the GST increase was a good idea, what the rate should be,
or what the government should do. Invariant A8.

It will not claim to identify a causal effect if the placebo test fails. Invariant
A10.

## Prior work I am not going to pretend does not exist

A Medium piece by Joel Wong on sgdecoded covers this ground. It uses annual headline
CPI and MAS core inflation for 2022 to 2025, plus anecdotes about coffee and bubble
tea prices, and concludes the macroeconomic impact was limited and transitory. It
reaches a defensible conclusion, and it has no counterfactual, no control group, no
monthly resolution, and it compares a one-off level step against annual inflation
rates without ever converting the two to the same units. That last point is the
thing I intend to do properly rather than the thing I intend to criticise.
