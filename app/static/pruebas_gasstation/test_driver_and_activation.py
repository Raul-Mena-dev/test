import time
import pytest
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from funciones.function import login, check_exists_by_xpath
from funciones.api_data_mock.api import ApiData
from selenium.common.exceptions import NoSuchElementException


def test_drivers(driver, name='multiplestation@yopmail.com', password='QChnra3FVQ'):
    data = {}
    new_list_number = ''
    list_number = ''
    x = random.randint(2, 49)
    api = ApiData(x)
    api.assign_values()
    try:
        login(driver, name, password)
        time.sleep(2)
        drivers = driver.find_element(By.XPATH, '//*[@id="sider"]/div/ul/li[2]/span/a')
        drivers.click()
        time.sleep(3)
        list_number = driver.find_element(By.XPATH, '//*[@id="root"]/section/section/section/div[4]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]/span').text
        new_user = driver.find_element(By.XPATH, '//*[@id="root"]/section/section/section/div[2]/div[2]/button')
        new_user.click()
        name = driver.find_element(By.XPATH, '//*[@id="first_name"]')
        data['name'] = api.nombre
        name.send_keys(data['name'])
        last_name = driver.find_element(By.XPATH, '//*[@id="last_name"]')
        data['last_name'] = api.apellido
        last_name.send_keys(data['last_name'])
        email = driver.find_element(By.XPATH, '//*[@id="email"]')
        data['email'] = api.nombre + api.apellido + '@yopmail.com'
        email.send_keys(data['email'])
        phone = driver.find_element(By.XPATH, '//*[@id="phone"]')
        data['phone'] = api.telefono
        phone.send_keys(data['phone'])
        role = driver.find_element(By.XPATH, '//*[@id="role"]')
        role.click()
        role_driver = driver.find_element(By.XPATH, '//*[@id="menu-"]/div[3]/ul/li')
        data['role'] = role_driver.text
        role_driver.click()
        stations = driver.find_element(By.XPATH, '//*[@id="permitted_stations"]')
        stations.click()
        station_selection = driver.find_element(By.XPATH, '//*[@id="menu-"]/div[3]/ul/li')
        data['station'] = station_selection.text
        station_selection.click()
        station_selection.send_keys(Keys.TAB)
        save = driver.find_element(By.XPATH, '//*[@id="root"]/section/section/section/div[1]/div[2]/div/div[2]/div[3]/button[2]')
        a = ActionChains(driver)
        a.click(save).perform()
        time.sleep(5)
        new_list_number = driver.find_element(By.XPATH, '//*[@id="root"]/section/section/section/div[4]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]/span').text
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
        assert False, f'Driver no añadido , {data}'
    new_nombre = api.nombre.replace('-', '')
    new_apellido = api.apellido.replace('-', '')
    new_telefono = api.telefono.replace('-', '')
    if (new_nombre.isdigit() or new_apellido.isdigit()) and int(new_list_number) > int(list_number) and status == 'Active':
        print(f'Permite el registro del conductor  con numeros en el nombre/apellido y se activo, {str(data)}')
        assert False, f'Permite el registro del conductor  con numeros en el nombre/apellido y se activo, {str(data)}'
    elif (new_nombre.isdigit() or new_apellido.isdigit()) and int(new_list_number) > int(list_number) and status == 'Pending':
        print(f'Permite el registro del conductor  con numeros en el nombre/apellido y no se activo, {str(data)}')
        assert False, f'Permite el registro del conductor  con numeros en el nombre/apellido y no se activo, {str(data)}'
    elif (new_nombre.isdigit() or new_apellido.isdigit()) and int(new_list_number) == int(list_number):
        print(f'No permite el registro del conductor con numeros en el nombre/apellido, {str(data)}')
        assert True, f'No permite el registro del conductor con numeros en el nombre/apellido, {str(data)}'
    elif (any(not c.isalnum() for c in new_nombre) or any(not c.isalnum() for c in new_apellido)) and int(new_list_number) > int(list_number) and status == 'Active':
        print(f'Permite el registro del conductor con caracteres especiales en el nombre/apellido y se activo, {str(data)}')
        assert False, f'Permite el registro del conductor  con numeros en el nombre/apellido y se activo, {str(data)}'
    elif (any(not c.isalnum() for c in new_nombre) or any(not c.isalnum() for c in new_apellido)) and int(new_list_number) > int(list_number) and status == 'Pending':
        print(f'Permite el registro del conductor con caracteres especiales en el nombre/apellido y no se activo, {str(data)}')
        assert False, f'Permite el registro del conductor  con numeros en el nombre/apellido y no se activo, {str(data)}'
    elif (any(not c.isalnum() for c in new_nombre) or any(not c.isalnum() for c in new_apellido)) and int(new_list_number) == int(list_number):
        print(f'No permite el registro del conductor con caracteres especiales en el nombre/apellido, {str(data)}')
        assert True, f'Permite el registro del conductor con caracteres especiales en el nombre/apellido, {str(data)}'
    elif new_telefono.isalpha() and int(new_list_number) > int(list_number) and status == 'Active':
        print(f'Permite el registro del conductor con letras en el telefono y se activo, {str(data)}')
        assert False, f'Permite el registro del conductor con letras en el telefono y se activo, {str(data)}'
    elif new_telefono.isalpha() and int(new_list_number) > int(list_number) and status == 'Pending':
        print(f'Permite el registro del conductor con letras en el telefono y no se activo, {str(data)}')
        assert False, f'Permite el registro del conductor con letras en el telefono y no se activo, {str(data)}'
    elif new_telefono.isalpha() and int(new_list_number) == int(list_number):
        print(f'No permite el registro del conductor con letras en el telefono, {str(data)}')
        assert True, f'No permite el registro del conductor con letras en el telefono, {str(data)}'
    else:
        assert int(new_list_number) > int(list_number) and status == 'Active', f'No se registro el usuario, {str(data)}'
        print(f'Usuario registrado y activado, {str(data)}')
