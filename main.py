from settings import *
import re
import pandas as pd
from typing import List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService


def main() -> None:
    pass


if __name__ == "__main__":
    chrome_options = Options()
    if not GUI:
        chrome_options.add_argument("--headless=new")
    service = ChromeService(executable_path=CHROME_DRIVER_PATH)

    browser = webdriver.Chrome(service=service, options=chrome_options)
    browser.get(SITE_URL)
    main()
    browser.close()
