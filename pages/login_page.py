from __future__ import annotations

from playwright.sync_api import expect

from .base_page import BasePage


class LoginPage(BasePage):
    path = "/"

    def expect_loaded(self) -> None:
        expect(self.username_input).to_be_visible()

    @property
    def username_input(self):
        return self.tid("username")

    @property
    def password_input(self):
        return self.tid("password")

    @property
    def login_button(self):
        return self.page.get_by_role("button", name="Login")

    @property
    def error(self):
        return self.tid("error")

    def login(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
