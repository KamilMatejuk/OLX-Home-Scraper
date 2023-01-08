from enum import Enum
import os

REGEX_POLISH_AZ = r'AaĄąBbCcĆćDdEeĘęFfGgHhIiJjKkLlŁłMmNnŃńOoÓóPpRrSsŚśTtUuWwYyZzŹźŻż'

# results
LINKS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'links.csv')
ITEMS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'items.csv')
ITEMS_HEADERS = ['link', 'date', 'build_type', 'rooms', 'level', 'furniture', 'area',
                 'price_base', 'price_additional', 'location_approximation',
                 'location', 'animals', 'shower', 'bath', 'balcony', 'dishwasher', 'induction_stove', 'deposit', # deduced from text
                 'whole_text']

# logs
LOG_FILE = None
LOG_OUTPUT = True

# selenium
SELENIUM_PROXY = False
SELENIUM_HEADLESS = False
SELENIUM_CHROMEDRIVER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'connection', 'chromedriver_108.0.5359.71')
os.chmod(SELENIUM_CHROMEDRIVER, 755)

# workload
class Workload(Enum):
    CREATE_LINKS_LIST = 1
    CLEAN_UP_LINKS_LIST = 2
    CREATE_ITEMS_CVS = 3
    CLEAN_UP_ITEMS_LIST = 4
    DEDUCE_DETAILS = 5 # animals, distances based on location
    FILTER_RESULTS = 6
TYPE = Workload.CLEAN_UP_ITEMS_LIST

# links
import linker_olx
LINK_OLX_LIST = linker_olx.LINK
