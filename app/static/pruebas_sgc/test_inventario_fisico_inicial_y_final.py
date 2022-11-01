import time
import datetime
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from funciones.function import login, check_exists_by_xpath, convertir_fecha_24
from selenium.common.exceptions import NoSuchElementException


def test_inventario_fisico_inicial(driver, fecha_test, name='administrador', password='administrador'):
    datos = {}
    dia_inventario = fecha_test
    try:
        login(driver, name, password)
        time.sleep(2)
        boton_inventario = driver.find_element(By.XPATH, '//*[@id="grouptab_7"]')
        boton_inventario.click()
        sub_boton_inventario = driver.find_element(By.XPATH, '//*[@id="moduleTab_7_isies_inventario_basico"]')
        sub_boton_inventario.click()
        time.sleep(2)
        datos['Dia inventario'] = dia_inventario
        fecha = driver.find_element(By.XPATH, '//*[@id="inventario_basic"]')
        fecha.send_keys(dia_inventario)
        fecha.send_keys(Keys.ENTER)
        time.sleep(1)
        if check_exists_by_xpath(driver, '//*[@id="MassUpdate"]/table/tbody/tr[3]/td[1]/a'):
            documento = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody/tr[3]/td[1]/a')
            documento.click()
            time.sleep(1)
            fecha_inicial = driver.find_element(By.XPATH, '//*[@id="lienzo"]/table[2]/tbody/tr[1]/td[2]').text
            datos['Fecha inicial inventario'] = fecha_inicial
            fecha_inicial = convertir_fecha_24(fecha_inicial)
            fecha_inicial = fecha_inicial.split(' ')
            hora_inicial = fecha_inicial[1]
            hora_inicial = hora_inicial.replace('pm', '')
            hora_inicial = hora_inicial.replace('am', '')
            hora_inicial = hora_inicial.replace(':', '')
            time.sleep(1)
            inventario_fisico_inicial = driver.find_element(By.XPATH, '//*[@id="lienzo"]/table[3]/tbody/tr[2]/td[2]').text
            boton_almacen = driver.find_element(By.XPATH, '//*[@id="grouptab_6"]')
            boton_almacen.click()
            sub_boton_almacen = driver.find_element(By.XPATH, '//*[@id="moduleTab_6_isies_registros_medidor_almacen"]')
            sub_boton_almacen.click()
            fecha_registro = driver.find_element(By.XPATH, '//*[@id="fecha_lectura_basic"]')
            fecha_registro.send_keys(datos['Dia inventario'])
            fecha_registro.send_keys(Keys.ENTER)
            i = 3
            tabla = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody')
            listado = tabla.find_elements(By.TAG_NAME, 'tr')
            len_listado = len(listado)
            len_listado -= 3
            if check_exists_by_xpath(driver, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[12]'):
                fecha_registro = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[12]').text
                datos['Fecha de registro mas proxima'] = fecha_registro
                fecha_registro = convertir_fecha_24(fecha_registro)
                solo_fecha_registro = fecha_registro.split(' ')
                hora_registro = solo_fecha_registro[1]
                hora_registro = hora_registro.replace('am', '')
                hora_registro = hora_registro.replace('pm', '')
                hora_registro = hora_registro.replace(':', '')
                while int(hora_registro) > int(hora_inicial):
                    if i > len_listado:
                        flecha_next = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody/tr[1]/td/table/tbody/tr/td[2]/button[3]')
                        flecha_next.click()
                        time.sleep(3)
                        i = 3
                    fecha_registro = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[12]').text
                    fecha_registro = convertir_fecha_24(fecha_registro)
                    solo_fecha_registro = fecha_registro.split(' ')
                    hora_registro = solo_fecha_registro[1]
                    hora_registro = hora_registro.replace('pm', '')
                    hora_registro = hora_registro.replace('am', '')
                    hora_registro = hora_registro.replace(':', '')
                    if int(hora_registro) <= int(hora_inicial):
                        datos['Fecha de registro mas proxima'] = fecha_registro
                        break
                    else:
                        i += 1
                folio = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[1]').text
                volumen = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[7]').text
                compensado = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[10]').text
                datos['Folio de registro mas proximo'] = folio
                datos['Volumen Fisico Inicial'] = inventario_fisico_inicial
                inventario_fisico_inicial = inventario_fisico_inicial.replace('kg', '')
                inventario_fisico_inicial = inventario_fisico_inicial.replace('lt', '')
                inventario_fisico_inicial = inventario_fisico_inicial.replace(' ', '')
                inventario_fisico_inicial = inventario_fisico_inicial.replace(',', '')
                datos['Volumen Fisico Inicial'] = inventario_fisico_inicial
                volumen = volumen.replace(',', '')
                datos['Volumen Registro'] = float(volumen) + float(compensado)
                datos['Volumen Registro'] = round(datos['Volumen Registro'], 2)
                datos['Diferencia'] = float(datos['Volumen Fisico Inicial']) - float(datos['Volumen Registro'])

            else:
                print('Datos: \n')
                for dato, valor in datos.items():
                    print(dato, ': ', valor)
                    print('Test Inventario Fisico Inicial \n')
                    print('Test Inventario Fisico Inicial, Compara el inventario Fisico Inicial del ultimo inventario el registro mas proximo a la fecha de inicio del inventario \n'
                          'Muestra las diferencias si existieran.\n'
                          'Instancias: http://192.168.9.164/sgcweb')
                    print('\n\n')
                    print('Inventario correcto:  \n')
                assert False, 'El registro de esa fecha no existe'
        else:
            print('Datos: \n')
            for dato, valor in datos.items():
                print(dato, ': ', valor)
                print('Test Inventario Fisico Inicial \n')
                print('Test Inventario Fisico Inicial, Compara el inventario Fisico Inicial del ultimo inventario el registro de almacen mas proximo a la fecha de inicio del inventario \n'
                      'Muestra las diferencias si existieran.\n'
                      'Instancias: http://192.168.9.164/sgcweb')
                print('\n\n')
                print('Inventario correcto:  \n')
            assert False, 'El inventario diario no existe'
    except NoSuchElementException as e:
        print(str(e))

    if float(datos['Volumen Fisico Inicial']) - float(datos['Volumen Registro']) != 0:
        print('Diferencia entre los datos registrados en inventario vs el ultimo corte \n')
        for dato, valor in datos.items():
            print(dato, ': ', valor)
            print('Test Inventario Fisico Inicial \n')
            print('Test Inventario Fisico Inicial, Compara el inventario Fisico Inicial del ultimo inventario el registro de almacen mas proximo a la fecha de inicio del inventario \n'
                  'Muestra las diferencias si existieran.\n'
                  'Instancias: http://192.168.9.164/sgcweb')
            print('\n\n')
            print('Inventario correcto:  \n')
        assert False, f'Diferencia entre los datos registrados en inventario vs el ultimo corte, diferencia = {str(datos["Diferencia"])}'
    else:
        print('Test Inventario Fisico Inicial \n')
        print('Test Inventario Fisico Inicial, Compara el inventario Fisico Inicial del ultimo inventario el registro de almacen mas proximo a la fecha de inicio del inventario \n'
              'Muestra las diferencias si existieran.\n'
              'Instancias: http://192.168.9.164/sgcweb')
        print('\n\n')
        print('Inventario correcto:  \n')
        for dato, valor in datos.items():
            print(dato, ': ', valor)
        assert True, f'Diferencia entre los datos registrados en inventario vs el ultimo corte, diferencia = {str(datos["Diferencia"])}'


def test_inventario_fisico_final(driver, fecha_test):
    datos = {}
    dia_inventario = fecha_test
    try:
        time.sleep(2)
        boton_inventario = driver.find_element(By.XPATH, '//*[@id="grouptab_7"]')
        boton_inventario.click()
        sub_boton_inventario = driver.find_element(By.XPATH, '//*[@id="moduleTab_7_isies_inventario_basico"]')
        sub_boton_inventario.click()
        time.sleep(2)
        datos['Dia inventario'] = dia_inventario
        fecha = driver.find_element(By.XPATH, '//*[@id="inventario_basic"]')
        fecha.send_keys(datos['Dia inventario'])
        fecha.send_keys(Keys.ENTER)
        time.sleep(1)
        if check_exists_by_xpath(driver, '//*[@id="MassUpdate"]/table/tbody/tr[3]/td[1]/a'):
            documento = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody/tr[3]/td[1]/a')
            documento.click()
            time.sleep(1)
            fecha_final = driver.find_element(By.XPATH, '//*[@id="tr1"]/td[2]').text
            datos['Fecha Final del Inventario'] = fecha_final
            fecha_final = convertir_fecha_24(fecha_final)
            fecha_final = fecha_final.split(' ')
            hora_final = fecha_final[1]
            fecha_final = fecha_final[0]
            hora_final = hora_final.replace('pm', '')
            hora_final = hora_final.replace('am', '')
            hora_final = hora_final.replace(':', '')
            time.sleep(1)
            inventario_fisico_final = driver.find_element(By.XPATH, '//*[@id="lienzo"]/table[1]/tbody/tr[2]/td[1]').text
            boton_almacen = driver.find_element(By.XPATH, '//*[@id="grouptab_6"]')
            boton_almacen.click()
            sub_boton_almacen = driver.find_element(By.XPATH, '//*[@id="moduleTab_6_isies_registros_medidor_almacen"]')
            sub_boton_almacen.click()
            fecha_registro = driver.find_element(By.XPATH, '//*[@id="fecha_lectura_basic"]')
            fecha_registro.send_keys(fecha_final)
            fecha_registro.send_keys(Keys.ENTER)
            i = 3
            tabla = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody')
            listado = tabla.find_elements(By.TAG_NAME, 'tr')
            len_listado = len(listado)
            len_listado -= 3
            if check_exists_by_xpath(driver, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[12]'):
                fecha_registro = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[12]').text
                fecha_registro = convertir_fecha_24(fecha_registro)
                datos['Fecha de registro mas proxima'] = fecha_registro
                solo_fecha_registro = fecha_registro.split(' ')
                hora_registro = solo_fecha_registro[1]
                hora_registro = hora_registro.replace('pm', '')
                hora_registro = hora_registro.replace('am', '')
                hora_registro = hora_registro.replace(':', '')
                while int(hora_registro) > int(hora_final):
                    if i > len_listado:
                        flecha_next = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody/tr[1]/td/table/tbody/tr/td[2]/button[3]')
                        flecha_next.click()
                        time.sleep(3)
                        i = 3
                    fecha_registro = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[12]').text
                    fecha_registro = convertir_fecha_24(fecha_registro)
                    solo_fecha_registro = fecha_registro.split(' ')
                    hora_registro = solo_fecha_registro[1]
                    hora_registro = hora_registro.replace('pm', '')
                    hora_registro = hora_registro.replace('am', '')
                    hora_registro = hora_registro.replace(':', '')
                    if int(hora_registro) <= int(hora_final):
                        datos['Fecha de registro mas proxima'] = fecha_registro
                        break
                    else:
                        i += 1
                folio = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[1]').text
                volumen = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[7]').text
                compensado = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[10]').text
                inventario_fisico_final = inventario_fisico_final.replace('kg', '')
                inventario_fisico_final = inventario_fisico_final.replace('lt', '')
                inventario_fisico_final = inventario_fisico_final.replace(' ', '')
                inventario_fisico_final = inventario_fisico_final.replace(',', '')
                datos['Folio de registro mas proximo'] = folio
                datos['Volumen Fisico Final Inventario'] = inventario_fisico_final
                volumen = volumen.replace(',', '')
                datos['Volumen Fisico Final Registro'] = float(volumen) + float(compensado)
                datos['Volumen Fisico Final Registro'] = round(datos['Volumen Fisico Final Registro'], 2)
                datos['Diferencia'] = float(datos['Volumen Fisico Final Inventario']) - float(datos['Volumen Fisico Final Registro'])
                datos['Diferencia'] = abs(float(datos['Diferencia']))
                datos['Diferencia'] = round(float(datos['Diferencia']), 2)
            else:
                print('Test Inventario Fisico Final \n')
                print('Test Inventario Fisico Final, Compara el inventario Fisico FInal del ultimo inventario el registro mas proximo de almacen a la fecha final del inventario \n'
                      'Muestra las diferencias si existieran.\n'
                      'Instancias: http://192.168.9.164/sgcweb')
                print('\n\n')
                print('Datos: \n')
                for dato, valor in datos.items():
                    print(dato, ': ', valor)
                assert False, 'El registro de esa fecha no existe'
        else:
            print('Test Inventario Fisico Final \n')
            print('Test Inventario Fisico Final, Compara el inventario Fisico FInal del ultimo inventario el registro mas proximo de almacen a la fecha final del inventario \n'
                  'Muestra las diferencias si existieran.\n'
                  'Instancias: http://192.168.9.164/sgcweb')
            print('\n\n')
            print('Datos: \n')
            for dato, valor in datos.items():
                print(dato, ': ', valor)
            assert False, 'El inventario diario no existe'
    except NoSuchElementException as e:
        print(str(e))
        print('Datos: \n')
        for dato, valor in datos.items():
            print(dato, ': ', valor)
        assert False, 'El registro de esa fecha no existe'

    if float(datos['Volumen Fisico Final Inventario']) - float(datos['Volumen Fisico Final Registro']) != 0:
        print('Diferencia entre los datos registrados en inventario vs el ultimo corte \n')
        for dato, valor in datos.items():
            print(dato, ': ', valor)
        assert False, f'Diferencia entre los datos registrados en inventario vs el ultimo corte, diferencia = {str(datos["Diferencia"])}'
    else:
        print('Test Inventario Fisico Final \n')
        print('Test Inventario Fisico Final, Compara el inventario Fisico FInal del ultimo inventario el registro mas proximo de almacen a la fecha final del inventario \n'
              'Muestra las diferencias si existieran.\n'
              'Instancias: http://192.168.9.164/sgcweb')
        print('\n\n')
        print('Inventario correcto:  \n')
        for dato, valor in datos.items():
            print(dato, ': ', valor)
        assert True, f'Diferencia entre los datos registrados en inventario vs el ultimo corte, diferencia = {str(datos["Diferencia"])}'
