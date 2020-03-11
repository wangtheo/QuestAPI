from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
import json
from api import Quest

class Grades(Quest): 
    def __init__(self, quest): 
        self.timeout = 10
        self.username = quest.username
        self.password = quest.password
        self.driver = quest.driver
        Quest.sidebarLoad(self, "Grades")
    
    def get(self, term):
        wait = WebDriverWait(self.driver, self.timeout)
        try:
            button = wait.until(ec.visibility_of_element_located((By.XPATH, "//*[contains(text(), '" + term + "')]")))
            button.click()
        except NoSuchElementException as exception:
            return json.dumps({term: "None avaiable"})
        
        table = wait.until(ec.visibility_of_element_located((By.ID, "TERM_CLASSES$scroll$0")))
        
        wait = WebDriverWait(table, self.timeout)
        wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "ul.gridformatter > li")))
        classes = table.find_elements_by_css_selector("ul.gridformatter > li")
        courses = []

        for c in classes:
            wait = WebDriverWait(c, self.timeout)
            wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "ui-li-desc")))
            rest = c.find_elements_by_class_name("ui-li-desc")
            course = {
                "Term": term,
                "Course": wait.until(ec.visibility_of_element_located((By.CLASS_NAME, "ui-li-heading"))).text
            }

            for r in rest:
                textArray = r.text.split(": ")
                if len(textArray) == 1:
                    course[textArray[0]] = r.find_element_by_tag_name("strong").text
                else:
                    course[textArray[0]] = textArray[1]
            courses.append(course)

        Quest.sidebarLoad(self, "Grades")

        return json.dumps(courses) 

    def getAll(self):
        wait = WebDriverWait(self.driver, self.timeout)
        table = wait.until(ec.visibility_of_element_located((By.ID, "win0divSSR_DUMMY_RECV1$0")))
        terms = list(map(lambda x: x.text, table.find_elements_by_css_selector("h2.ui-li-heading")))
        courses = []

        for term in terms:
            course = self.get(term)
            courses.append(json.loads(course))
        
        return json.dumps(courses)
