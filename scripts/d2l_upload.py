from datetime import datetime
from time import sleep

from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait

WEBDRIVER_PATH = 'F:\\Programs\\chromedriver.exe'
BASE_URL = 'https://d2l.langara.bc.ca/d2l/lms/dropbox/admin/folders_manage.d2l?ou=169914'
USERNAME = 'awatkins01@mylangara.ca'
PASSWORD = 'jiSgG%249bAm'
ASSIGNMENT = 1


def login(driver):
    wait = WebDriverWait(driver, 10)
    wait.until(lambda driver: driver.find_element_by_id('i0116'))
    driver.find_element_by_id("i0116").send_keys(USERNAME)
    driver.find_element_by_id("i0118").send_keys(PASSWORD)
    driver.find_element_by_xpath('//*[@id="idSIButton9"]').click()
    driver.find_element_by_xpath('//*[@id="idSIButton9"]').click()
#     wait for no button
    driver.find_element_by_xpath('//*[@id="idBtn_Back"]').click()




if __name__ == '__main__':

    with Chrome(executable_path=WEBDRIVER_PATH) as driver:
        driver.get(BASE_URL)
        login(driver)

        wait = WebDriverWait(driver, 1000)
        wait.until(lambda driver: driver.find_element_by_id('d2L_body'))

        # A1
        driver.find_element_by_xpath(f'// *[ @ id = "z_d"] / tbody / tr[3] / th / div / div / div[{ASSIGNMENT}] / div / a').click()

        # First student
        driver.find_element_by_xpath(f'// *[ @ id = "z_h"] / tbody / tr[2] / th / table / tbody / tr / td[1] / a').click()

        # Iterate over all student
        driver.find_element_by_xpath("//a[@title='Next Student']").click() # Next btn
        name = driver.find_element_by_css_selector('#z_r > div:nth-child(2) > div > div > div > div > div > div:nth-child(1) > div > table > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(1) > td > label > strong')

        html_editor = driver.find_element_by_xpath('//*[@id="d2l_1_147_75"]')
        html_editor_close = driver.find_element_by_id("d2l_1_6_406")
        document.querySelector("#z_h > tbody > tr:nth-child(2) > th > table > tbody > tr > td.dlay_l > a")

        while True:
            sleep(1)
            driver.find_element_by_xpath('//*[@id="d2l-navigation-iterator-item"]//button').click()

        while True:
            exit(0) if input("Would you like to exit? (y/n): ") == 'y' else None