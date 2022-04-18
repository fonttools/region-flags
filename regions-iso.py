#!/usr/bin/env python3
import datetime
import re
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver


def download_tsv(region):
    date = datetime.datetime.now()
    options = webdriver.FirefoxOptions()
    options.add_argument('headless')
    driver = webdriver.Firefox(options=options, firefox_binary='firefox-nightly')
    driver.get(f"https://www.iso.org/obp/ui/#iso:code:3166:{region}")

    wait = WebDriverWait(driver, 10)
    men_menu = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#subdivision > thead")))

    source = driver.find_element(By.CSS_SELECTOR, '#subdivision > tbody').get_attribute('innerHTML')
    source = re.sub(r'\s\s', '', source).replace("</td><td>", "\t").replace(" </tr> <tr>", "\n").removesuffix("</td> </tr>").removeprefix(" <tr><td>").replace("<td>|<\/td>", "")
    source = re.sub(r'<td>|</td>', '', source)

    if source.strip():
        print(f"; ISO 3166-2:{region}\n; Source: https://www.iso.org/obp/ui/#iso:code:3166:{region}\n; Extracted on: "
              f"{date.strftime('%Y%m%d')}\n; \n; Subdivision category	3166-2 code	Subdivision name	Local variant\t"
              f"Language code Romanization system	Parent subdivision")
        print(source)

    driver.close()


if __name__ == '__main__':
    download_tsv(sys.argv[1].upper())
