from playwright.sync_api import  expect, Page
import re
import pytest

from pages.courses_list_page import CoursesListPage


@pytest.mark.courses
@pytest.mark.regression
def test_empty_courses_list(courses_list_page: CoursesListPage) -> None:
    courses_list_page.visit("https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/courses")
    courses_list_page.sidebar.check_visible()
    courses_list_page.navbar.check_visible("username")
    courses_list_page.check_visible_empty_view()
    courses_list_page.toolbar_view.check_visible()
