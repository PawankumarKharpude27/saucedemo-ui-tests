import re

import pytest
from playwright.sync_api import expect

from pages import InventoryPage
from tests.data import LOCKED_OUT_USER

# Every test here exercises the login itself, so start logged out.
pytestmark = pytest.mark.no_auth


@pytest.mark.smoke
def test_valid_user_lands_on_inventory(login_page, inventory_page, credentials):
    login_page.open()
    login_page.login(credentials.username, credentials.password)

    inventory_page.expect_loaded()
    expect(inventory_page.items).to_have_count(6)


@pytest.mark.regression
@pytest.mark.parametrize(
    ("username", "password", "expected_error"),
    [
        pytest.param(LOCKED_OUT_USER, "{password}", "Epic sadface: Sorry, this user has been locked out.", id="locked-out-user"),
        pytest.param("", "{password}", "Epic sadface: Username is required", id="empty-username"),
        pytest.param("{username}", "", "Epic sadface: Password is required", id="empty-password"),
        pytest.param("{username}", "wrong", "Epic sadface: Username and password do not match any user in this service", id="wrong-password"),
    ],
)
def test_login_negative(login_page, credentials, username, password, expected_error):
    # "{username}" / "{password}" placeholders resolve to configured credentials.
    username = username.format(username=credentials.username)
    password = password.format(password=credentials.password)

    login_page.open()
    login_page.login(username, password)

    expect(login_page.error).to_have_text(expected_error)
    expect(login_page.page).not_to_have_url(re.compile(InventoryPage.path))
