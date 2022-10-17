import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import random


def login(driver, username, password):
    driver.get("http://dashboard.gas-station-dev.com.s3-website-us-west-2.amazonaws.com/")
    time.sleep(3)
    user = driver.find_element(By.XPATH, '//*[@id="email"]')
    user.clear()
    user.send_keys(username)
    password_field = driver.find_element(By.XPATH, '//*[@id="password"]')
    password_field.clear()
    password_field.send_keys(password)
    password_field.submit()


def logout(driver):
    try:

        driver.refresh()
        time.sleep(3)
        action = ActionChains(driver)
        drop = driver.find_element(By.XPATH, '/html/body/div[1]/section/section/header/div/div[3]/div/ul')
        action.move_to_element(drop).perform()
        log = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/ul/li[3]')
        time.sleep(1)
        action.move_to_element(log).click().perform()
        time.sleep(1)
    except NoSuchElementException as exc:
        print(exc)


# funcion para encontrar elementos, si existen o no, regresa un True si lo encuentra y un False si no
def is_element_present(driver, how, what):
    try:
        driver.find_element(by=how, value=what)
    except NoSuchElementException as exception:
        return False
    return True


def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


def id_generator():
    number = random.randint(1, 500)
    return str(number)


def price_generator():
    price = random.uniform(1.0, 10.0)
    price = round(price, 1)
    return price


def truck_list_num():
    i = random.randint(1, 2)
    return i


def random_int_with_limit(i):
    return random.randint(1, int(i))


def capacity_num_big():
    i = random.randint(9999, 1000000)
    return i


def capacity_num():
    i = random.randint(30, 100)
    return i


def dispenser_uid_generator():
    x = random.randint(1000, 9999)
    y = random.randint(1000, 9999)
    z = random.randint(1000, 9999)
    return str(x) + str(y) + str(z)


def xpath_dispenser(element):
    paths = {
        "dispenser": '//*[@id="sider"]/div/ul/li[7]/span/a',
        'new_dispenser_button': '//*[@id="root"]/section/section/section/div[1]/div[2]/button',
        'uid_field': '//*[@id="name"]',
        'station_field': '//*[@id="station"]',
        'station_menu_options': '//*[@id="menu-"]/div[3]/ul',
        'product': '/html/body/div[2]/div/div[2]/div/div[2]/div[2]/form/div[4]/div[1]/div/div/div/div/div/div/div',
        'product_menu': '//*[@id="menu-"]/div[3]/ul',
        'terminal_number_field': '/html/body/div[2]/div/div[2]/div/div[2]/div[2]/form/div[5]/div[1]/div/div/div/div/div/div/input',
        'dispenser_type': '/html/body/div[2]/div/div[2]/div/div[2]/div[2]/form/div[5]/div[2]/div/div/div/div/div/div/div',
        'dispenser_selection': '//*[@id="menu-"]/div[3]/ul/li',
        'save_button': '/html/body/div[2]/div/div[2]/div/div[2]/div[3]/button[2]',
    }

    return paths[element]


def xpath_products(element):
    paths = {
        'products': '/html/body/div[1]/section/div/div[2]/aside/div/ul/li[5]/span/a',
        'new_product': '/html/body/div[1]/section/section/section/div[1]/div[2]/button',
        'product_name': '/html/body/div[2]/div/div[2]/div/div[2]/div[2]/form/div[2]/div/div/div/div/div/input',
        'product_price': '//*[@id="price"]',
        'station': '/html/body/div[2]/div/div[2]/div/div[2]/div[2]/form/div[4]/div/div/div/div/div/div',
        'station_menu': '/html/body/div[3]/div[3]/ul',
        'save_button': '/html/body/div[2]/div/div[2]/div/div[2]/div[3]/button[2]',

    }

    return paths[element]


def xpath_users(element):
    paths = {
        'users': '/html/body/div[1]/section/div/div[2]/aside/div/ul/li[2]/span/a',
        'new_user': '//*[@id="root"]/section/section/section/div[2]/div[2]/button',
        'first_name': '//*[@id="first_name"]',
        'last_name': '//*[@id="last_name"]',
        'email': '//*[@id="email"]',
        'phone': '//*[@id="phone"]',
        'role': '//*[@id="role"]',
        'station_worker_role': '//*[@id="menu-"]/div[3]/ul/li[2]',
        'fleet_manager_role': '//*[@id="menu-"]/div[3]/ul/li[1]',
        'station': '//*[@id="assigned_stations"]',
        'stations_menu': '//*[@id="menu-"]/div[3]/ul',
        'station_fleet': '//*[@id="customer_stations"]',
        'customer_name': '//*[@id="customer_name"]',
        'save_button': '//*[@id="root"]/section/section/section/div[1]/div[2]/div/div[2]/div[3]/button[2]'

    }

    return paths[element]


def xpath_driver(element):
    path = {
        'drivers_option': '//*[@id="sider"]/div/ul/li[2]/span/a',
        'new_driver': '//*[@id="root"]/section/section/section/div[2]/div[2]/button',
        'first_name': '//*[@id="first_name"]',
        'last_name': '//*[@id="last_name"]',
        'email': '//*[@id="email"]',
        'phone': '//*[@id="phone"]',
        'role': '//*[@id="role"]',
        'role_selection': '//*[@id="menu-"]/div[3]/ul/li',
        'station': '//*[@id="permitted_stations"]',
        'station_menu': '//*[@id="menu-"]/div[3]/ul',
        'save_button': '//*[@id="root"]/section/section/section/div[1]/div[2]/div/div[2]/div[3]/button[2]'
    }

    return path[element]
