from playwright.sync_api import sync_playwright, expect
import re
import pytest

@pytest.mark.courses
@pytest.mark.regression
def test_empty_courses_list():
    with sync_playwright() as playwright:
        # Запускаем Chromium браузер в обычном режиме (не headless)
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
        context.close()

        context2 = browser.new_context(storage_state="browser-state.json")
        page2 = context2.new_page()

        # проверяем что страница открывается БЕЗ авторизации
        page2.goto("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/courses")
        # дополнительно убеждаемся что редирект произошел, в урле есть /#/courses
        expect(page2).to_have_url(re.compile(r".*/#/courses.*"))

        # проверяем наличие и текст заголовка "Courses"
        courses_toolbar_title_txt = page2.get_by_test_id("courses-list-toolbar-title-text")
        expect(courses_toolbar_title_txt).to_be_visible()
        expect(courses_toolbar_title_txt).to_have_text("Courses")

        # проверяем наличие и текст блока "There is no results"
        courses_view_title_txt = page2.get_by_test_id("courses-list-empty-view-title-text")
        expect(courses_view_title_txt).to_be_visible()
        expect(courses_view_title_txt).to_have_text("There is no results")

        # проверяем наличие и видимость иконки пустого блока
        courses_list_icon = page2.get_by_test_id("courses-list-empty-view-icon")
        expect(courses_list_icon).to_be_visible()

        # проверяем наличие и текст описания блока: "Results from the load test pipeline will be displayed here"
        courses_description_txt = page2.get_by_test_id("courses-list-empty-view-description-text")
        expect(courses_description_txt).to_be_visible()
        expect(courses_description_txt).to_have_text("Results from the load test pipeline will be displayed here")
