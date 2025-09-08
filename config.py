"""Configuration file for the CoursesScrape-TLV project.
This file contains various settings and constants used throughout the project.
If you wish to modify any settings, please do so here."""

from typing import List

# ============================ Configurations ============================ #
SITE_URL: str = 'https://www.ims.tau.ac.il/tal/kr/Search_P.aspx' # The URL of the site to scrape
CHROME_DRIVER_PATH: str = r"C:\WebDriver\chromedriver-win64\chromedriver.exe" # The path to the ChromeDriver executable

GUI: bool = True                                  # Weather the browser will be visible or not

YEARS_TO_SCRAPE: List[str] | None = None    # List of years to scrape, If empty it will scrape all years available, תשפ"ו = 2026

TMP_FOLDER_NAME: str = "tmp_CoursesScrapeTLV"  # The name of the temporary folder to store the HTML files
KEEP_TMP_FOLDER: bool = False                     # Whether to keep the temporary folder after scraping or delete it



# ============================ Site Elements Constants ============================ #
YEAR_DROPDOWN_ID: str = "lstYear"                        # The ID of the year dropdown
YEAR_DROPDOWN_OPTIONS_TAG_NAME: str = "option"           # The tag name of the year options in the dropdown

DEPARTMENT_DROPDOWN_ID: str = "lstDep6"                  # The ID of the department dropdown, set by default to "Science"
DEPARTMENT_DROPDOWN_OPTIONS_TAG_NAME: str = "option"     # The tag name of the department options in the dropdown
DEPARTMENT_DROPDOWN_WANTED_OPTION_INDEX: int = 1         # The index of the wanted department option in the dropdown, set by default to "All"

SEARCH_BUTTON_ID: str = "search1"                       # The ID of the search button
NEXT_PAGE_BUTTON_ID: str = "next"                        # The ID of the next page button
NEW_SEARCH_BUTTON_CLASS_NAME: str = "btnblues"              # The class name of the new search button
