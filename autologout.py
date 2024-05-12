from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

if __name__ == "__main__":
    options = Options()
    options.add_argument("headless")
    driver = webdriver.Chrome(executable_path="./chromedriver", options=options)
    driver.get("http://124.16.81.61")
    driver.find_element(By.ID, "logout").click()
    driver.find_element(By.CLASS_NAME, "btn-confirm").click()
    driver.quit()
