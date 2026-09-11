#!/usr/bin/env bash
# run_all.sh - run the whole pipeline in order from a clean checkout.
#
#   pip install -r requirements.txt
#   ./run_all.sh
#
# Requires raw/cpi_2024base_monthly.csv to be present. It is not in this repository
# by default if you cloned without it; see DATA_REQUEST.md and 00_download.py.
#
# 01 must run first: everything downstream reads out/analysis.csv. After that the
# order below is the order the analysis was developed in, and 02 to 14 are
# independent of each other.

set -euo pipefail

cd "$(dirname "$0")"

if [[ ! -f raw/cpi_2024base_monthly.csv ]]; then
  echo "raw/cpi_2024base_monthly.csv is missing. See DATA_REQUEST.md." >&2
  exit 1
fi

mkdir -p out figs

SCRIPTS=(
  01_clean.py
  02_parallel_trends.py
  03_passthrough.py
  04_placebo_and_window.py
  05_verify.py
  06_categories.py
  07_cny_controlled.py
  08_final_estimates.py
  09_robustness_and_verdicts.py
  10_lownoise.py
  11_lownoise_placebo.py
  12_figures.py
  14_staggered.py
)

for s in "${SCRIPTS[@]}"; do
  echo "=== ${s} ==="
  python3 "${s}"
done

# 13 needs the second raw file, which is a check rather than an input. Skip it if
# that file is absent rather than failing the whole run.
if [[ -f raw/cpi_2024base_monthly_tablebuilder.csv ]]; then
  echo "=== 13_crosscheck_export.py ==="
  python3 13_crosscheck_export.py
else
  echo "=== 13_crosscheck_export.py SKIPPED, second raw export not present ==="
fi

echo
echo "=== verifying checksums ==="
md5sum -c CHECKSUMS.md5

echo
echo "Done. Every file in CHECKSUMS.md5 matched, inputs and outputs alike."
