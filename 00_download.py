"""
00_download.py - fetch the raw CPI file and record provenance.

Run this on a machine that can reach data.gov.sg. The analysis sandbox cannot:
the egress proxy answers 403 to CONNECT for data.gov.sg, singstat.gov.sg and
iras.gov.sg.

    python 00_download.py

Writes raw/cpi_2024base_monthly.csv and raw/RETRIEVED.txt.

If this script fails for any reason, the manual path is identical in effect:
open https://data.gov.sg/datasets/d_bdaff844e3ef89d39fceb962ff8f0791/view in a
browser, click Download, save the file into raw/ under the name above, and write
raw/RETRIEVED.txt by hand in the format this script uses. Do not open the CSV in
Excel and re-save it; that rewrites dates and breaks the checksum.

Python 3.11. Standard library only, so there is nothing to install.
"""

import hashlib
import json
import pathlib
import sys
import urllib.request
from datetime import datetime, timezone

DATASET_ID = "d_bdaff844e3ef89d39fceb962ff8f0791"
DATASET_TITLE = "Consumer Price Index (CPI), 2024 As Base Year, Monthly"
DATASET_PAGE = f"https://data.gov.sg/datasets/{DATASET_ID}/view"
POLL_URL = (
    "https://api-open.data.gov.sg/v1/public/api/datasets/"
    f"{DATASET_ID}/poll-download"
)
OUT_NAME = "cpi_2024base_monthly.csv"

RAW = pathlib.Path(__file__).resolve().parent / "raw"


def fetch(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "gst-passthrough/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def main():
    RAW.mkdir(exist_ok=True)
    target = RAW / OUT_NAME

    print(f"Resolving download URL for {DATASET_ID} ...")
    try:
        meta = json.loads(fetch(POLL_URL).decode("utf-8"))
    except Exception as exc:
        print(f"FAILED to reach the data.gov.sg API: {exc}", file=sys.stderr)
        print(f"Use the manual path instead. See the docstring, or {DATASET_PAGE}",
              file=sys.stderr)
        return 1

    url = meta.get("data", {}).get("url")
    if not url:
        print(f"API returned no download URL. Full response:\n{meta}", file=sys.stderr)
        return 1

    print("Downloading ...")
    payload = fetch(url, timeout=180)
    target.write_bytes(payload)

    digest = hashlib.md5(payload).hexdigest()
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    (RAW / "RETRIEVED.txt").write_text(
        "GST pass-through analysis - raw data provenance\n"
        "\n"
        f"file       {OUT_NAME}\n"
        f"title      {DATASET_TITLE}\n"
        f"publisher  Department of Statistics Singapore\n"
        f"dataset    {DATASET_ID}\n"
        f"page       {DATASET_PAGE}\n"
        f"source     SingStat TableBuilder TS/M213751\n"
        f"licence    Singapore Open Data Licence\n"
        f"retrieved  {stamp}\n"
        f"bytes      {len(payload)}\n"
        f"md5        {digest}\n"
        "\n"
        "This is a fixed snapshot, not a live mirror. SingStat revises CPI and\n"
        "rebases it periodically. Re-downloading later will not reproduce the\n"
        "published figures and is not meant to.\n",
        encoding="utf-8",
        newline="\n",
    )

    print(f"\nWrote {target}")
    print(f"  bytes {len(payload)}")
    print(f"  md5   {digest}")
    print(f"Wrote {RAW / 'RETRIEVED.txt'}")
    print("\nNow upload raw/ back to the analysis chat.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
