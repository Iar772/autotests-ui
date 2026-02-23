from playwright.sync_api import sync_playwright, expect
import re

with sync_playwright() as playwright:
    # открываем браузер
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    # переходим на страницу регистрации
    page.goto("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/registration")

    #находим нужные нам элементы: имейл, пароль, юзернейм и кнопка регистрации
    email_input = page.get_by_test_id("registration-form-email-input").locator("input")
    email_input.fill("user.name@gmail.com")

    username_input = page.get_by_test_id("registration-form-username-input").locator("input")
    username_input.fill("username")

    password_input = page.get_by_test_id("registration-form-password-input").locator("input")
    password_input.fill("password")

    signup_button = page.get_by_test_id("registration-page-registration-button")
    signup_button.click()

    # дополнительно убеждаемся что редирект произошел, в урле есть /#/dashboard
    expect(page).to_have_url(re.compile(r".*/#/dashboard.*"))

    # вытаскиваем тайтл и проверяем что в тайтле отображается Dashboard
    dashboard_title = page.get_by_test_id("dashboard-toolbar-title-text")
    expect(dashboard_title).to_have_text("Dashboard")
