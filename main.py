"""Main module to run the CoursesScrape-TLV project."""
import pandas as pd

import config, scrape_data, parse_pages
import os

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver as WebDriver


def createTmpFolder() -> None:
    """
    Creates the temporary folder if it does not already exist.

    The folder path is defined in `config.TMP_FOLDER_NAME`. If the folder
    already exists, the function does nothing.

    @return: None
    """
    if not os.path.exists(config.TMP_FOLDER_NAME):
        os.mkdir(config.TMP_FOLDER_NAME)


def setupBrowser() -> WebDriver:
    """
    Sets up and returns a Selenium WebDriver instance for Chrome.
    
    Configuration:
     - If `config.GUI` is False, the browser runs in headless mode.
     - The ChromeDriver path is specified in `config.CHROME_DRIVER_PATH`.
     - The browser automatically navigates to the site URL defined in
       `config.SITE_URL`.

    @return: WebDriver A configured Selenium WebDriver instance.
    """
    chrome_options = Options()
    if not config.GUI:
        chrome_options.add_argument("--headless=new")
    service = ChromeService(executable_path=config.CHROME_DRIVER_PATH)

    browser = Chrome(service=service, options=chrome_options)
    browser.get(config.SITE_URL)
    return browser


def main() -> None:
    """
    Main entry point for running the scraping process.
    
    Workflow:
     1. Initialize a Selenium WebDriver instance with `setupBrowser`.
     2. Create the temporary folder (if needed) with `createTmpFolder`.
     3. Run the scraping handler via `scrape_data.scrapingHandler`.
     4. Remove the temporary folder if `config.KEEP_TMP_FOLDER` is False.
     5. Quit the WebDriver instance.

    @return: None
    """
    browser = setupBrowser()
    createTmpFolder()
    scrape_data.scrapingHandler(browser)
    browser.quit()
    df: pd.DataFrame = parse_pages.fileHandler()
    if not config.KEEP_TMP_FOLDER:
        os.rmdir(config.TMP_FOLDER_NAME)
    df.to_csv(f"data.csv", index=False)


if __name__ == "__main__":
    main()
