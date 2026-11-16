import pytest
from playwright.sync_api import expect

from tests.data import BACKPACK, BIKE_LIGHT


@pytest.mark.regression
def test_removing_item_in_cart_updates_inventory(inventory_page, cart_page):
    inventory_page.open()
    inventory_page.add_to_cart(BACKPACK, BIKE_LIGHT)
    inventory_page.open_cart()
    expect(cart_page.items).to_have_count(2)

    cart_page.remove(BACKPACK)
    expect(cart_page.items).to_have_count(1)
    expect(cart_page.names).to_have_text([BIKE_LIGHT])
    expect(cart_page.badge).to_have_text("1")

    cart_page.continue_shopping()
    inventory_page.expect_loaded()

    expect(inventory_page.cart_badge).to_have_text("1")
    expect(inventory_page.add_button(BACKPACK)).to_be_visible()   # back to "Add to cart"
    expect(inventory_page.remove_button(BACKPACK)).to_have_count(0)
    expect(inventory_page.remove_button(BIKE_LIGHT)).to_be_visible()  # untouched item
    expect(inventory_page.add_button(BIKE_LIGHT)).to_have_count(0)


@pytest.mark.regression
def test_removing_last_item_hides_badge(inventory_page, cart_page):
    inventory_page.open()
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.open_cart()

    cart_page.remove(BACKPACK)
    cart_page.continue_shopping()

    expect(inventory_page.cart_badge).to_have_count(0)
    expect(inventory_page.add_button(BACKPACK)).to_be_visible()
