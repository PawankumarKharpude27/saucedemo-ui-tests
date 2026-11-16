# Sauce Demo UI Tests

This is a small Playwright and pytest suite for the public Sauce Demo site. It covers login, sorting, cart behavior, checkout, and checkout validation.

**Project owner:** Rutuja Raikar

## Setup

Use Python 3.10 or newer. From PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
```

On macOS or Linux, activate with `source .venv/bin/activate`. To run another browser, install it with `python -m playwright install firefox webkit`.

## Running Tests

Run the full parallel suite with reports using `make test` or `./run_tests.sh`; on Windows, run `.\run_tests.ps1`. To run a marker subset, use `python -m pytest -m smoke` or `make smoke`; on Windows, pass `-Marker smoke` to `.\run_tests.ps1`. The `regression` marker selects the broader checks.

For a single test:

```powershell
python -m pytest tests/test_login.py::test_valid_user_lands_on_inventory --browser chromium -n 0
```

The runner writes JUnit and HTML reports to `reports/`. Playwright traces, screenshots, and videos are retained only for failures under `test-results/`. Open a trace with `python -m playwright show-trace <path-to-trace.zip>`.

The base URL and demo credentials are set in `pyproject.toml`; command-line options and environment variables can override them. The browser is selected with `--browser` or `BROWSER`, and the runner accepts `WORKERS` to control xdist.

## Design

The `pages/` classes keep locators and page actions together, and `conftest.py` exposes them as pytest fixtures. A session fixture signs in and saves storage state; tests get a fresh context using that state, while `no_auth` login tests start signed out. The contexts use pytest-playwright's factory so failure artifacts remain attached to the right test.

Tests use roles, Sauce Demo's `data-test` attributes, and Playwright's `expect` assertions. There are no fixed sleeps. Sorting is checked against an independently sorted list, and checkout amounts use `Decimal` to avoid float rounding. The suite currently collects 13 cases across the five scenario files.

## Azure Pipelines

`azure-pipelines.yml` runs a Chromium, Firefox, and WebKit matrix on pushes and pull requests. Its steps are:

1. Select Python 3.12 with `UsePythonVersion@0`.
2. Cache pip downloads with `Cache@2`.
3. Install the pinned Python dependencies from `requirements.txt`.
4. Install the matrix browser; Microsoft-hosted agents also install its system dependencies.
5. Run `run_tests.sh` with xdist to create the JUnit and HTML reports and retain failure artifacts.
6. Publish the JUnit file with `PublishTestResults@2`, including when tests fail.
7. Publish the HTML report as a pipeline artifact after each run.
8. Publish traces, screenshots, and videos as a separate artifact only when the job fails.

The `poolType` parameter selects Microsoft-hosted Ubuntu or the named self-hosted pool. Azure Repos pull requests need a branch build-validation policy because YAML `pr` triggers are not supported there.

The local run's JUnit and HTML reports are included in `sample-reports/`. Docker support is also provided as an optional way to run the suite with the matching Playwright image.

## Assumptions and Next Steps

The public demo credentials and current `data-test` attributes are stable, and the cart keeps the order in which items were added. With more time, I would add an accessibility check, a lint stage, and coverage for the other demo users.

## AI Assistance

I used GitHub Copilot to review the existing suite, diagnose the xdist base-URL issue, and make the related fixes and documentation updates. I ran the Chromium suite locally and reviewed the resulting changes.
