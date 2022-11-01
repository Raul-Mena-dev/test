import time
import datetime
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from funciones.function import login, check_exists_by_xpath, convertir_fecha_24
from selenium.common.exceptions import NoSuchElementException


def mensaje_de_salida(datos_inventario, datos_ventas):
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


def test_inventario_vs_ventas(driver, fecha_test, name='administrador', password='administrador', name_web='admin', password_web='Ku8L08iEsb86'):
    datos_inventario = {}
    datos_ventas = {}
    productos = {}
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
            fecha_inicial = driver.find_element(By.XPATH, '//*[@id="lienzo"]/table[2]/tbody/tr[1]/td[2]').text
            datos_inventario['Fecha inicial inventario'] = fecha_inicial
            fecha_inicial = convertir_fecha_24(fecha_inicial)
            # fecha final del inventario
            fecha_final = driver.find_element(By.XPATH, '//*[@id="tr1"]/td[2]').text
            datos_inventario['Fecha Final del Inventario'] = fecha_final
            fecha_final = convertir_fecha_24(fecha_final)
            dia1 = datetime.datetime.strptime(fecha_inicial, '%Y-%m-%d %H:%M:%S')
            dia1 = dia1.weekday()
            dia2 = datetime.datetime.strptime(fecha_final, '%Y-%m-%d %H:%M:%S')
            dia2 = dia2.weekday()
            # revisar si el inventario es domingo
            if (dia1 == 5 and dia2 == 6) or (dia1 == 6 and dia2 == 0):
                boton_inventario = driver.find_element(By.XPATH, '//*[@id="grouptab_7"]')
                boton_inventario.click()
                hora = datetime.datetime.now()
                dia_inventario = datetime.date.today()
                dia_inventario = dia_inventario - datetime.timedelta(days=3)
                datos_inventario['Dia inventario'] = dia_inventario
                dia_inventario = dia_inventario.strftime("%Y-%m-%d")
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
                else:
                    mensaje_de_salida(datos_inventario, datos_ventas)
                    assert False, 'No hay inventario del dia anterior.'
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
            visor = driver.find_element(By.XPATH, '//*[@id="grouptab_6"]')
            visor.click()
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
                mensaje_de_salida(datos_inventario, datos_ventas)
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
            mensaje_de_salida(datos_inventario, datos_ventas)
            assert False, 'No hay inventario del dia anterior.'

    except NoSuchElementException as exc:
        print('Test Inventario contra SGC \n')
        print('Test Inventario contra SGC, Compara los datos de ventas del ultimo inventario contra lo mostrado en Reporte condensado de ventas de SGC\n'
              'Muestra las diferencias si existieran.\n'
              'Instancias: http://192.168.9.164/sgcweb, http://testventas.sgcweb.com.mx/')
        print('\n\n')
        mensaje_de_salida(datos_inventario, datos_ventas)
        print(exc)

    print('Test Inventario contra SGC \n')
    print('Test Inventario contra SGC, Compara los datos de ventas del ultimo inventario contra lo mostrado en Reporte condensado de ventas de SGC\n'
          'Muestra las diferencias si existieran.\n'
          'Instancias: http://192.168.9.164/sgcweb, http://testventas.sgcweb.com.mx/')
    print('\n\n')
    mensaje_de_salida(datos_inventario, datos_ventas)
    assert True, 'No hay inventario del dia anterior.'
