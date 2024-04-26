import csv
import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from automation_utils.automation_script_context_manager import DownloadDataAutomationScriptContextManager


class DownloadDataAutomationScript:
    """A class for automating data download from a website."""

    def __init__(self, url: str, file_path: str) -> None:
        """
        Initialize the DownloadDataAutomationScript.

        Args:
            url (str): The URL of the website to scrape.
            file_path (str): The file path to save the scraped data.
        """
        self.url = url
        self.file_to_path = file_path
        self._ids_and_urls = None
        self._additional_info = None

    def scrap_data(self, start: int = 0, pages: int = 100) -> None:
        """
        Scrape data from the website and save it to a CSV file.

        Args:
            start (int, optional): The starting page number. Defaults to 0.
            pages (int, optional): The number of pages to scrape. Defaults to 100.
        """
        with DownloadDataAutomationScriptContextManager(self.url) as inst:
            for page_nr in range(start, pages + 1):
                web_driver = inst.get_driver()
                web_driver.get(inst.set_site_url(page_nr))
                """Wait until table loads successfully."""
                WebDriverWait(web_driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'table'))
                )
                """Get table from site."""
                table = web_driver.find_element(By.TAG_NAME, 'table')

                """Split rows."""
                table_rows = table.text.split('\n')

                self._extract(table_rows)
                rows_to_write = self._zip_tables()
                self._save_to_csv_file(rows_to_write)


    def _extract(self, table_rows: list) -> None:
        """
        Extract relevant data from table rows. Clean this data.

        Args:
            table_rows (list): List of table rows.
        """
        ids_and_urls = [row for idx, row in enumerate(table_rows) if idx % 2 == 1]
        additional_info = [row for idx, row in enumerate(table_rows) if idx % 2 == 0]

        self._ids_and_urls = ids_and_urls[:-1]
        self._additional_info = additional_info[1:]

    def _zip_tables(self):
        """
        Combine extracted data into rows to write in CSV.

        Returns:
            list[list[str]]: Rows to write in CSV.
        """
        rows_to_write_in_csv = []
        for row, additional_info in zip(self._ids_and_urls, self._additional_info):
            url_info = row.split()
            rows_to_write_in_csv.append([
                url_info[0],
                url_info[1],
                additional_info
            ])
        return rows_to_write_in_csv

    def _save_to_csv_file(self, rows_to_write_in_csv: list[list[str]]) -> None:
        """
        Save rows to a CSV file.

        Args:
            rows_to_write_in_csv (list[list[str]]): Rows to write in CSV.
        """
        with open(self.file_to_path, 'a', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            csvwriter.writerows(rows_to_write_in_csv)
