import time
import datetime
import math
from decimal import Decimal as d
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from funciones.function import login, login_web, check_exists_by_xpath, convertir_fecha_24
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


def test_inventario_vs_salidas_tanque(driver, name='administrador', password='administrador', name_web='admin', password_web='Ku8L08iEsb86'):
    datos_inventario = {}
    datos_ventas = {}
    try:
        login(driver, name, password)
        time.sleep(2)
        # sacar fechas del inventario
        boton_inventario = driver.find_element(By.XPATH, '//*[@id="grouptab_7"]')
        boton_inventario.click()
        hora = datetime.datetime.now()
        if hora.hour >= 13:
            dia_inventario = datetime.date.today()
            dia_inventario = dia_inventario - datetime.timedelta(days=1)
        else:
            dia_inventario = datetime.date.today()
            dia_inventario = dia_inventario - datetime.timedelta(days=2)
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
                if hora.hour >= 13:
                    dia_inventario = datetime.date.today()
                    dia_inventario = dia_inventario - datetime.timedelta(days=3)
                else:
                    dia_inventario = datetime.date.today()
                    dia_inventario = dia_inventario - datetime.timedelta(days=4)
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
            # sacamoss los datos a revisar carga auotanque y auditor
            time.sleep(2)
            carga_autotanques = driver.find_element(By.XPATH, '//*[@id="lienzo"]/table[5]/tbody/tr[2]/td[2]').text
            datos_inventario['carga_autotanqes'] = carga_autotanques
            carga_autotanques = carga_autotanques.replace(' ', '')
            carga_autotanques = carga_autotanques.replace(',', '')
            carga_autotanques = carga_autotanques.replace('kg', '')
            carga_autotanques = carga_autotanques.replace('lt', '')
            auditor = driver.find_element(By.XPATH, '//*[@id="lienzo"]/table[5]/tbody/tr[3]/td[2]').text
            datos_inventario['Auditor'] = auditor
            auditor = auditor.replace(' ', '')
            auditor = auditor.replace(',', '')
            auditor = auditor.replace('kg', '')
            auditor = auditor.replace('lt', '')
            total_tanque = driver.find_element(By.XPATH, '//*[@id="lienzo"]/table[5]/tbody/tr[5]/td[2]').text
            datos_inventario['Total salidas del tanque'] = total_tanque
            total_tanque = total_tanque.replace(' ', '')
            total_tanque = total_tanque.replace(',', '')
            total_tanque = total_tanque.replace('kg', '')
            total_tanque = total_tanque.replace('lt', '')
            inventario_movimiento = driver.find_element(By.XPATH, '//*[@id="lienzo"]/table[3]/tbody/tr[4]/td[2]').text
            inventario_movimiento = inventario_movimiento.replace(' ', '')
            inventario_movimiento = inventario_movimiento.replace(',', '')
            inventario_movimiento = inventario_movimiento.replace('kg', '')
            inventario_movimiento = inventario_movimiento.replace('lt', '')
            datos_inventario['Inventario en movimiento'] = inventario_movimiento
            salidas_venta = driver.find_element(By.XPATH, '//*[@id="lienzo"]/table[3]/tbody/tr[5]/td[2]').text
            datos_inventario['Salidas venta'] = salidas_venta
            salidas_venta = salidas_venta.replace(' ', '')
            salidas_venta = salidas_venta.replace(',', '')
            salidas_venta = salidas_venta.replace('kg', '')
            salidas_venta = salidas_venta.replace('lt', '')
            suma = float(inventario_movimiento) + float(salidas_venta)
            suma = round(suma, 2)
            suma_total_tanque = float(carga_autotanques) + float(auditor)
            suma_total_tanque = round(suma_total_tanque, 2)
            # se comprueba si los datos en inventario cuadran
            if float(suma_total_tanque) != float(total_tanque):
                mensaje_de_salida(datos_inventario, datos_ventas)
                assert False, 'La suma de la carga de autotanques + el auditor no cuadra con el total'
            if float(suma) != float(total_tanque):
                mensaje_de_salida(datos_inventario, datos_ventas)
                assert False, 'La suma del inventario en movimiento mas las salidas venta no cuadra con el total de salidas del tanque'
            # nos movemos a auditor anden
            auditor_anden = driver.find_element(By.XPATH, '//*[@id="grouptab_5"]')
            auditor_anden.click()
            busqueda_avanzada = driver.find_element(By.XPATH, '//*[@id="tab_link_isies_registros_masico|advanced_search"]')
            busqueda_avanzada.click()
            fecha_1 = driver.find_element(By.XPATH, '//*[@id="fecha_final_advanced"]')
            fecha_1.send_keys(fecha_inicial)
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
                datos_inventario['Ultimo registro'] = ultimo_registro
                flecha = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{lista_len - 2}]/td/table/tbody/tr/td[2]/button[4]')
                if flecha.is_enabled():
                    flecha.click()
                    time.sleep(2)
                    lista2 = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody')
                    lista2_len = len(lista2.find_elements(By.TAG_NAME, 'tr'))
                    datos_inventario['len'] = lista2_len
                    primer_registro = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{lista2_len - 3}]/td[5]').text
                    primer_registro = primer_registro.replace(',', '')
                    datos_inventario['Primer registro'] = primer_registro
                else:
                    time.sleep(2)
                    lista2 = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody')
                    lista2_len = len(lista2.find_elements(By.TAG_NAME, 'tr'))
                    datos_inventario['len'] = lista2_len
                    primer_registro = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{lista2_len - 3}]/td[5]').text
                    primer_registro = primer_registro.replace(',', '')
                    datos_inventario['Primer registro'] = primer_registro
                resta = float(datos_inventario['Ultimo registro']) - float(datos_inventario['Primer registro'])
                resta = round(resta, 2)
                datos_inventario['Diferencia entre primer y ultimo registro Auditor anden'] = resta
                # revisamos si el auditor cuadra con los datos de auditor anden
                if resta != float(auditor):
                    mensaje_de_salida(datos_inventario, datos_ventas)
                    assert False, 'Diferencia entre el auditor de inventario y el registro de auditor anden'
            # nos movemos a carga
            carga = driver.find_element(By.XPATH, '//*[@id="grouptab_3"]')
            carga.click()
            busqueda_avanzada2 = driver.find_element(By.XPATH, '//*[@id="tab_link_isies_servicios_carga|advanced_search"]')
            busqueda_avanzada2.click()
            fecha_3 = driver.find_element(By.XPATH, '//*[@id="fecha_final_advanced"]')
            fecha_4 = driver.find_element(By.XPATH, '//*[@id="fecha_final1_advanced"]')
            fecha_3.send_keys(fecha_inicial)
            fecha_4.send_keys(fecha_final)
            fecha_4.send_keys(Keys.ENTER)
            time.sleep(2)
            tabla_carga = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody')
            tabla_carga_len = len(tabla_carga.find_elements(By.TAG_NAME, 'tr'))
            tabla_carga_len -= 2
            i = 3
            if check_exists_by_xpath(driver, '//*[@id="MassUpdate"]/table/tbody/tr[3]'):
                total = 0
                while i < tabla_carga_len:
                    valor = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[5]').text
                    valor = valor.replace(',', '')
                    total = total + float(valor)
                    i += 1
                datos_inventario['Total en carga'] = total
            # revisamos si los datos en carga de autotanques cuadra con el mismo campo de inventarios
            if datos_inventario['Total en carga'] != float(carga_autotanques):
                mensaje_de_salida(datos_inventario, datos_ventas)
                assert False, 'No hay inventario del dia anterior.'

        else:
            mensaje_de_salida(datos_inventario, datos_ventas)
            assert False, 'No hay inventario del dia anterior.'

    except NoSuchElementException as exc:
        mensaje_de_salida(datos_inventario, datos_ventas)
        print(exc)
        assert False, 'No hay inventario del dia anterior.'
    mensaje_de_salida(datos_inventario, datos_ventas)
    assert True, 'No hay inventario del dia anterior.'