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

class CourseExtract():

    def __init__(self, study_program):

        self.list_of_courses = []
        self.study_program = study_program
        self.software_url = 'https://calendar.ualberta.ca/preview_program.php?catoid=39&poid=47959&returnto=12339'
        self.compe_normal_url = 'https://calendar.ualberta.ca/preview_program.php?catoid=39&poid=47952&returnto=12339'
        self.compe_nano_url = 'https://calendar.ualberta.ca/preview_program.php?catoid=39&poid=47954&returnto=12339'
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

        with open("proxies.txt", 'r') as file:
            for line in file:
                proxies.append(line)
                options.add_argument(f'--proxy-server={line}')

        random_proxy = random.choice(proxies)      

        seleniumwire_options = {
            'proxy': {
                'http': f'{random_proxy}',
                'https': f'{random_proxy}',
                'verify_ssl': False
            },
        }

        chrome_options = webdriver.ChromeOptions()
        self.driver = uc.Chrome(options=chrome_options, seleniumwire_options=seleniumwire_options)
    
    def extract_group_two(self):

        url_to_search = ''
        list_of_non_grp2s = []

        list_of_non_grp2_compe_normal = ['CMPUT 274', 'ECE 202', 'ECE 210', 'ENGG 299', 'MATH 201', 'MATH 209', 'CMPUT 272', 'CMPUT 275', 'ECE 212', 'ECE 240', 'PHYS 230', 'WKEXP 901', 'ECE 311', 'ECE 325', 'STAT 235', 'WKEXP 902', 'WKEXP 903', 'CMPUT 291', 'CMPUT 301', 'CMPUT 379', 'ECE 322', 'ECE 315', 'ECE 487', 'ENGG 404', 'WKEXP 904', 'WKEXP 905', 'ECE 420', 'ECE 422', 'ECE 493', 'ENGG 400','ECE 203', 'ECE 302', 'ECE 340', 'ECE 304', 'ECE 342', 'ECE 410', 'ECE 492']
        list_of_non_grp2_compe_nano = ['CMPUT 274', 'ECE 202', 'ECE 210', 'ENGG 299', 'MATH 201', 'MATH 209', 'CMPUT 272', 'CMPUT 275', 'ECE 203', 'ECE 212', 'ECE 240', 'PHYS 230', 'WKEXP 901', 'ECE 302', 'ECE 311', 'ECE 325', 'WKEXP 902', 'WKEXP 903', 'CMPUT 291', 'ECE 304', 'ECE 342', 'ECE 410', 'ENGG 404', 'CMPUT 301', 'ECE 315', 'ECE 403', 'ECE 450', 'ECE 475', 'WKEXP 904', 'WKEXP 905', 'ECE 412', 'ECE 457', 'ECE 492', 'ENGG 400']
        list_of_non_grp2_software = ['CMPUT 274', 'ECE 202', 'ECE 210', 'ENGG 299', 'MATH 201', 'MATH 209', 'CMPUT 272', 'CMPUT 275', 'ECE 212', 'ECE 240', 'PHYS 230', 'WKEXP 901', 'ECE 311', 'ECE 321', 'ECE 325', 'STAT 235', 'WKEXP 902', 'WKEXP 903', 'CMPUT 291', 'CMPUT 301', 'CMPUT 379', 'ECE 322', 'ECE 315', 'ECE 421', 'ECE 487', 'ENGG 404', 'WKEXP 904', 'WKEXP 905', 'ECE 420', 'ECE 422', 'ECE 493', 'ENGG 400']

        if self.study_program == 'compe':
            url_to_search = self.compe_normal_url
            list_of_non_grp2s = list_of_non_grp2_compe_normal
        elif self.study_program == 'software':
            url_to_search = self.software_url
            list_of_non_grp2s = list_of_non_grp2_software
        elif self.study_program == 'nano':
            url_to_search = self.compe_nano_url
            list_of_non_grp2s = list_of_non_grp2_compe_nano

        self.driver.get(url_to_search)

        h1 = self.driver.find_elements(By.CLASS_NAME, 'acalog-course')
        list_of_grp2 = []

        for i in range(0, len(h1)):
            split_elective = h1[i].text.split()
            try:
                value = int(split_elective[1])
                if (split_elective[0] + ' ' + split_elective[1]) not in list_of_non_grp2s:
                    if i<len(h1)-1:
                        list_of_grp2.append(split_elective[0] + ' ' + split_elective[1] + "\n")
                    else:
                        list_of_grp2.append(split_elective[0] + ' ' + split_elective[1])

            except ValueError:
                pass

        self.driver.quit()

        return list_of_grp2
    
    def create_grp2_text(self):
        if self.study_program == 'software':
            file_path = 'courses_softe/software_group2_electives.txt'

            if not os.path.exists(file_path):
                with open(file_path, 'w') as file:
                    file.writelines(self.extract_group_two())
        elif self.study_program == 'compe':
            file_path = 'courses_compe/compe_group2_electives.txt'
            
            if not os.path.exists(file_path):
                with open(file_path, 'w') as file:
                    file.writelines(self.extract_group_two())
        elif self.study_program == 'nano':
            file_path = 'courses_compe_nano/compe_nano_group2_electives.txt'
            
            if not os.path.exists(file_path):
                with open(file_path, 'w') as file:
                    file.writelines(self.extract_group_two())
    
    def course_description_extract(self, course_name):

        split_course = course_name.split()
        course_url = 'https://apps.ualberta.ca/catalogue/course/' + split_course[0].lower() + '/' + split_course[1]

        self.driver.get(course_url)

        course_info = (self.driver.find_element("xpath", "//div[@class='container']/p[2]").text).split('.')

        term_and_instructor_info = (self.driver.find_elements(By.CLASS_NAME, 'mb-5'))

        prerequisites = ""

        for i in range(0, len(course_info)):
            if "Prerequisite" in course_info[i]:
                prerequisites = course_info.pop(i)
                break
        
        course_description = '.'.join(course_info) # All course info sans prereqs

        
        term_and_instructor_info = self.driver.find_elements(By.CLASS_NAME, 'mb-5')

        term_and_profs = {}

        for element in term_and_instructor_info:

            what_term = element.find_element(By.TAG_NAME, 'h2').text
            
            try:
                table_elements = element.find_element(By.TAG_NAME, 'table')
                td_elements = table_elements.find_elements(By.TAG_NAME, 'td')
                
                # Process the table data
            except NoSuchElementException:
                term_and_profs[what_term] = []
                continue
            
            for td_element in td_elements:
                try:
                    data_card_title = td_element.get_attribute('data-card-title') # Check if the td element has the data-card-title attribute
                    if data_card_title == "Instructor(s)":

                        a_tags = td_element.find_elements(By.TAG_NAME, 'a')
                        if what_term not in term_and_profs:
                            term_and_profs[what_term] = []

                        for atag in a_tags:
                            term_and_profs[what_term].append(atag.text)
                except:
                    pass
        
        return term_and_profs, prerequisites, course_description
    
    def write_pdf(self):
        document = Document()

        document.add_heading('Group 2 Electives', 0)

        with open("courses_softe\software_group2_electives.txt", "r") as file:
            for course in file:
                terms_and_profs, prerequisites, course_description = self.course_description_extract(course)
                document.add_heading(course, level=1)
                description_paragraph = document.add_paragraph(style='List Bullet')
                run = description_paragraph.add_run("Course Description:" + "\n")
                run.bold = True
                
                # Add the course description to the parent paragraph
                description_paragraph.add_run('\n' + course_description)

        document.save('gfg.docx') 

    def run(self):
        self.setupDriver()
        self.write_pdf()

if __name__ == "__main__":
    extract_object = CourseExtract('compe') # can put compe, software, or nano i    n the constructor
    # extract_object.course_description_extract('ece 321')

    extract_object.run()