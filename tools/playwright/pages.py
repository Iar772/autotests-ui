# tools/playwright/pages.py
import allure
from playwright.sync_api import Playwright, Page

from config import settings, Browser  # Импортируем настройки


def initialize_playwright_page(
    playwright: Playwright,
    test_name: str,
    browser_type: Browser,
    storage_state: str | None = None,
) -> Page:
    # Используем settings.headless
    browser = playwright[browser_type].launch(headless=settings.headless)
    # Используем settings.videos_dir
    context = browser.new_context(
        base_url=settings.get_base_url(),
        storage_state=storage_state,
        record_video_dir=settings.videos_dir
    )
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()

    yield page

    # Используем settings.tracing_dir
    context.tracing.stop(path=settings.tracing_dir.joinpath(f'{test_name}.zip'))
    browser.close()

    # Используем settings.tracing_dir
    allure.attach.file(settings.tracing_dir.joinpath(f'{test_name}.zip'), name='trace', extension='zip')
    allure.attach.file(page.video.path(), name='video', attachment_type=allure.attachment_type.WEBM)
