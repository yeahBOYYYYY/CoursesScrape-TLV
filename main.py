import config, scrape_data
import os

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver as WebDriver


def createTmpFolder() -> None:
    if not os.path.exists(config.TMP_FOLDER_NAME):
        os.mkdir(config.TMP_FOLDER_NAME)

def main() -> None:
    chrome_options = Options()
    if not config.GUI:
        chrome_options.add_argument("--headless=new")
    service = ChromeService(executable_path=config.CHROME_DRIVER_PATH)

    browser = Chrome(service=service, options=chrome_options)
    browser.get(config.SITE_URL)
    
    createTmpFolder()
    scrape_data.scrapingHandler(browser)

    browser.quit()


if __name__ == "__main__":
    main()
