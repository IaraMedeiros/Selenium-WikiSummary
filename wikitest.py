from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

import time

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

list_pesquisa = [
    "Pink Floyd",
    "Judas Priest",
    "Nightwish",
    "The Smiths",
    "Deftones",
    "The Cure"
]

driver.get("https://pt.wikipedia.org/")

for i in list_pesquisa:
    try:
        input_element = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='search']"))
        )
        time.sleep(5)

        input_element.clear()

        input_element.send_keys(i + Keys.ENTER)
        time.sleep(5)


        WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".mw-content-ltr.mw-parser-output"))
            )

        div = driver.find_element(By.CSS_SELECTOR, ".mw-content-ltr.mw-parser-output")
        time.sleep(5)

        paragraphs = div.find_elements(By.TAG_NAME, "p")
        arquivo = open("biografias.txt", "a")
        arquivo.write(i + "\n" + paragraphs[0].text + "\n\n")

        time.sleep(12)

    except (TimeoutException, StaleElementReferenceException) as e:
        print(f"Error occurred: {e} in {i}")
        try: 
            driver.refresh()
            time.sleep(8)  
            input_element = driver.find_element(By.CSS_SELECTOR, "input[name='search']")
            input_element.clear()
            input_element.send_keys(i + Keys.ENTER)
        except Exception as e:  
            print(f"Search failed for '{i}': {e}")

driver.quit()