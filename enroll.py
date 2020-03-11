from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
import json
from api import Quest


class Enroll(Quest):
    def __init__(self, quest): 
        self.timeout = 10
        self.username = quest.username
        self.password = quest.password
        self.driver = quest.driver
        Quest.sidebarLoad(self, "Enroll")

    def addToCart(self, classNumber):
        Quest.sidebarLoad(self, "Add classes")
        wait = WebDriverWait(self.driver, self.timeout)
        
        inp = wait.until(ec.visibility_of_element_located((By.ID, "DERIVED_REGFRM1_CLASS_NBR")))
        inp.send_keys(classNumber)
        
        # wait until loading is finished
        wait.until(ec.invisibility_of_element_located((By.CLASS_NAME, "ui-loader"))) 
        enter = wait.until(ec.element_to_be_clickable((By.ID, "DERIVED_REGFRM1_SSR_PB_ADDTOLIST2$9$")))
        enter.click()
        
        wait.until(ec.invisibility_of_element_located((By.CLASS_NAME, "ui-loader"))) 
        nextbutton = wait.until(ec.element_to_be_clickable((By.LINK_TEXT, "Next")))
        nextbutton.click()
        
        wait.until(ec.invisibility_of_element_located((By.CLASS_NAME, "ui-loader"))) 
        nextbutton = wait.until(ec.element_to_be_clickable((By.LINK_TEXT, "Next")))
        nextbutton.click()

    def addCart(self):
        Quest.sidebarLoad(self, "Add classes")
        wait = WebDriverWait(self.driver, self.timeout)
        nextbutton = wait.until(ec.visibility_of_element_located((By.LINK_TEXT, "Continue")))
        nextbutton.click()
        
        wait.until(ec.invisibility_of_element_located((By.CLASS_NAME, "ui-loader"))) 
        nextbutton = wait.until(ec.visibility_of_element_located((By.LINK_TEXT, "Finish Enrolling")))
        nextbutton.click()

    def drop(self, classNumber):
        Quest.sidebarLoad(self, "Drop classes")
        wait = WebDriverWait(self.driver, self.timeout)

        wait.until(ec.invisibility_of_element_located((By.CLASS_NAME, "ui-loader"))) 
        table = wait.until(ec.visibility_of_element_located((By.ID, "STDNT_ENRL_SSV1$scroll$0")))
        tbody = table.find_element_by_css_selector("thead + tbody")
        rows = tbody.find_elements_by_tag_name("tr")

        for row in rows:
            cell = row.find_elements_by_tag_name("td")[1]
            course = cell.find_element_by_tag_name("span").text
            courseID = course.split('(')[1][:-1]
            if courseID == str(classNumber):
                try:
                    select = row.find_element_by_class_name("ui-btn-text")
                    select.click()
                except (NoSuchElementException, TimeoutException) as exception:
                    return
        
        wait.until(ec.invisibility_of_element_located((By.CLASS_NAME, "ui-loader"))) 
        dropButton = wait.until(ec.element_to_be_clickable((By.LINK_TEXT, "Drop Selected Classes")))
        dropButton.click()

        wait.until(ec.invisibility_of_element_located((By.CLASS_NAME, "ui-loader")))
        finish = wait.until(ec.element_to_be_clickable((By.LINK_TEXT, "Finish Dropping")))
        finish.click()

    def swap(self, driver):
        Quest.sidebarLoad(self, "Swap classes")

    def edit(self, driver):
        Quest.sidebarLoad(self, "Edit classes")

    def getDates(self, driver):
        Quest.sidebarLoad(self, "Enrollment dates")

    def searchClasses(self, driver):
        Quest.sidebarLoad(self, "Search for classes")

    def examInfo(self, driver):
        Quest.sidebarLoad(self, "Exam information")
