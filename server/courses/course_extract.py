from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
import random
import undetected_chromedriver as uc
from seleniumwire import webdriver
from selenium.webdriver.common.by import By

class CourseExtract():

    def __init__(self):
        self.list_of_courses = []
    
    def getProxies(self):
        r = requests.get('https://free-proxy-list.net/')
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('tbody')

        proxies = []
        for row in table:
            if row.find_all('td')[4].text == 'elite proxy' and row.find_all('td')[5].text == 'yes':
                proxy = ':'.join([row.find_all('td')[0].text, row.find_all('td')[1].text])
                proxies.append(proxy)
            else:
                pass

        return proxies
    
    def extract_group_two(self):
        list_of_proxies = self.getProxies()

        options = Options()

        for i in range(0, len(list_of_proxies)):
            options.add_argument(f'--proxy-server={list_of_proxies[i]}')

        random_proxy = random.choice(list_of_proxies)      

        seleniumwire_options = {
            'proxy': {
                'http': f'{random_proxy}',
                'https': f'{random_proxy}',
            },
        }

        chrome_options = webdriver.ChromeOptions()

        driver = uc.Chrome(options=chrome_options, seleniumwire_options=seleniumwire_options)
        driver.get('https://calendar.ualberta.ca/preview_program.php?catoid=39&poid=47959&returnto=12339')
        h1 = driver.find_elements(By.CLASS_NAME, 'acalog-course')
        for i in range(0, len(h1)):
            print(h1[i].text)
        driver.quit()

    def run(self):
        self.extract_group_two()

if __name__ == "__main__":
    extract_object = CourseExtract()
    extract_object.run()