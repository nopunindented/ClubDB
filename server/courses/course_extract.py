from selenium import webdriver


list_of_courses = ["ece 202", "ece 203"]


class CourseExtract():

    def __init__(self):
        self.DRIVER_PATH = "C:/Users/umerf\Downloads\chrome-win64\chrome-win64\chrome.exe"
    
    def extract(self):
        driver = webdriver.Chrome()
        driver.get('https://apps.ualberta.ca/catalogue/course/ece/202')
    def run(self):
        self.extract()

if __name__ == "__main__":
    extract_object = CourseExtract()
    extract_object.run()