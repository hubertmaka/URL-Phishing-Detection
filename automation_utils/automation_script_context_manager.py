import csv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class DownloadDataAutomationScriptContextManager:
    def __init__(self, url: str, valid_data: bool = True) -> None:
        self.valid_data = valid_data
        self.valid_data_flag = 'n' if valid_data else 'y'
        self.url = url
        self.title = ['ID', 'PHISH_URL', 'ADDITIONAL_INFO']
        self.service = Service(executable_path='automation_utils/chromedriver.exe')
        self.webdriver = webdriver.Chrome(service=self.service)
        self.site_url = self.set_site_url()

    def __enter__(self):
        self.initiate_file()
        return DownloadDataAutomationScriptContextManager(self.url, self.valid_data, self.start_page)

    def __exit__(self):
        self.webdriver.quit()

    def initiate_file(self):
        with open('datasets/non-phishing-urls-phishtank.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            csvwriter.writerow(self.title)

    def get_driver(self) -> webdriver.Chrome:
        return self.webdriver

    def get_site_url(self) -> str:
        return self.site_url

    def set_site_url(self, page: int = 0) -> str:
        return f'{self.url}?page={page}&valid={self.valid_data_flag}'
