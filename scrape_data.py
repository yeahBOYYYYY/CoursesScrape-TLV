"""Module for scraping and saving locally pages data from the website."""

import config
import re
from typing import List

from selenium.webdriver.chrome.webdriver import WebDriver as WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def getPossibleYears(browser: WebDriver) -> List[str]:
    """
    Retrieves all possible academic years available on the website.

    The function opens the year dropdown, extracts all options, and parses
    their accessible names to return a clean list of year strings.

    @param browser: Selenium WebDriver instance used to control the browser.

    @return: List[str] List of available academic years.
    """
    yearPop = browser.find_element(By.ID, config.YEAR_DROPDOWN_ID)
    yearPop.click()
    years = yearPop.find_elements(By.TAG_NAME, "option")
    yearNames = [''.join(re.findall(r'\d', year.accessible_name))[4::] for year in years]
    return yearNames


def scrapeYear(browser: WebDriver, yearName: str) -> None:
    """
    Scrapes all pages for a given academic year and saves the HTMLs locally.

    Each page's HTML source is saved into the temporary folder defined by
    `config.TMP_FOLDER_NAME`, with filenames in the format:
        {yearName}-{pageNumber}.html
    
    The function repeatedly clicks the "next page" button (configured in
    `config.NEXT_PAGE_BUTTON_ID`) until no further page is available.

    @param browser: Selenium WebDriver instance used to control the browser.
    @param yearName: Name of the academic year, used for naming saved HTML files.

    @return: None
    """
    pageNumber = 0
    while True:
        WebDriverWait(browser, config.TIMEOUT_FOR_SCRAPING).until(
            EC.any_of(
                EC.visibility_of_element_located((By.ID, config.NEXT_PAGE_BUTTON_ID)),
                EC.visibility_of_element_located((By.ID, config.PREV_PAGE_BUTTON_ID)),
            )
        )

        html = browser.page_source
        with open(f"{config.TMP_FOLDER_NAME}/{yearName}-{pageNumber}.html", "w", encoding="utf-8") as file:
            file.write(html)

        try:
            browser.find_element(By.ID, config.NEXT_PAGE_BUTTON_ID).click()
        except:
            return
        pageNumber += 1


def yearSwitcher(browser: WebDriver, yearIndex: int) -> None:
    """
    Switches the website to the desired academic year.

    Opens the year dropdown menu and selects the year at the given index.

    @param browser: Selenium WebDriver instance used to control the browser.
    @param yearIndex: Index of the desired year in the dropdown options.

    @return: None
    """
    yearPop = browser.find_element(By.ID, config.YEAR_DROPDOWN_ID)
    yearPop.click()
    years = yearPop.find_elements(By.TAG_NAME, "option")
    years[yearIndex].click()


def setFaculty(browser: WebDriver) -> None:
    """
    Sets the faculty/department filter to the desired option.

    Opens the department dropdown and selects the option at the index defined
    in `config.DEPARTMENT_DROPDOWN_WANTED_OPTION_INDEX`.

    @param browser: Selenium WebDriver instance used to control the browser.

    @return: None
    """
    depPop = browser.find_element(By.ID, config.DEPARTMENT_DROPDOWN_ID)
    depPop.click()
    departments = depPop.find_elements(By.TAG_NAME, "option")
    departments[config.DEPARTMENT_DROPDOWN_WANTED_OPTION_INDEX].click()


def reset(browser: WebDriver) -> None:
    """
    Resets the search form to its initial state.

    Clicks the reset/new search button configured in
    `config.NEW_SEARCH_BUTTON_CLASS_NAME`.

    @param browser: Selenium WebDriver instance used to control the browser.

    @return: None
    """
    browser.find_element(By.CLASS_NAME, config.NEW_SEARCH_BUTTON_CLASS_NAME).click()


def scrapingHandler(browser: WebDriver) -> None:
    """
    Main handler function for scraping and saving pages.

    Determines which years to scrape based on `config.YEARS_TO_SCRAPE`. For each
    selected year, the function switches the year, sets the faculty, starts the
    search, scrapes all pages for that year, and resets the form.

    Workflow:
     1. Collect possible years from the website.
     2. Filter them according to config settings.
     3. For each selected year:
        - Switch year
        - Set faculty
        - Start search
        - Scrape pages
        - Reset search
    
    @param browser: Selenium WebDriver instance used to control the browser.

    @return: None
    """
    possibleYears: List[str] = getPossibleYears(browser)
    wantedYears: List[str] = config.YEARS_TO_SCRAPE if config.YEARS_TO_SCRAPE is not None else possibleYears
    yearsIndices: List[int] = [i for i in range(len(possibleYears)) if possibleYears[i] in wantedYears]

    for i in yearsIndices:
        yearSwitcher(browser, i)
        setFaculty(browser)
        browser.find_element(By.ID, config.SEARCH_BUTTON_ID).click()
        scrapeYear(browser, possibleYears[i])
        reset(browser)
