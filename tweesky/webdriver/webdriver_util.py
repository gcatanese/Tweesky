from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.remote.remote_connection import LOGGER, logging
from selenium.webdriver.chrome.service import Service

# Logging on Remote Selenium
from tweesky.config import get_webdriver_type, get_webdriver_remote_host, get_webdriver_path

LOGGER.setLevel(logging.WARNING)

WEBDRIVER_MAX_TABS = 10

n = 0
driver = None


def save_screenshot(url, filename):
    try:
        driver = open_driver()

        # driver.set_window_size(480, 320)
        tic = time.perf_counter()

        open_tab()

        driver.get(url)
        toc = time.perf_counter()
        logging.info(f"Get in {toc - tic:0.4f} seconds")

        tic = time.perf_counter()
        img = driver.save_screenshot(filename)
        toc = time.perf_counter()

        logging.info(f"Saving {filename} in {toc - tic:0.4f} seconds")

    finally:
        close_tab()
        close_driver()

    return img


def open_driver():
    global n
    global driver

    if driver is None:
        options = ChromeOptions()
        # options = FirefoxOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option("detach", True)
        # options.add_argument("--enable-javascript")

        user_agent = get_browser_user_agent()
        options.add_argument('user-agent={0}'.format(user_agent))

        tic = time.perf_counter()

        if get_webdriver_type() == 'local':
            s = Service(get_webdriver_path())
            driver = webdriver.Chrome(options=options, service=s)
            # driver = webdriver.Firefox(options=options, executable_path=get_webdriver_path())
        else:
            driver = webdriver.Remote(get_webdriver_remote_host() + "/wd/hub", options.to_capabilities())

        toc = time.perf_counter()
        logging.info(f"Open driver in {toc - tic:0.4f} seconds")

    return driver


def open_tab():
    global n
    global driver

    if driver is not None:
        driver.execute_script("window.open();")
        logging.info(f"Open tab #{n}")
        n = n + 1
    else:
        logging.warning("Driver is None!! Cannot open new tab")


def close_tab():
    global n
    global driver

    if driver is not None:
        #tag = driver.find_element_by_tag_name('body')
        tag = driver.find_element(by=By.TAG_NAME, value='body')
        if tag is not None:
            tag.send_keys(Keys.COMMAND + 'w')
            n = n - 1
            logging.info(f"Close tab #{n}")


def close_driver():
    global n
    global driver

    if driver is not None and n >= WEBDRIVER_MAX_TABS:
        logging.warning(f"Closing Webdriver (num tabs: {n})")
        driver.quit()
        n = 0
        driver = None


def force_close_driver():
    global n
    global driver

    if driver is not None:
        logging.warning(f"Force closing Webdriver (num tabs: {n})")
        driver.quit()
        n = 0
        driver = None


# User-Agent HTTP Header
def get_browser_user_agent():
    return 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) ' \
           'Chrome/83.0.4103.61 Safari/537.36 '
