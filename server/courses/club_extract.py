from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
import random
import undetected_chromedriver as uc
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import os
from docx import *
from googlesearch import search
from fake_useragent import UserAgent
from reddit_extract import RedditExtract

class ClubExtract():
    def __init__(self):
        self.driver = ''
    
    def getProxies(self):
        r = requests.get('https://free-proxy-list.net/', verify=False)
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('tbody')
        total_rows = len(table)
        with open("proxies.txt", 'w') as file:
            for index, row in enumerate(table):
                if row.find_all('td')[4].text == 'elite proxy' and row.find_all('td')[5].text == 'yes':
                    proxy = ':'.join([row.find_all('td')[0].text, row.find_all('td')[1].text])
                    file.write(proxy)
                    if index < total_rows - 1:
                        file.write('\n')

    def setupDriver(self):

        proxies = []
        options = Options()

        user_agent = UserAgent()

        user_string = user_agent.random

        with open("proxies.txt", 'r') as file:
            for line in file:
                proxies.append(line)
                options.add_argument(f'--proxy-server={line}')
        options.add_argument('--headless')

        random_proxy = random.choice(proxies)      

        seleniumwire_options = {
            'proxy': {
                'http': f'{random_proxy}',
                'https': f'{random_proxy}',
                'verify_ssl': False
            },
        }

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f'--user-agent={user_string}')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.headless = True
        self.driver = uc.Chrome(options=chrome_options, seleniumwire_options=seleniumwire_options)
    
    def extract_clubs(self):
        self.driver.get("https://alberta.campuslabs.ca/engage/organizations?categories=512")
        org_results = self.driver.find_element(By.ID, "org-search-results")
        outlined_button = self.driver.find_element(By.CLASS_NAME, "outlinedButton")
        for i in range(0, 8):
            outlined_button.click()
        
        div_of_student_organizations = self