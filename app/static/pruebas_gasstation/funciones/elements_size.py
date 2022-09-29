import time
from selenium.webdriver.common.by import By
from funciones.function import login


def test_list_size(driver, name='rmteste3@yopmail.com', password='3R5f7PX59r'):
    login(driver, name, password)
    time.sleep(2)
    drivers = driver.find_element(By.XPATH, '//*[@id="sider"]/div/ul/li[2]/span/a')
    drivers.click()
    time.sleep(2)
    table = driver.find_element(By.XPATH, '//*[@id="root"]/section/section/section/div[4]/div[2]/div/div/div/div/div/table/tbody')
    size = len(table.find_elements(By.TAG_NAME, 'tr'))
    for i in range(size):
        status = driver.find_element(By.XPATH, f'//*[@id="root"]/section/section/section/div[4]/div[2]/div/div/div/div/div/table/tbody/tr[{i+1}]/td[4]/span').text
        if status == 'Active':
            print(status)

