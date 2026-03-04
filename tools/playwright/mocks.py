from playwright.sync_api import Page, Route


def mock_static_resources(page: Page):
    page.route("**/*.{ico,png,svg,webm,mp3,mp4,woff,woff2}", lambda route: route.abort())
