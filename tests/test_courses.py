from playwright.sync_api import  expect, Page
import re
import pytest

@pytest.mark.courses
@pytest.mark.regression
def test_empty_courses_list(chromium_page_with_state: Page) -> None:
    chromium_page_with_state.goto("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/courses")
    # дополнительно убеждаемся что редирект произошел, в урле есть /#/courses
    expect(chromium_page_with_state).to_have_url(re.compile(r".*/#/courses.*"))

    # проверяем наличие и текст заголовка "Courses"
    courses_toolbar_title_txt = chromium_page_with_state.get_by_test_id("courses-list-toolbar-title-text")
    expect(courses_toolbar_title_txt).to_be_visible()
    expect(courses_toolbar_title_txt).to_have_text("Courses")

    # проверяем наличие и текст блока "There is no results"
    courses_view_title_txt = chromium_page_with_state.get_by_test_id("courses-list-empty-view-title-text")
    expect(courses_view_title_txt).to_be_visible()
    expect(courses_view_title_txt).to_have_text("There is no results")

    # проверяем наличие и видимость иконки пустого блока
    courses_list_icon = chromium_page_with_state.get_by_test_id("courses-list-empty-view-icon")
    expect(courses_list_icon).to_be_visible()

    # проверяем наличие и текст описания блока: "Results from the load test pipeline will be displayed here"
    courses_description_txt = chromium_page_with_state.get_by_test_id("courses-list-empty-view-description-text")
    expect(courses_description_txt).to_be_visible()
    expect(courses_description_txt).to_have_text("Results from the load test pipeline will be displayed here")

