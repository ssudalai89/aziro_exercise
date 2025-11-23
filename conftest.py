import os
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

# ============================================================
# Browser Fixture Setup
# ============================================================
@pytest.fixture(scope="function")
def browser():
    """Launches and quits the browser for the test session."""
    from selenium.webdriver.chrome.service import Service
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://trends.builtwith.com/websitelist/Responsive-Tables")
    driver.maximize_window()
    yield driver
    driver.quit()

# ============================================================
# Pytest HTML Report Configuration
# ============================================================
def pytest_configure(config):
    """Customize HTML report output directory and metadata."""
    # Create reports and screenshots folders if not exist
    reports_dir = os.path.join(os.getcwd(), "reports")
    screenshots_dir = os.path.join(reports_dir, "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)

    # Dynamic HTML report name
    report_file = f"report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html"
    config.option.htmlpath = os.path.join(reports_dir, report_file)

    # Metadata
    metadata = getattr(config, '_metadata', {})
    metadata["Project Name"] = "Aziro Automation Tests Development Exercise"
    metadata["Test Environment"] = "PROD"
    metadata["Browser"] = "Chrome"
    metadata["Executed By"] = os.getenv("USERNAME") or os.getenv("USER", "Unknown")

    # Store screenshot path for access in hook
    config.screenshots_dir = screenshots_dir

# ============================================================
# Modify HTML Report Title
# ============================================================
def pytest_html_report_title(report):
    report.title = "Pytest Selenium Automation Report"

# ============================================================
# Screenshot on Failure (Saved Inside reports/screenshots/)
# ============================================================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a screenshot and additional details to the HTML report on test failure."""
    outcome = yield
    report = outcome.get_result()

    # Only handle failures during the "call" phase
    if report.when == "call" and report.failed:
        browser_fixture = item.funcargs.get("browser", None)
        if browser_fixture:
            try:
                # Access screenshots folder from config
                screenshots_dir = getattr(item.config, "screenshots_dir", "reports/screenshots")
                os.makedirs(screenshots_dir, exist_ok=True)

                # Create a timestamp for unique screenshot names
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # Screenshot file path with timestamp
                screenshot_name = f"{item.name}_{timestamp}.png"
                screenshot_path = os.path.join(screenshots_dir, screenshot_name)
                
                # Capture screenshot
                browser_fixture.save_screenshot(screenshot_path)

                # Attach to HTML report if pytest-html is available
                if hasattr(report, "extra"):
                    pytest_html = item.config.pluginmanager.getplugin("html")
                    if pytest_html:
                        # Add failure details
                        report.extra.append(pytest_html.extras.html(
                            f"<div><h3>Failure Details:</h3>"
                            f"<p>Test: {item.name}</p>"
                            f"<p>URL: {browser_fixture.current_url}</p>"
                            f"<p>Time: {timestamp}</p></div>"
                        ))
                        
                        # Add screenshot
                        with open(screenshot_path, "rb") as img:
                            # Convert to base64 for embedding in HTML
                            import base64
                            screenshot_base64 = base64.b64encode(img.read()).decode('utf-8')
                            report.extra.append(pytest_html.extras.html(
                                f'<div><img src="data:image/png;base64,{screenshot_base64}" width="800px"></div>'
                            ))
                            
                        print(f"\nScreenshot saved: {screenshot_path}")
                        
            except Exception as e:
                print(f"\nFailed to capture screenshot: {str(e)}")

# ============================================================
# Clean Up Metadata (Optional)
# ============================================================
@pytest.hookimpl(optionalhook=True)
def pytest_metadata(metadata):
    """Clean up default environment info in pytest-html report."""
    metadata.pop("Plugins", None)
    metadata.pop("Packages", None)