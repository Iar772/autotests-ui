import re

import pytest
from playwright.sync_api import Page, Playwright, expect


@pytest.fixture  # Объявляем фикстуру, по умолчанию скоуп function, то что нам нужно
def chromium_page(playwright: Playwright) -> Page:  # type: ignore
    """
    Фикстура для инициализации страницы в браузере Chromium
    :param playwright: встроенная фикстура Playwright
    :return:
    """
    # Запускаем браузер
    browser = playwright.chromium.launch(headless=False)

    # Передаем страницу для использования в тесте
    yield browser.new_page() # type: ignore

    # Закрываем браузер после выполнения тестов
    browser.close()


from pages.authentication.registration_page import RegistrationPage


@pytest.fixture(scope="session")
def initialize_browser_state(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Работаем с регистрационной страницей через Page Object
    registration_page = RegistrationPage(page=page)
    registration_page.visit('https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/registration')
    registration_page.registration_form.fill(email='user.name@gmail.com', username='username', password='password')
    registration_page.click_registration_button()

    context.storage_state(path="browser-state.json")
    browser.close()

@pytest.fixture
def chromium_page_with_state(initialize_browser_state, playwright: Playwright) -> Page:  # type: ignore
    """
    Фикстура для открытия новой страницы браузера, используя ранее сохраненное состояние в фикстуре
    initialize_browser_state
    :param initialize_browser_state: фикстура для регистрации нового юзера и сохранения состояния браузера
    :param playwright: встроенная фикстура Playwright
    :return:
    """
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="browser-state.json")
    page = context.new_page()
    yield page  # type: ignore
