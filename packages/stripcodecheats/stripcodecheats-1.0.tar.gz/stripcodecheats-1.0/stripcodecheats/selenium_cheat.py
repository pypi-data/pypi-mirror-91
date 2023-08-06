from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os
import github_requests

def loop(driver):
    filename = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".my-8.text-4xl"))).text

    answer_buttons = driver.find_elements_by_css_selector(".bg-sandy.rounded.px-4.py-4.text-left.border")
    repo_ids = [int(answer_button.get_attribute("phx-value-githubrepoid")) for answer_button in answer_buttons]

    answer_index = github_requests.search_repos_for_file_name(filename, repo_ids)
    answer_buttons[answer_index].click()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[phx-click='nextQuestion']"))).click()
    
    time.sleep(5)

def init(github_username, github_password, executable_path, iteration_count):
    logged_in = True

    if not os.path.isdir("selenium"):
        logged_in = False

    options = Options()
    options.add_argument("user-data-dir=selenium")

    driver = webdriver.Chrome(executable_path, options=options)

    driver.get("https://stripcode.dev/ranked")

    if not logged_in:
        driver.find_element_by_id("login_field").send_keys(github_username)
        driver.find_element_by_id("password").send_keys(github_password)
        driver.find_element_by_name("commit").click()

    if iteration_count == True:
        while True:
            loop(driver)
    else:
        i = 0

        while i < iteration_count:
            loop(driver)
            i += 1