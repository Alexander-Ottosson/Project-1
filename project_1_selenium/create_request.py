from time import sleep

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

ser = Service('D:/Documents/Work Related Documents/geckodriver.exe')
driver: WebDriver = webdriver.Firefox(service=ser)

if __name__ == '__main__':
    driver.get(
        'D:\\Documents\\Work Related Documents\\Training Projects\\Major Projects\\project_1\\front_end\\login.html'
    )
    try:
        username: WebElement = driver.find_element(by=By.ID, value='username-input')
        username.send_keys("tdgroot")
        password: WebElement = driver.find_element(by=By.ID, value='password-input')
        password.send_keys('password')
        login_button: WebElement = driver.find_element(by=By.ID, value='login-button')
        login_button.click()
        sleep(2)
        create_request_link: WebElement = driver.find_element(by=By.XPATH, value='/html/body/nav/div/div/ul/li[2]/a')
        create_request_link.click()
        sleep(2)
        event_name: WebElement = driver.find_element(by=By.ID, value='event-name')
        event_name.send_keys('Explosive Web Design')
        sleep(0.5)
        event_description: WebElement = driver.find_element(by=By.ID, value='event-description')
        event_description.send_keys('A class on various new web design techniques that have been exploding in popularity')
        sleep(0.5)
        justification: WebElement = driver.find_element(by=By.ID, value='justification')
        justification.send_keys('I want to learn new web design trends for a future project')
        sleep(0.5)
        grade_type: WebElement = driver.find_element(by=By.ID, value='grade-type')
        grade_type.send_keys('Pass/Fail')
        sleep(0.5)
        start_date: WebElement = driver.find_element(by=By.XPATH, value='//*[@id="start-date"]')
        start_date.send_keys('05/18/2022')
        sleep(0.5)
        missed_start: WebElement = driver.find_element(by=By.XPATH, value='//*[@id="missed-start"]')
        missed_start.send_keys('05/18/2022')
        sleep(0.5)
        cost: WebElement = driver.find_element(by=By.ID, value='cost')
        cost.send_keys('200')
        sleep(0.5)
        event_type: WebElement = driver.find_element(by=By.ID, value='event-type')
        event_type.send_keys('Technical Training')
        sleep(0.5)
        street: WebElement = driver.find_element(by=By.ID, value='street')
        street.send_keys('313 Knowledge Avenue')
        sleep(0.5)
        city: WebElement = driver.find_element(by=By.ID, value='city')
        city.send_keys('Teufort')
        sleep(0.5)
        state: WebElement = driver.find_element(by=By.ID, value='state')
        state.send_keys('New Mexico')
        sleep(0.5)
        zip_code: WebElement = driver.find_element(by=By.ID, value='zip')
        zip_code.send_keys('66266', Keys.TAB)
        sleep(0.5)
        submit_button: WebElement = driver.find_element(by=By.ID, value='submit')
        submit_button.click()

    finally:
        sleep(10)
        driver.quit()
