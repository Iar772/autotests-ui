from playwright.sync_api import Page, expect

from components.authentication.registration_form_component import RegistrationFormComponent
from pages.base_page import BasePage


class RegistrationPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.registration_form = RegistrationFormComponent(page, 'registration-form')
        self.registration_button = page.get_by_test_id('registration-page-registration-button')

    def click_registration_button(self):
        self.registration_button.click()
