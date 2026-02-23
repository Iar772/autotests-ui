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

@pytest.fixture(scope="session")
def initialize_browser_state(playwright: Playwright) -> None:
    """
    Фикстура для регистрации нового пользователя и сохранения состояния браузера для последующего
    использования в тестах
    :param playwright: встроенная фикстура Playwright
    :return:
    """
    browser = playwright.chromium.launch(headless=False)
    # Создаем новый контекст браузера (новая сессия, которая изолирована от других)
    context = browser.new_context()
    # Открываем новую страницу в рамках контекста
    page = context.new_page()

    page.goto("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/registration")

    email_input = page.get_by_test_id('registration-form-email-input').locator('input')
    email_input.fill('user.name@gmail.com')

    username_input = page.get_by_test_id('registration-form-username-input').locator('input')
    username_input.fill('username')

    password_input = page.get_by_test_id('registration-form-password-input').locator('input')
    password_input.fill('password')

    registration_button = page.get_by_test_id('registration-page-registration-button')
    registration_button.click()

    # дожидаемся что регистрация завершилась и мы оказались на странице с дашбордами
    expect(page).to_have_url(re.compile(r".*/#/dashboard.*"))

    # Сохраняем состояние браузера (куки и localStorage) в файл для дальнейшего использования
    context.storage_state(path="browser-state.json")
    # закрываем контекст (чтобы проверить что действительно в след шагах мы работаем с уже авторизованным юзером)


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
