from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import json

class Quest:
    def __init__(self, username, password):
        self.timeout = 10 
        self.username = username
        self.password = password

        opts = Options()
        opts.add_argument("user-agent=Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) CriOS/60.0.3112.72 Mobile/15A5327g Safari/602.1")
        driver = webdriver.Chrome(options=opts)
        driver.get('https://quest.pecs.uwaterloo.ca/psp/SS/ACADEMIC/SA/?cmd=login&languageCd=ENG')
        wait = WebDriverWait(driver, self.timeout)
        button = wait.until(ec.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Sign in')]")))
        button.click()
        user = wait.until(ec.visibility_of_element_located((By.ID, "username")))
        pword =  wait.until(ec.visibility_of_element_located((By.ID, "password")))
        login = wait.until(ec.visibility_of_element_located((By.ID, "saml-submit")))
        user.send_keys(username)
        pword.send_keys(password)
        login.click()

        self.driver = driver

    def sidebarLoad(self, name):
        wait = WebDriverWait(self.driver, self.timeout)

        try: 
            sidebar = wait.until(ec.visibility_of_element_located((By.ID, "panel-breadcrumbs")))
            wait = WebDriverWait(sidebar, self.timeout)
            button = wait.until(ec.visibility_of_element_located((By.XPATH, "//*[contains(text(), '" + name + "')]")))
            button.click()
        except (NoSuchElementException, TimeoutException) as exception:
            wait = WebDriverWait(self.driver, self.timeout)
            button = wait.until(ec.visibility_of_element_located((By.LINK_TEXT, name)))
            button.click()