from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup

class CourseExtract():

    def __init__(self):
        self.DRIVER_PATH = "C:/Users/umerf\Downloads\chrome-win64\chrome-win64\chrome.exe"
        self.list_of_courses = []
    
    def getProxies():
        r = requests.get('<https://free-proxy-list.net/>')
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('tbody')

        proxies = []
        for row in table:
            if row.find_all('td')[4].text == 'elite proxy':
                proxy = ':'.join([row.find_all('td')[0].text, row.find_all('td')[1].text])
                proxies.append(proxy)
            else:
                pass

        return proxies
    
    def extract(self):
        list_of_proxies = self.getProxies()
        
        options = Options()
        driver = webdriver.Chrome()
        driver.get('https://apps.ualberta.ca/catalogue/course/ece/202')

    def run(self):
        self.extract()

if __name__ == "__main__":
    extract_object = CourseExtract()
    extract_object.run()