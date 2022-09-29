import time
import random
import pytest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from funciones.function import login, logout, check_exists_by_xpath
from funciones.api_data_mock.api import ApiData
from selenium.common.exceptions import NoSuchElementException


def test_user(driver, name="raulmanager@yopmail.com", password="NZcSFdaNAc"):
    data = {}
    new_list_number = ''
    list_number = ''
    i = random.randint(2, 999)
    api = ApiData(i)
    api.assign_values()
    status = ''
    try:
        login(driver, name, password)
        mock_email = '@yopmail.com'
        time.sleep(3)
        users = driver.find_element(By.XPATH, '//*[@id="sider"]/div/ul/li[2]/span/a')
        users.click()
        time.sleep(3)
        list_number = driver.find_element(By.XPATH, '/html/body/div/section/section/section/div[4]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]/span').text
        new_users = driver.find_element(By.XPATH, '//*[@id="root"]/section/section/section/div[2]/div[2]/button')
        new_users.click()
        name = driver.find_element(By.XPATH, '//*[@id="first_name"]')
        data['name'] = api.nombre
        name.send_keys(data['name'])
        time.sleep(1)
        last_name = driver.find_element(By.XPATH, '/html/body/div[1]/section/section/section/div[1]/div[2]/div/div[2]/div[2]/form/div[2]/div[2]/div/div/div/div/div/div/input')
        data['last_name'] = api.apellido
        last_name.send_keys(data['last_name'])
        time.sleep(1)
        phone = driver.find_element(By.XPATH, '//*[@id="phone"]')
        data['telefono'] = api.telefono
        phone.send_keys(data['telefono'])
        time.sleep(1)
        email = driver.find_element(By.XPATH, '//*[@id="email"]')
        new_email = api.nombre + api.apellido + mock_email
        data['email'] = new_email
        email.send_keys(new_email)
        time.sleep(1)
        a = ActionChains(driver)
        role = driver.find_element(By.XPATH, '//*[@id="role"]')
        a.click(role).perform()
        station_worker = driver.find_element(By.XPATH, '//*[@id="menu-"]/div[3]/ul/li[2]')
        data['role'] = station_worker.text
        station_worker.click()
        time.sleep(2)
        station = driver.find_element(By.XPATH, '//*[@id="assigned_stations"]')
        station.click()
        time.sleep(2)
        x = random.randint(1, 3)
        stationselection = driver.find_element(By.XPATH, f'//*[@id="menu-"]/div[3]/ul/li[{x}]')
        data['station'] = stationselection.text
        stationselection.click()
        stationselection.send_keys(Keys.TAB)
        time.sleep(1)
        save_button = driver.find_element(By.XPATH, '//*[@id="root"]/section/section/section/div[1]/div[2]/div/div[2]/div[3]/button[2]')
        save_button.click()
        time.sleep(4)
        new_list_number = driver.find_element(By.XPATH, '/html/body/div/section/section/section/div[4]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]/span').text
        driver.refresh()
        time.sleep(2)
        # empieza el proceso de activacion
        if new_list_number > list_number:
            principal = driver.current_window_handle
            driver.execute_script('''window.open("https://yopmail.com/es/","_blank");''')
            time.sleep(3)
            parent = driver.window_handles[0]
            chld = driver.window_handles[1]
            driver.switch_to.window(parent)
            time.sleep(3)
            selected_user = driver.find_element(By.XPATH, '//*[@id="root"]/section/section/section/div[4]/div[2]/div/div/div/div/div/table/tbody/tr[1]')
            selected_user.click()
            time.sleep(1)
            selected_user_email = driver.find_element(By.XPATH, '//*[@id="email"]').get_attribute("value")
            time.sleep(1)
            driver.switch_to.window(chld)
            time.sleep(1)
            yop_login = driver.find_element(By.XPATH, '//*[@id="login"]')
            yop_login.send_keys(selected_user_email)
            yop_login.submit()
            time.sleep(5)
            if check_exists_by_xpath(driver, '/html/body/div[1]/div/main/div[2]/div[1]/div/div[1]/div[6]/button'):
                driver.switch_to.frame((driver.find_element(By.XPATH, '//*[@id="ifmail"]')))
                if check_exists_by_xpath(driver, "//a[contains(text(),'Verify email')]"):
                    correo = driver.find_element(By.XPATH, "//a[contains(text(),'Verify email')]")
                    correo.click()
                    driver.switch_to.window(chld)
                    driver.back()
                    time.sleep(2)
                    borrar = driver.find_element(By.XPATH, '/html/body/div/div[2]/main/div[3]/div/div[1]/div[2]/div/div/form/div/div[1]/div[3]/a')
                    borrar.click()
                    time.sleep(2)
                    driver.switch_to.window(parent)
                    time.sleep(5)
                    cancel_button = driver.find_element(By.XPATH, '//*[@id="root"]/section/section/section/div[1]/div[2]/div/div[2]/div[3]/button[1]')
                    cancel_button.click()
                    time.sleep(3)
                else:
                    driver.back()
                    time.sleep(2)
                    borrar = driver.find_element(By.XPATH, '/html/body/div/div[2]/main/div[3]/div/div[1]/div[2]/div/div/form/div/div[1]/div[3]/a')
                    borrar.click()
                    time.sleep(2)
                    driver.switch_to.window(parent)
                    time.sleep(5)
                    cancel_button = driver.find_element(By.XPATH, '//*[@id="root"]/section/section/section/div[1]/div[2]/div/div[2]/div[3]/button[1]')
                    cancel_button.click()
                    time.sleep(3)
                    driver.refresh()
                    time.sleep(2)
                    status = driver.find_element(By.XPATH, '//*[@id="root"]/section/section/section/div[4]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[4]').text
                    data['status'] = status
                    time.sleep(1)
            else:
                driver.back()
                time.sleep(2)
                borrar = driver.find_element(By.XPATH, '/html/body/div/div[2]/main/div[3]/div/div[1]/div[2]/div/div/form/div/div[1]/div[3]/a')
                borrar.click()
                time.sleep(2)
                driver.switch_to.window(parent)
                time.sleep(5)
                cancel_button = driver.find_element(By.XPATH, '//*[@id="root"]/section/section/section/div[1]/div[2]/div/div[2]/div[3]/button[1]')
                cancel_button.click()
                time.sleep(3)
                driver.refresh()
                time.sleep(2)
                status = driver.find_element(By.XPATH, '//*[@id="root"]/section/section/section/div[4]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[4]').text
                data['status'] = status
                time.sleep(1)
        driver.refresh()
        time.sleep(2)
        status = driver.find_element(By.XPATH, '//*[@id="root"]/section/section/section/div[4]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[4]').text
        data['status'] = status
        time.sleep(1)
    except NoSuchElementException as exc:
        print(exc)
    new_nombre = api.nombre.replace('-', '')
    new_apellido = api.apellido.replace('-', '')
    new_telefono = api.telefono.replace('-', '')
    if (new_nombre.isdigit() or new_apellido.isdigit()) and int(new_list_number) > int(list_number) and status == 'Active':
        print(f'Permite el registro de usuario  con numeros en el nombre y se activo, {str(data)}')
        assert False, f'Permite el registro de usuario  con numeros en el nombre y se activo, {str(data)}'
    elif (new_nombre.isdigit() or new_apellido.isdigit()) and int(new_list_number) > int(list_number) and status == 'Pending':
        print(f'Permite el registro de usuario  con numeros en el nombre y no se activo, {str(data)}')
        assert False, f'Permite el registro de usuario  con numeros en el nombre y no se activo, {str(data)}'
    elif (new_nombre.isdigit() or new_apellido.isdigit()) and int(new_list_number) == int(list_number):
        print(f'No permite el registro de usuario  con numeros en el nombre, {str(data)}')
        assert True, f'No permite el registro de usuario  con numeros en el nombre, {str(data)}'
    elif new_telefono.isalpha() and int(new_list_number) > int(list_number) and status == 'Active':
        print(f'Permite el registro de usuario con letras en el telefono y se activo, {str(data)}')
        assert False, f'Permite el registro de usuario con letras en el telefono y se activo, {str(data)}'
    elif new_telefono.isalpha() and int(new_list_number) > int(list_number) and status == 'Pending':
        print(f'Permite el registro de usuario con letras en el telefono y no se activo, {str(data)}')
        assert False, f'Permite el registro de usuario con letras en el telefono y no se activo, {str(data)}'
    elif new_telefono.isalpha() and int(new_list_number) == int(list_number):
        print(f'No permite el registro de usuario con letras en el telefono, {str(data)}')
        assert True, f'No permite el registro con numeros, {str(data)}'
    else:
        assert int(new_list_number) > int(list_number) and status == 'Active', f'No se registro el usuario, {str(data)}'
        print(f'Usuario registrado y activado, {str(data)}')

