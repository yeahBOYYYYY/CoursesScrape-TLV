import config
import re
from typing import List

from selenium.webdriver.chrome.webdriver import WebDriver as WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def getPossibleYears(browser: WebDriver) -> List[str]:
    yearPop = browser.find_element(By.ID, config.YEAR_DROPDOWN_ID)
    yearPop.click()
    years = yearPop.find_elements(By.TAG_NAME, config.YEAR_DROPDOWN_OPTIONS_TAG_NAME)
    yearNames = [''.join(re.findall(r'\d', year.accessible_name))[4::] for year in years]
    return yearNames

def scrapeYear(browser: WebDriver, yearName: str) -> None:
    pageNumber = 0
    while True:
        WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "body")))
        html = browser.page_source
        with open(f"{config.TMP_FOLDER_NAME}/{yearName}-{pageNumber}.html", "w", encoding="utf-8") as file:
            file.write(html)

        try:
            browser.find_element(By.ID, config.NEXT_PAGE_BUTTON_ID).click()
        except:
            return
        pageNumber += 1

def yearSwitcher(browser: WebDriver, yearIndex: int) -> None:
    yearPop = browser.find_element(By.ID, config.YEAR_DROPDOWN_ID)
    yearPop.click()
    years = yearPop.find_elements(By.TAG_NAME, config.YEAR_DROPDOWN_OPTIONS_TAG_NAME)
    years[yearIndex].click()

def setFaculty(browser: WebDriver) -> None:
    depPop = browser.find_element(By.ID, config.DEPARTMENT_DROPDOWN_ID)
    depPop.click()
    departments = depPop.find_elements(By.TAG_NAME, config.DEPARTMENT_DROPDOWN_OPTIONS_TAG_NAME)
    departments[config.DEPARTMENT_DROPDOWN_WANTED_OPTION_INDEX].click()

def reset(browser: WebDriver) -> None:
    browser.find_element(By.CLASS_NAME, config.NEW_SEARCH_BUTTON_CLASS_NAME).click()

def scrapingHandler(browser: WebDriver) -> None:
    possibleYears: List[str] = getPossibleYears(browser)
    wantedYears: List[str] = config.YEARS_TO_SCRAPE if config.YEARS_TO_SCRAPE is not None else possibleYears
    yearsIndices: List[set] = [i for i in range(len(possibleYears)) if possibleYears[i] in wantedYears]
    
    for i in yearsIndices:
        yearSwitcher(browser, i)
        setFaculty(browser)
        browser.find_element(By.ID, config.SEARCH_BUTTON_ID).click()
        scrapeYear(browser, possibleYears[i])
        reset(browser)