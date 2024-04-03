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

class RedditExtract():
    
    def __init__(self, driver):
        self.driver = driver
    
    def get_reddit_links(self, course):
        course_code_first_and_last = course.split()
        course_to_find = f"https://www.google.com/search?q={'+'.join(course_code_first_and_last)}+uAlberta+Reddit"
        self.driver.get(course_to_find)
        course_urls = []
        try:
            regular_results = self.driver.find_elements(By.CLASS_NAME, "MjjYud")

            for result in regular_results[:5]:
                try:
                    link_element = result.find_element(By.TAG_NAME, "a")
                    
                    href_value = link_element.get_attribute("href")
                    if "uAlberta" in href_value:
                        course_urls.append(href_value)
                except NoSuchElementException:
                    print("No <a> tag with jsname='UWckNb' found in this search result")
        except NoSuchElementException:
            print("No regular search results found")
        
        print(course_urls)
        return course_urls
    
    def check_if_course_valid(self, course):
        links = self.get_reddit_links(course)

        valid_paragraphs = []
        valid_paragraphs_overall = []
        overall_descript = ''

        for i in range(0, len(links)):
            try:
                self.driver.get(links[i])
                paragraphs_divs = self.driver.find_elements(By.ID, "-post-rtjson-content")
                post_title = self.driver.find_element(By.CSS_SELECTOR, '[id*="post-title"]')

                for div in paragraphs_divs:
                    # Extract paragraphs from the div
                    paragraphs = div.find_elements(By.TAG_NAME, "p")
                    
                    # Print or process the paragraphs as needed
                    for paragraph in paragraphs:
                        if (course.lower() in paragraph.text.lower())  or (course.lower() in post_title.text.lower() and ("vs" not in post_title.text.lower())):
                            valid_paragraphs.append('"' + paragraph.text + '"')
                        elif course.lower() in post_title.text.lower() and (("vs" in post_title.text.lower())):
                            if course.lower() in paragraph.text.lower():
                                valid_paragraphs.append('"' + paragraph.text + '"')
                    if len(valid_paragraphs)>0:
                        valid_paragraphs_overall.append(' '.join(valid_paragraphs))
                        overall_descript = ' '.join(valid_paragraphs_overall)
                        valid_paragraphs = []
            except NoSuchElementException:
                print("No comments available!")
        
        os.system("taskkill /im chrome.exe /f")
        self.driver.quit()
        print(overall_descript)
        return overall_descript
        
    def llm_opinion(self):
        template = """ You will have to judge the difficulty of a university course, based off of comments from the social media site Reddit.
        Each separate comment will be enclosed in double quotes (e.g. "Hello") and you will be passed a number of them at once.
        Each comment should represent someone's thoughts on the course {course} (make sure that the person is talking about the course in question and not a different course).
        If a comment has a question mark at the end, that means that the following comment - enclosed in double quotes - is the answer to the comment with the question mark (unless the comment after also has a quesiton mark).
        Provide a summary on the difficulty of the course using the context provided.
        Context: {context}
        Only return the helpful answer below and nothing else.
        Helpful answer:
        """