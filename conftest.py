"""Fixtures and configuration.

Config precedence (highest first):  CLI option  >  environment variable  >  pyproject.toml
  base URL    --base-url            PYTEST_BASE_URL     base_url
  username    --sauce-username      SAUCE_USERNAME      sauce_username
  password    --sauce-password      SAUCE_PASSWORD      sauce_password
  browser     --browser chromium|firefox|webkit  (BROWSER env var in run_tests.*)
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path

import pytest
from playwright.sync_api import Browser, Page, Playwright, expect

from pages import (
    CartPage,
    CheckoutCompletePage,
    CheckoutInfoPage,
    CheckoutOverviewPage,
    InventoryPage,
    LoginPage,
)


# --------------------------------------------------------------------------- config
def pytest_addoption(parser: pytest.Parser) -> None:
    group = parser.getgroup("saucedemo")
    group.addoption("--sauce-username", default=None, help="Valid user (env: SAUCE_USERNAME)")
    group.addoption("--sauce-password", default=None, help="Password (env: SAUCE_PASSWORD)")
    parser.addini("sauce_username", help="Default valid username")
    parser.addini("sauce_password", help="Default password")


@pytest.fixture(scope="session")
def base_url(pytestconfig: pytest.Config) -> str:
    """Keep the configured base URL available in xdist worker processes."""
    return (
        pytestconfig.getoption("base_url")
        or os.environ.get("PYTEST_BASE_URL")
        or pytestconfig.getini("base_url")
    )


@dataclass(frozen=True)
class Credentials:
    username: str
    password: str


def _resolve(config: pytest.Config, option: str, env: str, ini: str) -> str:
    value = config.getoption(option) or os.environ.get(env) or config.getini(ini)
    if not value:
        raise pytest.UsageError(f"Missing config: set --{option.replace('_', '-')}, ${env} or '{ini}'")
    return value


@pytest.fixture(scope="session")
def credentials(pytestconfig: pytest.Config) -> Credentials:
    return Credentials(
        username=_resolve(pytestconfig, "sauce_username", "SAUCE_USERNAME", "sauce_username"),
        password=_resolve(pytestconfig, "sauce_password", "SAUCE_PASSWORD", "sauce_password"),
    )


# --------------------------------------------------------------------------- playwright
@pytest.fixture(scope="session", autouse=True)
def _use_data_test_as_test_id(playwright: Playwright) -> None:
    """Sauce Demo uses data-test instead of Playwright's default data-testid."""
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture(scope="session")
def auth_state(
    browser: Browser,
    browser_context_args: dict,
    credentials: Credentials,
    tmp_path_factory: pytest.TempPathFactory,
    _use_data_test_as_test_id: None,
) -> Path:
    """Log in once per session (once per xdist worker) and save cookies + localStorage.

    tmp_path_factory gives every xdist worker its own directory, so workers never
    race on the same file."""
    path = tmp_path_factory.mktemp("auth") / "state.json"
    context = browser.new_context(**browser_context_args)
    try:
        page = context.new_page()
        LoginPage(page).open().login(credentials.username, credentials.password)
        expect(page).to_have_url(re.compile(r"/inventory\.html$"))
        context.storage_state(path=path)
    finally:
        context.close()
    return path


@pytest.fixture
def page(request: pytest.FixtureRequest, new_context) -> Page:
    """Override of pytest-playwright's `page`.

    Logged in via storage state by default; tests marked `no_auth` start logged out.
    Using the plugin's `new_context` factory (instead of browser.new_context) keeps
    trace / screenshot / video retain-on-failure working."""
    if request.node.get_closest_marker("no_auth"):
        context = new_context()
    else:
        # Lazy lookup: no_auth tests never trigger the login at all.
        context = new_context(storage_state=request.getfixturevalue("auth_state"))
    return context.new_page()


# --------------------------------------------------------------------------- page objects
@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    return InventoryPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture
def checkout_info_page(page: Page) -> CheckoutInfoPage:
    return CheckoutInfoPage(page)


@pytest.fixture
def checkout_overview_page(page: Page) -> CheckoutOverviewPage:
    return CheckoutOverviewPage(page)


@pytest.fixture
def checkout_complete_page(page: Page) -> CheckoutCompletePage:
    return CheckoutCompletePage(page)
