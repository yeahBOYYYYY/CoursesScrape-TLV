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



def findNumberOfYear() -> int:
    yearPop = browser.find_element(By.ID, "lstYear")
    yearPop.click()
    years = yearPop.find_elements(By.TAG_NAME, "option")
    return len(years)

def changeYear(i: int) -> str:
    yearPop = browser.find_element(By.ID, "lstYear")
    yearPop.click()
    years = yearPop.find_elements(By.TAG_NAME, "option")
    years[i].click()
    return years[i].accessible_name

def reset():
    browser.find_element(By.CLASS_NAME, "btnblues").click()

def parseNumber(name: str):
    return re.sub("[^0-9]", "", name)

def parseFaculty(fac: str):
    if "/" in fac:
        return fac[fac.find("/") + 1::]
    return fac

def parseYear(year: str) -> str:
    for i in range(2030, 2010, -1):
        if str(i) in year:
            return str(i)


utils = {0: "Instructor", 1: "Method", 2: "Building", 3: "Room", 4: "Day", 5: "Hour", 6: "Semester"}

def appendToDict(dic: dict, more: List, i: int):
    try:
        dic[utils[i]].append(more[i].text.strip())
    except:
        pass

def parseCourses(data: List[List[WebElement]], year: str):
    final = []
    for i in range(len(data)):
        try:
            dic: dict = {"Instructor": [], "Method": [], "Building": [], "Room": [], "Day": [], "Hour": [], "Semester": [],
                        "Number": parseNumber(data[i][0].find_elements(By.TAG_NAME, "td")[0].text.strip()),
                        "Name": data[i][0].find_elements(By.TAG_NAME, "td")[1].text.strip(),
                        "Faculty": parseFaculty(data[i][1].find_elements(By.TAG_NAME, "td")[1].text.strip()),
                        "Year": year
                        }
        except:
            print(len(data[i]), [d.get_attribute("outerHTML") for d in data[i]])
            raise Exception("Error parsing course data")
        for j in range(len(data[i][2::])):
            more = data[i][j + 2].find_elements(By.TAG_NAME, "td")
            for k in range(7):
                appendToDict(dic, more, k)
        for k in range(7):
            dic[utils[k]] = ";".join(dic[utils[k]])
        final.append(dic)
    a = pd.DataFrame(final)
    return a


# def seperateCourses(year: str):
#     # coursesList = browser.find_elements(By.TAG_NAME, "tbody")[1]
#     # dataList = coursesList.find_elements(By.XPATH, ".//tr[@class='listtdbld' or @class='listtd' or @style='text-align:right']")[1::]

#     # wait = WebDriverWait(browser, 10)

#     dataList = wait.until(EC.presence_of_all_elements_located((By.XPATH, "(//tbody)[2]//tr[@class='listtdbld' or @class='listtd' or @style='text-align:right']")))[1:]

#     dataStorage: List[List[WebElement]] = []
#     tmp: list = []
#     for i in range(len(dataList)):
#         if 'listtdbld' in dataList[i].get_attribute("class"):
#             dataStorage.append(tmp)
#             tmp = []
#         tmp.append(dataList[i])
#     dataStorage.append(tmp)
#     return parseCourses(dataStorage[1::], year)

def seperateCourses(year: str):
    wait = WebDriverWait(browser, 10)
    dataList: List[WebElement] = wait.until(EC.presence_of_all_elements_located((By.XPATH, "(//tbody)[2]//tr[@class='listtdbld' or @class='listtd' or @style='text-align:right']")))[1:]

    dataStorage: List[List[WebElement]] = []
    tmp: List[WebElement] = []

    for row in dataList:
        print(row.get_attribute("outerHTML"))
        if 'listtdbld' in (row.get_attribute("class") or ""):
            dataStorage.append(tmp)
            tmp = []
        tmp.append(row)
    dataStorage.append(tmp)

    ret = parseCourses(dataStorage[1:], year)
    return ret


def copyCourses(year: str) -> pd.DataFrame:
    df = None
    while True:
        try:
            tmp = seperateCourses(year)
        except Exception as e:
            print("Error!")
            raise e
        try:
            df = pd.concat([df, tmp], ignore_index=True, sort=False)
        except:
            df = tmp
        try:
            nextB = browser.find_element(By.ID, "next")
        except:
            return df
        nextB.click()


def main():
    df = None
    yearNumbers = findNumberOfYear()
    for i in range(yearNumbers):
        currYear = changeYear(i)
        print(currYear)
        browser.find_element(By.ID, "lstDep6").find_elements(By.TAG_NAME, "option")[1].click()
        browser.find_element(By.ID, "search1").click()
        tmp = copyCourses(parseYear(currYear.strip()))
        try:
            df = pd.concat([df, tmp], ignore_index=True, sort=False)
        except:
            df = tmp
        reset()
    df.to_csv(f"data.csv", index=False)


if __name__ == "__main__":
    chrome_options = Options()
    # chrome_options.add_argument("--headless=new")  # for Chrome >= 109
    service = ChromeService(executable_path=r"C:\WebDriver\chromedriver-win64\chromedriver.exe")

    browser = webdriver.Chrome(service=service, options=chrome_options)
    browser.get('https://www.ims.tau.ac.il/tal/kr/Search_P.aspx')
    # browser.save_screenshot("screenshot.png")
    main()
    browser.close()
