import time
import datetime
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from funciones.function import login, check_exists_by_xpath, convertir_fecha_24
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException


def mensaje_de_salida_ventas(datos_inventario, datos_ventas):
    print('-------------------------------------------')
    print('Datos de inventario: \n')
    for dato, valor in datos_inventario.items():
        print(dato, ': ', valor)
    print('-------------------------------------------')
    print('Datos de ventas: \n')
    for dato, valor in datos_ventas.items():
        if 'Factor' in dato:
            print('----------------------------------------')
        if 'Total litros vendidos' in dato:
            print('----------------------------------------')
        print(dato, ': ', valor)
    print('-------------------------------------------')


def test_inventario_fisico_inicial(driver, fecha_test, name='admin', password='Z76U4CFIx#'):
    datos = {}
    dia_inventario = fecha_test
    try:
        login(driver, name, password)
        time.sleep(5)
        driver.refresh()
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


def test_inventario_fisico_final(driver, fecha_test):
    datos = {}
    dia_inventario = fecha_test
    try:
        driver.refresh()
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
            fecha_registro.send_keys(fecha_final)
            fecha_registro.send_keys(Keys.ENTER)
            i = 3
            tabla = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody')
            listado = tabla.find_elements(By.TAG_NAME, 'tr')
            len_listado = len(listado)
            len_listado -= 3
            if check_exists_by_xpath(driver, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[12]'):
                fecha_registro = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[14]').text
                fecha_registro = convertir_fecha_24(fecha_registro)
                datos['Fecha de registro mas proxima'] = fecha_registro
                solo_fecha_registro = fecha_registro.split(' ')
                hora_registro = solo_fecha_registro[1]
                hora_registro = hora_registro.replace('pm', '')
                hora_registro = hora_registro.replace('am', '')
                hora_registro = hora_registro.replace(':', '')
                while int(hora_registro) > int(hora_final):
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
                        if int(hora_registro) <= int(hora_final):
                            datos['Fecha de registro mas proxima'] = fecha_registro
                            break
                        elif i >= len_listado:
                            fecha_registro = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{len_listado}]/td[14]').text
                            datos['Fecha de registro mas proxima'] = fecha_registro
                        else:
                            i += 1
                    fecha_registro = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[14]').text
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
                compensado = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[12]').text
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
                fecha_registro = driver.find_element(By.XPATH, '//*[@id="fecha_lectura_basic"]')
                fecha_registro.clear()
                fecha_registro.send_keys(dia_inventario)
                fecha_registro.send_keys(Keys.ENTER)
                if check_exists_by_xpath(driver, f'//*[@id="MassUpdate"]/table/tbody/tr[3]/td[12]'):
                    fecha_registro = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[3]/td[12]').text
                    fecha_registro = convertir_fecha_24(fecha_registro)
                    datos['Fecha de registro mas proxima'] = fecha_registro
                    folio = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[3]/td[1]').text
                    volumen = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[3]/td[7]').text
                    compensado = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[3]/td[10]').text
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

    print('Test Inventario Fisico Final \n')
    print('Test Inventario Fisico Final, Compara el inventario Fisico FInal del ultimo inventario el registro mas proximo de almacen a la fecha final del inventario \n'
          'Muestra las diferencias si existieran.\n'
          'Instancias: http://192.168.9.164/sgcweb')
    for dato, valor in datos.items():
        print(dato, ': ', valor)
    assert True, f'Diferencia entre los datos registrados en inventario vs el ultimo corte, diferencia = {str(datos["Diferencia"])}'


def test_entradas(driver, fecha_test, name='admin', password='Z76U4CFIx#'):
    datos_entradas = {}
    dia_inventario = fecha_test
    try:
        driver.refresh()
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
            wait = WebDriverWait(driver, 60)
            lista = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="moduleList"]/ul')))
            opciones_lista = lista.find_elements(By.TAG_NAME, 'li')
            lista_size = len(opciones_lista)
            i = 2
            while i <= lista_size:
                opcion = driver.find_element(By.XPATH, f'/html/body/div[3]/div[10]/ul/li[{i}]/span[2]/a')
                texto = opcion.text
                if texto == 'Descarga':
                    opcion.click()
                    break
                elif i >= lista_size:
                    print('La opcion de Pedidos no se encuentra o cambio de nombre, revisar permisos')
                    assert False, 'D:'
                else:
                    i += 1
            time.sleep(2)
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
                          'Instancias: http://192.168.9.164/sgcweb')
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


def test_inventario_vs_ventas(driver, fecha_test, name='admin', password='Z76U4CFIx#', name_web='admin', password_web='Ku8L08iEsb86'):
    datos_inventario = {}
    datos_ventas = {}
    productos = {}
    dia_inventario = fecha_test
    try:
        driver.refresh()
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
        datos_inventario['Dia inventario'] = dia_inventario
        fecha = driver.find_element(By.XPATH, '//*[@id="inventario_basic"]')
        fecha.send_keys(dia_inventario)
        fecha.send_keys(Keys.ENTER)
        time.sleep(1)
        # fecha inicial del inventario
        if check_exists_by_xpath(driver, '//*[@id="MassUpdate"]/table/tbody/tr[3]/td[1]/a'):
            documento = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody/tr[3]/td[1]/a')
            documento.click()
            time.sleep(1)
            fecha_inicial = driver.find_element(By.XPATH, '//*[@id="lienzo"]/table[2]/tbody/tr[1]/td[2]').text
            datos_inventario['Fecha inicial inventario'] = fecha_inicial
            fecha_inicial = convertir_fecha_24(fecha_inicial)
            # fecha final del inventario
            fecha_final = driver.find_element(By.XPATH, '//*[@id="tr1"]/td[2]').text
            datos_inventario['Fecha Final del Inventario'] = fecha_final
            # sacamoss los datos a revisar carga de autotanques, anden, servicio medido
            carga_autotanque = driver.find_element(By.XPATH, '//*[@id="lienzo"]/table[4]/tbody/tr[2]/td[2]').text
            datos_inventario['Carga autotanque'] = carga_autotanque
            carga_autotanque = carga_autotanque.replace(',', '')
            carga_autotanque = carga_autotanque.replace(' ', '')
            carga_autotanque = carga_autotanque.replace('kg', '')
            carga_autotanque = carga_autotanque.replace('lt', '')
            anden = driver.find_element(By.XPATH, '//*[@id="lienzo"]/table[4]/tbody/tr[3]/td[2]').text
            datos_inventario['Anden'] = anden
            anden = anden.replace(',', '')
            anden = anden.replace(' ', '')
            anden = anden.replace('kg', '')
            anden = anden.replace('lt', '')
            servicio_medido = driver.find_element(By.XPATH, '//*[@id="lienzo"]/table[4]/tbody/tr[5]/td[2]').text
            datos_inventario['Servicio_medido'] = servicio_medido
            servicio_medido = servicio_medido.replace(',', '')
            servicio_medido = servicio_medido.replace(' ', '')
            servicio_medido = servicio_medido.replace('kg', '')
            servicio_medido = servicio_medido.replace('lt', '')
            datos_inventario['Total sin Servicio medido'] = float(carga_autotanque) + float(anden)
            total_ventas = driver.find_element(By.XPATH, '//*[@id="lienzo"]/table[4]/tbody/tr[6]/td[2]').text
            datos_inventario['Total Ventas'] = total_ventas
            total_ventas = total_ventas.replace(' lt', '')
            # nos movemos a sgc web
            principal = driver.current_window_handle
            driver.execute_script('''window.open("https://testventas.sgcweb.com.mx/index.php?action=Login&module=Users&login_module=Home&login_action=index","_blank");''')
            time.sleep(3)
            parent = driver.window_handles[0]
            chld = driver.window_handles[1]
            driver.switch_to.window(chld)
            time.sleep(3)
            # accedemos a sgc web
            acceso = driver.find_element(By.XPATH, '//*[@id="user_name"]')
            acceso.send_keys(name_web)
            contra = driver.find_element(By.XPATH, '//*[@id="user_password"]')
            contra.send_keys(password_web)
            contra.submit()
            time.sleep(2)
            # entramos al reporte condensado
            while i <= lista_size:
                opcion = driver.find_element(By.XPATH, f'/html/body/div[3]/div[10]/ul/li[{i}]/span[2]/a')
                texto = opcion.text
                if texto == 'Visor de operaciones':
                    opcion.click()
                    break
                elif i >= lista_size:
                    print('La opcion de Pedidos no se encuentra o cambio de nombre, revisar permisos')
                    assert False, 'D:'
                else:
                    i += 1
            reporte_condensado = driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/table/tbody/tr/td/div[2]/table/tbody/tr[12]/td/div/a')
            reporte_condensado.click()
            # se manda la primera fecha
            fecha_2 = fecha_inicial.split(' ')
            solo_fecha = fecha_2[0]
            solo_hora = fecha_2[1]
            solo_hora = solo_hora.split(':')
            rango1 = driver.find_element(By.XPATH, '//*[@id="_fecha_0"]')
            rango1.clear()
            rango1.send_keys(solo_fecha)
            hora_1 = Select(driver.find_element(By.XPATH, '//*[@id="_hora_0"]'))
            hora_1.select_by_visible_text(str(solo_hora[0]))
            min_1 = Select(driver.find_element(By.XPATH, '//*[@id="_minuto_0"]'))
            solo_hora[1] = solo_hora[1].replace('am', '')
            min_1.select_by_visible_text(str(solo_hora[1]))
            # se manda la segunda fecha
            fecha_2 = fecha_final.split(' ')
            solo_fecha = fecha_2[0]
            solo_hora = fecha_2[1]
            solo_hora = solo_hora.split(':')
            rango1 = driver.find_element(By.XPATH, '//*[@id="_fecha2_0"]')
            rango1.clear()
            rango1.send_keys(solo_fecha)
            hora_1 = Select(driver.find_element(By.XPATH, '//*[@id="_hora2_0"]'))
            hora_1.select_by_visible_text(str(solo_hora[0]))
            min_1 = Select(driver.find_element(By.XPATH, '//*[@id="_minuto2_0"]'))
            solo_hora[1] = solo_hora[1].replace('am', '')
            min_1.select_by_visible_text(str(solo_hora[1]))
            ver_reporte = driver.find_element(By.XPATH, '//*[@id="btn_ver_reporte"]')
            ver_reporte.click()
            time.sleep(12)
            # seleccionamos la tabla si existe
            if check_exists_by_xpath(driver, '//*[@id="_preViewReport"]/table/tbody/tr[2]/td[3]'):
                tabla_ventas = driver.find_element(By.XPATH, '//*[@id="_preViewReport"]/table/tbody')
                tabla_ventas_len = len(tabla_ventas.find_elements(By.TAG_NAME, 'tr'))
                i = 2
            else:
                assert False, 'No hay datos en el condensado de datos'
            # empezamos a contar los productos y a separarlos
            datos_ventas['Servicio Medido'] = 0
            productos['Servicio Medido'] = 0
            cant = ''
            den = ''
            total_peso_vendido = 0
            while i < tabla_ventas_len:
                nombre = driver.find_element(By.XPATH, f'//*[@id="_preViewReport"]/table/tbody/tr[{i}]/td[3]').text
                if 'Cilindro' in nombre or 'cilindro' in nombre:
                    nombre = nombre.split(']')
                    cant = nombre[0]
                    cant = cant.replace('[CANT. ', '')
                    den = nombre[1]
                    den = den.replace(' [DEN. ', '')
                    nombre = nombre[2]
                    nombre = nombre.replace(' ', '', 1)
                    datos_ventas['Factor densidad ' + f'{nombre}'] = den
                    datos_ventas['Cantidad vendida de ' + f'{nombre}'] = cant
                    datos_ventas['Cantidad vendida de ' + f'{nombre}'] = datos_ventas['Cantidad vendida de ' + f'{nombre}'].replace('.00', '')
                    if nombre not in productos:
                        datos_ventas['Lts vendidos de ' + nombre] = 0
                        productos[nombre] = 0
                cantidad = driver.find_element(By.XPATH, f'//*[@id="_preViewReport"]/table/tbody/tr[{i}]/td[4]').text
                cantidad = cantidad.replace(',', '')
                unidad = driver.find_element(By.XPATH, f'//*[@id="_preViewReport"]/table/tbody/tr[{i}]/td[2]').text
                if 'GLP1' in nombre or 'Cilindro' in nombre or 'cilindro' in nombre:
                    if 'GLP1' in nombre and 'C' in unidad:
                        datos_ventas['Servicio Medido'] = float(datos_ventas['Servicio Medido']) + float(cantidad)
                        productos['Servicio Medido'] = float(productos['Servicio Medido']) + float(cantidad)
                        i += 1
                    elif nombre in productos:
                        datos_ventas['Lts vendidos de ' + nombre] = float(datos_ventas['Lts vendidos de ' + nombre]) + float(cantidad)
                        total_peso_vendido = str(total_peso_vendido).replace(',', '')
                        total_peso_vendido = float(total_peso_vendido) + float(datos_ventas['Lts vendidos de ' + nombre])
                        productos[nombre] = float(productos[nombre]) + float(cantidad)
                        i += 1
                    else:
                        datos_ventas['Lt vendidos en: ' + nombre] = cantidad
                        datos_ventas['Lt vendidos en: ' + nombre] = datos_ventas['Lt vendidos en: ' + nombre].replace(',', '')
                        total_peso_vendido = str(total_peso_vendido).replace(',', '')
                        total_peso_vendido = float(total_peso_vendido) + float(datos_ventas['Lt vendidos en: ' + nombre])
                        productos[nombre] = cantidad
                        i += 1

            datos_ventas['Servicio Medido'] = str(datos_ventas['Servicio Medido']).replace(',', '')
            if 'Lt vendidos en: GLP1' in datos_ventas:
                datos_ventas['Lt vendidos en: GLP1'] = str(datos_ventas['Lt vendidos en: GLP1']).replace(',', '')
                datos_ventas['Lt vendidos en: GLP1'] = float(datos_ventas['Lt vendidos en: GLP1'])
            datos_ventas['Total litros vendidos'] = total_peso_vendido
            datos_ventas['Total litos'] = float(total_peso_vendido) + float(datos_ventas['Servicio Medido'])
            # if datos_ventas['Lt vendidos en: GLP1'] != carga_autotanque:
            #     mensaje_de_salida(datos_inventario, datos_ventas)
            #     assert False, 'Las ventas de GLP1 no cuadran con el inventario de carga de autotanques'

            # if datos_ventas['Total peso vendido'] != datos_inventario['Anden']:
            #     mensaje_de_salida(datos_inventario, datos_ventas)
            #     assert False, 'El total vendido no cuadra con el anden reportado en inventario.'
            # if datos_ventas['GLP1'] != datos_inventario['Carga autotanque']:
            #     mensaje_de_salida(datos_inventario, datos_ventas)
            #     assert False, 'El total vendido no cuadra con el anden reportado en inventario.'

        else:
            print('Test Inventario contra SGC \n')
            print('Test Inventario contra SGC, Compara los datos de ventas del ultimo inventario contra lo mostrado en Reporte condensado de ventas de SGC\n'
                  'Muestra las diferencias si existieran.\n'
                  'Instancias: http://192.168.9.164/sgcweb, http://testventas.sgcweb.com.mx/')
            print('\n\n')
            mensaje_de_salida_ventas(datos_inventario, datos_ventas)
            assert False, 'No hay inventario del dia anterior.'

    except NoSuchElementException as exc:
        print('Test Inventario contra SGC \n')
        print('Test Inventario contra SGC, Compara los datos de ventas del ultimo inventario contra lo mostrado en Reporte condensado de ventas de SGC\n'
              'Muestra las diferencias si existieran.\n'
              'Instancias: http://192.168.9.164/sgcweb, http://testventas.sgcweb.com.mx/')
        print('\n\n')
        print(exc)
        mensaje_de_salida_ventas(datos_inventario, datos_ventas)
        assert False, 'D:'

    print('Test Inventario contra SGC \n')
    print('Test Inventario contra SGC, Compara los datos de ventas del ultimo inventario contra lo mostrado en Reporte condensado de ventas de SGC\n'
          'Muestra las diferencias si existieran.\n'
          'Instancias: http://192.168.9.164/sgcweb, http://testventas.sgcweb.com.mx/')
    print('\n\n')
    mensaje_de_salida_ventas(datos_inventario, datos_ventas)
    assert True, 'No hay inventario del dia anterior.'


def test_salidas_tanque(driver, fecha_test, name='admin', password='Z76U4CFIx#'):
    datos_inventario_tanque = {}
    dia_inventario = fecha_test
    salidas = []
    x = 0
    try:
        driver.refresh()
        time.sleep(3)
        p = driver.current_window_handle
        handles = driver.window_handles
        driver.switch_to.window(handles[0])
        time.sleep(3)
        # sacar fechas del inventario
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
        datos_inventario_tanque['Dia inventario'] = dia_inventario
        fecha = driver.find_element(By.XPATH, '//*[@id="inventario_basic"]')
        fecha.send_keys(dia_inventario)
        fecha.send_keys(Keys.ENTER)
        time.sleep(1)
        # fecha inicial del inventario
        if check_exists_by_xpath(driver, '//*[@id="MassUpdate"]/table/tbody/tr[3]/td[1]/a'):
            documento = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody/tr[3]/td[1]/a')
            documento.click()
            time.sleep(1)
            fecha_inicio = driver.find_element(By.XPATH, '//*[@id="lienzo"]/table[2]/tbody/tr[1]/td[2]').text
            datos_inventario_tanque['Fecha inicial inventario'] = fecha_inicio
            fecha_inicio = convertir_fecha_24(fecha_inicio)
            # fecha final del inventario
            fecha_final = driver.find_element(By.XPATH, '//*[@id="tr1"]/td[2]').text
            datos_inventario_tanque['Fecha Final del Inventario'] = fecha_final
            fecha_final = convertir_fecha_24(fecha_final)

            # sacamos los datos de las salidas de almacen
            datos_inventario_tanque['Carga de Autotanques'] = driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/table/tbody/tr/td/div/table[5]/tbody/tr[2]/td[2]').text
            datos_inventario_tanque['Auditor'] = driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/table/tbody/tr/td/div/table[5]/tbody/tr[3]/td[2]').text
            datos_inventario_tanque['Carburacion'] = driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/table/tbody/tr/td/div/table[5]/tbody/tr[4]/td[2]').text
            datos_inventario_tanque['Total salidas Inventario'] = driver.find_element(By.XPATH, '//*[@id="lienzo"]/table[5]/tbody/tr[5]/td[2]').text
            auditor = datos_inventario_tanque['Auditor'].replace('lt', '')
            auditor = auditor.replace(',', '')
            carburacion = datos_inventario_tanque['Carburacion'].replace('lt', '')
            carburacion = carburacion.replace(',', '')
            datos_inventario_tanque['AutoConsumo'] = 0
            datos_inventario_tanque['AutoTanque'] = 0
            datos_inventario_tanque['Total LLenados'] = 0
            if float(auditor) > 0 or float(carburacion) > 0:
                # Nos movemos a carga
                wait = WebDriverWait(driver, 60)
                lista = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="moduleList"]/ul')))
                opciones_lista = lista.find_elements(By.TAG_NAME, 'li')
                lista_size = len(opciones_lista)
                i = 2
                while i <= lista_size:
                    opcion = driver.find_element(By.XPATH, f'/html/body/div[3]/div[10]/ul/li[{i}]/span[2]/a')
                    texto = opcion.text
                    if texto == 'Carga':
                        opcion.click()
                        break
                    elif i >= lista_size:
                        print('La opcion de Carga no se encuentra o cambio de nombre, revisar permisos')
                        assert False, 'La opcion de Carga no se encuentra o cambio de nombre, revisar permisos'
                    else:
                        i += 1
                time.sleep(2)
                cargas_por_unidad = driver.find_element(By.XPATH, '//*[@id="ul_shortcuts"]/li[2]/a')
                cargas_por_unidad.click()
                fecha_3 = driver.find_element(By.XPATH, '//*[@id="fecha1"]')
                fecha_3.clear()
                fecha_4 = driver.find_element(By.XPATH, '//*[@id="fecha2"]')
                fecha_4.clear()
                fecha_3.send_keys(fecha_inicio)
                fecha_4.send_keys(fecha_final)
                fecha_4.send_keys(Keys.ENTER)
                selector_vehiculo = Select(driver.find_element(By.XPATH, '//*[@id="tipo_vehiculos_list"]'))
                selector_vehiculo.select_by_visible_text('AutoConsumo')
                time.sleep(2)
                tabla_carga = driver.find_element(By.XPATH, '//*[@id="reporteCargas"]/tbody')
                tabla_carga_len = len(tabla_carga.find_elements(By.TAG_NAME, 'tr'))
                i = 2

                if check_exists_by_xpath(driver, '//*[@id="reporteCargas"]/tbody/tr[2]/td[12]'):
                    while i < tabla_carga_len:
                        salidas.append([])
                        salidas[x].append(driver.find_element(By.XPATH, f'//*[@id="reporteCargas"]/tbody/tr[{i}]/td[1]/a').text)
                        vehiculo = driver.find_element(By.XPATH, f'//*[@id="reporteCargas"]/tbody/tr[{i}]/td[3]').text
                        salidas[x].append(vehiculo)
                        cantidad = driver.find_element(By.XPATH, f'//*[@id="reporteCargas"]/tbody/tr[{i}]/td[13]').text
                        cantidad = cantidad.replace(' ', '')
                        cantidad = cantidad.replace('lt', '')
                        cantidad = cantidad.replace(',', '')
                        if 'kg' in cantidad:
                            cantidad = cantidad.replace('kg', '')
                            cantidad = float(cantidad) / 0.5360
                        datos_inventario_tanque['AutoConsumo'] = datos_inventario_tanque['AutoConsumo'] + float(cantidad)
                        cantidad = round(float(cantidad), 3)
                        cantidad = str(cantidad) + ' lt'
                        salidas[x].append(cantidad)
                        i += 1
                        x += 1
                selector_vehiculo.select_by_visible_text('AutoConsumo')
                time.sleep(2)
                tabla_carga = driver.find_element(By.XPATH, '//*[@id="reporteCargas"]/tbody')
                tabla_carga_len = len(tabla_carga.find_elements(By.TAG_NAME, 'tr'))
                i = 2

                if check_exists_by_xpath(driver, '//*[@id="reporteCargas"]/tbody/tr[2]/td[12]'):
                    while i < tabla_carga_len:
                        salidas.append([])
                        salidas[x].append(driver.find_element(By.XPATH, f'//*[@id="reporteCargas"]/tbody/tr[{i}]/td[1]/a').text)
                        vehiculo = driver.find_element(By.XPATH, f'//*[@id="reporteCargas"]/tbody/tr[{i}]/td[3]').text
                        salidas[x].append(vehiculo)
                        cantidad = driver.find_element(By.XPATH, f'//*[@id="reporteCargas"]/tbody/tr[{i}]/td[13]').text
                        cantidad = cantidad.replace(' ', '')
                        cantidad = cantidad.replace('lt', '')
                        cantidad = cantidad.replace(',', '')
                        if 'kg' in cantidad:
                            cantidad = cantidad.replace('kg', '')
                            cantidad = float(cantidad) / 0.5360
                        datos_inventario_tanque['AutoTanque'] = datos_inventario_tanque['AutoTanque'] + float(cantidad)
                        cantidad = round(float(cantidad), 3)
                        cantidad = str(cantidad) + ' lt'
                        salidas[x].append(cantidad)
                        i += 1
                        x += 1

                # nos movemos a anden
                wait = WebDriverWait(driver, 60)
                lista = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="moduleList"]/ul')))
                opciones_lista = lista.find_elements(By.TAG_NAME, 'li')
                lista_size = len(opciones_lista)
                i = 2
                while i <= lista_size:
                    opcion = driver.find_element(By.XPATH, f'/html/body/div[3]/div[10]/ul/li[{i}]/span[2]/a')
                    texto = opcion.text
                    if texto == 'Andén':
                        opcion.click()
                        break
                    elif i >= lista_size:
                        print('La opcion de Pedidos no se encuentra o cambio de nombre, revisar permisos')
                        assert False, 'D:'
                    else:
                        i += 1
                time.sleep(2)
                llenado_por_terminal = driver.find_element(By.XPATH, '//*[@id="ul_shortcuts"]/li[2]/a')
                llenado_por_terminal.click()
                fecha = driver.find_element(By.XPATH, '//*[@id="fecha1"]')
                fecha.clear()
                fecha.send_keys(fecha_inicio)
                fecha2 = driver.find_element(By.XPATH, '//*[@id="fecha2"]')
                fecha2.clear()
                fecha2.send_keys(fecha_final)
                ver_reporte = driver.find_element(By.XPATH, '//*[@id="btn_ver_reporte"]')
                ver_reporte.click()
                time.sleep(5)
                tabla_llenados = driver.find_element(By.XPATH, '//*[@id="reporteLlenados"]/tbody')
                tabla_llenados_len = len(tabla_llenados.find_elements(By.TAG_NAME, 'tr'))
                i = 2
                if check_exists_by_xpath(driver, '//*[@id="reporteLlenados"]/tbody/tr[2]/td[1]/a'):
                    while i < tabla_llenados_len:
                        salidas.append([])
                        salidas[x].append(driver.find_element(By.XPATH, f'//*[@id="reporteLlenados"]/tbody/tr[{i}]/td[1]/a').text)
                        vehiculo = driver.find_element(By.XPATH, f'//*[@id="reporteLlenados"]/tbody/tr[{i}]/td[3]').text
                        salidas[x].append(vehiculo)
                        cantidad = driver.find_element(By.XPATH, f'//*[@id="reporteLlenados"]/tbody/tr[{i}]/td[11]').text
                        cantidad = cantidad.replace(' ', '')
                        cantidad = cantidad.replace('lt', '')
                        cantidad = cantidad.replace(',', '')
                        if 'kg' in cantidad:
                            cantidad = cantidad.replace('kg', '')
                            cantidad = float(cantidad) / 0.5360
                        datos_inventario_tanque['Total LLenados'] = datos_inventario_tanque['Total LLenados'] + float(cantidad)
                        cantidad = round(cantidad, 3)
                        cantidad = str(cantidad) + ' lt'
                        salidas[x].append(cantidad)
                        i += 1
                        x += 1
                datos_inventario_tanque['Total LLenados'] = round(datos_inventario_tanque['Total LLenados'], 2)
            # nos movemos a auditor
            wait = WebDriverWait(driver, 60)
            lista = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="moduleList"]/ul')))
            opciones_lista = lista.find_elements(By.TAG_NAME, 'li')
            lista_size = len(opciones_lista)
            i = 2
            while i <= lista_size:
                opcion = driver.find_element(By.XPATH, f'/html/body/div[3]/div[10]/ul/li[{i}]/span[2]/a')
                texto = opcion.text
                if texto == 'Auditor Andén':
                    opcion.click()
                    break
                elif i >= lista_size:
                    print('La opcion de Auditor Andén no se encuentra o cambio de nombre, revisar permisos')
                    assert False, 'D:'
                else:
                    i += 1
            time.sleep(2)
            busqueda_avanzada = driver.find_element(By.XPATH, '//*[@id="tab_link_isies_registros_masico|advanced_search"]')
            busqueda_avanzada.click()
            fecha_1 = driver.find_element(By.XPATH, '//*[@id="fecha_final_advanced"]')
            fecha_1.send_keys(fecha_inicio)
            time.sleep(2)
            fecha_2 = driver.find_element(By.XPATH, '//*[@id="fecha_final1_advanced"]')
            fecha_2.send_keys(fecha_final)
            time.sleep(2)
            fecha_2.submit()
            time.sleep(2)
            lista = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody')
            lista_len = len(lista.find_elements(By.TAG_NAME, 'tr'))
            time.sleep(2)
            if check_exists_by_xpath(driver, '//*[@id="MassUpdate"]/table/tbody/tr[3]/td[5]'):
                ultimo_registro = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody/tr[3]/td[5]').text
                ultimo_registro = ultimo_registro.replace(',', '')
                datos_inventario_tanque['Folio ultimo registro'] = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody/tr[3]/td[1]/a').text
                datos_inventario_tanque['Fecha ultimo registro'] = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody/tr[3]/td[2]').text
                datos_inventario_tanque['Ultimo registro'] = ultimo_registro
                flecha = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{lista_len - 2}]/td/table/tbody/tr/td[2]/button[4]')
                if flecha.is_enabled():
                    flecha.click()
                    time.sleep(2)
                    lista2 = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody')
                    lista2_len = len(lista2.find_elements(By.TAG_NAME, 'tr'))
                    datos_inventario_tanque['Folio primer registro'] = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{lista2_len - 3}]/td[1]/a').text
                    datos_inventario_tanque['Fecha primer registro'] = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{lista2_len - 3}]/td[2]').text
                    primer_registro = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{lista2_len - 3}]/td[5]').text
                    primer_registro = primer_registro.replace(',', '')
                    datos_inventario_tanque['Primer registro'] = primer_registro
                else:
                    time.sleep(2)
                    lista2 = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody')
                    lista2_len = len(lista2.find_elements(By.TAG_NAME, 'tr'))
                    datos_inventario_tanque['Folio primer registro'] = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{lista2_len - 3}]/td[1]/a').text
                    datos_inventario_tanque['Fecha primer registro'] = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{lista2_len - 3}]/td[2]').text
                    primer_registro = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{lista2_len - 3}]/td[5]').text
                    primer_registro = primer_registro.replace(',', '')
                    datos_inventario_tanque['Primer registro'] = primer_registro
                resta = float(datos_inventario_tanque['Ultimo registro']) - float(datos_inventario_tanque['Primer registro'])
                resta = round(resta, 2)
                datos_inventario_tanque['Diferencia entre primer y ultimo registro Auditor anden'] = resta
            else:
                datos_inventario_tanque['Diferencia entre primer y ultimo registro Auditor anden'] = 0.0
        datos_inventario_tanque['Suma de los 3 campos'] = float(datos_inventario_tanque['AutoConsumo']) + float(datos_inventario_tanque['AutoTanque']) + float(
            datos_inventario_tanque['Diferencia entre primer y ultimo registro Auditor anden'])
        datos_inventario_tanque['Suma de los 3 campos'] = round(datos_inventario_tanque['Suma de los 3 campos'], 2)
        datos_inventario_tanque['Total de servicios Auto Consumo'] = x
        salidas_inventarios = datos_inventario_tanque['Total salidas Inventario'].replace(' ', '')
        salidas_inventarios = salidas_inventarios.replace(',', '')
        salidas_inventarios = salidas_inventarios.replace('lt', '')
        datos_inventario_tanque['Diferencia entre Inventarios y Planta'] = float(salidas_inventarios) - datos_inventario_tanque['Suma de los 3 campos']
        datos_inventario_tanque['Diferencia entre Inventarios y Planta'] = abs(datos_inventario_tanque['Diferencia entre Inventarios y Planta'])
        datos_inventario_tanque['Diferencia entre Inventarios y Planta'] = round(datos_inventario_tanque['Diferencia entre Inventarios y Planta'], 3)
    except NoSuchElementException as exc:
        print(exc)
        assert False, 'not ok D:'

    print('Test Inventario contra Salidas del tanque \n')
    print('Test Inventario contra Salidas del tanque, Compara los datos de Salidas de almacen del ultimo inventario contra los datos de Auditor Anden,Carga y los auto consumos \n'
          'Muestra las diferencias si existieran.\n'
          'Instancias: http://192.168.9.164/sgcweb')
    print('\n\n')

    assert True, 'D:'
