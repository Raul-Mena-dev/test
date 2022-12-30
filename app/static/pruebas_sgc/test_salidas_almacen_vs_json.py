import time
import os
import json
import datetime
from tabulate import tabulate
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from zipfile import ZipFile
from funciones.function import login, check_exists_by_xpath, convertir_fecha_24
from selenium.common.exceptions import NoSuchElementException


def mensaje_de_salida(datos_inventario, datos_json, datos_ventas, salidas, ventas_que_no_aparecen):
    print('-------------------------------------------')
    print('-------------------------------------------')
    print('Datos y diferencias: \n')
    print('-------------------------------------------')
    print('Datos en inventario:\n')
    print('------------Salidas del almacen------------')
    for dato, valor in datos_inventario.items():
        if 'AutoConsumo' in dato:
            print('\n----------------AutoConsumo-----------------\n')
        if 'AutoTanque' in dato:
            print('\n----------------AutoTanque------------------\n')
        if 'Folio ultimo registro' in dato:
            print('\n-----------------Auditor--------------------')
        if 'Suma' in dato:
            print('\n----Suma AutoConsumo, AutoTanque, Auditor---\n')
        print(dato + ': ' + str(valor))
    print('-------------------------------------------')
    print('----------------Datos JSON-----------------\n')
    for dato, valor in datos_json.items():
        if 'Diferencia en entregas vs nodo Total entregas JSON' in dato:
            print('-------------------------------------------')
            print('-------------------------------------------')
            print('--------------Diferencias------------------\n')
        print(dato + ': ' + str(valor))
    print('-------------------------------------------')

    print('-------------------------------------------')
    print('-------------------------------------------')
    columnas = ['Folio', 'Vehiculo', 'Cantidad Real']
    print('Folios de Salidas de almacen: \n')
    print(tabulate(salidas, headers=columnas, tablefmt="fancy_grid"))
    print('-------------------------------------------')
    print('-------------------------------------------')
    columnas = ['Num.registro', 'Fecha', 'Volumen entregado']
    print('Entregas en JSON: \n')
    print(tabulate(datos_ventas, headers=columnas, tablefmt="fancy_grid"))
    print('-------------------------------------------')
    print('-------------------------------------------')
    columnas = ['Folio', 'Vehiculo', 'Cantidad Real']
    print('Salidas registradas que no aparece en el JSON: \n')
    print(tabulate(ventas_que_no_aparecen, headers=columnas, tablefmt="fancy_grid"))
    print('-------------------------------------------')


def test_ventas_vs_json(driver, fecha_test, name='admin', password='Z76U4CFIx#'):
    datos_inventario = {}
    datos_json = {}
    datos_ventas = []
    salidas = []
    ventas_que_no_aparecen = []
    fecha_inicio = ''
    fecha_final = ''
    x = 0
    dia_inventario = fecha_test
    try:
        login(driver, name, password)
        time.sleep(2)
        # sacar fechas del inventario
        boton_inventario = driver.find_element(By.XPATH, '//*[@id="grouptab_7"]')
        boton_inventario.click()
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
            fecha_inicio = driver.find_element(By.XPATH, '//*[@id="lienzo"]/table[2]/tbody/tr[1]/td[2]').text
            datos_inventario['Fecha inicial inventario'] = fecha_inicio
            fecha_inicio = convertir_fecha_24(fecha_inicio)
            # fecha final del inventario
            fecha_final = driver.find_element(By.XPATH, '//*[@id="tr1"]/td[2]').text
            datos_inventario['Fecha Final del Inventario'] = fecha_final
            fecha_final = convertir_fecha_24(fecha_final)

            # sacamos los datos de las salidas de almacen
            datos_inventario['Carga de Autotanques'] = driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/table/tbody/tr/td/div/table[5]/tbody/tr[2]/td[2]').text
            datos_inventario['Auditor'] = driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/table/tbody/tr/td/div/table[5]/tbody/tr[3]/td[2]').text
            datos_inventario['Carburacion'] = driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/table/tbody/tr/td/div/table[5]/tbody/tr[4]/td[2]').text
            datos_inventario['Total salidas Inventario'] = driver.find_element(By.XPATH, '//*[@id="lienzo"]/table[5]/tbody/tr[5]/td[2]').text
            auditor = datos_inventario['Auditor'].replace('lt', '')
            auditor = auditor.replace(',', '')
            carburacion = datos_inventario['Carburacion'].replace('lt', '')
            carburacion = carburacion.replace(',', '')
            datos_inventario['AutoConsumo'] = 0
            datos_inventario['AutoTanque'] = 0
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
                            datos_inventario['AutoConsumo'] = datos_inventario['AutoConsumo'] + float(cantidad)
                        else:
                            datos_inventario['AutoTanque'] = datos_inventario['AutoTanque'] + float(cantidad)
                        cantidad = round(float(cantidad), 3)
                        cantidad = str(cantidad) + ' lt'
                        salidas[x].append(cantidad)
                        i += 1
                        x += 1
                # # nos movemos a anden
                # anden = driver.find_element(By.XPATH, '//*[@id="grouptab_1"]')
                # anden.click()
                # llenado_por_terminal = driver.find_element(By.XPATH, '//*[@id="ul_shortcuts"]/li[2]/a')
                # llenado_por_terminal.click()
                # fecha = driver.find_element(By.XPATH, '//*[@id="fecha1"]')
                # fecha.clear()
                # fecha.send_keys(fecha_inicio)
                # fecha2 = driver.find_element(By.XPATH, '//*[@id="fecha2"]')
                # fecha2.clear()
                # fecha2.send_keys(fecha_final)
                # ver_reporte = driver.find_element(By.XPATH, '//*[@id="btn_ver_reporte"]')
                # ver_reporte.click()
                # time.sleep(5)
                # tabla_llenados = driver.find_element(By.XPATH, '//*[@id="reporteLlenados"]/tbody')
                # tabla_llenados_len = len(tabla_llenados.find_elements(By.TAG_NAME, 'tr'))
                # i = 2
                # if check_exists_by_xpath(driver, '//*[@id="reporteLlenados"]/tbody/tr[2]/td[1]/a'):
                #     while i < tabla_llenados_len:
                #         salidas.append([])
                #         salidas[x].append(driver.find_element(By.XPATH, f'//*[@id="reporteLlenados"]/tbody/tr[{i}]/td[1]/a').text)
                #         vehiculo = driver.find_element(By.XPATH, f'//*[@id="reporteLlenados"]/tbody/tr[{i}]/td[3]').text
                #         salidas[x].append(vehiculo)
                #         cantidad = driver.find_element(By.XPATH, f'//*[@id="reporteLlenados"]/tbody/tr[{i}]/td[11]').text
                #         cantidad = cantidad.replace(' ', '')
                #         cantidad = cantidad.replace('lt', '')
                #         cantidad = cantidad.replace(',', '')
                #         if 'kg' in cantidad:
                #             cantidad = cantidad.replace('kg', '')
                #             cantidad = float(cantidad) / 0.5360
                #         if vehiculo == 'AutoConsumo':
                #             datos_inventario['AutoConsumo'] = datos_inventario['AutoConsumo'] + float(cantidad)
                #         else:
                #             datos_inventario['AutoTanque'] = datos_inventario['AutoTanque'] + float(cantidad)
                #         cantidad = round(cantidad, 3)
                #         cantidad = str(cantidad) + ' lt'
                #         salidas[x].append(cantidad)
                #         i += 1
                #         x += 1
                # datos_inventario['AutoConsumo'] = round(datos_inventario['AutoConsumo'], 2)
                # datos_inventario['AutoTanque'] = round(datos_inventario['AutoTanque'], 2)
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
                datos_inventario['Folio ultimo registro'] = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody/tr[3]/td[1]/a').text
                datos_inventario['Fecha ultimo registro'] = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody/tr[3]/td[2]').text
                datos_inventario['Ultimo registro'] = ultimo_registro
                flecha = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{lista_len - 2}]/td/table/tbody/tr/td[2]/button[4]')
                if flecha.is_enabled():
                    flecha.click()
                    time.sleep(2)
                    lista2 = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody')
                    lista2_len = len(lista2.find_elements(By.TAG_NAME, 'tr'))
                    datos_inventario['Folio primer registro'] = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{lista2_len - 3}]/td[1]/a').text
                    datos_inventario['Fecha primer registro'] = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{lista2_len - 3}]/td[2]').text
                    primer_registro = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{lista2_len - 3}]/td[5]').text
                    primer_registro = primer_registro.replace(',', '')
                    datos_inventario['Primer registro'] = primer_registro
                else:
                    time.sleep(2)
                    lista2 = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody')
                    lista2_len = len(lista2.find_elements(By.TAG_NAME, 'tr'))
                    datos_inventario['Folio primer registro'] = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{lista2_len - 3}]/td[1]/a').text
                    datos_inventario['Fecha primer registro'] = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{lista2_len - 3}]/td[2]').text
                    primer_registro = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{lista2_len - 3}]/td[5]').text
                    primer_registro = primer_registro.replace(',', '')
                    datos_inventario['Primer registro'] = primer_registro
                resta = float(datos_inventario['Ultimo registro']) - float(datos_inventario['Primer registro'])
                resta = round(resta, 2)
                datos_inventario['Diferencia entre primer y ultimo registro Auditor anden'] = resta
            else:
                datos_inventario['Diferencia entre primer y ultimo registro Auditor anden'] = 0.0
        datos_inventario['Suma de los 3 campos'] = float(datos_inventario['AutoConsumo']) + float(datos_inventario['AutoTanque']) + float(
            datos_inventario['Diferencia entre primer y ultimo registro Auditor anden'])
        datos_inventario['Suma de los 3 campos'] = round(datos_inventario['Suma de los 3 campos'], 2)
        datos_inventario['Total de servicios Auto Consumo'] = x
        # sacamos el JSON
        controles_volumetricos = driver.find_element(By.XPATH, '//*[@id="grouptab_8"]')
        controles_volumetricos.click()
        generar_reportes = driver.find_element(By.XPATH, '//*[@id="ul_shortcuts"]/li[6]/a')
        generar_reportes.click()
        seleccion = Select(driver.find_element(By.XPATH, '//*[@id="json"]'))
        seleccion.select_by_value('Diario')
        seleccion_fecha = driver.find_element(By.XPATH, '//*[@id="dia"]')
        seleccion_fecha.send_keys(dia_inventario)
        generar = driver.find_element(By.XPATH, '//*[@id="Generar"]/input')
        generar.click()
        json_vntad = driver.find_element(By.XPATH, '//*[@id="mnsj_generado"]/a[1]')
        json_d = driver.find_element(By.XPATH, '//*[@id="mnsj_generado"]/a[2]')
        nombre_json_vntad = json_vntad.text
        nombre_json_d = json_d.text
        json_vntad.click()
        json_d.click()
        time.sleep(8)
        with ZipFile(f'/home/rmenapc/Escritorio/test_station/{nombre_json_vntad}', 'r') as z:
            z.extractall('/home/rmenapc/Escritorio/test_station/')
        os.remove(f'/home/rmenapc/Escritorio/test_station/{nombre_json_vntad}')
        with ZipFile(f'/home/rmenapc/Escritorio/test_station/{nombre_json_d}', 'r') as z:
            z.extractall('/home/rmenapc/Escritorio/test_station/')
        os.remove(f'/home/rmenapc/Escritorio/test_station/{nombre_json_d}')

        # sacamos los datos del json
        nombre_json_vntad = nombre_json_vntad.replace('.zip', '.json')
        nombre_json_d = nombre_json_d.replace('.zip', '.json')
        with open(f'/home/rmenapc/Escritorio/test_station/{nombre_json_d}', 'r') as json_file:
            json_load = json.load(json_file)

        num_entregas = json_load['ControlesVolumetricos']['Producto'][0]['Tanque'][0]['Entregas']['TotalEntregas']
        datos_json['Total entregado JSON'] = 0.0
        if int(num_entregas) > 0:
            data = json_load['ControlesVolumetricos']['Producto'][0]['Tanque'][0]['Entregas']['Entrega']

            aux = 0

            data_len = len(data)
            fecha1 = fecha_inicio
            fecha2 = fecha_final
            fecha1 = datetime.datetime.strptime(fecha1, '%Y-%m-%d %H:%M:%S')
            fecha2 = datetime.datetime.strptime(fecha2, '%Y-%m-%d %H:%M:%S')
            i = 0

            for dato in data:
                fecha = str(dato['FechaYHoraFinalEntrega']).replace('T', ' ')
                fecha = fecha.split(' ')
                sfecha = fecha[0]
                shora = fecha[1]
                shora = shora.split('-')
                fecha = sfecha + ' ' + shora[0]
                fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
                fecha = fecha - datetime.timedelta(hours=5)
                datos_ventas.append([])
                datos_ventas[i].append(str(dato['NumeroDeRegistro']))
                volumen = str(dato['VolumenEntregado'])
                if 'kg' in volumen:
                    volumen = str(dato['VolumenEntregado'])
                    volumen = volumen.replace(' ', '')
                    volumen = volumen.replace('kg', '')
                    volumen = volumen.replace(',', '')
                    volumen = float(volumen) / 0.5360
                    volumen = str(volumen) + ' lt'
                    datos_ventas[i].append(str(volumen))
                else:
                    volumen = volumen.replace(',', '')
                    datos_ventas[i].append(str(volumen))
                datos_json['Total entregado JSON'] = float(datos_json['Total entregado JSON']) + float(volumen)
                fecha = str(dato['FechaYHoraFinalEntrega']).replace('T', ' ')
                fecha = fecha.split(' ')
                sfecha = fecha[0]
                shora = fecha[1]
                shora = shora.split('-')
                fecha = sfecha + ' ' + shora[0]
                fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
                fecha = fecha - datetime.timedelta(hours=5)
                datos_ventas[i].append(fecha)
                aux += 1
                i += 1
            datos_ventas = sorted(datos_ventas, key=lambda r: r[0])
            datos_json['Total entregado JSON'] = round(datos_json['Total entregado JSON'], 2)

            aux4 = 0
            for salida in salidas:
                if not any(valor[0] in salida[0] for valor in datos_ventas):
                    ventas_que_no_aparecen.append([])
                    ventas_que_no_aparecen[aux4].append(salida[0])
                    ventas_que_no_aparecen[aux4].append(salida[1])
                    ventas_que_no_aparecen[aux4].append(salida[2])
                    aux4 += 1

            json_entregas = int(json_load['ControlesVolumetricos']['Producto'][0]['Tanque'][0]['Entregas']['TotalEntregas'])
            datos_json['Entregas en nodo entregas en JSON'] = json_entregas
            datos_json['Conteo Entregas en JSON'] = data_len
            datos_json['Diferencia en entregas vs nodo Total entregas JSON'] = int(datos_json['Entregas en nodo entregas en JSON']) - int(datos_json['Conteo Entregas en JSON'])
            datos_json['Diferencia de entregas en JSON vs entregas en sistema'] = int(datos_inventario['Total de servicios Auto Consumo']) - int(datos_json['Conteo Entregas en JSON'])
            volumen_inventario = str(datos_inventario['Total salidas Inventario']).replace('lt', '')
            volumen_inventario = volumen_inventario.replace(',', '')
            volumen_inventario = volumen_inventario.replace(' ', '')
            datos_json['Diferencia de litros de JSON contra inventario'] = float(datos_json['Total entregado JSON']) - float(volumen_inventario)
            datos_json['Diferencia de litros de JSON contra inventario'] = abs(datos_json['Diferencia de litros de JSON contra inventario'])
            datos_json['Diferencia de litros de JSON contra inventario'] = round(datos_json['Diferencia de litros de JSON contra inventario'], 3)
            datos_json['Diferencia de litros de JSON contra planta'] = float(datos_json['Total entregado JSON']) - float(datos_inventario['Suma de los 3 campos'])
            datos_json['Diferencia de litros de JSON contra planta'] = abs(datos_json['Diferencia de litros de JSON contra planta'])
            datos_json['Diferencia de litros de JSON contra planta'] = round(datos_json['Diferencia de litros de JSON contra planta'], 3)
        else:
            aux4 = 0
            for salida in salidas:
                if not any(valor[0] in salida[0] for valor in datos_json):
                    ventas_que_no_aparecen.append([])
                    ventas_que_no_aparecen[aux4].append(salida[0])
                    ventas_que_no_aparecen[aux4].append(salida[1])
                    ventas_que_no_aparecen[aux4].append(salida[2])
                    aux4 += 1

            json_entregas = int(json_load['ControlesVolumetricos']['Producto'][0]['Tanque'][0]['Entregas']['TotalEntregas'])
            datos_json['Entregas en nodo entregas en JSON'] = json_entregas
            datos_json['Conteo Entregas en JSON'] = 0
            datos_json['Total Documentos JSON'] = 0
            datos_json['Diferencia en entregas vs nodo Total entregas JSON'] = int(datos_json['Entregas en nodo entregas en JSON']) - int(datos_json['Conteo Entregas en JSON'])
            datos_json['Diferencia de entregas en JSON vs entregas en sistema'] = int(datos_inventario['Total de servicios Auto Consumo']) - int(datos_json['Conteo Entregas en JSON'])
            volumen_inventario = str(datos_inventario['Total salidas Inventario']).replace('lt', '')
            volumen_inventario = volumen_inventario.replace(',', '')
            volumen_inventario = volumen_inventario.replace(' ', '')
            datos_json['Diferencia de litros de JSON contra inventario'] = float(datos_json['Total entregado JSON']) - float(volumen_inventario)
            datos_json['Diferencia de litros de JSON contra inventario'] = abs(datos_json['Diferencia de litros de JSON contra inventario'])
            datos_json['Diferencia de litros de JSON contra inventario'] = round(datos_json['Diferencia de litros de JSON contra inventario'], 3)
            datos_json['Diferencia de litros de JSON contra planta'] = float(datos_json['Total entregado JSON']) - float(datos_inventario['Suma de los 3 campos'])
            datos_json['Diferencia de litros de JSON contra planta'] = abs(datos_json['Diferencia de litros de JSON contra planta'])
            datos_json['Diferencia de litros de JSON contra planta'] = round(datos_json['Diferencia de litros de JSON contra planta'], 3)
    except NoSuchElementException as exc:
        print(exc)
        assert False, 'not ok D:'

    os.remove(f'/home/rmenapc/Escritorio/test_station/{nombre_json_vntad}')
    os.remove(f'/home/rmenapc/Escritorio/test_station/{nombre_json_d}')
    print('Test Salidas Almacen contra el JSON Diario\n')
    print('Test Salidas Almacen contra el JSON Diario, Compara las salidas de almacen contra el JSON diario,\n'
          'Comprueba si las entragas y litros cuadran entre inventario y JSON.\n'
          'Instancias: http://192.168.9.164/sgcweb, http://testventas.sgcweb.com.mx/')
    print('\n\n')
    mensaje_de_salida(datos_inventario, datos_json, datos_ventas, salidas, ventas_que_no_aparecen)
    assert True, 'D:'
