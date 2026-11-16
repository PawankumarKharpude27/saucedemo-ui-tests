import pytest
from playwright.sync_api import expect

from tests.data import BACKPACK, BIKE_LIGHT, CHECKOUT_THANK_YOU


@pytest.mark.smoke
@pytest.mark.regression
def test_end_to_end_checkout(
    inventory_page, cart_page, checkout_info_page, checkout_overview_page, checkout_complete_page
):
    inventory_page.open()
    inventory_page.add_to_cart(BACKPACK, BIKE_LIGHT)
    expect(inventory_page.cart_badge).to_have_text("2")

    inventory_page.open_cart()
    cart_page.expect_loaded()
    expect(cart_page.names).to_have_text([BACKPACK, BIKE_LIGHT])
    expect(cart_page.badge).to_have_text("2")
    cart_prices = cart_page.read_prices()

    cart_page.checkout()
    checkout_info_page.expect_loaded()
    checkout_info_page.fill_form("Ada", "Lovelace", "12345")
    checkout_info_page.continue_()

    checkout_overview_page.expect_loaded()
    expect(checkout_overview_page.names).to_have_text([BACKPACK, BIKE_LIGHT])
    subtotal = checkout_overview_page.subtotal()
    tax = checkout_overview_page.tax()
    total = checkout_overview_page.total()
    assert subtotal == sum(cart_prices), "item total must equal the sum of the cart prices"
    assert subtotal + tax == total, f"{subtotal} + {tax} != {total}"

    checkout_overview_page.finish()
    checkout_complete_page.expect_loaded()
    expect(checkout_complete_page.header).to_have_text(CHECKOUT_THANK_YOU)
    expect(inventory_page.cart_badge).to_have_count(0)
