from playwright.sync_api import sync_playwright

BASE_URL = "https://nikita-filonov.github.io/qa-automation-engineer-ui-course"

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)

    # Регистрация и сохранение состояния браузера
    context = browser.new_context()
    page = context.new_page()

    page.goto(f"{BASE_URL}/#/auth/registration")

    page.get_by_test_id("registration-form-email-input").locator("input").fill("user.name@gmail.com")
    page.get_by_test_id("registration-form-username-input").locator("input").fill("username")
    page.get_by_test_id("registration-form-password-input").locator("input").fill("password")
    page.get_by_test_id("registration-page-registration-button").click()

    page.wait_for_timeout(3000)

    context.storage_state(path="browser-state.json")
    context.close()

    # Новая сессия с сохранённым состоянием
    new_context = browser.new_context(storage_state="browser-state.json")
    new_page = new_context.new_page()

    new_page.goto(f"{BASE_URL}/#/courses")
    new_page.wait_for_timeout(3000)

    # Проверки страницы Courses
    title = new_page.get_by_test_id("courses-list-toolbar-title-text")
    assert title.is_visible()
    assert title.text_content() == "Courses"

    empty_title = new_page.get_by_test_id("courses-list-empty-view-title-text")
    assert empty_title.is_visible()
    assert empty_title.text_content() == "There is no results"

    icon = new_page.get_by_test_id("courses-list-empty-view-icon")
    assert icon.is_visible()

    description = new_page.get_by_test_id("courses-list-empty-view-description-text")
    assert description.is_visible()
    assert description.text_content() == "Results from the load test pipeline will be displayed here"

    new_context.close()
    browser.close()