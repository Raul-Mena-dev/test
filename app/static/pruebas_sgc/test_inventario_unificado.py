import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from funciones.function import login, check_exists_by_xpath, convertir_fecha_24
from selenium.common.exceptions import NoSuchElementException


def mensaje_de_salida(datos_inventario_inicial, datos_inventario_final, datos_entradas, datos_inventario, datos_ventas, datos_inventario_tanque):
    print('\n-------------------------------------------')
    print('---------Test 1 Inventario inicial---------')
    print('Test Inventario Fisico Inicial \n')
    print('Test Inventario Fisico Inicial, Compara el inventario Fisico Inicial del ultimo inventario el registro de almacen mas proximo a la fecha de inicio del inventario \n'
          'Muestra las diferencias si existieran.')
    print('-------------------------------------------\n')
    print('Datos de inventario fisico inicial: \n')
    for dato, valor in datos_inventario_inicial.items():
        print(dato, ': ', valor)
    print('\n-------------------------------------------')
    print('----------Test 2 Inventario final----------')
    print('Test Inventario Fisico Final \n')
    print('Test Inventario Fisico Final, Compara el inventario Fisico FInal del ultimo inventario el registro mas proximo de almacen a la fecha final del inventario \n'
          'Muestra las diferencias si existieran.')
    print('-------------------------------------------\n')
    print('Datos de inventario fisico final: \n')
    for dato, valor in datos_inventario_final.items():
        print(dato, ': ', valor)
    print('\n-------------------------------------------')
    print('----------Test 3 Inventario Entradas/Compras----------')
    print('Test Entradas\n')
    print('Test Entradas, Compara los datos de Entradas/compras del ultimo inventario contra los datos de planta,\n'
          ' en descargas por documento., muestra diferencias si existen')
    print('-------------------------------------------\n')
    print('Datos Entradas/compras: \n')
    for dato, valor in datos_entradas.items():
        print(dato, ': ', valor)
    print('\n-------------------------------------------')
    print('-----Test 4 Inventario contra ventas-------')
    print('Test Inventario contra SGC \n')
    print('Test Inventario contra SGC, Compara los datos de ventas del ultimo inventario contra lo mostrado en Reporte condensado de ventas de SGC\n'
          'Muestra las diferencias si existieran.')
    print('-------------------------------------------\n')
    print('Datos de inventario (apartado ventas): \n')
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
    print('\n-------------------------------------------')
    print('-----Test 5 Inventario Salidas de almacen----')
    print('Test Inventario contra Salidas del tanque \n')
    print('Test Inventario contra Salidas del tanque, Compara los datos de Salidas de almacen del ultimo inventario contra los datos de Auditor Anden,Carga y los auto consumos \n'
          'Muestra las diferencias si existieran.')
    print('-------------------------------------------\n')
    print('------------Salidas del almacen------------\n')
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


def test_inventario_fisico_inicial(driver, fecha_test, name='admin', password='Z76U4CFIx#', name_web='admin', password_web='Ku8L08iEsb86'):
    datos_inventario_inicial = {}
    datos_inventario_final = {}
    datos_entradas = {}
    datos_inventario = {}
    datos_ventas = {}
    productos = {}
    datos_inventario_tanque = {}
    dia_inventario = fecha_test
    try:
        login(driver, name, password)
        time.sleep(2)
        boton_inventario = driver.find_element(By.XPATH, '//*[@id="grouptab_7"]')
        boton_inventario.click()
        sub_boton_inventario = driver.find_element(By.XPATH, '//*[@id="moduleTab_7_isies_inventario_basico"]')
        sub_boton_inventario.click()
        time.sleep(2)
        datos_inventario_inicial['Dia inventario'] = dia_inventario
        fecha = driver.find_element(By.XPATH, '//*[@id="inventario_basic"]')
        fecha.send_keys(dia_inventario)
        fecha.send_keys(Keys.ENTER)
        time.sleep(1)
        if check_exists_by_xpath(driver, '//*[@id="MassUpdate"]/table/tbody/tr[3]/td[1]/a'):
            documento = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody/tr[3]/td[1]/a')
            documento.click()
            time.sleep(1)
            fecha_inicial = driver.find_element(By.XPATH, '//*[@id="lienzo"]/table[2]/tbody/tr[1]/td[2]').text
            datos_inventario_inicial['Fecha inicial inventario'] = fecha_inicial
            fecha_inicial = convertir_fecha_24(fecha_inicial)
            fecha_inicial = fecha_inicial.split(' ')
            hora_inicial = fecha_inicial[1]
            hora_inicial = hora_inicial.replace('pm', '')
            hora_inicial = hora_inicial.replace('am', '')
            hora_inicial = hora_inicial.replace(':', '')
            time.sleep(1)
            inventario_fisico_inicial = driver.find_element(By.XPATH, '//*[@id="lienzo"]/table[3]/tbody/tr[2]/td[2]').text
            # nos movemos a almacen
            boton_almacen = driver.find_element(By.XPATH, '//*[@id="grouptab_6"]')
            boton_almacen.click()
            sub_boton_almacen = driver.find_element(By.XPATH, '//*[@id="moduleTab_6_isies_registros_medidor_almacen"]')
            sub_boton_almacen.click()
            fecha_registro = driver.find_element(By.XPATH, '//*[@id="fecha_lectura_basic"]')
            fecha_registro.send_keys(datos_inventario_inicial['Dia inventario'])
            fecha_registro.send_keys(Keys.ENTER)
            i = 3
            tabla = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody')
            listado = tabla.find_elements(By.TAG_NAME, 'tr')
            len_listado = len(listado)
            len_listado -= 3
            if check_exists_by_xpath(driver, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[12]'):
                fecha_registro = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[14]').text
                datos_inventario_inicial['Fecha de registro mas proxima'] = fecha_registro
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
                    fecha_registro = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[14]').text
                    fecha_registro = convertir_fecha_24(fecha_registro)
                    solo_fecha_registro = fecha_registro.split(' ')
                    hora_registro = solo_fecha_registro[1]
                    hora_registro = hora_registro.replace('pm', '')
                    hora_registro = hora_registro.replace('am', '')
                    hora_registro = hora_registro.replace(':', '')
                    if int(hora_registro) <= int(hora_inicial):
                        datos_inventario_inicial['Fecha de registro mas proxima'] = fecha_registro
                        break
                    else:
                        i += 1
                folio = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[1]').text
                volumen = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[7]').text
                compensado = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[12]').text
                datos_inventario_inicial['Folio de registro mas proximo'] = folio
                inventario_fisico_inicial = inventario_fisico_inicial.replace('kg', '')
                inventario_fisico_inicial = inventario_fisico_inicial.replace('lt', '')
                inventario_fisico_inicial = inventario_fisico_inicial.replace(' ', '')
                inventario_fisico_inicial = inventario_fisico_inicial.replace(',', '')
                datos_inventario_inicial['Volumen Fisico Inicial'] = inventario_fisico_inicial
                volumen = volumen.replace(',', '')
                compensado.replace(',', '')
                datos_inventario_inicial['Volumen Almacen + Compensado'] = float(volumen) + float(compensado)
                datos_inventario_inicial['Volumen Almacen + Compensado'] = round(datos_inventario_inicial['Volumen Almacen + Compensado'], 2)
                datos_inventario_inicial['Diferencia'] = float(datos_inventario_inicial['Volumen Fisico Inicial']) - float(datos_inventario_inicial['Volumen Almacen + Compensado'])
        else:
            print('Test Unificado\n')
            print('Test Unificado, Test que junta 5 test para contrstar cada apartado del inventario contra sus respectivos apartados:\n'
                  'Test que se ejecutan:\n'
                  'Inventario inicial\n'
                  'Inventario final\n'
                  'Inventario Entradas/Compras\n'
                  'Inventario contra ventas\n'
                  'Inventario contra Auditor anden \n'
                  '\n\n'
                  'Instancias: http://192.168.9.164/sgcweb, http://testventas.sgcweb.com.mx/')
            print('\n\n')
            mensaje_de_salida(datos_inventario_inicial, datos_inventario_final, datos_entradas, datos_inventario, datos_ventas, datos_inventario_tanque)
            assert False, f'No hay inventario del dia seleccionado. Fecha: {fecha_test}'
        # se empieza el proceso para inventario final
        time.sleep(2)
        boton_inventario = driver.find_element(By.XPATH, '//*[@id="grouptab_7"]')
        boton_inventario.click()
        sub_boton_inventario = driver.find_element(By.XPATH, '//*[@id="moduleTab_7_isies_inventario_basico"]')
        sub_boton_inventario.click()
        time.sleep(2)
        datos_inventario_final['Dia inventario'] = dia_inventario
        fecha = driver.find_element(By.XPATH, '//*[@id="inventario_basic"]')
        fecha.send_keys(datos_inventario_final['Dia inventario'])
        fecha.send_keys(Keys.ENTER)
        time.sleep(1)
        if check_exists_by_xpath(driver, '//*[@id="MassUpdate"]/table/tbody/tr[3]/td[1]/a'):
            documento = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody/tr[3]/td[1]/a')
            documento.click()
            time.sleep(1)
            fecha_final = driver.find_element(By.XPATH, '//*[@id="tr1"]/td[2]').text
            datos_inventario_final['Fecha Final del Inventario'] = fecha_final
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
            if check_exists_by_xpath(driver, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[14]'):
                fecha_registro = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[14]').text
                fecha_registro = convertir_fecha_24(fecha_registro)
                datos_inventario_final['Fecha de registro mas proxima'] = fecha_registro
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
                    fecha_registro = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[14]').text
                    fecha_registro = convertir_fecha_24(fecha_registro)
                    solo_fecha_registro = fecha_registro.split(' ')
                    hora_registro = solo_fecha_registro[1]
                    hora_registro = hora_registro.replace('pm', '')
                    hora_registro = hora_registro.replace('am', '')
                    hora_registro = hora_registro.replace(':', '')
                    if int(hora_registro) <= int(hora_final):
                        datos_inventario_final['Fecha de registro mas proxima'] = fecha_registro
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
                datos_inventario_final['Folio de registro mas proximo'] = folio
                datos_inventario_final['Volumen Fisico Final Inventario'] = inventario_fisico_final
                volumen = volumen.replace(',', '')
                compensado.replace(',', '')
                datos_inventario_final['Volumen Almacen + Compensado'] = float(volumen) + float(compensado)
                datos_inventario_final['Volumen Almacen + Compensado'] = round(datos_inventario_final['Volumen Almacen + Compensado'], 2)
                datos_inventario_final['Diferencia'] = float(datos_inventario_final['Volumen Fisico Final Inventario']) - float(datos_inventario_final['Volumen Almacen + Compensado'])
                datos_inventario_final['Diferencia'] = abs(float(datos_inventario_final['Diferencia']))
                datos_inventario_final['Diferencia'] = round(float(datos_inventario_final['Diferencia']), 2)

        # empezamos el test de entradas
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
            datos_entradas['Entradas/compras'] = entradas_kg
            cantidad_de_entradas = entradas[0]
            cantidad_de_entradas = cantidad_de_entradas.replace('[', '')
            cantidad_de_entradas = cantidad_de_entradas.replace(']', '')
            datos_entradas['Cantidad de entradas/compras'] = cantidad_de_entradas
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

        # nos pasamos a hacer la prueba de inventario vs ventas

        time.sleep(2)
        # sacar fechas del inventario
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
            fecha_inicial = driver.find_element(By.XPATH, '//*[@id="lienzo"]/table[2]/tbody/tr[1]/td[2]').text
            datos_inventario['Fecha inicial inventario'] = fecha_inicial
            fecha_inicial = convertir_fecha_24(fecha_inicial)
            # fecha final del inventario
            fecha_final = driver.find_element(By.XPATH, '//*[@id="tr1"]/td[2]').text
            datos_inventario['Fecha Final del Inventario'] = fecha_final
            fecha_final = convertir_fecha_24(fecha_final)
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
            datos_inventario['Total sin Servicio medido'] = float(carga_autotanque) + float(anden)
            total_ventas = driver.find_element(By.XPATH, '//*[@id="lienzo"]/table[4]/tbody/tr[6]/td[2]').text
            datos_inventario['Total Ventas'] = total_ventas
            campo_variable = driver.find_element(By.XPATH, '//*[@id="lienzo"]/table[3]/tbody/tr[5]/td[1]').text
            if 'almacén' not in campo_variable:
                datos_inventario['Total en movimientos del sistema'] = driver.find_element(By.XPATH, '//*[@id="lienzo"]/table[3]/tbody/tr[5]/td[2]').text
            # nos movemos a sgc web
            principal = driver.current_window_handle
            driver.execute_script('''window.open("https://testventas.sgcweb.com.mx/index.php?action=Login&module=Users&login_module=Home&login_action=index","_blank");''')
            time.sleep(3)
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
            visor = driver.find_element(By.XPATH, '//*[@id="grouptab_6"]')
            visor.click()
            reporte_condensado = driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/table/tbody/tr/td/div[2]/table/tbody/tr[12]/td/div/a')
            reporte_condensado.click()
            # se manda la primera fecha
            time.sleep(5)
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
                mensaje_de_salida(datos_inventario_inicial, datos_inventario_final, datos_entradas, datos_inventario, datos_ventas, datos_inventario_tanque)
                assert False, 'No hay datos en el condensado de datos'
            # empezamos a contar los productos y a separarlos
            datos_ventas['Servicio Medido'] = 0
            productos['Servicio Medido'] = 0
            total_peso_vendido = 0
            while i < tabla_ventas_len:
                time.sleep(1)
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
                if 'GLP' in nombre or 'Cilindro' in nombre or 'cilindro' in nombre:
                    if 'GLP' in nombre and 'C' in unidad:
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
            if 'Lt vendidos en: GLP' in datos_ventas:
                datos_ventas['Lt vendidos en: GLP'] = str(datos_ventas['Lt vendidos en: GLP']).replace(',', '')
                datos_ventas['Lt vendidos en: GLP'] = float(datos_ventas['Lt vendidos en: GLP'])
            datos_ventas['Total litros vendidos'] = total_peso_vendido
            datos_ventas['Total litos'] = float(total_peso_vendido) + float(datos_ventas['Servicio Medido'])

            # empezamos el test de salidas del tanque
            # val = WebDriverWait(driver, 5).until(EC.visibility_of_element_located)
            salidas = []
            x = 0
            time.sleep(3)
            driver.switch_to.window(principal)
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
                if 'almacén' in campo_variable:
                    datos_inventario_tanque['Total en movimientos del sistema'] = driver.find_element(By.XPATH, '//*[@id="lienzo"]/table[3]/tbody/tr[5]/td[2]').text

                datos_inventario_tanque['AutoConsumo'] = 0
                datos_inventario_tanque['AutoTanque'] = 0
                datos_inventario_tanque['Total LLenados'] = 0
                if float(auditor) > 0.0 or float(carburacion) > 0.0:
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
                    selector_vehiculo = Select(driver.find_element(By.XPATH, '//*[@id="tipo_vehiculos_list"]'))
                    selector_vehiculo.select_by_visible_text('AutoConsumo')
                    ver_reporte_carga = driver.find_element(By.XPATH, '//*[@id="btn_ver_reporte"]')
                    ver_reporte_carga.click()
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
                    selector_vehiculo = Select(driver.find_element(By.XPATH, '//*[@id="tipo_vehiculos_list"]'))
                    selector_vehiculo.select_by_visible_text('Interno')
                    ver_reporte_carga = driver.find_element(By.XPATH, '//*[@id="btn_ver_reporte"]')
                    ver_reporte_carga.click()
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
                    datos_inventario_tanque['AutoConsumo'] = round(datos_inventario_tanque['AutoConsumo'], 4)
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
                        cantidad = cantidad.replace('*', '')
                        if 'kg' in cantidad:
                            cantidad = cantidad.replace('kg', '')
                            cantidad = float(cantidad) / 0.550
                        datos_inventario_tanque['Total LLenados'] = datos_inventario_tanque['Total LLenados'] + float(cantidad)
                        cantidad = round(cantidad, 3)
                        cantidad = str(cantidad) + ' lt'
                        salidas[x].append(cantidad)
                        i += 1
                        x += 1
                datos_inventario_tanque['AutoTanque'] = round(datos_inventario_tanque['AutoTanque'], 4)
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
            datos_inventario_tanque['Diferencia entre Inventarios -> Salidas almacen y Datos de Planta'] = float(salidas_inventarios) - datos_inventario_tanque['Suma de los 3 campos']
            datos_inventario_tanque['Diferencia entre Inventarios -> Salidas almacen y Datos de Planta'] = abs(datos_inventario_tanque['Diferencia entre Inventarios -> Salidas almacen y Datos de Planta'])
            datos_inventario_tanque['Diferencia entre Inventarios -> Salidas almacen y Datos de Planta'] = round(datos_inventario_tanque['Diferencia entre Inventarios -> Salidas almacen y Datos de Planta'], 3)
            datos_inventario_tanque['Diferencia Real de inventario'] = datos_inventario_final['Volumen Almacen + Compensado'] - (datos_inventario_inicial['Volumen Almacen + Compensado'] - datos_inventario_tanque['Suma de los 3 campos'])
            datos_inventario_tanque['Diferencia Real de inventario'] = abs(datos_inventario_tanque['Diferencia Real de inventario'])
            datos_inventario_tanque['Diferencia Real de inventario'] = round(datos_inventario_tanque['Diferencia Real de inventario'], 3)
        else:
            print('Test Unificado\n')
            print('Test Unificado, Test que junta 5 test para contrstar cada apartado del inventario contra sus respectivos apartados:\n'
                  'Test que se ejecutan:\n'
                  'Inventario inicial\n'
                  'Inventario final\n'
                  'Inventario Entradas/Compras\n'
                  'Inventario contra ventas\n'
                  'Inventario contra Auditor anden \n'
                  '\n\n'
                  'Instancias: http://192.168.9.164/sgcweb, http://testventas.sgcweb.com.mx/')
            print('\n\n')
            mensaje_de_salida(datos_inventario_inicial, datos_inventario_final, datos_entradas, datos_inventario, datos_ventas, datos_inventario_tanque)
            assert False, 'No hay inventario del dia anterior.'

        print('Test Unificado\n')
        print('Test Unificado, Test que junta 5 test para contrstar cada apartado del inventario contra sus respectivos apartados:\n'
              'Test que se ejecutan:\n'
              'Inventario inicial\n'
              'Inventario final\n'
              'Inventario Entradas/Compras\n'
              'Inventario contra ventas\n'
              'Inventario contra Auditor anden \n'
              '\n\n'
              'Instancias: http://192.168.9.164/sgcweb, http://testventas.sgcweb.com.mx/')
        print('\n\n')
        mensaje_de_salida(datos_inventario_inicial, datos_inventario_final, datos_entradas, datos_inventario, datos_ventas, datos_inventario_tanque)
        assert True, 'No hay inventario del dia anterior.'

    except NoSuchElementException as e:
        print('Test Unificado\n')
        print('Test Unificado, Test que junta 5 test para contrstar cada apartado del inventario contra sus respectivos apartados:\n'
              'Test que se ejecutan:\n'
              'Inventario inicial\n'
              'Inventario final\n'
              'Inventario Entradas/Compras\n'
              'Inventario contra ventas\n'
              'Inventario contra Auditor anden \n'
              '\n\n'
              'Instancias: http://192.168.9.164/sgcweb, http://testventas.sgcweb.com.mx/')
        print('\n\n')
        mensaje_de_salida(datos_inventario_inicial, datos_inventario_final, datos_entradas, datos_inventario, datos_ventas, datos_inventario_tanque)
        print(str(e))
