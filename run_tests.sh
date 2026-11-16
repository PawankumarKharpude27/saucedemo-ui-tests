#!/usr/bin/env bash
# One-command run: parallel, JUnit + HTML reports in reports/, failure artifacts in test-results/.
#   ./run_tests.sh                          # whole suite, chromium
#   MARKER=smoke ./run_tests.sh             # marker subset
#   BROWSER=firefox WORKERS=2 ./run_tests.sh
#   ./run_tests.sh tests/test_login.py -k locked   # extra args go straight to pytest
set -euo pipefail
cd "$(dirname "$0")"

BROWSER="${BROWSER:-chromium}"
WORKERS="${WORKERS:-auto}"
MARKER="${MARKER:-}"
REPORT_DIR="${REPORT_DIR:-reports}"

mkdir -p "$REPORT_DIR" test-results

args=(
  --browser "$BROWSER"
  -n "$WORKERS"
  --output "test-results/$BROWSER"
  --junitxml="$REPORT_DIR/junit-$BROWSER.xml"
  --html="$REPORT_DIR/report-$BROWSER.html" --self-contained-html
)
[[ -n "$MARKER" ]] && args+=(-m "$MARKER")

exec python -m pytest "${args[@]}" "$@"
