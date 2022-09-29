import time
import datetime
import math
from decimal import Decimal as d
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from funciones.function import login, check_exists_by_xpath, convertir_fecha_24
from selenium.common.exceptions import NoSuchElementException


def test_anden(driver, name='administrador', password='administrador'):
    datos = {}
    dia = ''
    fecha_inicial = '2022-09-22 13:00:00'
    fecha_final = '2022-09-23 13:00:00'
    try:
        login(driver, name, password)
        time.sleep(1)
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
        datos['Dia inventario'] = '2022-09-22'
        fecha = driver.find_element(By.XPATH, '//*[@id="inventario_basic"]')
        fecha.send_keys(datos['Dia inventario'])
        fecha.send_keys(Keys.ENTER)
        time.sleep(1)
        # fecha inicial del inventario
        if check_exists_by_xpath(driver, '//*[@id="MassUpdate"]/table/tbody/tr[3]/td[1]/a'):
            documento = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody/tr[3]/td[1]/a')
            documento.click()
            time.sleep(1)
            datos['Fecha inicial inventario'] = fecha_inicial
            # fecha final del inventario
            datos['Fecha Final del Inventario'] = fecha_final
            dia1 = datetime.datetime.strptime(fecha_inicial, '%Y-%m-%d %H:%M:%S')
            dia1 = dia1.weekday()
            dia2 = datetime.datetime.strptime(fecha_final, '%Y-%m-%d %H:%M:%S')
            dia2 = dia2.weekday()
            boton_inventario = driver.find_element(By.XPATH, '//*[@id="grouptab_7"]')
            boton_inventario.click()
            hora = datetime.datetime.now()
            # revisar si el inventario es domingo
            if (dia1 == 5 and dia2 == 6) or (dia1 == 6 and dia2 == 0 and hora.hour < 13):
                if hora.hour >= 13:
                    dia_inventario = datetime.date.today()
                    dia_inventario = dia_inventario - datetime.timedelta(days=3)
                else:
                    dia_inventario = datetime.date.today()
                    dia_inventario = dia_inventario - datetime.timedelta(days=4)
                datos['Dia inventario'] = dia_inventario
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
                    datos['Fecha inicial inventario'] = fecha_inicial
                    # fecha final del inventario
                    datos['Fecha Final del Inventario'] = fecha_final
                else:
                    print('No hay invetario del dia anterior, Datos: \n')
                    for dato, valor in datos.items():
                        print(dato, ': ', valor)
                    assert False, 'No hay invetario del dia anterior.'
            time.sleep(1)
            # Nos movemos a Anden
            anden = driver.find_element(By.XPATH, '//*[@id="grouptab_1"]')
            anden.click()
            llenados_terminal = driver.find_element(By.XPATH, '//*[@id="ul_shortcuts"]/li[2]/a')
            llenados_terminal.click()
            # mandamos las fechas del inventario
            fecha1 = driver.find_element(By.XPATH, '//*[@id="fecha1"]')
            fecha1.clear()
            fecha1.send_keys(fecha_inicial)
            time.sleep(2)
            fecha2 = driver.find_element(By.XPATH, '//*[@id="fecha2"]')
            fecha2.clear()
            fecha2.send_keys(fecha_final)
            time.sleep(2)
            fecha2.send_keys(Keys.ENTER)
            time.sleep(3)
            lista_detallado = driver.find_element(By.XPATH, '//*[@id="reporteLlenados"]/tbody')
            lista_detallado_len = len(lista_detallado.find_elements(By.TAG_NAME, 'tr'))
            if lista_detallado_len > 2:
                # sacamos el peso aplicado y hacemos la comparativas de los datos en anden( total de llenados, peso final, peso programado, diferencia, peso aplicado)
                total_llenados = driver.find_element(By.XPATH, '//*[@id="tTotales"]/tbody/tr[2]/td[1]').text
                datos['total_llenados'] = total_llenados
                total_detallado = driver.find_element(By.XPATH, f'/html[1]/body[1]/div[4]/div[3]/table[1]/tbody[1]/tr[1]/td[1]/div[2]/table[1]/tbody[1]/tr[{lista_detallado_len}]/td[2]').text
                datos['total_detallado'] = total_detallado
                if total_detallado != total_llenados:
                    print('Los totales no coinciden, Datos: \n')
                    for dato, valor in datos.items():
                        print(dato, ': ', valor)
                    assert False, f'Los totales no coinciden.'
                peso_final = driver.find_element(By.XPATH, '//*[@id="tTotales"]/tbody/tr[2]/td[2]').text
                datos['peso_final'] = peso_final
                peso_final_detallado = driver.find_element(By.XPATH, f'//*[@id="reporteLlenados"]/tbody/tr[{lista_detallado_len}]/td[3]').text
                datos['peso_final_detallado'] = peso_final_detallado
                if peso_final_detallado != peso_final:
                    print('Los pesos finales no coinciden, Datos: \n')
                    for dato, valor in datos.items():
                        print(dato, ': ', valor)
                    assert False, f'Los pesos finales no coinciden.'
                peso_programado = driver.find_element(By.XPATH, '//*[@id="tTotales"]/tbody/tr[2]/td[3]').text
                datos['peso_programado'] = peso_programado
                peso_programado_detallado = driver.find_element(By.XPATH, f'//*[@id="reporteLlenados"]/tbody/tr[{lista_detallado_len}]/td[4]').text
                datos['peso_programado_detallado'] = peso_programado_detallado
                peso_programado = peso_programado.replace(' ', '')
                peso_programado = peso_programado.replace('kg', '')
                peso_programado_detallado = peso_programado_detallado.replace(' ', '')
                peso_programado_detallado = peso_programado_detallado.replace('kg', '')
                if peso_programado != peso_programado_detallado:
                    print('Los pesos programados no coinciden, Datos: \n')
                    for dato, valor in datos.items():
                        print(dato, ': ', valor)
                    assert False, f'Los pesos programados no coinciden.'
                diferencia = driver.find_element(By.XPATH, '//*[@id="tTotales"]/tbody/tr[2]/td[4]').text
                diferencia = diferencia.replace('kg', '')
                diferencia = diferencia.replace('g', '')
                diferencia = diferencia.replace(' ', '')
                datos['diferencia'] = diferencia
                peso_final = peso_final.replace('kg', '')
                peso_final = peso_final.replace('g', '')
                peso_final = peso_final.replace(' ', '')
                diferencia_real = d(peso_programado) - d(peso_final)
                if diferencia_real < 1:
                    diferencia_real = (diferencia_real * 1000)
                    diferencia_real = math.ceil(diferencia_real)
                datos['diferencia_real'] = diferencia_real
                if diferencia_real != d(diferencia):
                    print('La diferencia nos coincide con los valores, Datos: \n')
                    for dato, valor in datos.items():
                        print(dato, ': ', valor)
                    assert False, f'La diferencia nos coincide con los valores.'
                peso_aplicado = driver.find_element(By.XPATH, '//*[@id="tTotales"]/tbody/tr[2]/td[5]').text
                peso_aplicado_detallado = driver.find_element(By.XPATH, f'//*[@id="reporteLlenados"]/tbody/tr[{lista_detallado_len}]/td[5]').text
                datos['Peso aplicado'] = peso_aplicado
                peso_aplicado = peso_aplicado.replace('kg', '')
                peso_aplicado = peso_aplicado.replace('g', '')
                peso_aplicado = peso_aplicado.replace(' ', '')
                datos['Peso aplicado detallado'] = peso_aplicado_detallado
                peso_aplicado_detallado = peso_aplicado_detallado.replace('kg', '')
                peso_aplicado_detallado = peso_aplicado_detallado.replace('g', '')
                peso_aplicado_detallado = peso_aplicado_detallado.replace(' ', '')
                if peso_aplicado != peso_aplicado_detallado:
                    print('Los pesos aplicados son diferentes, Datos: \n')
                    for dato, valor in datos.items():
                        print(dato, ': ', valor)
                    assert False, f'Los pesos aplicados son diferentes.'
                # nos movemos a auditor anden
                time.sleep(3)
                auditor_anden = driver.find_element(By.XPATH, '//*[@id="grouptab_5"]')
                auditor_anden.click()
                reporte_gral = driver.find_element(By.XPATH, '//*[@id="ul_shortcuts"]/li[2]/a')
                reporte_gral.click()
                fecha_auditor1 = driver.find_element(By.XPATH, '//*[@id="fecha1"]')
                fecha_auditor2 = driver.find_element(By.XPATH, '//*[@id="fecha2"]')
                fecha_auditor1.clear()
                fecha_auditor2.clear()
                fecha_auditor1.send_keys(fecha_inicial)
                fecha_auditor2.send_keys(fecha_final)
                time.sleep(2)
                fecha_auditor2.send_keys(Keys.ENTER)
                time.sleep(5)
                llenado = driver.find_element(By.XPATH, '//*[@id="lienzo"]/table[1]/tbody/tr[2]/td[1]').text
                datos['Llenado'] = llenado
                llenado = llenado.replace('kg', '')
                llenado = llenado.replace('g', '')
                llenado = llenado.replace(' ', '')
                if llenado != peso_aplicado:
                    print('El peso aplicado no concuerda con el llenado, Datos: \n')
                    for dato, valor in datos.items():
                        print(dato, ': ', valor)
                    assert False, f'El peso aplicado no concuerda con el llenado.'
                porcentaje = float(llenado) * .01
                datos['Diferencia tolerable'] = porcentaje
                masico = driver.find_element(By.XPATH, '//*[@id="lienzo"]/table[1]/tbody/tr[2]/td[2]').text
                datos['masico'] = masico
                masico = masico.replace('kg', '')
                masico = masico.replace('g', '')
                masico = masico.replace(' ', '')
                datos['Diferencia masico'] = float(llenado) - float(masico)
                datos['Diferencia masico'] = abs(datos['Diferencia masico'])
                if abs(datos['Diferencia masico']) > porcentaje:
                    print('La diferencia entre masico y el llenado es superior al 1%, Datos: \n')
                    for dato, valor in datos.items():
                        print(dato, ': ', valor)
                    assert False, f'La diferencia entre masico y el llenado es superior al 1% .'
                else:
                    print('Prueba correcta los datos coinciden: \n')
                    for dato, valor in datos.items():
                        print(dato, ': ', valor)
                    assert datos['Diferencia masico'] < porcentaje, 'Prueba con errores'
            else:
                print('Datos: \n')
                for dato, valor in datos.items():
                    print(dato, ': ', valor)
                assert False, 'No hay informacion de esas fechas.'

        else:
            print('No hay invetario del dia anterior, Datos: \n')
            for dato, valor in datos.items():
                print(dato, ': ', valor)
            assert False, 'No hay invetario del dia anterior.'

    except NoSuchElementException as exc:
        print(exc)
        print('Datos: \n')
        for dato, valor in datos.items():
            print(dato, ': ', valor)
        assert False, 'Error en la prueba.'


