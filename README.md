# CoursesScrape-TLV
Scrapes courses data from the Tel-Aviv University servers.


## Usage

1. Download from here a [ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/), make sure it's the same version of the chrome you have installed.
2. In [config.py](config.py) update to your local 'CHROME_DRIVER_PATH'.
3. Run [main.py](main.py).
4. After running there should be a file named "Data.csv" in the same folder as the script with all the courses information.
5. You can import the file into Excel for cleaner view and filters usage, 'Excel -> Data -> From Text/CSV -> Data.csv".


## Configuration

In the [config.py](config.py) file you'll find many configuration options, some should be interacted with and other only if you know what you're doing.

All the options under 'Configurations' are safe to tamper with, they are mostly user experience and options.

The options under 'Site Elements Constants' should not be changed unless you know what you're doing and the site of TLV has changed, those constants keep the site pages layout, like the class of a button that the script has to interact with.
