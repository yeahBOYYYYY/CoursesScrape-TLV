"""Module for parsing and creating CSV file from locally saved HTML pages."""

import config

import os, re
from typing import Generator, List, Optional, Tuple, Set, Dict
import pandas as pd

from lxml import etree, html
from lxml.etree import _ElementTree as ElementTree
from lxml.html import HtmlElement


class CourseData:
    def __init__(
            self,
            number: Optional[str] = None,
            group: Optional[str] = None,
            name: Optional[str] = None,
            faculty: Optional[str] = None,
            school: Optional[str] = None,
            year: Optional[str] = None,
            instructor: Optional[List[str]] = None,
            method: Optional[List[str]] = None,
            building: Optional[List[str]] = None,
            room: Optional[List[str]] = None,
            day: Optional[List[str]] = None,
            hour: Optional[List[str]] = None,
            semester: Optional[List[str]] = None
    ):
        self.Number: Optional[str] = number
        self.Group: Optional[str] = group
        self.Name: Optional[str] = name
        self.Faculty: Optional[str] = faculty
        self.School: Optional[str] = school
        self.Year: Optional[str] = year

        self.Instructor: List[str] = instructor if instructor is not None else []
        self.Method: List[str] = method if method is not None else []
        self.Building: List[str] = building if building is not None else []
        self.Room: List[str] = room if room is not None else []
        self.Day: List[str] = day if day is not None else []
        self.Hour: List[str] = hour if hour is not None else []
        self.Semester: List[str] = semester if semester is not None else []

    def __repr__(self):
        return f"{{Number = {self.Number}; Group = {self.Group}; Name = {self.Name}; Faculty = {self.Faculty}; School = {self.School}; Year = {self.Year}; Instructor = {self.Instructor}; Method = {self.Method}; Building = {self.Building}; Room = {self.Room}; Day = {self.Day}; Hour = {self.Hour}; Semester = {self.Semester}}}"

    def toDict(self) -> dict[str, str]:
        instructorStr = "\n".join(self.Instructor)
        methodStr = "\n".join(self.Method)
        buildingStr = "\n".join(self.Building)
        roomStr = "\n".join(self.Room)
        dayStr = "\n".join(self.Day)
        hourStr = "\n".join(self.Hour)
        semesterStr = "\n".join(self.Semester)

        return {
            "Number": self.Number,
            "Group": self.Group,
            "Name": self.Name,
            "Instructor": instructorStr,
            "Year": self.Year,
            "Semester": semesterStr,
            "Method": methodStr,
            "School": self.School,
            "Faculty": self.Faculty,
            "Building": buildingStr,
            "Room": roomStr,
            "Day": dayStr,
            "Hour": hourStr
        }


def element_to_html_str(element: HtmlElement) -> str:
    """
    Convert an HtmlElement to its full HTML string.

    @param element: The HtmlElement to convert.
    @return: The full HTML string representation of the element.
    """
    return etree.tostring(element, encoding="unicode", method="html")


def openHTMLFileGenerator() -> Generator[Tuple[ElementTree, str], None, None]:
    """
    Generator that iterates over all HTML files inside `config.TMP_FOLDER_NAME`
    and yields them as parsed `ElementTree` objects using UTF-8 encoding.

    @yield: ElementTree Parsed HTML tree for each file.
    """
    for filename in os.listdir(config.TMP_FOLDER_NAME):
        if filename.endswith(".html"):
            filepath = os.path.join(config.TMP_FOLDER_NAME, filename)
            file = open(filepath, "r", encoding="utf-8")
            fileContent: str = file.read()
            file.close()
            yield html.fromstring(fileContent), filename


def getCoursesData(pageTree: ElementTree) -> List[HtmlElement]:
    """
    Extracts course row elements from a parsed HTML page tree.

    The function extracts all course rows matching the XPath `config.COURSE_DATA_XPATH`,
    which are the XPaths to the rows in the courses data.

    @param pageTree: Parsed HTML tree `ElementTree` of a page.

    @return: List[HtmlElement] List of HtmlElement rows representing courses data.
            Returns an empty list if there are fewer than two body elements.
    """
    bodyElements: List[HtmlElement] = pageTree.xpath(config.BODY_ELEMENTS_TAG_NAME)
    if len(bodyElements) < 2:
        return []

    coursesElement: HtmlElement = bodyElements[1]

    coursesList: List[HtmlElement] = coursesElement.xpath(config.COURSE_DATA_XPATH)
    return coursesList


def parseBoldRow(boldRow: HtmlElement) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Parses a course bold row <tr> and extracts (course_code, section_number, course_name).

    @param boldRow: HtmlElement representing the <tr> bold row.

    @return: Tuple of three option strings:
            (course_code, section_number, course_name)
    """
    course_code: Optional[str] = None
    section_number: Optional[str] = None
    course_name: Optional[str] = None

    tds = boldRow.xpath("./td")
    if not tds or len(tds) < 2:
        return course_code, section_number, course_name

    first_td_text = tds[0].text_content().strip()
    code_match = re.search(r"\d{4}-\d{4}", first_td_text)
    if code_match:
        course_code = code_match.group(0)

    section_match = re.search(r"קב':\s*(\d+)", first_td_text)
    if section_match:
        section_number = section_match.group(1)

    course_name = tds[1].text_content().strip() if tds[1].text_content().strip() else None

    return course_code, section_number, course_name


def parseFacultyRow(facultyRow: HtmlElement) -> Tuple[Optional[str], Optional[str]]:
    """
    Parses a faculty row <tr> and extracts the faculty name.

    @param facultyRow: HtmlElement representing the <tr> faculty row.

    @return: Tuple of two option strings:
            (faculty_name, school_name)
    """
    tds = facultyRow.xpath("./td")
    if not tds:
        return None, None

    faculty_text: str = tds[-1].text_content().strip()
    school_name, faculty_name = faculty_text.split("/", 1)
    return school_name, faculty_name


def parseDataRows(dataRows: List[HtmlElement], lecturers: List[str], methods: List[str], buildings: List[str],
                  rooms: List[str], days: List[str], hours: List[str], semesters: List[str]) -> None:
    """
    Recursively parses data rows corresponding to a single course instance,
    extracting lecturer, method, building, room, day, hour, and semester
    information from <td> cells.

    Each recursive call consumes one row (the first in the list) and
    appends its data into the given lists, then continues parsing
    the remaining rows until none are left.

    @param dataRows:    List of HtmlElement rows (<tr>) to be parsed.
                        Each row is expected to contain at least 7 <td> elements.
    @param lecturers:   List collecting lecturer names (appended in order).
    @param methods:     List collecting teaching methods.
    @param buildings:   List collecting building names or codes.
    @param rooms:       List collecting room identifiers.
    @param days:        List collecting day information.
    @param hours:       List collecting hour/time ranges.
    @param semesters:   List collecting semester information.

    @return: None
    """
    if not dataRows:
        return
    dataRow = dataRows[0]
    tds = dataRow.xpath("./td")
    if (not tds) or (len(tds) < 7):
        return

    lecturer: str = tds[0].text_content().strip()
    lecturer = lecturer.replace(u"\xa0", " ")
    lecturers.append(lecturer)
    methods.append(tds[1].text_content().strip())
    buildings.append(tds[2].text_content().strip())
    rooms.append(tds[3].text_content().strip())
    days.append(tds[4].text_content().strip())
    hours.append(tds[5].text_content().strip())
    semesters.append(tds[6].text_content().strip())

    parseDataRows(dataRows[1::], lecturers, methods, buildings, rooms, days, hours, semesters)


def parseYear(filename: str) -> str:
    """
    Extracts the academic year string from a given filename.

    The year is assumed to be encoded in the first four characters
    of the filename, which is consistent with the naming convention:
        {year}-{pageNumber}.html

    @param filename: Filename string to parse.

    @return: The 4-character year prefix.
    """
    return filename[:4:]


def parseCourses(coursesSeparated: List[List[HtmlElement]], filename: str) -> List[CourseData]:
    """
    Parses groups of course HTML elements into structured CourseData objects.

    The function performs the following steps for each course group:
    - Extracts number, group, and name from the bold row.
    - Extracts faculty and school from the faculty row.
    - Derives the academic year from the filename.
    - Recursively parses schedule rows into Instructor, Method, Building,
      Room, Day, Hour, and Semester lists.

    @param coursesSeparated:    List of course groups, where each group is a list of
                                HtmlElements representing rows (<tr>) for a single course.
                                The first row contains bold data (course number, group, name),
                                the second row contains faculty/school info, and the
                                subsequent rows contain schedule data.
    @param filename:            Name of the file being parsed (used to derive the year).

    @return: List of fully populated CourseData objects for all parsed courses.
    """
    li: List[CourseData] = []
    for courseGroup in coursesSeparated:
        Number, Group, Name = parseBoldRow(courseGroup[0])
        print(Number, Group, Name)
        School, Faculty = parseFacultyRow(courseGroup[1])
        Year = parseYear(filename)
        courseData = CourseData(number=Number, group=Group, name=Name, faculty=Faculty, school=School, year=Year)
        parseDataRows(courseGroup[2:-1:], courseData.Instructor, courseData.Method, courseData.Building,
                      courseData.Room, courseData.Day, courseData.Hour, courseData.Semester)
        li.append(courseData)
    return li


def separateCourses(coursesDataList: List[HtmlElement]) -> List[List[HtmlElement]]:
    """
    Separates a flat list of course rows into grouped sublists based on bold rows.

    Rows with the class specified in `config.COURSE_BOLD_ROW_CLASS` are treated as
    the start of a new course entry. All subsequent rows until the next bold row
    are grouped together in the same sublist.

    @param coursesDataList: List of HtmlElement objects representing <tr> rows of courses.

    @return: List[List[HtmlElement]] A list of course groups, each group being a list
            of HtmlElement rows belonging to that course.
    """
    result: List[List[HtmlElement]] = []
    currentSublist: List[HtmlElement] = []

    for el in coursesDataList:
        class_attr: str = el.get('class') or ''
        if config.COURSE_BOLD_ROW_CLASS in class_attr:
            if currentSublist:
                result.append(currentSublist)
            currentSublist = [el]
        else:
            currentSublist.append(el)

    if currentSublist:
        result.append(currentSublist)

    return result


def convertToPandas(df: pd.DataFrame, coursesData: List[CourseData]) -> pd.DataFrame:
    """
    Append a list of course data objects to an existing Pandas DataFrame.

    @param df: Existing DataFrame containing course data.
    @param coursesData: List of CourseData objects to be appended.

    @return: A new DataFrame combining the input DataFrame and the converted course data.
    """
    coursesDataSet: List[Dict[str, Optional[str] | List[str]]] = [course.toDict() for course in coursesData]
    coursesDataPandas: pd.DataFrame = pd.DataFrame(coursesDataSet)

    return pd.concat([df, coursesDataPandas], ignore_index=True, sort=False)


def fileHandler() -> pd.DataFrame:
    """
    Process all temporary HTML files and extract course data into a Pandas DataFrame.
    - Iterates through the HTML file generator.
    - Extracts course elements.
    - Splits and parses them into CourseData objects.
    - Appends them to a cumulative DataFrame.
    - Optionally deletes temporary files after processing.

    @return: pd.DataFrame DataFrame containing all parsed course data.
    """
    htmlFiles: Generator[Tuple[ElementTree, str], None, None] = openHTMLFileGenerator()
    df: pd.DataFrame = pd.DataFrame()

    for file, filename in htmlFiles:
        coursesList: List[HtmlElement] = getCoursesData(file)
        separatedCourses: List[List[HtmlElement]] = separateCourses(coursesList)
        coursesData: List[CourseData] = parseCourses(separatedCourses, filename)
        df = convertToPandas(df, coursesData)

        if not config.KEEP_TMP_FOLDER:
            os.remove(config.TMP_FOLDER_NAME + "/" + filename)

    return df


if __name__ == "__main__":
    fileHandler()
