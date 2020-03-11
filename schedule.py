from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
import json
from api import Quest

class Schedule(Quest):
    def __init__(self, quest): 
        self.timeout = 10
        self.username = quest.username
        self.password = quest.password
        self.driver = quest.driver
        Quest.sidebarLoad(self, "Class schedule")

    #todo: implement filtering

    def get(self):
        wait = WebDriverWait(self.driver, self.timeout)
        table = wait.until(ec.visibility_of_element_located((By.ID, "ACE_STDNT_ENRL_SSV2$0")))
        rows = table.find_elements_by_css_selector("td.gsgroupbox")
        schedule = []
        
        for row in rows:
            wait = WebDriverWait(row, self.timeout)
            course = wait.until(ec.visibility_of_element_located((By.TAG_NAME, "h3"))).text
            
            tables = row.find_elements_by_css_selector("td.gsgrid")

            thead = tables[0].find_element_by_tag_name("thead")
            tbody = tables[0].find_element_by_css_selector("thead + tbody")
            headers = thead.find_elements_by_tag_name("th")
            contents = tbody.find_elements_by_tag_name("span")
            courseInfo = {}
            for e in range(0, len(contents)-1):
                courseInfo[headers[e].text] = contents[e].text

            thead = tables[1].find_element_by_tag_name("thead")
            tbody = tables[1].find_element_by_css_selector("thead + tbody")
            headers = thead.find_elements_by_tag_name("th")
            trows = tbody.find_elements_by_tag_name("tr")

            calendar = []

            for trow in trows:
                contents = trow.find_elements_by_tag_name("span")
                calendarItem = {}
                for e in range(0, len(contents)):
                    calendarItem[headers[e].text] = contents[e].text
                calendar.append(calendarItem)            

            schedule.append({
                "Course": course,
                "Course Info": courseInfo, 
                "Calendar": calendar
            })
        
        return schedule
