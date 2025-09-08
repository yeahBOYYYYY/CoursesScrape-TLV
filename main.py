import settings, scrape_data
import os

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver as WebDriver


def createTmpFolder() -> None:
    if not os.path.exists(settings.TMP_FOLDER_NAME):
        os.mkdir(settings.TMP_FOLDER_NAME)

def main() -> None:
    chrome_options = Options()
    if not settings.GUI:
        chrome_options.add_argument("--headless=new")
    service = ChromeService(executable_path=settings.CHROME_DRIVER_PATH)

    browser = Chrome(service=service, options=chrome_options)
    browser.get(settings.SITE_URL)
    
    createTmpFolder()
    scrape_data.scrapingHandler(browser)

    browser.quit()


if __name__ == "__main__":
    main()
