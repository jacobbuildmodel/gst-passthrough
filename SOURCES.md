# Sources

Every item marked PRIMARY or SECONDARY, with the date it was retrieved. Invariant A6:
news reporting is never the source of a number.

All retrievals dated 4 September 2026 unless stated. Retrieved through WebFetch,
which reaches iras.gov.sg, mof.gov.sg, mti.gov.sg, spgroup.com.sg and data.gov.sg.
It does not reach singstat.gov.sg, which returns 403 on every path tried. It reaches
mas.gov.sg HTML pages but not MAS PDFs, which return 403.

## PRIMARY, quoted and used

1. Ministry of Finance, "Goods and Services Tax".
   https://www.mof.gov.sg/policies/taxes/goods-and-services-tax/
   Retrieved 4 September 2026.
   Quoted: "When GST was introduced on 1 April 1994, the rate was 3%. This increased
   to 4% in 2003, 5% in 2004, 7% in 2007, 8% in 2023 and 9% in 2024."
   Also states the Assurance Package "Ensures that majority of the households do not
   feel the impact of the 2023/24 GST rate increase for at least 5 years", and lists
   "GST absorption on publicly subsidised education and healthcare".
   USED FOR: the five-event design, and the definition of the GST-absorbed control
   group.
   LIMITATION: gives years, not exact effective dates, for 2003, 2004 and 2007. The
   exact dates still need a statutory or IRAS source before publication.

2. Ministry of Trade and Industry, written reply to Parliamentary Question on
   businesses using the GST increase as a pretext for raising prices.
   https://www.mti.gov.sg/newsroom/written-reply-to-pqs-on-businesses-using-gst-increase-as-a-pretext-for-raising-prices
   Gan Kim Yong, Minister for Trade and Industry, 6 February 2023.
   Retrieved 4 September 2026.
   Numbers: Committee Against Profiteering received 286 feedback submissions from
   1 April 2022 to 31 January 2023, of which 26 involved specific allegations of GST
   misrepresentation.
   NOTE: the reply does not say how many of the 26 were substantiated. Do not write
   that they were.

3. Ministry of Trade and Industry, written reply to Parliamentary Question on
   complaints about raised prices due to the GST increase.
   https://www.mti.gov.sg/newsroom/written-reply-to-pq-on-complaints-about-raised-prices-due-to-gst-increase-and-feedback-in-businesses-increasing-prices-together
   Gan Kim Yong, Minister for Trade and Industry, 5 February 2024.
   Retrieved 4 September 2026.
   Quoted: the CAP "has not seen a significant increase in such feedback in January
   2024 and has not received allegations of anti-competitive behaviour during this
   period."
   NOTE: contains no case counts. The 286 and 26 figures above are 2023 only.

4. SP Group, "Electricity Tariff Revision For The Period 1 January to 31 March 2024",
   media release 29 December 2023.
   https://www.spgroup.com.sg/about-us/media-resources/news-and-media-releases/Electricity-Tariff-Revision-For-The-Period-1-January-to-31-March-2024
   Retrieved 4 September 2026.
   Numbers: household tariff up 4.1 per cent, or 1.19 cents per kWh, quarter on
   quarter. Overall up an average 4.3 per cent, or 1.18 cents per kWh. Average
   monthly bill up 4.39 dollars before GST for an HDB four-room flat. All figures
   quoted before GST.
   NOTE: on the text retrieved, the release attributes the rise to higher energy
   costs and does NOT mention carbon tax. Press coverage at the time did attribute
   it to carbon tax. This gap needs resolving from the full release before either
   claim goes in the piece.

5. data.gov.sg, "Consumer Price Index (CPI), 2024 As Base Year, Monthly", SINGSTAT.
   https://data.gov.sg/datasets/d_bdaff844e3ef89d39fceb962ff8f0791/view
   Retrieved 4 September 2026. Coverage January 1961 to July 2026.
   Source table SingStat TS/M213751. CSV about 961 KB.
   Page states the weighting pattern derives from the 2023 Household Expenditure
   Survey, adjusted to 2024 values using price changes between those years.
   STATUS: NOT DOWNLOADED. Sandbox returns 403. See DATA_REQUEST.md.
   NOTE: the page reported "last updated 27 August 2026" on one retrieval and
   "24 August 2026" on another within the same session. Record whichever the file
   itself carries when it arrives; do not publish either date until then.

## SECONDARY, used only for orientation, never for a number in the piece

6. Joel Wong, "Dissecting Price Increases in Singapore (2023-2024)", sgdecoded,
   Medium. Retrieved 4 September 2026. The existing loose treatment of this
   question. Used in THESIS.md to state what it did and did not do.

7. Wikipedia, "Goods and Services Tax (Singapore)". Retrieved 4 September 2026.
   Gives 1 January 2003, 1 January 2004 and 1 July 2007 as effective dates, citing
   contemporaneous CNA reporting. These dates are consistent with MOF's years but
   are NOT yet primary-sourced. Marked unresolved.

## Retrieved and found to contain nothing usable

8. RESOLVED, see item 13. IRAS, "Goods and Services Tax (GST): What It Is and How It Works".
   https://www.iras.gov.sg/taxes/goods-services-tax-(gst)/basics-of-gst/goods-and-services-tax-(gst)-what-it-is-and-how-it-works
   Retrieved 4 September 2026. Navigation only. The rate-change and exempt-supplies
   detail sits on child pages, two of which returned 404 on the URLs tried. The
   working URL for exempt supplies is
   https://www.iras.gov.sg/taxes/goods-services-tax-(gst)/charging-gst-(output-tax)/when-is-gst-not-charged/supplies-exempt-from-gst
   but the fetched body did not include the list itself. Retry needed.

## Blocked, 403 from this environment

9. PARTLY RESOLVED 7 September 2026. SingStat PDF paths return 403, but the SAME
   documents are readable on their `.ashx` paths. See item 14. tablebuilder is a
   different host and remains unreachable. Any SingStat document written off on
   4 September should be retried as `.ashx` before asking Jacob for it.
10. MAS PDFs only, including every Macroeconomic Review chapter PDF. The MAS HTML
    pages do load: see items 11 and 12, retrieved later in the same session. The
    chapter PDFs would settle whether MAS published a methodology behind its
    1.0 percentage point figure, and remain unread.

## Open questions that must be closed before publication

- Exact effective dates for the 2003, 2004 and 2007 rate changes, from statute or
  IRAS rather than Wikipedia.
- CLOSED 7 September 2026, see item 14. The new basket starts January 2024. The
  current series cannot identify the 2024 event; the 2019-based series can.
- A SingStat statement that CPI prices are collected inclusive of GST. Now likely
  reachable on an `.ashx` path; retry before asking Jacob.
- Whether MAS published a pass-through estimate, and what it was.
- CLOSED 4 September 2026, see item 13.

## Added later on 4 September 2026, after the first pass

11. MAS, "MAS Monetary Policy Statement - April 2023", 14 April 2023.
    https://www.mas.gov.sg/news/monetary-policy-statements/2023/mas-monetary-policy-statement-14apr23
    Retrieved 4 September 2026. PRIMARY.
    2023 forecasts including GST: MAS Core 3.5-4.5%, CPI-All Items 5.5-6.5%.
    Excluding GST: core 2.5-3.5%, headline 4.5-5.5%.
    Quoted: "Excluding the effects of the GST increase, core inflation is projected
    to average 2.5-3.5%, and headline inflation 4.5-5.5%."
    USED FOR: the implied 1.0 percentage point GST contribution. See
    notes/01_mas_implied_estimate.md for the four ways this could be wrong.
    CAUTION: these are forecasts, not outcomes, and both bands move by exactly 1.0,
    which may be rounding rather than a computed estimate.

12. MAS, Macroeconomic Review Volume XXII Issue 1, April 2023 (landing page, not
    the PDF chapters, which are 403).
    https://www.mas.gov.sg/publications/macroeconomic-review/2023/volume-xxii-issue-1-apr-2023
    Retrieved 4 September 2026. PRIMARY.
    Quoted: core inflation rose to 5.4% year on year in Q1 2023 partly "on account
    of the GST hike as well as firm business cost pressures"; and "Abstracting from
    the GST increase, various measures of core inflation indicate that the
    underlying pace of price increases in the economy has moderated."
    Contains no percentage-point estimate in the retrieved text.

## Added to the open questions

- The CPI weighting pattern by category, for the 2024 base and ideally the 2019
  base. This is now ESSENTIAL rather than optional: the GST-liable share of the
  basket is the denominator for any statement about over-shifting.
- Whether MAS's "effects of the GST increase" means the direct mechanical step only,
  or includes second-round cost effects. This decides whether 1.0 percentage point
  can be compared with the mechanical figure at all.
- CDC voucher tranche dates and values for January 2023 and January 2024. The CDC
  site retrieved on 4 September 2026 shows only 2026 tranches. Not yet sourced.

13. IRAS e-Tax Guide, "GST: General Guide for Businesses", Seventeenth Edition,
    30 January 2026.
    https://www.iras.gov.sg/media/docs/default-source/e-tax/etaxguide_gst_gst-general-guide-for-businesses(1).pdf
    Retrieved 4 September 2026. PRIMARY.
    Exempt supplies, quoted: "These are supplies that are specifically exempted from
    GST under the Fourth Schedule to the GST Act. They include the provision of
    financial services, sale and lease of residential properties and local supply of
    investment precious metals (IPM)."
    Zero-rated supplies, quoted: "exports of goods" and "provision of international
    services".
    Out-of-scope examples given: salaries paid to employees, goods delivered from
    outside Singapore to outside Singapore, sales within a Free Trade Zone or a
    Zero GST / Licensed warehouse, and private transactions.
    USED FOR: the definition of the control group.
    NOTE: the exempt list is introduced with "They include", so it is not
    exhaustive. Digital payment tokens have been exempt since 1 January 2020 and do
    not appear in this sentence. Do not present the quoted three as the complete
    Fourth Schedule.
    IMPLICATION FOR THE DESIGN, recorded before seeing data: of the exempt
    categories, only "sale and lease of residential properties" has meaningful
    weight in the CPI. Zero-rated supplies are exports and international services,
    which by construction are not in a domestic consumer price index at all. So the
    briefed control group reduces, in practice, to accommodation.

14. Department of Statistics Singapore, Information Paper on Rebasing of the
    Consumer Price Index (2024 as Base Year).
    https://www.singstat.gov.sg/-/media/files/publications/economy/ip-e61.ashx
    Retrieved 7 September 2026. PRIMARY.
    NOTE ON ACCESS: the `.pdf` path for this document returns 403 from this
    environment; the `.ashx` path serves it.
    Quoted: the rebased series "will be released on 24 February 2025"; the new
    series begins "with indices commencing from January 2024"; and "the 2019-based
    CPI data series are linked to the 2024-based CPI data series by re-scaling them
    to the new base year of 2024 via a link factor. The link factor is the ratio of
    the annual 2024-based index in 2024 to the annual 2019-based index in 2024."
    States the CPI was reclassified to S-COICOP 2022, retaining ten main divisions,
    with Information & Communication renamed from Communication and Recreation,
    Sport & Culture renamed from Recreation & Culture.
    Appendix III gives division and group weights for both bases. Transcribed to
    cpi_weights.csv. All division and group totals reconcile to their parents and to
    10,000, which is the check that the table was read correctly.
    USED FOR: closing C2; establishing that January 2023 is clean because a scalar
    link factor preserves month-on-month changes; and computing the GST-liable share
    of the basket, which is the denominator for any over-shifting claim.

15. Department of Statistics Singapore, Consumer Price Index January 2025 press
    release.
    https://www.singstat.gov.sg/-/media/files/news/cpijan25.ashx
    Retrieved 7 September 2026. PRIMARY.
    Quoted: "The CPI for general households has been rebased from base year of 2019
    to 2024." Weighting pattern "derived from the expenditure values obtained from
    the Household Expenditure Survey (HES) 2023, and updated to 2024 values by
    taking into account price changes between 2023 and 2024."

16. Department of Statistics Singapore, Information Paper ip-e60.
    https://www.singstat.gov.sg/-/media/files/publications/economy/ip-e60.ashx
    Retrieved 7 September 2026. CHECKED AND NOT RELEVANT. It is "Rebasing of
    Singapore Manufactured Products and Domestic Supply Price Indices (Base Year
    2023=100)", February 2024, and concerns producer prices, not consumer prices.
    Recorded so a later session does not re-fetch it.

17. Ministry of Trade and Industry, "Consumer Price Developments in January 2023",
    released 23 February 2023. Base 2019 = 100.
    https://www.mti.gov.sg/-/media/MTI/Newsroom/Press-Releases/2023/02/Consumer-Price-Developments-in-January-2023.pdf
    Retrieved 7 September 2026. PRIMARY, and contemporaneous with the first event.
    Table A.1 index levels for January 2023 quoted in the release: All Items 111.397,
    MAS Core 108.195, Food 113.743, Services 106.669, Retail & Other Goods 100.861,
    Electricity & Gas 115.037, Private Transport 134.513, Accommodation 108.142.
    Year on year for January 2023: All Items 6.6%, MAS Core 5.5%, Food 8.1%,
    Services 4.2%, Retail & Other Goods 3.3%, Electricity & Gas 11.5%, Private
    Transport 14.3%, Accommodation 5.0%.
    Quoted on GST: "the one-off effect of the 1%-point GST increase as well as
    seasonal effects associated with the Chinese New Year".
    STATUS UNDER A4: these are figures read off a document. They are quotable as
    primary but they are NOT the analysis. The analysis must come from a downloaded
    series file. Use these as a cross-check on whatever the file gives.

18. Ministry of Trade and Industry, "Consumer Price Developments in January 2024",
    released 23 February 2024. Base 2019 = 100.
    https://www.mti.gov.sg/-/media/MTI/Newsroom/Press-Releases/2024/02/Consumer-Price-Developments-in-January-2024.pdf
    Retrieved 7 September 2026. PRIMARY, and contemporaneous with the second event,
    a year before the rebasing existed.
    Quoted: "MAS Core Inflation fell to 3.1% on a year-on-year basis in January,
    from 3.3% in December. This was driven by lower services and food inflation,
    notwithstanding the increase in the GST rate from 8% to 9% in January."
    Quoted: "On a month-on-month basis, core CPI rose by 0.6%, due in part to the
    1%-point GST rate increase."
    Quoted outlook: "For 2024 as a whole, both headline and core inflation are
    projected to average 2.5-3.5%. Excluding the transitory effects of the 1%-point
    increase in the GST rate to 9%, headline and core inflation are expected to come
    in at 1.5-2.5%."
    USED FOR: the implied 1.0 percentage point for the 2024 event, which matches the
    2023 implied figure exactly although the mechanical effects differ. See
    THESIS_ADDENDUM.md sections 11 and 12.

## Access routes learned, for later sessions

- singstat.gov.sg: `.pdf` paths 403, `.ashx` paths serve. Not every `.ashx` works:
  ip-e61.ashx, ip-e60.ashx and cpijan25.ashx served; cpijan24.ashx and cpijan23.ashx
  did not. tablebuilder.singstat.gov.sg is a separate host and is unreachable.
- mti.gov.sg: fully reachable, including the monthly Consumer Price Developments
  PDFs. This is the best route to contemporaneous 2019-base CPI figures.
- mas.gov.sg: HTML pages serve, PDFs 403.
- data.gov.sg: dataset pages serve; the actual file download does not.

19. PUB, Singapore's National Water Agency, "Water price to rise from April 2024;
    Government to provide support for lower- and middle-income households",
    press release 27 September 2023.
    https://www.pub.gov.sg/Resources/News-Room/PressReleases/2023/09/Water-price-to-rise-from-April-2024-Government-to-provide-support
    Retrieved 8 September 2026. PRIMARY.
    States the previous water price revision was in 2017, and announces +20 cents per
    cubic metre from 1 April 2024 and a further +30 cents from 1 April 2025, from a
    base of $2.74 per cubic metre. Quoted: "All figures are before GST."
    USED FOR: establishing that no water price change took effect on 1 January 2023 or
    1 January 2024, which is what makes the Water Supply CPI series a clean natural
    experiment for GST pass-through. Also, indirectly, for C3: PUB quotes the tariff
    before GST and the CPI series steps by very close to the statutory multiplier,
    which is only possible if the collected consumer price includes GST.
    CROSS-CHECK PASSED: every change in the Water Supply index since 2015 matches a
    dated administrative decision. 2017-07 +15.10% and 2018-07 +14.70% are the two
    phases of the 2017 revision; 2024-04 +6.99% and 2025-04 +10.46% are the two
    phases announced here; the only other moves are 2023-01 and 2024-01.

## Access routes, updated 8 September 2026

- pub.gov.sg: press releases under /Resources/News-Room/ serve. The
  /Public/WaterLoop/ pages 403.

20. data.gov.sg, dataset d_ba8a05c8908b5e1dc13540286d585f8a, "Consumer Price Index
    (CPI), 2019 As Base Year, Monthly".
    https://data.gov.sg/datasets/d_ba8a05c8908b5e1dc13540286d585f8a/view
    Checked 4 September 2026 and again 8 September 2026. Both times the page returns
    "You might have followed an invalid link or this dataset has been unpublished."
    PRIMARY, in the sense that the portal's own response is the evidence.
    USED FOR: the article's claim that the index in force during both rate changes is
    no longer on the open data portal. Two checks four days apart.

## Note on API access, 8 September 2026

Jacob offered a SingStat TableBuilder Developer API key. It cannot help this
environment. Tested 8 September 2026: curl to api-open.data.gov.sg, data.gov.sg and
tablebuilder.singstat.gov.sg all return HTTP 000, meaning the egress proxy refuses
CONNECT before any request is sent. Authentication happens after a connection is
established, so no key, header or token changes the outcome. Any API retrieval has to
run on Jacob's own machine, with the result uploaded.

21. Monetary Authority of Singapore, Macroeconomic Review, Volume XXII Issue 1,
    April 2023. PDF supplied by Jacob 8 September 2026 because MAS PDF paths return
    403 from this environment. PRIMARY.

    Methodology footnote, Chapter 4 Macroeconomic Policy, footnote 1, quoted in full:
      "Although subject to significant uncertainty, MAS estimates' indicate that a
       full pass-through of the GST rate hike will occur over the course of 2023."

    Section 3.2 Consumer Price Developments, quoted:
      "EPG estimates that a substantial proportion of the GST hike has already been
       reflected in consumer prices, even as the full degree of pass-through has yet
       to occur for a few CPI components. There was strong evidence of significant
       GST pass-through in the services components, particularly food services, where
       business cost pressures have accumulated. In comparison, some local supermarket
       and pharmacy chains, as well as other retailers, absorbed the GST increase for
       some items, albeit temporarily for three to six months."

    Also quoted: "The impact of the GST increase on m-o-m core inflation ebbed in
    February and March."

    Chapter 4, quoted:
      "Notably, the extent of GST hike pass-through in January was relatively modest
       compared to that seen during the previous GST increase in 2007."

    USED FOR: MAS's own account that the January 2023 step was modest and that
    pass-through was expected to complete over the year rather than in January. This
    CORROBORATES the null rather than contradicting it.
    NOTE ON WORDING: MAS uses "significant" in its ordinary sense, not the
    statistical one. Do not quote it in a way that implies a p-value.

22. Monetary Authority of Singapore, Macroeconomic Review, Volume XXII Issue 2,
    October 2023. PDF supplied by Jacob 8 September 2026. PRIMARY.

    Footnote 16, Chapter 3, quoted in full. This is the single most important
    quotation in the piece:
      "The increase in the GST will still add to core inflation next year, albeit
       marginally, as the impact of the GST hike this year was staggered across
       several months, instead of passing through fully at the start of the year.
       Several retailers such as major supermarket chains announced a temporary
       absorption of the tax increase or offered a token discount early this year. In
       the absence of similar announcements for 2024 thus far, the upcoming GST hike
       is assumed to pass through fully in January under the current baseline."

    USED FOR: two things. First, MAS states that the 2023 pass-through was staggered
    rather than concentrated in January, which is why a January-only test finds
    nothing. Second, MAS states that full January pass-through in 2024 is an
    ASSUMPTION under its baseline. That closes the question the piece previously
    hedged: the one percentage point is not a measurement, and MAS says so itself.
    The article can now say "assumed" rather than "consistent with a convention".

    Also quoted, on water: "the planned increase in water prices next year - the
    first adjustment since 2018". PUB's own release says the last revision was 2017.
    Both are right: the 2017 revision was implemented in two phases, July 2017 and
    July 2018, which is exactly what the CPI water series shows.

## Open questions closed on 8 September 2026

- Whether MAS published a methodology behind the 1.0 percentage point. CLOSED. It is
  an assumption of full pass-through, stated as such in both Reviews. See items 21
  and 22.
- Whether the data.gov.sg copy of the CPI faithfully reproduces SingStat's own
  numbers. CLOSED. Jacob supplied a direct TableBuilder export of the same table,
  TS/M213751, on 8 September 2026. All 37,881 observations agree exactly with the
  data.gov.sg download, with no value mismatches and no observations present in one
  and absent from the other. See 13_crosscheck_export.py. This also settles the
  earlier ambiguity about the last-updated date: SingStat's own export header says
  24/08/2026.

## Still open

- The 2019-base monthly series. Not supplied. No claim in the article depends on it.
- Exact statutory effective dates for the 2003, 2004 and 2007 changes. The article
  names no day for any of those three.
- Whether PUB rounds billed rates to the cent, which would explain the 0.089 and
  0.048 percentage point excess over statutory in the water series. The article
  states the gap and does not explain it.
