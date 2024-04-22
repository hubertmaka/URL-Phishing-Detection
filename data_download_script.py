import time
import csv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

service = Service(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=service)

invalid_phishing_sites_link = 'https://phishtank.org/phish_search.php?page=0&valid=n&Search=Search'

PAGES = 100
start = 0

title = ['ID', 'PHISH_URL', 'ADDITIONAL_INFO']
with open('datasets/non-phishing-urls-phishtank.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
    csvwriter.writerow(title)


# Last scraped page 99

for i in range(start, PAGES + 1):
    print(i)
    driver.get(f'https://phishtank.org/phish_search.php?page={i}&valid=n&Search=Search')
    # Wait until load table
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'table'))
    )
    # Get Table
    table = driver.find_element(By.TAG_NAME, 'table')

    # Split rows
    table_rows = table.text.split('\n')

    # Extract id, url and additional info
    important_data = [row for idx, row in enumerate(table_rows) if idx % 2 == 1]
    less_important_data = [row for idx, row in enumerate(table_rows) if idx % 2 == 0]

    # Clean this data
    important_data = important_data[:-1]
    less_important_data = less_important_data[1:]

    # merge two tables
    rows_to_write_in_csv = []
    for row, additional_info in zip(important_data, less_important_data):
        url_info = row.split()
        rows_to_write_in_csv.append([
            url_info[0],
            url_info[1],
            additional_info
        ])

    # Append data to file
    with open('datasets/non-phishing-urls-phishtank.csv', 'a', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        csvwriter.writerows(rows_to_write_in_csv)


driver.quit()

