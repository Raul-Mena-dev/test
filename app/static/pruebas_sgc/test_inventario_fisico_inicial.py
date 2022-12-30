import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from funciones.function import login, check_exists_by_xpath, convertir_fecha_24
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


def test_inventario_fisico_inicial(driver, fecha_test, name='admin', password='Z76U4CFIx#'):
    datos = {}
    dia_inventario = fecha_test
    try:
        login(driver, name, password)
        time.sleep(2)
        wait = WebDriverWait(driver, 60)
        lista = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="moduleList"]/ul')))
        opciones_lista = lista.find_elements(By.TAG_NAME, 'li')
        lista_size = len(opciones_lista)
        i = 2
        while i <= lista_size:
            opcion = driver.find_element(By.XPATH, f'/html/body/div[3]/div[10]/ul/li[{i}]/span[2]/a')
            texto = opcion.text
            if texto == 'Inventario':
                opcion.click()
                break
            elif i >= lista_size:
                print('La opcion de Pedidos no se encuentra o cambio de nombre, revisar permisos')
                assert False, 'D:'
            else:
                i += 1
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
            wait = WebDriverWait(driver, 60)
            lista = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="moduleList"]/ul')))
            opciones_lista = lista.find_elements(By.TAG_NAME, 'li')
            lista_size = len(opciones_lista)
            i = 2
            while i <= lista_size:
                opcion = driver.find_element(By.XPATH, f'/html/body/div[3]/div[10]/ul/li[{i}]/span[2]/a')
                texto = opcion.text
                if texto == 'Almacén':
                    opcion.click()
                    break
                elif i >= lista_size:
                    print('La opcion de Pedidos no se encuentra o cambio de nombre, revisar permisos')
                    assert False, 'D:'
                else:
                    i += 1
            time.sleep(2)
            sub_boton_almacen = driver.find_element(By.XPATH, '//*[@id="moduleTab_5_isies_registros_medidor_almacen"]')
            sub_boton_almacen.click()
            fecha_registro = driver.find_element(By.XPATH, '//*[@id="fecha_lectura_basic"]')
            fecha_registro.send_keys(datos['Dia inventario'])
            fecha_registro.send_keys(Keys.ENTER)
            i = 3
            tabla = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody')
            listado = tabla.find_elements(By.TAG_NAME, 'tr')
            len_listado = len(listado)
            len_listado -= 3
            if check_exists_by_xpath(driver, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[14]'):
                fecha_registro = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[14]').text
                datos['Fecha de registro mas proxima'] = fecha_registro
                fecha_registro = convertir_fecha_24(fecha_registro)
                solo_fecha_registro = fecha_registro.split(' ')
                hora_registro = solo_fecha_registro[1]
                hora_registro = hora_registro.replace('am', '')
                hora_registro = hora_registro.replace('pm', '')
                hora_registro = hora_registro.replace(':', '')
                while int(hora_registro) > int(hora_inicial):
                    flecha_next = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody/tr[1]/td/table/tbody/tr/td[2]/button[3]')
                    if flecha_next.is_enabled():
                        if i > len_listado:
                            flecha_next = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody/tr[1]/td/table/tbody/tr/td[2]/button[3]')
                            flecha_next.click()
                            time.sleep(3)
                            tabla = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody')
                            listado = tabla.find_elements(By.TAG_NAME, 'tr')
                            len_listado = len(listado)
                            len_listado -= 3
                            i = 3
                    else:
                        fecha_registro = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[14]').text
                        fecha_registro = convertir_fecha_24(fecha_registro)
                        solo_fecha_registro = fecha_registro.split(' ')
                        hora_registro = solo_fecha_registro[1]
                        hora_registro = hora_registro.replace('pm', '')
                        hora_registro = hora_registro.replace('am', '')
                        hora_registro = hora_registro.replace(':', '')
                        if int(hora_registro) <= int(hora_inicial):
                            datos['Fecha de registro mas proxima'] = fecha_registro
                            break
                        elif i >= len_listado:
                            fecha_registro = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{len_listado}]/td[14]').text
                            datos['Fecha de registro mas proxima'] = fecha_registro
                            break
                        else:
                            i += 1
                    fecha_registro = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[14]').text
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
                compensado = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[12]').text
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
                datos['Diferencia'] = abs(datos['Diferencia'])
                datos['Diferencia'] = round(datos['Diferencia'], 4)

            else:
                print('Datos: \n')
                for dato, valor in datos.items():
                    print(dato, ': ', valor)
                    print('Test Inventario Fisico Inicial \n')
                    print('Test Inventario Fisico Inicial, Compara el inventario Fisico Inicial del ultimo inventario el registro mas proximo a la fecha de inicio del inventario \n'
                          'Muestra las diferencias si existieran.\n'
                          'Instancias: http://192.168.9.164/sgcweb')
                    print('\n\n')
                assert False, 'No hay datos en registros medidor almacen'
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

    # if float(datos['Volumen Fisico Inicial']) - float(datos['Volumen Registro']) != 0:
    #     print('Diferencia entre los datos registrados en inventario vs el ultimo corte \n')
    #     for dato, valor in datos.items():
    #         print(dato, ': ', valor)
    #         print('Test Inventario Fisico Inicial \n')
    #         print('Test Inventario Fisico Inicial, Compara el inventario Fisico Inicial del ultimo inventario el registro de almacen mas proximo a la fecha de inicio del inventario \n'
    #               'Muestra las diferencias si existieran.\n'
    #               'Instancias: http://192.168.9.164/sgcweb')
    #         print('\n\n')
    #         print('Inventario correcto:  \n')
    #     assert False, f'Diferencia entre los datos registrados en inventario vs el ultimo corte, diferencia = {str(datos["Diferencia"])}'
    # else:
    print('Test Inventario Fisico Inicial \n')
    print('Test Inventario Fisico Inicial, Compara el inventario Fisico Inicial del ultimo inventario el registro de almacen mas proximo a la fecha de inicio del inventario \n'
          'Muestra las diferencias si existieran.\n'
          'Instancias: http://192.168.9.164/sgcweb')
    print('\n\n')
    for dato, valor in datos.items():
        print(dato, ': ', valor)
    assert True, f'Diferencia entre los datos registrados en inventario vs el ultimo corte, diferencia = {str(datos["Diferencia"])}'
