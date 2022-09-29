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
        print(dato, ': ', valor)
    print('-------------------------------------------')


def test_inventario_vs_ventas(driver, name='administrador', password='administrador', name_web='admin', password_web='Ku8L08iEsb86'):
    datos_inventario = {}
    datos_ventas = {}
    productos = {}
    try:
        login(driver, name, password)
        time.sleep(2)
        # sacar fechas del inventario
        boton_inventario = driver.find_element(By.XPATH, '//*[@id="grouptab_7"]')
        boton_inventario.click()
        hora = datetime.datetime.now()
        # if hora.hour >= 13:
        #     dia_inventario = datetime.date.today()
        #     dia_inventario = dia_inventario - datetime.timedelta(days=1)
        # else:
        #     dia_inventario = datetime.date.today()
        #     dia_inventario = dia_inventario - datetime.timedelta(days=2)
        dia_inventario = datetime.datetime.strptime('2022-09-13 13:00', '%Y-%m-%d %H:%M')
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
            dia1 = datetime.datetime.strptime(fecha_inicial, '%Y-%m-%d %H:%M:%S')
            dia1 = dia1.weekday()
            dia2 = datetime.datetime.strptime(fecha_final, '%Y-%m-%d %H:%M:%S')
            dia2 = dia2.weekday()
            # revisar si el inventario es domingo
            if (dia1 == 5 and dia2 == 6) or (dia1 == 6 and dia2 == 0 and hora.hour > 13):
                boton_inventario = driver.find_element(By.XPATH, '//*[@id="grouptab_7"]')
                boton_inventario.click()
                hora = datetime.datetime.now()
                # if hora.hour >= 13:
                #     dia_inventario = datetime.date.today()
                #     dia_inventario = dia_inventario - datetime.timedelta(days=3)
                # else:
                #     dia_inventario = datetime.date.today()
                #     dia_inventario = dia_inventario - datetime.timedelta(days=4)
                dia_inventario = datetime.datetime.strptime('2022-09-13 13:00', '%Y-%m-%d %H:%M')
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
            hora_1.select_by_value(solo_hora[0])
            min_1 = Select(driver.find_element(By.XPATH, '//*[@id="_minuto_0"]'))
            if solo_hora[1] == '00':
                min_1.select_by_value('0')
            else:
                min_1.select_by_value(solo_hora[1])
            # se manda la segunda fecha
            fecha_2 = fecha_final.split(' ')
            solo_fecha = fecha_2[0]
            solo_hora = fecha_2[1]
            solo_hora = solo_hora.split(':')
            rango1 = driver.find_element(By.XPATH, '//*[@id="_fecha2_0"]')
            rango1.clear()
            rango1.send_keys(solo_fecha)
            hora_1 = Select(driver.find_element(By.XPATH, '//*[@id="_hora2_0"]'))
            hora_1.select_by_value(solo_hora[0])
            min_1 = Select(driver.find_element(By.XPATH, '//*[@id="_minuto2_0"]'))
            if solo_hora[1] == '00':
                min_1.select_by_value('0')
            else:
                min_1.select_by_value(solo_hora[1])
            ver_reporte = driver.find_element(By.XPATH, '//*[@id="btn_ver_reporte"]')
            ver_reporte.click()
            time.sleep(10)
            # seleccionamos la tabla si existe
            if check_exists_by_xpath(driver, '//*[@id="_preViewReport"]/table/tbody/tr[2]/td[3]'):
                tabla_ventas = driver.find_element(By.XPATH, '//*[@id="_preViewReport"]/table/tbody')
                tabla_ventas_len = len(tabla_ventas.find_elements(By.TAG_NAME, 'tr'))
                i = 2
            else:
                mensaje_de_salida(datos_inventario, datos_ventas)
                assert False, 'No hay datos en el condensado de datos'
            # empezamos a contar los productos y a separarlos
            datos_ventas['Auto medido'] = 0
            productos['Auto medido'] = 0
            while i < tabla_ventas_len:
                nombre = driver.find_element(By.XPATH, f'//*[@id="_preViewReport"]/table/tbody/tr[{i}]/td[3]').text
                cantidad = driver.find_element(By.XPATH, f'//*[@id="_preViewReport"]/table/tbody/tr[{i}]/td[4]').text
                unidad = driver.find_element(By.XPATH, f'//*[@id="_preViewReport"]/table/tbody/tr[{i}]/td[2]').text
                if 'GLP1' in nombre or 'Cilindro' in nombre or 'cilindro' in nombre:
                    if 'GLP1' in nombre and 'C' in unidad:
                        datos_ventas['Auto medido'] = float(datos_ventas['Auto medido']) + float(cantidad)
                        productos['Auto medido'] = float(productos['Auto medido']) + float(cantidad)
                        i += 1
                    elif nombre in productos:
                        datos_ventas[nombre] = float(datos_ventas[nombre]) + float(cantidad)
                        productos[nombre] = float(productos[nombre]) + float(cantidad)
                        i += 1
                    else:
                        datos_ventas[nombre] = cantidad
                        productos[nombre] = cantidad
                        i += 1
            datos_ventas['GLP1'] = float(datos_ventas['GLP1']) + float(datos_ventas['Auto medido'])
            # if datos_ventas['GLP1'] != carga_autotanque:
            #     mensaje_de_salida(datos_inventario, datos_ventas)
            #     assert False, 'Las ventas de GLP1 no cuadran con el inventario de carga de autotanques'
            admin = driver.find_element(By.XPATH, '//*[@id="globalLinks"]/ul/li[3]/a')
            datos_ventas['Total peso vendido'] = 0
            for x in productos.keys():
                if x != 'GLP1' and x != 'Auto medido':
                    time.sleep(3)
                    admin = driver.find_element(By.XPATH, '//*[@id="globalLinks"]/ul/li[3]/a')
                    admin.click()
                    time.sleep(3)
                    productos_link = driver.find_element(By.XPATH, '//*[@id="content"]/table/tbody/tr/td/table[14]/tbody/tr[6]/td[3]/a')
                    productos_link.click()
                    time.sleep(1)
                    buscar_nombre = driver.find_element(By.XPATH, '//*[@id="name_basic"]')
                    buscar_nombre.send_keys(x)
                    buscar_nombre.submit()
                    time.sleep(3)
                    seleccion = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody/tr[3]/td[2]/a')
                    seleccion.click()
                    time.sleep(3)
                    peso = x.split(' ')
                    factor_densidad = driver.find_element(By.XPATH, '//*[@id="factor_densidad"]').text
                    datos_ventas['Factor densidad '+f'{x}'] = factor_densidad
                    datos_ventas['Peso '+f'{x}'] = float(datos_ventas[x]) * float(peso[1])
                    datos_ventas['Peso '+f'{x} convertido'] = float(datos_ventas['Peso '+f'{x}']) / float(datos_ventas['Factor densidad '+f'{x}'])
                    datos_ventas['Peso ' + f'{x} convertido'] = str(round(datos_ventas['Peso ' + f'{x} convertido'], 2))
                    datos_ventas['Total peso vendido'] = float(datos_ventas['Total peso vendido']) + float(datos_ventas['Peso ' + f'{x} convertido'])
                    datos_ventas['Peso ' + f'{x} convertido'] = datos_ventas['Peso ' + f'{x} convertido'] + ' lt'
            # if datos_ventas['Total peso vendido'] != datos_inventario['Anden']:
            #     mensaje_de_salida(datos_inventario, datos_ventas)
            #     assert False, 'El total vendido no cuadra con el anden reportado en inventario.'
            # if datos_ventas['GLP1'] != datos_inventario['Carga autotanque']:
            #     mensaje_de_salida(datos_inventario, datos_ventas)
            #     assert False, 'El total vendido no cuadra con el anden reportado en inventario.'
        else:
            mensaje_de_salida(datos_inventario, datos_ventas)
            assert False, 'No hay inventario del dia anterior.'

    except NoSuchElementException as exc:
        mensaje_de_salida(datos_inventario, datos_ventas)
        print(exc)
    mensaje_de_salida(datos_inventario, datos_ventas)
    assert False, 'No hay inventario del dia anterior.'
