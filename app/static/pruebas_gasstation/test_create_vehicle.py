import time
import random
import pytest
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from funciones.function import login, logout, random_int_with_limit, capacity_num, truck_list_num, id_generator
from funciones.api_data_mock.api import ApiData
from selenium.common.exceptions import NoSuchElementException

r = random.randint(1, 999)
api = ApiData(r)
api.assign_values()


@pytest.mark.parametrize('numero, placas', [(id_generator(), api.plate),
                                            ('¿?¡])(=', api.plate),
                                            (id_generator(), '[]{}{{}}+{]'),
                                            ('==)?¡}{', '=(/9=?[')
                                            ])
def test_create_vehicle(driver2, numero, placas, name='multiplestation@yopmail.com', password='QChnra3FVQ'):
    data = {}
    try:
        login(driver2, name, password)
        time.sleep(1)
        vehicles = driver2.find_element(By.XPATH, '//*[@id="sider"]/div/ul/li[6]/span/a')
        vehicles.click()
        time.sleep(3)
        list_num = driver2.find_element(By.XPATH, '//*[@id="root"]/section/section/section/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]/span').text
        new_vehicle_button = driver2.find_element(By.XPATH, '//*[@id="root"]/section/section/section/div[1]/div[2]/button[1]')
        new_vehicle_button.click()
        time.sleep(2)
        truck_number = driver2.find_element(By.XPATH, '//*[@id="unit_code"]')
        plate = driver2.find_element(By.XPATH, '//*[@id="plate_number"]')
        brand = driver2.find_element(By.XPATH, '//*[@id="vehicle_brand"]')
        model = driver2.find_element(By.XPATH, '//*[@id="vehicle_model"]')
        year = driver2.find_element(By.XPATH, '//*[@id="year"]')
        tank_capacity = driver2.find_element(By.XPATH, '//*[@id="tank_capacity"]')
        drivers = driver2.find_element(By.XPATH, '//*[@id="drivers"]')
        truck_number.send_keys(numero)
        time.sleep(1)
        plate.send_keys(placas)
        time.sleep(1)
        brand.click()
        time.sleep(1)
        i = truck_list_num()
        brand_selection = driver2.find_element(By.XPATH, f'//*[@id="menu-"]/div[3]/ul/li[{i}]')
        data['brand'] = brand_selection.text
        brand_selection.click()
        model.click()
        time.sleep(1)
        list_of_models = driver2.find_element(By.XPATH, '//*[@id="menu-"]/div[3]/ul')
        size_of_list_of_models = len(list_of_models.find_elements(By.TAG_NAME, 'li'))
        i = random_int_with_limit(size_of_list_of_models)
        model_selection = driver2.find_element(By.XPATH, f'//*[@id="menu-"]/div[3]/ul/li[{i}]')
        data['model'] = model_selection.text
        model_selection.click()
        time.sleep(1)
        year.click()
        time.sleep(1)
        year_options = driver2.find_element(By.XPATH, '//*[@id="menu-"]/div[3]/ul')
        number_of_year_option = len(year_options.find_elements(By.TAG_NAME, 'li'))
        y = random_int_with_limit(number_of_year_option)
        year_selection = driver2.find_element(By.XPATH, f'//*[@id="menu-"]/div[3]/ul/li[{y}]')
        year_selection.click()
        time.sleep(1)
        tank_capacity.send_keys(capacity_num())
        time.sleep(1)
        drivers.click()
        time.sleep(1)
        drivers_list = driver2.find_element(By.XPATH, '//*[@id="menu-"]/div[3]/ul')
        size_of_drivers_list = len(drivers_list.find_elements(By.TAG_NAME, 'li'))
        z = random_int_with_limit(size_of_drivers_list)
        driver_selection = driver2.find_element(By.XPATH, f'//*[@id="menu-"]/div[3]/ul/li[{z}]')
        data['driver'] = driver_selection.text
        driver_selection.click()
        driver_selection.send_keys(Keys.TAB)
        save_button = driver2.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div[2]/div[3]/button[2]')
        save_button.click()
        time.sleep(3)
        data['truc_number'] = numero
        data['plate'] = placas
        new_list_num = driver2.find_element(By.XPATH, '//*[@id="root"]/section/section/section/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]/span').text
        logout(driver2)
    except NoSuchElementException as exc:
        print(exc)
        print(f'No se pudo añadir el vehiculo, datos: {str(data)}')
        assert False, f'No se pudo añadir el vehiculo, datos: {str(data)}'
    new_numero = numero
    new_placas = placas
    if (any(not c.isalnum() for c in new_numero) or any(not c.isalnum() for c in new_placas)) and new_list_num > list_num:
        print(f'Permite el registro del vehiculo con caracteres especiales en el numero de camion/placas, {str(data)}')
        assert False, f'Permite el registro del vehiculo con caracteres especiales en el numero de camion/placas, {str(data)}'
    elif (any(not c.isalnum() for c in new_numero) or any(not c.isalnum() for c in new_placas)) and new_list_num == list_num:
        print(f'No permite el registro del vehiculo con caracteres especiales en el numero de camion/placas, {str(data)}')
        assert True, f'No permite el registro del vehiculo con caracteres especiales en el numero de camion/placas, {str(data)}'
    else:
        print(f'Vehiculo agregado :D, {str(data)}')
        assert True, f'Vehiculo no agregado, {str(data)}'
