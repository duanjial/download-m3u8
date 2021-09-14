import time
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


class FakeBrowser:
    def __init__(self, headless=False) -> None:
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
        scriptToExecute = 'var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntriesByType("resource") || {}; return network;'
        netData = self.driver.execute_script(scriptToExecute)
        return netData

    def _get_random_useragent(self) -> str:
        ua = UserAgent(verify_ssl=False)
        return ua.random

    def _is_verification_needed(self, driver) -> bool:
        try:
            driver.find_element_by_xpath("/html/body/table/tbody/tr/td/b/font")
            return True
        except NoSuchElementException as e:
            print(f"{e}")
            return False

    def _click_link(self, driver) -> None:
        try:
            element = driver.find_element_by_xpath("/html/body/table/tbody/tr/td/a")
            element.click()
        except NoSuchElementException as e:
            print(f"{e}")

    def close(self) -> None:
        self.driver.close()
