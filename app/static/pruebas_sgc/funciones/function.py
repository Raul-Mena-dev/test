import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import random


def login(driver, username, password):
    driver.get("http://192.168.9.164/sgcweb")
    time.sleep(3)
    user = driver.find_element(By.XPATH, '//*[@id="user_name"]') 
    user.clear()
    user.send_keys(username)
    password_field = driver.find_element(By.XPATH, '//*[@id="user_password"]')
    password_field.clear()
    password_field.send_keys(password)
    password_field.submit()


def login_web(driver, username, password):
    driver.get("http://testventas.sgcweb.com.mx/index.php?action=Login&module=Users&login_module=Home&login_action=index")
    time.sleep(3)
    user = driver.find_element(By.XPATH, '//*[@id="user_name"]')
    user.clear()
    user.send_keys(username)
    password_field = driver.find_element(By.XPATH, '//*[@id="user_password"]')
    password_field.clear()
    password_field.send_keys(password)
    password_field.submit()


def login_carburacion(driver, username, password):
    driver.get("http://192.168.9.163/sgcweb")
    time.sleep(3)
    user = driver.find_element(By.XPATH, '//*[@id="user_name"]')
    user.clear()
    user.send_keys(username)
    password_field = driver.find_element(By.XPATH, '//*[@id="user_password"]')
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


def convertir_fecha_24(fecha):
    if 'pm' in fecha:
        fecha_nueva = fecha.split(' ')
        hora_a_modificar = fecha_nueva[1]
        hora_a_modificar = hora_a_modificar.replace(':', '')
        hora_a_modificar = hora_a_modificar.replace('pm', '')
        hora_a_modificar = int(hora_a_modificar) + 1200
        if hora_a_modificar >= 2400:
            hora_a_modificar = int(hora_a_modificar) - 1200
        hora_a_modificar = str(hora_a_modificar)
        hora_a_modificar = hora_a_modificar[:2] + ':' + hora_a_modificar[2:]
        hora_a_modificar = hora_a_modificar + ':00'
        fecha_final = fecha_nueva[0] + ' ' + hora_a_modificar
    else:
        fecha_nueva = fecha.split(' ')
        hora_a_modificar = fecha_nueva[1]
        hora_a_modificar = hora_a_modificar.replace(':', '')
        hora_a_modificar = hora_a_modificar.replace('am', '')
        hora_a_modificar = hora_a_modificar[:2] + ':' + hora_a_modificar[2:]
        hora_a_modificar = hora_a_modificar + ':00'
        fecha_final = fecha_nueva[0] + ' ' + hora_a_modificar
    return fecha_final


def convertir_mes(fecha):
    meses = {
        'Enero': '01',
        'Febrero': '02',
        'Marzo': '03',
        'Abril': '04',
        'Mayo': '05',
        'Junio': '06',
        'Julio': '07',
        'Agosto': '08',
        'Septiembre': '09',
        'Octubre': '10',
        'Noviembre': '11',
        'Diciembre': '12'
    }
    fecha = fecha.split('-')
    dia = fecha[0]
    mes = fecha[1]
    anio = fecha[2]

    numero_mes = str(meses[mes])
    fecha_nueva = anio + '-' + numero_mes + '-' + dia
    return fecha_nueva

