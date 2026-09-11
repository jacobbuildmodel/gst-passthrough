# The official numbers already imply over-shifting

Written 4 September 2026, from published documents only. No CPI file has been read.
Everything here is arithmetic on figures I have quoted from primary sources, plus
one number that is not yet sourced and is flagged as such.

## What MAS published

MAS Monetary Policy Statement, 14 April 2023. Retrieved 4 September 2026.
https://www.mas.gov.sg/news/monetary-policy-statements/2023/mas-monetary-policy-statement-14apr23

    2023 forecast          Including GST      Excluding GST
    MAS Core Inflation     3.5 to 4.5%        2.5 to 3.5%
    CPI-All Items          5.5 to 6.5%        4.5 to 5.5%

MAS's own wording: "Excluding the effects of the GST increase, core inflation is
projected to average 2.5-3.5%, and headline inflation 4.5-5.5%."

The two pairs of bands are separated by exactly 1.0 percentage point, on both
measures.

## Why that is interesting

A one-off level step of size d on 1 January raises the year-on-year inflation rate
in every month of that year by d, so it raises the annual average by d. The units
line up: MAS's 1.0 percentage point is directly comparable to a level step.

Full statutory pass-through of the 7 to 8 per cent change is

    1.08 / 1.07 - 1 = 0.9346 per cent

but only on the part of the basket that actually carries GST. Residential rent is an
exempt supply, and MOF states that the government absorbs GST on publicly subsidised
education and healthcare. So the expected effect on the whole index is

    0.9346 per cent x (GST-liable share of the CPI basket)

which is strictly less than 0.9346, and if the liable share is around 70 per cent it
is around 0.65.

MAS put it at 1.0.

That gap is the piece. If the liable share is well under 100 per cent and the
measured aggregate step is 1.0 percentage point, then pass-through on the taxable
base exceeded 100 per cent of the statutory amount, which is over-shifting, stated
by the central bank in its own published forecast, and as far as I can find nobody
has pointed at it.

## Four reasons this might evaporate, all of which must be checked

1. THE BANDS MAY BE ROUNDED. Both bands move by exactly 1.0, and both are exactly
   1.0 wide. MAS may simply have shifted a band by a round number rather than
   published a computed estimate. If so, "1.0" is a presentation artefact and cannot
   carry the weight of the argument. This is the single biggest threat and it has to
   go in the piece whatever the answer.

2. THESE ARE FORECASTS, NOT OUTCOMES. The April 2023 statement forecasts the 2023
   average. Realised 2023 headline inflation was lower than the 5.5-6.5 per cent
   forecast. The excluding-GST figure is a counterfactual that was never measured.

3. THE LIABLE SHARE IS NOT YET KNOWN. The whole argument turns on the GST-liable
   share of the CPI basket, and I do not have the weights. This is the number to be
   most careful about. It needs the CPI weighting pattern, and a defensible mapping
   from CPI categories to GST treatment.

4. MAS MAY MEAN SOMETHING WIDER BY "EFFECTS OF THE GST INCREASE" than the direct
   mechanical step: second-round effects through business costs, for instance. If
   so, 1.0 against 0.65 is not over-shifting, it is direct plus indirect, and the
   comparison is wrong. MAS's methodology note, if there is one, decides this.

## What this changes about the design

The CPI weights move from nice-to-have to essential. Without the GST-liable share of
the basket there is no denominator, and with no denominator there is no statement
about over-shifting at the aggregate level.

Add to the conditional data request once the main file is in hand.

## Related, from MAS Macroeconomic Review April 2023

Retrieved 4 September 2026. States core inflation rose to 5.4 per cent year on year
in Q1 2023 partly "on account of the GST hike as well as firm business cost
pressures", and that "Abstracting from the GST increase, various measures of core
inflation indicate that the underlying pace of price increases in the economy has
moderated."

No percentage-point estimate appears in the text retrieved. The PDF chapters are
403 from this environment.
