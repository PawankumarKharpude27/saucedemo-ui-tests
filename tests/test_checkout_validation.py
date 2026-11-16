import pytest
from playwright.sync_api import expect

from tests.data import BACKPACK


@pytest.mark.regression
@pytest.mark.parametrize(
    ("first", "last", "postal", "expected_error"),
    [
        pytest.param("", "Lovelace", "12345", "Error: First Name is required", id="missing-first-name"),
        pytest.param("Ada", "", "12345", "Error: Last Name is required", id="missing-last-name"),
        pytest.param("Ada", "Lovelace", "", "Error: Postal Code is required", id="missing-postal-code"),
    ],
)
def test_checkout_form_validation(
    inventory_page, cart_page, checkout_info_page, first, last, postal, expected_error
):
    inventory_page.open()
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.open_cart()
    cart_page.checkout()

    checkout_info_page.expect_loaded()
    checkout_info_page.fill_form(first, last, postal)
    checkout_info_page.continue_()

    expect(checkout_info_page.error).to_have_text(expected_error)
    checkout_info_page.expect_loaded()  # still on step one
