username="your_username"
password="your_password"

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
number=100
# Set up the Chrome browser
driver = webdriver.Chrome()
def logon():
    # Open a new tab and navigate to a website
    driver.get("https://achieve.hashtag-learning.co.uk/accounts/login/")
    username = driver.find_element("id", "id_login")  # Replace with actual section ID
    username.send_keys(username)  # Replace with the text you want to fill
    password = driver.find_element("id", "id_password")  # Replace with actual section ID
    password.send_keys(password)  # Replace with the text you want to fill
    submit = driver.find_element(By.XPATH, '//button[@type="submit"]')  # Finds a <button> element with type="submit"
    submit.click()
def answer(number):
    for i in range(number):
        driver.get("https://achieve.hashtag-learning.co.uk/assess/259/topic/choose-questions/")
        time.sleep(2)
        submit = driver.find_element(By.XPATH,'//button[@type="submit"]')  # Finds a <button> element with type="submit"
        time.sleep(1)
        submit.click()
        for i in range(3):
            time.sleep(1)
            if "During evaluation, a database is said to be fit for purpose if:" in driver.page_source:
                print("During evaluation, a database is said to be fit for purpose if:")#C
                submit = driver.find_element(By.ID, "button_3")  # Finds a <button> element with type="submit"
                submit.click()
            elif "A database is fit for purpose if it.." in driver.page_source:
                print("A database is fit for purpose if it..")#b
                submit = driver.find_element(By.ID, "button_2")  # Finds a <button> element with type="submit"
                submit.click()
            elif "Database output is accurate if.." in driver.page_source:
                print("Database output is accurate if...")#D
                submit = driver.find_element(By.ID, "button_4")  # Finds a <button> element with type="submit"
                submit.click()
            else:
                print("error")
                break
            time.sleep(1)
            if "Next Question" in driver.page_source:
                driver.get("https://achieve.hashtag-learning.co.uk/assess/question-page/")
logon()
answer(number)
# Close the browser
driver.quit()
# driver.quit()


