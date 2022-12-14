import time
import datetime
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from funciones.function import login, logout, check_exists_by_xpath, convertir_fecha_24
from selenium.common.exceptions import NoSuchElementException


def test_entradas(driver, fecha_test, name='administrador', password='administrador'):
    datos_entradas = {}
    dia_inventario = fecha_test
    try:
        login(driver, name, password)
        time.sleep(2)
        boton_inventario = driver.find_element(By.XPATH, '//*[@id="grouptab_7"]')
        boton_inventario.click()
        sub_boton_inventario = driver.find_element(By.XPATH, '//*[@id="moduleTab_7_isies_inventario_basico"]')
        sub_boton_inventario.click()
        time.sleep(2)
        datos_entradas['Dia inventario'] = dia_inventario
        fecha = driver.find_element(By.XPATH, '//*[@id="inventario_basic"]')
        fecha.send_keys(dia_inventario)
        fecha.send_keys(Keys.ENTER)
        time.sleep(1)
        if check_exists_by_xpath(driver, '//*[@id="MassUpdate"]/table/tbody/tr[3]/td[1]/a'):
            documento = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody/tr[3]/td[1]/a')
            documento.click()
            time.sleep(1)
            fecha_inicial = driver.find_element(By.XPATH, '//*[@id="lienzo"]/table[2]/tbody/tr[1]/td[2]').text
            datos_entradas['Fecha inicial inventario'] = fecha_inicial
            fecha_final = driver.find_element(By.XPATH, '//*[@id="tr1"]/td[2]').text
            datos_entradas['Fecha Final del Inventario'] = fecha_final
            time.sleep(1)
            entradas = driver.find_element(By.XPATH, '/html[1]/body[1]/div[4]/div[3]/table[1]/tbody[1]/tr[1]/td[1]/div[1]/table[3]/tbody[1]/tr[3]/td[2]').text
            entradas = entradas.replace(' ', '', 10)
            entradas = entradas.split(']')
            entradas_kg = entradas[1]
            entradas_kg = entradas_kg.replace(',', '')
            entradas_kg = entradas_kg.replace('lt', '')
            entradas_kg = entradas_kg.replace('kg', '')
            datos_entradas['entradas_kg'] = entradas_kg
            cantidad_de_entradas = entradas[0]
            cantidad_de_entradas = cantidad_de_entradas.replace('[', '')
            cantidad_de_entradas = cantidad_de_entradas.replace(']', '')
            datos_entradas['cantidad_de_entradas'] = cantidad_de_entradas
            boton_descarga = driver.find_element(By.XPATH, '/html[1]/body[1]/div[3]/div[10]/ul[1]/li[6]/span[2]/a[1]')
            boton_descarga.click()
            sub_boton_descarga = driver.find_element(By.XPATH, '/html[1]/body[1]/div[3]/div[12]/span[5]/ul[1]/li[1]/a[1]')
            sub_boton_descarga.click()
            boton_descargas_documento = driver.find_element(By.XPATH, '/html[1]/body[1]/div[4]/div[2]/div[1]/ul[1]/li[2]/a[1]')
            boton_descargas_documento.click()
            rango1 = convertir_fecha_24(datos_entradas['Fecha inicial inventario'])
            rango2 = convertir_fecha_24(datos_entradas['Fecha Final del Inventario'])
            fecha1 = driver.find_element(By.XPATH, '/html[1]/body[1]/div[4]/div[3]/table[1]/tbody[1]/tr[1]/td[1]/form[1]/div[1]/table[1]/tbody[1]/tr[1]/td[2]/input[1]')
            fecha2 = driver.find_element(By.XPATH, '/html[1]/body[1]/div[4]/div[3]/table[1]/tbody[1]/tr[1]/td[1]/form[1]/div[1]/table[1]/tbody[1]/tr[1]/td[2]/input[2]')
            time.sleep(2)
            fecha1.clear()
            fecha2.clear()
            fecha1.send_keys(rango1)
            fecha2.send_keys(rango2)
            fecha2.send_keys(Keys.ENTER)
            time.sleep(1)
            unidades_de_medida = driver.find_element(By.XPATH, '/html[1]/body[1]/div[4]/div[3]/table[1]/tbody[1]/tr[1]/td[1]/form[1]/div[1]/table[1]/tbody[1]/tr[6]/td[2]/input[1]')
            unidades_de_medida.click()
            time.sleep(3)
            if check_exists_by_xpath(driver, '/html[1]/body[1]/div[4]/div[3]/table[1]/tbody[1]/tr[1]/td[1]/table[4]/tbody[1]/tr[3]/td[2]'):
                total = driver.find_element(By.XPATH, '/html[1]/body[1]/div[4]/div[3]/table[1]/tbody[1]/tr[1]/td[1]/table[4]/tbody[1]/tr[3]/td[2]').text
                datos_entradas['Total de cargas'] = total
                compensado = driver.find_element(By.XPATH, '//*[@id="content"]/table/tbody/tr/td/table[4]/tbody/tr[3]/td[13]').text
                compensado = compensado.replace(',', '')
                compensado = compensado.replace('kg', '')
                compensado = compensado.replace('lt', '')
                compensado = compensado.replace(' ', '', 10)
                datos_entradas['compensado'] = compensado

                if datos_entradas['compensado'] != datos_entradas['entradas_kg'] and datos_entradas['Total de cargas'] != datos_entradas['cantidad_de_entradas']:
                    print('Test Entradas\n')
                    print('Test Entradas, Compara los datos de Entradas/compras del ultimo inventario contra los datos de planta,\n'
                          ' en descargas por documento., muestra diferencias si existen\n'
                          'Instancias: httpdia_inventario = dia_inventario.strftime("%Y-%m-%d")://192.168.9.164/sgcweb')
                    print('\n\n')
                    for dato, valor in datos_entradas.items():
                        print(dato, ': ', valor)
                    assert False, 'Tanto el compensado como el total no coincide'
                elif datos_entradas['compensado'] == datos_entradas['entradas_kg'] and datos_entradas['Total de cargas'] != datos_entradas['cantidad_de_entradas']:
                    print('Test Entradas\n')
                    print('Test Entradas, Compara los datos de Entradas/compras del ultimo inventario contra los datos de planta,\n'
                          ' en descargas por documento., muestra diferencias si existen\n'
                          'Instancias: http://192.168.9.164/sgcweb')
                    print('\n\n')
                    for dato, valor in datos_entradas.items():
                        print(dato, ': ', valor)
                    assert False, 'La cantidad de entradas no es la misma'
                elif datos_entradas['compensado'] != datos_entradas['entradas_kg'] and datos_entradas['Total de cargas'] == datos_entradas['cantidad_de_entradas']:
                    print('Test Entradas\n')
                    print('Test Entradas, Compara los datos de Entradas/compras del ultimo inventario contra los datos de planta,\n'
                          ' en descargas por documento., muestra diferencias si existen\n'
                          'Instancias: http://192.168.9.164/sgcweb')
                    print('\n\n')
                    for dato, valor in datos_entradas.items():
                        print(dato, ': ', valor)
                    assert False, 'La cantidad de compensado no es la misma'
                elif datos_entradas['compensado'] == datos_entradas['entradas_kg'] and datos_entradas['Total de cargas'] == datos_entradas['cantidad_de_entradas']:
                    print('Test Entradas\n')
                    print('Test Entradas, Compara los datos de Entradas/compras del ultimo inventario contra los datos de planta,\n'
                          ' en descargas por documento., muestra diferencias si existen\n'
                          'Instancias: http://192.168.9.164/sgcweb')
                    print('\n\n')
                    print('Prueba exitosa ambos valores son iguales: \n')
                    for dato, valor in datos_entradas.items():
                        print(dato, ': ', valor)
                    assert True, 'Prueba exitosa ambos valores son iguales'
            else:
                print('Test Entradas\n')
                print('Test Entradas, Compara los datos de Entradas/compras del ultimo inventario contra los datos de planta,\n'
                      ' en descargas por documento., muestra diferencias si existen\n'
                      'Instancias: http://192.168.9.164/sgcweb')
                print('\n\n')
                print('Sin compras registradas: \n')
                for dato, valor in datos_entradas.items():
                    print(dato, ': ', valor)
                assert True, 'No hay compras registradas'

        else:
            print('Test Entradas\n')
            print('Test Entradas, Compara los datos de Entradas/compras del ultimo inventario contra los datos de planta,\n'
                  ' en descargas por documento., muestra diferencias si existen\n'
                  'Instancias: http://192.168.9.164/sgcweb')
            print('\n\n')
            print('Datos: \n')
            for dato, valor in datos_entradas.items():
                print(dato, ': ', valor)
            assert False, 'El inventario diario no existe'
    except NoSuchElementException as exc:
        print(str(exc))


