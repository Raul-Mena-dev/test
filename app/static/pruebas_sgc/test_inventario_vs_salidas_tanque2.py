import time
import datetime
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from funciones.function import login, check_exists_by_xpath, convertir_fecha_24
from selenium.common.exceptions import NoSuchElementException


def mensaje_de_salida(datos_inventario_tanque):
    print('-------------------------------------------')
    print('-------------------------------------------')
    print('Datos y diferencias: \n')
    print('-------------------------------------------')
    print('Datos en inventario:\n')
    print('------------Salidas del almacen------------')
    for dato, valor in datos_inventario_tanque.items():
        if 'AutoConsumo' in dato:
            print('\n----------------AutoConsumo-----------------\n')
        if 'AutoTanque' in dato:
            print('\n----------------AutoTanque------------------\n')
        if 'Total LLenados' in dato:
            print('\n----------------Total LLenados------------------\n')
        if 'Folio ultimo registro' in dato:
            print('\n-----------------Auditor--------------------')
        if 'Suma' in dato:
            print('\n----Suma AutoConsumo, AutoTanque, Auditor---\n')
        if 'Diferencia entre Inventarios y Planta' in dato:
            print('\n---------------Diferencias--------------------\n')
        print(dato + ': ' + str(valor))
    print('\n-------------------------------------------')
    print('-------------------------------------------\n')


def test_ventas_vs_json(driver, fecha_test, name='admin', password='Z76U4CFIx#'):
    datos_inventario_tanque = {}
    dia_inventario = fecha_test
    salidas = []
    x = 0
    try:
        login(driver, name, password)
        time.sleep(2)
        # sacar fechas del inventario
        boton_inventario = driver.find_element(By.XPATH, '//*[@id="grouptab_7"]')
        boton_inventario.click()
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
                carga = driver.find_element(By.XPATH, '//*[@id="grouptab_3"]')
                carga.click()
                cargas_por_unidad = driver.find_element(By.XPATH, '//*[@id="ul_shortcuts"]/li[2]/a')
                cargas_por_unidad.click()
                fecha_3 = driver.find_element(By.XPATH, '//*[@id="fecha1"]')
                fecha_3.clear()
                fecha_4 = driver.find_element(By.XPATH, '//*[@id="fecha2"]')
                fecha_4.clear()
                fecha_3.send_keys(fecha_inicio)
                fecha_4.send_keys(fecha_final)
                fecha_4.send_keys(Keys.ENTER)
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
                        if vehiculo == 'AutoConsumo':
                            datos_inventario_tanque['AutoConsumo'] = datos_inventario_tanque['AutoConsumo'] + float(cantidad)
                        else:
                            datos_inventario_tanque['AutoTanque'] = datos_inventario_tanque['AutoTanque'] + float(cantidad)
                        cantidad = round(float(cantidad), 3)
                        cantidad = str(cantidad) + ' lt'
                        salidas[x].append(cantidad)
                        i += 1
                        x += 1
                # nos movemos a anden
                anden = driver.find_element(By.XPATH, '//*[@id="grouptab_1"]')
                anden.click()
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
            auditor_anden = driver.find_element(By.XPATH, '//*[@id="grouptab_5"]')
            auditor_anden.click()
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
    mensaje_de_salida(datos_inventario_tanque)
    assert True, 'D:'
