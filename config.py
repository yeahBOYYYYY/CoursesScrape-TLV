"""Configuration file for the CoursesScrape-TLV project.
This file contains various settings and constants used throughout the project.
If you wish to modify any settings, please do so here."""

from typing import List, Optional

# ============================ Configurations ============================ #
CHROME_DRIVER_PATH: str = r"C:\WebDriver\chromedriver-win64\chromedriver.exe"  # The path to the ChromeDriver executable

GUI: bool = False  # Weather the browser will be visible or not

YEARS_TO_SCRAPE: Optional[List[str]] = None  # List of years to scrape, If empty it will scrape all years available, תשפ"ו = 2026

TMP_FOLDER_NAME: str = "tmp_CoursesScrapeTLV"  # The name of the temporary folder to store the HTML files
KEEP_TMP_FOLDER: bool = False  # Whether to keep the temporary folder after scraping or delete it

TIMEOUT_FOR_SCRAPING = 60       # Number of seconds to wait for a web page before moving on

# ============================ Site Elements Constants ============================ #
SITE_URL: str = 'https://www.ims.tau.ac.il/tal/kr/Search_P.aspx'  # The URL of the site to scrape

YEAR_DROPDOWN_ID: str = "lstYear"  # The ID of the year dropdown

DEPARTMENT_DROPDOWN_ID: str = "lstDep6"  # The ID of the department dropdown, set by default to "Science"
DEPARTMENT_DROPDOWN_WANTED_OPTION_INDEX: int = 1  # The index of the wanted department option in the dropdown, set by default to "All"

SEARCH_BUTTON_ID: str = "search1"  # The ID of the search button
NEXT_PAGE_BUTTON_ID: str = "next"  # The ID of the next page button
PREV_PAGE_BUTTON_ID: str = "prev"  # The ID of the prev page button
NEW_SEARCH_BUTTON_CLASS_NAME: str = "btnblues"  # The class name of the new search button

BODY_ELEMENTS_TAG_NAME: str = "//tbody"  # The tag name of the body elements containing the courses
COURSE_BOLD_ROW_CLASS: str = "listtdbld"  # The class name of the bold course rows. course number, group and name
COURSE_BOLD_ROW_CLASS_XPATH: str = f"@class='{COURSE_BOLD_ROW_CLASS}'"  # The class xpath of the bold course rows. course number, group and name
COURSE_FACULTY_ROW_CLASS_XPATH: str = "@class='listtd'"  # The class xpath of the faculty course rows. faculty name
COURSE_DATA_ROW_STYLE_XPATH: str = "@style='text-align:right'"  # The style attribute xpath of the data course rows. lecturer, type, building, room, day, hour and semester
COURSE_METADATA_ROW_STYLE_XPATH: str = "@style='border-bottom:solid thin #1398ff;text-align:right;background-color: #ffffff;'"  # The class xpath of the metadata course rows. Syllabus link and exam links.
COURSE_DATA_XPATH: str = f".//tr[{COURSE_BOLD_ROW_CLASS_XPATH} or {COURSE_FACULTY_ROW_CLASS_XPATH} or {COURSE_DATA_ROW_STYLE_XPATH} or {COURSE_METADATA_ROW_STYLE_XPATH}]"  # The combined xpath to select course rows
