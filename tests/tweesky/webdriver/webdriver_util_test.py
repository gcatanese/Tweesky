import logging
import unittest

from tweesky.webdriver.webdriver_util import get_screenshot_from_url


class WebDriverUtilTest(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger().setLevel(logging.DEBUG)

    # def test_get_screenshot(self):
    #     self.assertIsNotNone(get_screenshot("https://perosa.github.io/"))

    def test_get_screenshot_from_url(self):
        self.assertIsNotNone(get_screenshot_from_url("https://perosa.github.io/"))