import random

from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
import time
from funciones.function import login, loginprod, xpath_dispenser, dispenser_uid_generator, random_int_with_limit, id_generator, \
    xpath_products, price_generator, xpath_users, xpath_driver, truck_list_num, capacity_num
from funciones.api_data_mock.api import ApiData
from selenium.common.exceptions import NoSuchElementException


# test para login
def test_log_manager(driver, name='raulmanager@yopmail.com', password='Rm+123456'):
    login(driver, name, password)
    print('Login como station manager: exitoso')


# test para login en prod
# def test_log_manager(driver, name='manunez16@yopmail.com', password='93JFjex2J4'):
#     loginprod(driver, name, password)
#     print('Login como station manager: exitoso')


# test para crear un producto
def test_create_product(driver):
    data = {}
    new_list_number = ''
    list_number = ''
    try:

        time.sleep(1)
        products = driver.find_element(By.XPATH, xpath_products('products'))
        products.click()
        time.sleep(5)
        list_number = driver.find_element(By.CSS_SELECTOR, 'section.ant-layout.ant-layout-has-sider section.ant-layout.site-layout section.ant-layout div.ant-table-wrapper.sc-egiyK.VgbMS:nth-child(2) div.ant-spin-nested-loading div.ant-spin-container div.ant-table div.ant-table-container div.ant-table-content tbody.ant-table-tbody:nth-child(3) tr.ant-table-row.ant-table-row-level-0:nth-child(1) td.ant-table-cell:nth-child(1) span.ant-typography > strong:nth-child(1)').text
        new_product = driver.find_element(By.XPATH, xpath_products('new_product'))
        new_product.click()
        i = random.randint(2, 49)
        api = ApiData(i)
        api.assign_values()
        product_name = driver.find_element(By.XPATH, xpath_products('product_name'))
        name = api.nombre + 'Test'
        data['name'] = name
        product_name.send_keys(name)
        price = driver.find_element(By.XPATH, xpath_products('product_price'))
        price_value = price_generator()
        data['price'] = price_value
        price.send_keys(price_value)
        station = driver.find_element(By.XPATH, xpath_products('station'))
        station.click()
        time.sleep(1)
        station_menu = driver.find_element(By.XPATH, xpath_products('station_menu'))
        station_options_len = len((station_menu.find_elements(By.TAG_NAME, 'li')))
        if station_options_len == 1:
            station_selection = driver.find_element(By.XPATH, '//*[@id="menu-"]/div[3]/ul/li')
            data['station'] = station_selection.text
        else:
            station_selection = driver.find_element(By.XPATH, f'//*[@id="menu-"]/div[3]/ul/li[{random_int_with_limit(station_options_len)}]')
            data['station'] = station_selection.text

        station_selection.click()
        save_button = driver.find_element(By.XPATH, xpath_products('save_button'))
        save_button.click()
        time.sleep(2)
        new_list_number = driver.find_element(By.CSS_SELECTOR, 'section.ant-layout.ant-layout-has-sider section.ant-layout.site-layout section.ant-layout div.ant-table-wrapper.sc-egiyK.VgbMS:nth-child(2) div.ant-spin-nested-loading div.ant-spin-container div.ant-table div.ant-table-container div.ant-table-content tbody.ant-table-tbody:nth-child(3) tr.ant-table-row.ant-table-row-level-0:nth-child(1) td.ant-table-cell:nth-child(1) span.ant-typography > strong:nth-child(1)').text

    except NoSuchElementException as exc:
        assert int(new_list_number) > int(list_number), f"Prueba fallida, con los datos: {str(data)}"
        print(exc)
        print(f'prueba finalizada incorrectamente con los datos: {str(data)}, mensaje de error{exc}')

    print(f'prueba finalizada correctamente con los datos: \n')
    for dato, valor in data.items():
        print(dato, ': ', valor)
    assert int(new_list_number) > int(list_number), f"Prueba fallida, con los datos: {str(data)}"


# test para crear un dispenser
# @pytest.mark.flaky(reruns=2)
def test_dispenser(driver):
    data = {}
    list_num = ''
    new_list_num = ''
    try:
        time.sleep(1)
        driver.refresh()
        time.sleep(3)
        dispenser_menu = driver.find_element(By.XPATH, xpath_dispenser('dispenser'))
        dispenser_menu.click()
        time.sleep(2)
        list_num = driver.find_element(By.CSS_SELECTOR, 'section.ant-layout.ant-layout-has-sider section.ant-layout.site-layout section.ant-layout div.ant-table-wrapper.sc-egiyK.VgbMS:nth-child(2) div.ant-spin-nested-loading div.ant-spin-container div.ant-table div.ant-table-container div.ant-table-content tbody.ant-table-tbody:nth-child(3) tr.ant-table-row.ant-table-row-level-0:nth-child(1) td.ant-table-cell:nth-child(1) span.ant-typography > strong:nth-child(1)').text
        new_dispenser_button = driver.find_element(By.XPATH, xpath_dispenser('new_dispenser_button'))
        new_dispenser_button.click()
        time.sleep(2)
        uid_field = driver.find_element(By.XPATH, xpath_dispenser('uid_field'))
        uid = dispenser_uid_generator()
        data['uid'] = uid
        uid_field.send_keys(uid)
        station_field = driver.find_element(By.XPATH, xpath_dispenser('station_field'))
        station_field.click()
        station_options_menu = driver.find_element(By.XPATH, xpath_dispenser('station_menu_options'))
        station_options = station_options_menu.find_elements(By.TAG_NAME, 'li')
        station_options_len = len(station_options)
        if station_options_len == 1:
            station_selection = driver.find_element(By.XPATH, '//*[@id="menu-"]/div[3]/ul/li')
            data['station'] = station_selection.text
        else:
            station_selection = driver.find_element(By.XPATH, f'//*[@id="menu-"]/div[3]/ul/li[{random_int_with_limit(station_options_len)}]')
            data['station'] = station_selection.text

        station_selection.click()
        time.sleep(1)

        product = driver.find_element(By.XPATH, xpath_dispenser('product'))
        product.click()
        time.sleep(1)
        product_list = driver.find_element(By.XPATH, xpath_dispenser('product_menu'))
        product_list_len = len(product_list.find_elements(By.TAG_NAME, 'li'))
        if product_list_len == 1:
            product_selection = driver.find_element(By.XPATH, f'//*[@id="menu-"]/div[3]/ul/li')
            data['product'] = product_selection.text
        else:
            i = random_int_with_limit(product_list_len)
            product_selection = driver.find_element(By.XPATH, f'//*[@id="menu-"]/div[3]/ul/li[{i}]')
            k = product_selection.get_attribute('aria-disabled')
            data['product'] = product_selection.text
            while k == 'true':
                i = random_int_with_limit(product_list_len)
                product_selection = driver.find_element(By.XPATH, f'//*[@id="menu-"]/div[3]/ul/li[{i}]')
                k = product_selection.get_attribute('aria-disabled')
                data['product'] = product_selection.text

        product_selection.click()

        terminal_number_field = driver.find_element(By.XPATH, xpath_dispenser('terminal_number_field'))
        terminal_number = id_generator()
        data['terminal_number'] = terminal_number
        terminal_number_field.send_keys(terminal_number)
        dispenser_type = driver.find_element(By.XPATH, xpath_dispenser('dispenser_type'))
        dispenser_type.click()
        time.sleep(1)
        dispenser_selection = driver.find_element(By.XPATH, xpath_dispenser('dispenser_selection'))
        dispenser_selection.click()
        data['dispenser_type'] = dispenser_selection.text
        save_button = driver.find_element(By.XPATH, xpath_dispenser('save_button'))
        save_button.click()
        time.sleep(1)
        new_list_num = driver.find_element(By.CSS_SELECTOR, 'section.ant-layout.ant-layout-has-sider section.ant-layout.site-layout section.ant-layout div.ant-table-wrapper.sc-egiyK.VgbMS:nth-child(2) div.ant-spin-nested-loading div.ant-spin-container div.ant-table div.ant-table-container div.ant-table-content tbody.ant-table-tbody:nth-child(3) tr.ant-table-row.ant-table-row-level-0:nth-child(1) td.ant-table-cell:nth-child(1) span.ant-typography > strong:nth-child(1)').text

    except NoSuchElementException as exc:
        assert int(new_list_num) > int(list_num), f"Prueba fallida con los datos = {str(data)}"
        print(exc)
        print(f'prueba finalizada incorrectamente con los datos: {str(data)}, mensaje de error{exc}')

    print(f'prueba finalizada correctamente con los datos: \n')
    for dato, valor in data.items():
        print(dato, ': ', valor)
    assert int(new_list_num) > int(list_num), f"Prueba fallida con los datos = {str(data)}"


# test para crear un station worker
def test_create_station_worker(driver):
    data = {}
    list_num = ''
    new_list_num = ''
    try:
        time.sleep(1)
        driver.refresh()
        time.sleep(3)
        user = driver.find_element(By.XPATH, xpath_users('users'))
        user.click()
        time.sleep(2)
        list_num = driver.find_element(By.XPATH, '//*[@id="root"]/section/section/section/div[4]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]/span').text
        new_user = driver.find_element(By.XPATH, xpath_users('new_user'))
        new_user.click()
        i = random.randint(2, 49)
        api = ApiData(i)
        api.assign_values()
        mock_email = api.nombre + api.apellido + '@yopmail.com'
        data['email'] = mock_email
        first_name_field = driver.find_element(By.XPATH, xpath_users('first_name'))
        last_name_field = driver.find_element(By.XPATH, xpath_users('last_name'))
        email_field = driver.find_element(By.XPATH, xpath_users('email'))
        phone_field = driver.find_element(By.XPATH, xpath_users('phone'))
        role_field = driver.find_element(By.XPATH, xpath_users('role'))
        save_button = driver.find_element(By.XPATH, xpath_users('save_button'))
        first_name = api.nombre
        data['first_name'] = first_name
        first_name_field.send_keys(first_name)
        last_name = api.apellido
        data['last_name'] = last_name
        last_name_field.send_keys(last_name)
        email_field.send_keys(mock_email)
        phone = api.telefono
        data['phone'] = phone
        phone_field.send_keys(phone)
        role_field.click()
        time.sleep(2)
        role_selection = driver.find_element(By.XPATH, xpath_users('station_worker_role'))
        data['role'] = role_selection.text
        role_selection.click()
        station = driver.find_element(By.XPATH, xpath_users('station'))
        station.click()
        time.sleep(2)
        station_menu = driver.find_element(By.XPATH, xpath_users('stations_menu'))
        station_menu_len = len(station_menu.find_elements(By.TAG_NAME, 'li'))
        if station_menu_len == 1:
            station_selection = driver.find_element(By.XPATH, '//*[@id="menu-"]/div[3]/ul/li')
            data['station'] = station_selection.text
        else:
            station_selection = driver.find_element(By.XPATH, f'//*[@id="menu-"]/div[3]/ul/li[{random_int_with_limit(station_menu_len)}]')
            data['station'] = station_selection.text
        station_selection.click()
        station_selection.send_keys(Keys.TAB)
        save_button.click()
        time.sleep(3)
        new_list_num = driver.find_element(By.XPATH, '//*[@id="root"]/section/section/section/div[4]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]/span').text
    except NoSuchElementException as exc:
        print(exc)
        print(f'prueba finalizada incorrectamente con los datos: {str(data)}, mensaje de error{exc}')
        assert int(new_list_num) > int(list_num), f"Prueba fallida con los datos = {str(data)}"

    print(f'prueba finalizada correctamente con los datos: \n')
    for dato, valor in data.items():
        print(dato, ': ', valor)
    assert int(new_list_num) > int(list_num), f"Prueba fallida con los datos, no se creo el usuario = {str(data)}"


# test para crear un fleet manager
def test_create_fleet_manager(driver):
    data = {}
    list_num = ''
    new_list_num = ''
    try:
        time.sleep(1)
        driver.refresh()
        time.sleep(3)
        user = driver.find_element(By.XPATH, xpath_users('users'))
        user.click()
        time.sleep(3)
        list_num = driver.find_element(By.XPATH, '//*[@id="root"]/section/section/section/div[4]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]/span').text
        new_user = driver.find_element(By.XPATH, xpath_users('new_user'))
        new_user.click()
        i = random.randint(2, 49)
        api = ApiData(i)
        api.assign_values()
        mock_email = api.nombre + api.apellido + '@yopmail.com'
        data['email'] = mock_email
        first_name = driver.find_element(By.XPATH, xpath_users('first_name'))
        last_name = driver.find_element(By.XPATH, xpath_users('last_name'))
        email = driver.find_element(By.XPATH, xpath_users('email'))
        phone = driver.find_element(By.XPATH, xpath_users('phone'))
        role = driver.find_element(By.XPATH, xpath_users('role'))
        save_button = driver.find_element(By.XPATH, xpath_users('save_button'))
        nombre = api.nombre
        data['first_name'] = nombre
        first_name.send_keys(nombre)
        apellido = api.apellido
        data['last_name'] = apellido
        last_name.send_keys(apellido)
        email.send_keys(mock_email)
        telefono = api.telefono
        data['phone'] = telefono
        phone.send_keys(api.telefono)
        role.click()
        time.sleep(2)
        role_selection = driver.find_element(By.XPATH, xpath_users('fleet_manager_role'))
        data['role'] = role_selection.text
        role_selection.click()
        customer_name = driver.find_element(By.XPATH, xpath_users('customer_name'))
        data['customer_name'] = nombre + 'Customer'
        customer_name.send_keys(data['customer_name'])
        station = driver.find_element(By.XPATH, xpath_users('station_fleet'))
        station.click()
        time.sleep(2)
        station_menu = driver.find_element(By.XPATH, xpath_users('stations_menu'))
        station_menu_len = len(station_menu.find_elements(By.TAG_NAME, 'li'))
        if station_menu_len == 1:
            station_selection = driver.find_element(By.XPATH, '//*[@id="menu-"]/div[3]/ul/li')
            data['station'] = station_selection.text
        else:
            station_selection = driver.find_element(By.XPATH,
                                                    f'//*[@id="menu-"]/div[3]/ul/li[{random_int_with_limit(station_menu_len)}]')
            data['station'] = station_selection.text

        station_selection.click()
        station_selection.send_keys(Keys.TAB)
        save_button.click()
        time.sleep(3)
        new_list_num = driver.find_element(By.XPATH, '//*[@id="root"]/section/section/section/div[4]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]/span').text
    except NoSuchElementException as exc:
        print(exc)
        print(f'prueba finalizada incorrectamente con los datos: {str(data)}, mensaje de error{exc}')
        assert int(new_list_num) > int(list_num), f"Prueba fallida con los datos = {str(data)}"

    print(f'prueba finalizada correctamente con los datos: \n')
    for dato, valor in data.items():
        print(dato, ': ', valor)
    assert int(new_list_num) > int(list_num), f"Prueba fallida con los datos = {str(data)}"


# test para cerrar la sesion
def test_logout(driver):
    try:
        time.sleep(1)
        driver.refresh()
        time.sleep(3)
        action = ActionChains(driver)
        drop = driver.find_element(By.XPATH, ' /html/body/div[1]/section/section/header/div/div[2]/ul/li/div/span/div/div')
        action.move_to_element(drop).perform()
        log = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/ul/li[3]')
        time.sleep(1)
        action.move_to_element(log).click().perform()
        time.sleep(1)
    except NoSuchElementException as exc:
        print(exc)
        assert False, f'No se pudo hacer el logout, {str(exc)}'
    print('Logout exitoso')
    assert True, 'No se pudo hacer el logout '


# test para login
def test_log_fleet(driver, name='multiplestation@yopmail.com', password='12345678'):
    login(driver, name, password)
    print('Login como fleet manager: exitoso')


# test para login en prod
# def test_log_fleet(driver, name='sersaldivar@yopmail.com', password='12qwaszxZX.'):
#     login(driver, name, password)
#     print('Login como fleet manager: exitoso')


def test_driver(driver):
    new_list_number = ''
    list_number = ''
    data = {}
    try:
        time.sleep(1)
        drivers_option = driver.find_element(By.XPATH, xpath_driver('drivers_option'))
        drivers_option.click()
        time.sleep(5)
        list_number = driver.find_element(By.CSS_SELECTOR, 'section.ant-layout.ant-layout-has-sider section.ant-layout.site-layout section.ant-layout div.ant-table-wrapper.sc-egiyK.jfbgly:nth-child(2) div.ant-spin-nested-loading div.ant-spin-container div.ant-table div.ant-table-container div.ant-table-content tbody.ant-table-tbody:nth-child(3) tr.ant-table-row.ant-table-row-level-0:nth-child(1) td.ant-table-cell:nth-child(1) span.ant-typography > strong:nth-child(1)').text
        new_driver = driver.find_element(By.XPATH, xpath_driver('new_driver'))
        new_driver.click()
        time.sleep(1)
        i = random.randint(2, 49)
        api = ApiData(i)
        api.assign_values()
        data['first_name'] = api.nombre
        first_name = driver.find_element(By.XPATH, xpath_driver('first_name'))
        first_name.send_keys(data['first_name'])
        data['last_name'] = api.apellido
        last_name = driver.find_element(By.XPATH, xpath_driver('last_name'))
        last_name.send_keys(data['last_name'])
        data['email'] = data['first_name'] + 'driver@yopmail.com'
        email = driver.find_element(By.XPATH, xpath_driver('email'))
        email.send_keys(data['email'])
        data['phone'] = api.telefono
        phone = driver.find_element(By.XPATH, xpath_driver('phone'))
        phone.send_keys(data['phone'])
        role = driver.find_element(By.XPATH, xpath_driver('role'))
        role.click()
        role_selection = driver.find_element(By.XPATH, xpath_driver('role_selection'))
        role_selection.click()
        data['role'] = role_selection.text
        station = driver.find_element(By.XPATH, xpath_driver('station'))
        station.click()
        time.sleep(1)
        station_menu = driver.find_element(By.XPATH, xpath_driver('station_menu'))
        station_options_len = len((station_menu.find_elements(By.TAG_NAME, 'li')))
        if station_options_len == 1:
            station_selection = driver.find_element(By.XPATH, '//*[@id="menu-"]/div[3]/ul/li')
            data['station'] = station_selection.text
        else:
            station_selection = driver.find_element(By.XPATH, f'//*[@id="menu-"]/div[3]/ul/li[{random_int_with_limit(station_options_len)}]')
            data['station'] = station_selection.text

        station_selection.click()
        station_selection.send_keys(Keys.TAB)
        save_button = driver.find_element(By.XPATH, xpath_driver('save_button'))
        save_button.click()
        time.sleep(5)
        new_list_number = driver.find_element(By.CSS_SELECTOR, 'section.ant-layout.ant-layout-has-sider section.ant-layout.site-layout section.ant-layout div.ant-table-wrapper.sc-egiyK.jfbgly:nth-child(2) div.ant-spin-nested-loading div.ant-spin-container div.ant-table div.ant-table-container div.ant-table-content tbody.ant-table-tbody:nth-child(3) tr.ant-table-row.ant-table-row-level-0:nth-child(1) td.ant-table-cell:nth-child(1) span.ant-typography > strong:nth-child(1)').text
    except NoSuchElementException as exc:
        print(exc)

    print(f'prueba finalizada correctamente con los datos: \n')
    for dato, valor in data.items():
        print(dato, ': ', valor)
    assert int(new_list_number) > int(list_number), f"Prueba fallida, con los datos: {str(data)}"


def test_add_vehicle(driver):
    data = {}
    new_list_number = ''
    list_number = ''
    try:
        time.sleep(1)
        driver.refresh()
        time.sleep(2)
        vehicles = driver.find_element(By.XPATH, '//*[@id="sider"]/div/ul/li[6]/span/a')
        vehicles.click()
        time.sleep(5)
        list_number = driver.find_element(By.CSS_SELECTOR, 'section.ant-layout.ant-layout-has-sider section.ant-layout.site-layout section.ant-layout div.ant-table-wrapper.sc-egiyK.jfbgly:nth-child(2) div.ant-spin-nested-loading div.ant-spin-container div.ant-table div.ant-table-container div.ant-table-content tbody.ant-table-tbody:nth-child(3) tr.ant-table-row.ant-table-row-level-0:nth-child(1) td.ant-table-cell:nth-child(1) span.ant-typography > strong:nth-child(1)').text
        new_vehicle_button = driver.find_element(By.XPATH, '//*[@id="root"]/section/section/section/div[1]/div[2]/button[1]')
        new_vehicle_button.click()
        i = random.randint(2, 49)
        api = ApiData(i)
        api.assign_values()
        truck_number = driver.find_element(By.XPATH, '//*[@id="unit_code"]')
        plate = driver.find_element(By.XPATH, '//*[@id="plate_number"]')
        brand = driver.find_element(By.XPATH, '//*[@id="vehicle_brand"]')
        model = driver.find_element(By.XPATH, '//*[@id="vehicle_model"]')
        year = driver.find_element(By.XPATH, '//*[@id="year"]')
        tank_capacity = driver.find_element(By.XPATH, '//*[@id="tank_capacity"]')
        drivers = driver.find_element(By.XPATH, '//*[@id="drivers"]')
        numero = id_generator()
        truck_number.send_keys(numero)
        plate.send_keys(api.plate)
        brand.click()
        i = truck_list_num()
        brand_selection = driver.find_element(By.XPATH, f'//*[@id="menu-"]/div[3]/ul/li[{i}]')
        data['brand'] = brand_selection.text
        brand_selection.click()
        model.click()
        list_of_models = driver.find_element(By.XPATH, '//*[@id="menu-"]/div[3]/ul')
        size_of_list_of_models = len(list_of_models.find_elements(By.TAG_NAME, 'li'))
        i = random_int_with_limit(size_of_list_of_models)
        model_selection = driver.find_element(By.XPATH, f'//*[@id="menu-"]/div[3]/ul/li[{i}]')
        data['model'] = model_selection.text
        model_selection.click()
        year.click()
        year_options = driver.find_element(By.XPATH, '//*[@id="menu-"]/div[3]/ul')
        number_of_year_option = len(year_options.find_elements(By.TAG_NAME, 'li'))
        y = random_int_with_limit(number_of_year_option)
        year_selection = driver.find_element(By.XPATH, f'//*[@id="menu-"]/div[3]/ul/li[{y}]')
        data['year'] = year_selection.text
        year_selection.click()
        tank_capacity.send_keys(capacity_num())
        drivers.click()
        drivers_list = driver.find_element(By.XPATH, '//*[@id="menu-"]/div[3]/ul')
        size_of_drivers_list = len(drivers_list.find_elements(By.TAG_NAME, 'li'))
        z = random_int_with_limit(size_of_drivers_list)
        driver_selection = driver.find_element(By.XPATH, f'//*[@id="menu-"]/div[3]/ul/li[{z}]')
        driver_selection.click()
        driver_selection.send_keys(Keys.TAB)
        save_button = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div[2]/div[3]/button[2]')
        save_button.click()
        time.sleep(5)
        new_list_number = driver.find_element(By.CSS_SELECTOR, 'section.ant-layout.ant-layout-has-sider section.ant-layout.site-layout section.ant-layout div.ant-table-wrapper.sc-egiyK.jfbgly:nth-child(2) div.ant-spin-nested-loading div.ant-spin-container div.ant-table div.ant-table-container div.ant-table-content tbody.ant-table-tbody:nth-child(3) tr.ant-table-row.ant-table-row-level-0:nth-child(1) td.ant-table-cell:nth-child(1) span.ant-typography > strong:nth-child(1)').text
        data['truc_number'] = numero
        data['plate'] = api.plate
    except NoSuchElementException as exc:
        print(exc)
    print(f'prueba finalizada correctamente con los datos: \n')
    for dato, valor in data.items():
        print(dato, ': ', valor)
    assert int(new_list_number) > int(list_number), f"Prueba fallida, con los datos: {str(data)}"

