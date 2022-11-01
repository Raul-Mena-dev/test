import time
import datetime
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from funciones.function import login
from selenium.common.exceptions import NoSuchElementException


def test_inventario_nuevo(driver, name='administrador', password='administrador'):
    datos = {}
    try:
        login(driver, name, password)
        time.sleep(2)
        boton_inventario = driver.find_element(By.XPATH, '//*[@id="grouptab_7"]')
        boton_inventario.click()
        sub_boton_inventario = driver.find_element(By.XPATH, '//*[@id="moduleTab_7_isies_inventario_basico"]')
        sub_boton_inventario.click()
        time.sleep(2)
        hora = datetime.datetime.now()
        if hora.hour >= 13:
            x = datetime.date.today()
            x = x - datetime.timedelta(days=1)
        else:
            x = datetime.date.today()
            x = x - datetime.timedelta(days=2)
        x = x.strftime("%Y-%m-%d")
        datos['Fecha a buscar'] = x
        fecha_inventario = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody/tr[3]/td[1]/a').text
        datos['Fecha Ultimo inventario'] = fecha_inventario
    except NoSuchElementException as exc:
        print(str(exc))

    print('Datos: \n')
    for dato, valor in datos.items():
        print(dato, ': ', valor)
    assert datos['Fecha a buscar'] == datos['Fecha Ultimo inventario'], f'No existe el inventario del dia:{str(datos["Fecha a buscar"])}'

