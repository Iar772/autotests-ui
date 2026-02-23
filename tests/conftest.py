import pytest  # Импортируем pytest
from playwright.sync_api import Page, Playwright


@pytest.fixture  # Объявляем фикстуру, по умолчанию скоуп function, то что нам нужно
def chromium_page(playwright: Playwright) -> Page:  # type: ignore
    # Запускаем браузер
    browser = playwright.chromium.launch(headless=False)

    # Передаем страницу для использования в тесте
    yield browser.new_page() # type: ignore

    # Закрываем браузер после выполнения тестов
    browser.close()