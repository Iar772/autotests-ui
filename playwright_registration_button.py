from playwright.sync_api import sync_playwright, expect


with sync_playwright() as playwright:
    # открываем браузер
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    # переходим на страницу регистрации
    page.goto("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/registration")

    # находим кнопку регистрации и проверяем что она недоступна для клика
    signup_button = page.get_by_test_id("registration-page-registration-button")
    expect(signup_button).to_be_disabled()

    # находим нужные нам элементы: имейл, пароль, юзернейм и кнопка регистрации
    email_input = page.get_by_test_id("registration-form-email-input").locator("input")
    email_input.fill("user.name@gmail.com")

    username_input = page.get_by_test_id("registration-form-username-input").locator("input")
    username_input.fill("username")

    password_input = page.get_by_test_id("registration-form-password-input").locator("input")
    password_input.fill("password")

    # проверяем что кнопка регистрации сменила свое состояние на enabled (доступна для клика)
    expect(signup_button).to_be_enabled()
