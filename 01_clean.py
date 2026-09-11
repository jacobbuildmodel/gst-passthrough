"""
01_clean.py - reshape the raw CPI file into a tidy long series.

Input  raw/cpi_2024base_monthly.csv   (fixed snapshot, md5 in raw/RETRIEVED.txt)
Output out/analysis.csv               (long: series, level, parent, date, index)
       out/series_index.csv           (the hierarchy, one row per series)

The raw file is wide: one row per series, one column per month, newest month first,
with hierarchy carried in the leading whitespace of the DataSeries label
(0, 4, 8, 12 spaces). Nothing else in the file records the hierarchy, so the indent
is load-bearing and is parsed rather than assumed.
"""
import csv, hashlib, pathlib, sys
from datetime import date

HERE = pathlib.Path(__file__).resolve().parent
RAW = HERE / "raw" / "cpi_2024base_monthly.csv"
OUT = HERE / "out"
EXPECTED_MD5 = "a48b09388082c3545e461d5c58bb6b90"

MONTHS = {m: i for i, m in enumerate(
    ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"], 1)}


def main():
    OUT.mkdir(exist_ok=True)
    payload = RAW.read_bytes()
    got = hashlib.md5(payload).hexdigest()
    if got != EXPECTED_MD5:
        print(f"FAIL raw file md5 {got}, expected {EXPECTED_MD5}", file=sys.stderr)
        return 1
    print(f"raw md5 {got} OK")

    rows = list(csv.reader(RAW.open()))
    hdr, body = rows[0], rows[1:]

    periods = []
    for col in hdr[1:]:
        y, m = col[:4], col[4:]
        periods.append((int(y), MONTHS[m], col))
    print(f"{len(periods)} monthly columns, {periods[-1][2]} to {periods[0][2]}")

    # hierarchy from indent
    series, stack = [], {}
    for r in body:
        lab = r[0]
        indent = len(lab) - len(lab.lstrip())
        name = lab.strip()
        level = indent // 4
        stack[level] = name
        parent = stack.get(level - 1, "") if level > 0 else ""
        series.append({"series": name, "level": level, "parent": parent, "row": r})

    with (OUT / "series_index.csv").open("w", newline="\n") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["series", "level", "parent"])
        for s in series:
            w.writerow([s["series"], s["level"], s["parent"]])

    n_obs = n_missing = 0
    with (OUT / "analysis.csv").open("w", newline="\n") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["series", "level", "parent", "year", "month", "date", "index"])
        for s in series:
            for j, (y, m, _col) in enumerate(periods):
                raw = s["row"][j + 1].strip()
                if raw in ("", "na", "-", "n.a."):
                    n_missing += 1
                    continue
                w.writerow([s["series"], s["level"], s["parent"], y, m,
                            f"{y}-{m:02d}", raw])
                n_obs += 1

    print(f"{len(series)} series, {n_obs} observations written, {n_missing} blank cells skipped")
    print(f"wrote {OUT/'analysis.csv'} and {OUT/'series_index.csv'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
