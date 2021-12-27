import time
import logging
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from exceptions import UnableToClickException


class FakeBrowser:
    def __init__(self, headless=False) -> None:
        self._logger = logging.getLogger()
        self.headless = headless
        chrome_options = Options()
        chrome_options.add_argument(f"user-agent={self._get_random_useragent()}")
        if self.headless:
            chrome_options.add_argument("--headless")
        self.driver = (
            webdriver.Chrome()
            if not headless
            else webdriver.Chrome(options=chrome_options)
        )

    def get_net_data(self, url) -> list:
        self.driver.get(url)
        is_verification_needed = self._is_verification_needed(self.driver)
        if is_verification_needed:
            self._click_link(self.driver)
        time.sleep(3)
        script_to_execute = 'var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntriesByType("resource") || {}; return network;'
        net_data = self.driver.execute_script(script_to_execute)
        return net_data

    def _get_random_useragent(self) -> str:
        ua = UserAgent(verify_ssl=False)
        return ua.random

    def _is_verification_needed(self, driver) -> bool:
        try:
            driver.find_element_by_xpath("/html/body/table/tbody/tr/td/b/font")
            return True
        except NoSuchElementException as verify_exception:
            return False

    def _click_link(self, driver) -> None:
        try:
            element = driver.find_element_by_xpath("/html/body/table/tbody/tr/td/a")
            element.click()
        except NoSuchElementException as e:
            self._logger.error(f"{e.msg}")
            raise UnableToClickException("Unable to verify due to no element found to click")

    def close(self) -> None:
        self.driver.close()
