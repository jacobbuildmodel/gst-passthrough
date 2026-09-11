# Data request: GST pass-through

Written 4 September 2026, before any data was downloaded.

The sandbox cannot reach SingStat, data.gov.sg or IRAS. Re-tested 4 September 2026:
the egress proxy answers 403 to CONNECT for all three hosts. Your computer and your
Chrome are both unreachable from this session as well, so the files have to come
from you by hand.

The whole analysis runs on ONE file. Everything else is conditional and I will only
ask for it once I have seen the first one.

## Step 1. The only file I need to start (one click)

Open this page:

  https://data.gov.sg/datasets/d_bdaff844e3ef89d39fceb962ff8f0791/view

Click Download. You will get a CSV of about 961 KB.

  Title      Consumer Price Index (CPI), 2024 As Base Year, Monthly
  Publisher  Department of Statistics Singapore
  Coverage   January 1961 to July 2026
  Source     SingStat TableBuilder table TS/M213751
  Licence    Singapore Open Data Licence

Upload that CSV to this chat. Do not rename it, do not open it in Excel and save it
again. Excel rewrites dates and strips leading zeros, and the MD5 has to match what
you downloaded or the reproducibility invariant fails.

## Step 2. Tell me the download date

Paste one line with the file, or type it into the chat:

  Downloaded 2026-09-0X from https://data.gov.sg/datasets/d_bdaff844e3ef89d39fceb962ff8f0791/view

I will write it into raw/RETRIEVED.txt and checksum the file myself.

## That is the whole blocking ask

Below is what I expect to need afterwards. Do not fetch any of it yet. I am listing
it so you can see where this is going, and so a later session knows what is
outstanding.

## Conditional, after I see the first file

### C1. The 2019-base monthly series - PROMOTED 7 September 2026 to ESSENTIAL

No longer conditional, and no longer a robustness check. It is the only public
series that can measure the January 2024 rate change without confounding it against
a basket revision.

SingStat's Information Paper confirms the 2024-based indices commence from January
2024, so in the current series the December-to-January step spans both the tax
change and the reweighting. The rebasing was released on 24 February 2025, which
means every CPI release through 2024 was published on the 2019 base. That series
therefore contains a December 2023 to January 2024 change computed wholly within the
old basket.

data.gov.sg has unpublished this one. The dataset page
d_ba8a05c8908b5e1dc13540286d585f8a now returns "dataset not found", which is itself
worth a line in the piece: the index that was actually published during the 2023 and
2024 rate changes is no longer on the open data portal.

It should still be in TableBuilder. Go to tablebuilder.singstat.gov.sg, search
"Consumer Price Index (CPI), 2019 As Base Year, Monthly", select all categories and
the full date range, and download as CSV.

### C2. RESOLVED 7 September 2026, do not fetch

The rebasing information paper

  https://www.singstat.gov.sg/modules/infographics/-/media/Files/publications/economy/ip-e61.pdf

Retrieved directly on the `.ashx` path, which serves where the `.pdf` path 403s. The
weights took effect in January 2024, the same month as the 8 to 9 per cent change.
Appendix III also gave the full weighting pattern for both bases, which closes the
separate question of the GST-liable share of the basket.

### C3. Confirmation that CPI prices include GST - I will retry this myself first

Any SingStat methodology page or the CPI "Our Data Explained" page stating that
collected prices are inclusive of GST. I am confident this is true, and SP Group
quotes tariffs "before GST" with GST applied on top, which points the same way, but
under invariant A6 the piece should cite a statistics-office statement rather than
an inference.

## What is NOT needed

IRAS pages. I can read iras.gov.sg through WebFetch, and mof.gov.sg too. The exempt
supplies list and the rate history are already sourced.
