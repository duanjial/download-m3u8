from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


class FakeBrowser:
    def __init__(self, headless=False) -> None:
        self.headless = headless
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        self.driver = (
            webdriver.Chrome()
            if not headless
            else webdriver.Chrome(options=chrome_options)
        )

    def get_net_data(self, url) -> list:
        self.driver.get(url)
        scriptToExecute = 'var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntriesByType("resource") || {}; return network;'
        netData = self.driver.execute_script(scriptToExecute)
        return netData

    def close(self) -> None:
        self.driver.close()
