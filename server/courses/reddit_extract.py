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
from langchain_community.llms import HuggingFaceEndpoint
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

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

            for result in regular_results[:10]:
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

                print(post_title.text.lower())

                for div in paragraphs_divs:
                    # Extract paragraphs from the div
                    paragraphs = div.find_elements(By.TAG_NAME, "p")
                    
                    # Print or process the paragraphs as needed
                    print(course.lower())
                    if course.lower() in post_title.text.lower():
                        print("hello")
                        for paragraph in paragraphs:
                            if(("vs" in post_title.text.lower())):
                                if course.lower() in paragraph.text.lower():
                                    valid_paragraphs.append('"' + paragraph.text + '"')

                            elif course.lower() in paragraph.text.lower():
                                print(f"Course found in paragraph or post title: '{course}'")
                                valid_paragraphs.append('"' + paragraph.text + '"')
                                print(paragraph.text)
                    else:
                        overall_descript = ''
                    if len(valid_paragraphs)>0:
                        valid_paragraphs_overall.append(' '.join(valid_paragraphs))
                        overall_descript = ' '.join(valid_paragraphs_overall)
                        valid_paragraphs = []
            except NoSuchElementException:
                print("No comments available!")

        self.driver.quit()
        print(overall_descript)
        return overall_descript
        
    def llm_opinion(self, course):
        load_dotenv()
        HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
        reddit_comments = self.check_if_course_valid(course)

        template = """ You will have to judge the difficulty of a university course, based off of comments from the social media site Reddit.
        Each separate comment will be enclosed in double quotes (e.g. "Hello") and you will be passed a number of them at once.
        Each comment should represent someone's thoughts on the course {course} (make sure that the person is talking about the course in question and not a different course).
        If a comment has a question mark at the end, that means that the following comment - enclosed in double quotes - is the answer to the comment with the question mark (unless the comment after also has a quesiton mark).
        Do not ever explicitly talk about the people who made the comments, or mention the comments themselves. You only want to summarize the difficulty.
        Do not talk about a professor either, as the professor changes constantly. You only want to summarize the difficulty.
        Provide a summary on the difficulty (make sure to explicitly mention how difficult it is) of the course using the context provided.
        Context: {context}
        Only return the helpful answer below and nothing else.
        Helpful answer:
        """

        repo_id = "mistralai/Mistral-7B-Instruct-v0.2"

        llm = HuggingFaceEndpoint(
              repo_id=repo_id, max_length = 100, temperature=0.1, token=HUGGINGFACEHUB_API_TOKEN
        )

        prompt = PromptTemplate(template=template, input_variables=['course', 'context'])
        llm_chain = LLMChain(prompt=prompt, llm=llm)

        course_difficulty = ''
        if reddit_comments.strip()=='' or reddit_comments.strip()=="":
            course_difficulty = "Insufficient information available on course difficulty"
        else:
            print(reddit_comments)
            course_difficulty = llm_chain.run({
                "course": course,
                "context": reddit_comments
            })
        
        print(course_difficulty)

        return course_difficulty