# Helper functions:
# Noah Rubin 2023

import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


def configure_options():
    """
    Configures options for the Chrome webdriver.
    :return: options: ChromeOptions object with various options set
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument("--disable-gpu")
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-default-apps')
    options.add_argument('disable-infobars')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-web-security')
    options.add_argument('--disable-site-isolation-trials')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-setuid-sandbox')
    options.add_argument('--no-sandbox')
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument('--remote-debugging-address=0.0.0.0')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-zygote')
    options.add_argument('--disable-setuid-sandbox')
    return options


def scrape_bball_stats(start_year: int, end_year: int, driver_path: str='/Users/noahrubin/Desktop/chromedriver'):
    """
    Scrapes basketball statistics from espn.com for the specified range of years
    :param start_year: int, the first year of the range
    :param end_year: int, the last year of the range
    :param driver_path: str, the path to your chromedriver
    :return: final: DataFrame, containing all scraped statistics
    """
    options = configure_options()
    dataframes = []

    for y in np.arange(start_year, end_year + 1, 1):
        service = Service(driver_path)
        service.start()
        
        url = f'https://www.espn.com.au/nba/stats/player/_/season/{y}/seasontype/2'
        driver = webdriver.Remote(service.service_url, options=options)
        driver.get(url)

        while True:
            try:
                element = driver.find_element(By.CLASS_NAME, 'loadMore__link')
                if element.is_displayed():
                    element.click()
                    time.sleep(5)
                else:
                    break
            except:
                break

        html_source = driver.page_source
        soup = BeautifulSoup(html_source, 'html.parser')

        try:
            tables = soup.find_all("table")
            df = pd.concat([pd.read_html(str(tables[i]))[0] for i in range(len(tables))], axis=1)
            df['Year'] = y
            dataframes.append(df)
        except (IndexError, ValueError): 
            print(f'No tables found for year {y}')

        driver.close()

    final = pd.concat(dataframes, axis=0)
    return final