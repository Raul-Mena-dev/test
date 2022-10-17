from selenium.webdriver.common.by import By
from funciones.function import login, check_exists_by_xpath


def test_visible_window(driver, name='rmteste3@yopmail.com', password='3R5f7PX59r'):
    login(driver, name, password)
    vehicles = driver.find_element(By.XPATH, '//*[@id="sider"]/div/ul/li[6]/span/a')
    vehicles.click()
    window = driver.find_element(By.CSS_SELECTOR, '#root > section > section > section > div.ant-row > div:nth-child(2) > button.ant-btn.ant-btn-primary.sc-crHmcD.jcZohB.ml-2.mb-2')
    window.click()
    if check_exists_by_xpath(driver, '/html/body/div[2]/div/div[2]/div'):
        print("encontrado")
    else:
        print('No encontrado')
