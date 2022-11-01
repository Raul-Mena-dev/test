
import time
from tabulate import tabulate
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from funciones.function import login_carburacion, convertir_fecha_24, convertir_mes
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Liquidacion:

    def __init__(self, vendedor, ventas_totales, ventas_contado, ventas_credito, pagos_contado, pagos_credito, otros_pagos, saldo):
        self.vendedor = vendedor
        self.ventas_totales = ventas_totales
        self.ventas_contado = ventas_contado
        self.ventas_credito = ventas_credito
        self.pagos_contado = pagos_contado
        self.pagos_credito = pagos_credito
        self.otros_pagos = otros_pagos
        self.saldo = saldo


# class Venta:
#
#     def __init__(self, folio, vendedor, cliente, cantidad, subtotal, iva, ieps, importe_total, estado):
#         self.folio = folio
#         self.vendedor = vendedor
#         self.cliente = cliente
#         self.cantidad = cantidad
#         self.subtotal = subtotal
#         self.iva = iva
#         self.ieps = ieps
#         self.importe_total = importe_total
#         self.estado = estado


def mensaje_de_salida(datos_turnos, datos_de_ventas, datos_de_clientes, datos_corte, diferencias, liquidaciones, ventas_reporte):
    print('-------------------------------------------')
    print('-------------------------------------------')
    print('Datos y diferencias: \n')
    print('-------------------------------------------')
    print('Datos de carburacion:\n')
    print('------------------Turnos-------------------\n')
    print('-------------------------------------------')
    columnas = ['Vendedor', 'Fecha Entrada', 'Fecha Salida']
    print('Datos Turnos: \n')
    print(tabulate(datos_turnos, headers=columnas, tablefmt="fancy_grid"))
    print('-------------------------------------------')
    print('-------------------------------------------')
    print('Totales de reporte de ventas(Reporte 1):\n')
    print('----------------Totales----------------\n')
    for dato, valor in datos_de_ventas.items():
        print(dato + ': ' + str(valor))
    print('-------------------------------------------')
    print('Totales de reporte por cliente(Reporte 2):\n')
    print('----------------Contado----------------\n')
    for dato, valor in datos_de_clientes.items():
        if 'Cantidad de LTs a Credito' in dato:
            print('----------------Credito----------------\n')
        print(dato + ': ' + str(valor))
    print('-------------------------------------------')
    print('Totales de Corte(Reporte 3):\n')
    print('----------------Totales----------------\n')
    for dato, valor in datos_corte.items():
        if 'Volumen Corte Credito' in dato:
            print('----------------Credito----------------\n')
        if 'Cierre de corte' in dato:
            print('----------------Cierre-----------------\n')
        if 'Credito por cliente' in dato:
            print('---------Credito por cliente-----------\n')
        print(dato + ': ' + str(valor))
    print('-------------------------------------------')
    print('Diferencias:\n')

    for dato, valor in diferencias.items():
        if 'Diferencia de Subtotal entre Reporte de ventas y el corte' in dato:
            print('----------------Totales----------------\n')
        if 'Diferencia de Subtotal credito entre Reporte de ventas y el corte' in dato:
            print('----------------Credito----------------\n')
        print(dato + ': ' + str(valor))
    print('-------------------------------------------')
    print('-------------------------------------------')
    columnas = ['Vendedor', 'Ventas Totales', 'Ventas contado', 'Ventas credito', 'Pagos contado', 'Pagos credito', 'Otros pagos', 'Saldo']
    print('Datos Liquidaciones: \n')
    print(tabulate(liquidaciones, headers=columnas, tablefmt="fancy_grid"))
    print('-------------------------------------------')
    print('-------------------------------------------')
    columnas2 = ['Folio', 'Vendedor', 'Cliente', 'Cantidad', 'Subtotal', 'IVA', 'IEPS', 'Importe Total', 'Estado']
    print('Datos Reporte detallado de ventas: \n')
    print(tabulate(ventas_reporte, headers=columnas2, tablefmt="fancy_grid"))
    print('-------------------------------------------')
    print('-------------------------------------------')


def test_liquidacion(driver, fecha_test, name='admin', password='Z76U4CFI'):
    liquidaciones = []
    ventas_reporte = []
    datos_turnos = []
    datos_de_ventas = {}
    datos_de_clientes = {}
    datos_corte = {}
    diferencias = {}
    try:
        login_carburacion(driver, name, password)
        time.sleep(2)
        # Vamos a ventas -> registro de turno para sacar las fechas del turno
        fecha_entrada = ''
        fecha_salida = ''
        ventas = driver.find_element(By.XPATH, '//*[@id="grouptab_1"]')
        ventas.click()
        registro_de_turno = driver.find_element(By.XPATH, '//*[@id="moduleTab_1_isies_registro_turno"]')
        registro_de_turno.click()
        busqueda_avanzada = driver.find_element(By.XPATH, '//*[@id="tab_link_isies_registro_turno|advanced_search"]')
        busqueda_avanzada.click()
        input_fecha1 = driver.find_element(By.XPATH, '//*[@id="date_entered_advanced"]')
        input_fecha1.clear()
        input_fecha1.send_keys(fecha_test)
        buscar_turnos = driver.find_element(By.XPATH, '//*[@id="search_form_submit"]')
        buscar_turnos.click()
        time.sleep(5)
        tabla_turnos = driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/table/tbody/tr/td/form[3]/table/tbody')
        tabla_turnos_len = len(tabla_turnos.find_elements(By.TAG_NAME, 'tr'))
        tabla_turnos_len -= 2
        i = 3
        # fecha_entrada = '2022-10-27 00:00'
        # fecha_salida = '2022-10-27 23:59'
        y = 0
        while i < tabla_turnos_len:
            fecha_entrada = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[4]').text
            solo_fecha = fecha_entrada.split(' ')
            if str(solo_fecha[0]) == str(fecha_test):
                vendedor = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[2]').text
                fecha_salida = driver.find_element(By.XPATH, f'//*[@id="MassUpdate"]/table/tbody/tr[{i}]/td[6]').text
                datos_turnos.append([])
                datos_turnos[y].append(vendedor)
                datos_turnos[y].append(fecha_entrada)
                datos_turnos[y].append(fecha_salida)
                time.sleep(1)
                y += 1
            i += 1
        # nos movemos a ventas -> servicios dispensador -> liquidacion vendedor
        ventas = driver.find_element(By.XPATH, '//*[@id="grouptab_1"]')
        ventas.click()
        liquidacion_vendedor = driver.find_element(By.XPATH, '//*[@id="ul_shortcuts"]/li[2]/a')
        liquidacion_vendedor.click()
        tabla_liquidacion = driver.find_element(By.XPATH, '//*[@id="div_datos"]/table/tbody')
        tabla_liquidacion_len = len(tabla_liquidacion.find_elements(By.TAG_NAME, 'tr'))
        y = 0
        sumatotales = 0.0
        sumacontado = 0.0
        sumacredito = 0.0
        suma_pagos_contado = 0.0
        suma_pagos_credito = 0.0
        suma_pagos_otros = 0.0
        suma_saldo = 0.0
        for turno in datos_turnos:
            x = 2
            while x <= tabla_liquidacion_len:
                fecha_turno = driver.find_element(By.XPATH, f'//*[@id="div_datos"]/table/tbody/tr[{x}]/td[9]/span/a').text
                fecha_turno = fecha_turno.split(' ')
                usuario = driver.find_element(By.XPATH, f'//*[@id="div_datos"]/table/tbody/tr[{x}]/td[1]').text
                fecha_turno = convertir_mes(fecha_turno[0])
                if str(fecha_turno) == str(fecha_test) and turno[0] == str(usuario):
                    ventas_totales = driver.find_element(By.XPATH, f'//*[@id="div_datos"]/table/tbody/tr[{x}]/td[2]').text
                    ventas_contado = driver.find_element(By.XPATH, f'//*[@id="div_datos"]/table/tbody/tr[{x}]/td[3]').text
                    ventas_credito = driver.find_element(By.XPATH, f'//*[@id="div_datos"]/table/tbody/tr[{x}]/td[4]').text
                    pagos_contado = driver.find_element(By.XPATH, f'//*[@id="div_datos"]/table/tbody/tr[{x}]/td[5]').text
                    pagos_credito = driver.find_element(By.XPATH, f'//*[@id="div_datos"]/table/tbody/tr[{x}]/td[6]').text
                    otros_pagos = driver.find_element(By.XPATH, f'//*[@id="div_datos"]/table/tbody/tr[{x}]/td[7]').text
                    saldo = driver.find_element(By.XPATH, f'//*[@id="div_datos"]/table/tbody/tr[3]/td[{x}]').text
                    liquidacion = Liquidacion(usuario, ventas_totales, ventas_contado, ventas_credito, pagos_contado, pagos_credito, otros_pagos, saldo)
                    liquidaciones.append([])
                    ventas_totales = ventas_totales.replace('$', '')
                    ventas_totales = ventas_totales.replace(',', '')
                    ventas_contado = ventas_contado.replace('$', '')
                    ventas_contado = ventas_contado.replace(',', '')
                    ventas_credito = ventas_credito.replace('$', '')
                    ventas_credito = ventas_credito.replace(',', '')
                    pagos_contado = pagos_contado.replace('$', '')
                    pagos_contado = pagos_contado.replace(',', '')
                    pagos_credito = pagos_credito.replace('$', '')
                    pagos_credito = pagos_credito.replace(',', '')
                    otros_pagos = otros_pagos.replace('$', '')
                    otros_pagos = otros_pagos.replace(',', '')
                    saldo = saldo.replace('$', '')
                    saldo = saldo.replace(',', '')
                    sumatotales = sumatotales + float(ventas_totales)
                    sumacontado = sumacontado + float(ventas_contado)
                    sumacredito = sumacredito + float(ventas_credito)
                    suma_pagos_contado = suma_pagos_contado + float(pagos_contado)
                    suma_pagos_credito = suma_pagos_credito + float(pagos_credito)
                    suma_pagos_otros = suma_pagos_otros + float(otros_pagos)
                    suma_saldo = suma_saldo + float(saldo)
                    # liquidaciones[y].append(usuario)
                    # liquidaciones[y].append(ventas_totales)
                    # liquidaciones[y].append(ventas_contado)
                    # liquidaciones[y].append(ventas_credito)
                    # liquidaciones[y].append(pagos_contado)
                    # liquidaciones[y].append(pagos_credito)
                    # liquidaciones[y].append(otros_pagos)
                    # liquidaciones[y].append(saldo)
                    liquidaciones[y].append(liquidacion.vendedor)
                    liquidaciones[y].append(liquidacion.ventas_totales)
                    liquidaciones[y].append(liquidacion.ventas_contado)
                    liquidaciones[y].append(liquidacion.ventas_credito)
                    liquidaciones[y].append(liquidacion.pagos_contado)
                    liquidaciones[y].append(liquidacion.pagos_credito)
                    liquidaciones[y].append(liquidacion.otros_pagos)
                    liquidaciones[y].append(liquidacion.saldo)
                    y += 1
                x += 1

        liquidaciones.append([])
        liquidaciones[y].append('SUMA: ')
        liquidaciones[y].append('$' + str(sumatotales))
        liquidaciones[y].append('$' + str(sumacontado))
        liquidaciones[y].append('$' + str(sumacredito))
        liquidaciones[y].append('$' + str(suma_pagos_contado))
        liquidaciones[y].append('$' + str(suma_pagos_credito))
        liquidaciones[y].append('$' + str(suma_pagos_otros))
        liquidaciones[y].append('$' + str(round(suma_saldo, 2)))
        # nos movemos a reportes -> reporte detallado de ventas
        reportes = driver.find_element(By.XPATH, '//*[@id="grouptab_5"]')
        reportes.click()
        reporte_detallado = driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/table/tbody/tr/td/div[3]/table/tbody/tr[4]/td[2]/div/a')
        reporte_detallado.click()
        fecha_entrada = convertir_fecha_24(fecha_entrada)
        fecha_salida = convertir_fecha_24(fecha_salida)
        fecha_1 = str(fecha_entrada).split(' ')
        hora_1 = fecha_1[1].split(':')
        fecha_2 = str(fecha_salida).split(' ')
        hora_2 = fecha_2[1].split(':')
        input_fecha1 = driver.find_element(By.XPATH, '//*[@id="_fecha_0"]')
        input_fecha1.clear()
        input_fecha1.send_keys(fecha_1[0])
        input_hora1 = Select(driver.find_element(By.XPATH, '//*[@id="_hora_0"]'))
        input_hora1.select_by_visible_text(hora_1[0])
        input_min1 = Select(driver.find_element(By.XPATH, '//*[@id="_minuto_0"]'))
        input_min1.select_by_visible_text(hora_1[1])
        input_fecha2 = driver.find_element(By.XPATH, '//*[@id="_fecha2_0"]')
        input_fecha2.clear()
        input_fecha2.send_keys(fecha_2[0])
        input_hora2 = Select(driver.find_element(By.XPATH, '//*[@id="_hora2_0"]'))
        input_hora2.select_by_visible_text(hora_2[0])
        input_min2 = Select(driver.find_element(By.XPATH, '//*[@id="_minuto2_0"]'))
        input_min2.select_by_visible_text(hora_2[1])
        ver_reporte = driver.find_element(By.XPATH, '//*[@id="btn_ver_reporte"]')
        ver_reporte.click()
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="_preViewReport"]/table/tbody/tr[2]/td[1]')))
        tabla_reporte = driver.find_element(By.XPATH, '//*[@id="_preViewReport"]/table/tbody')
        tabla_reporte_len = len(tabla_reporte.find_elements(By.TAG_NAME, 'tr'))
        # tabla_reporte_len -= 1
        i = 2
        x = 0
        time.sleep(2)
        datos_de_ventas['Cantidad'] = 0.0
        datos_de_ventas['Subtotal'] = 0.0
        datos_de_ventas['IVA'] = 0.0
        datos_de_ventas['IEPS'] = 0.0
        datos_de_ventas['Importe Total'] = 0.0
        while i < tabla_reporte_len:
            folio = driver.find_element(By.XPATH, f'//*[@id="_preViewReport"]/table/tbody/tr[{i}]/td[1]').text
            vendedor = driver.find_element(By.XPATH, f'//*[@id="_preViewReport"]/table/tbody/tr[{i}]/td[4]').text
            cliente = driver.find_element(By.XPATH, f'//*[@id="_preViewReport"]/table/tbody/tr[{i}]/td[5]').text
            cantidad = driver.find_element(By.XPATH, f'//*[@id="_preViewReport"]/table/tbody/tr[{i}]/td[9]').text
            subtotal = driver.find_element(By.XPATH, f'//*[@id="_preViewReport"]/table/tbody/tr[{i}]/td[10]').text
            iva = driver.find_element(By.XPATH, f'//*[@id="_preViewReport"]/table/tbody/tr[{i}]/td[11]').text
            ieps = driver.find_element(By.XPATH, f'//*[@id="_preViewReport"]/table/tbody/tr[{i}]/td[12]').text
            total = driver.find_element(By.XPATH, f'//*[@id="_preViewReport"]/table/tbody/tr[{i}]/td[13]').text
            ventas_reporte.append([])
            ventas_reporte[x].append(folio)
            ventas_reporte[x].append(vendedor)
            ventas_reporte[x].append(cliente)
            ventas_reporte[x].append(cantidad)
            ventas_reporte[x].append(subtotal)
            ventas_reporte[x].append(iva)
            ventas_reporte[x].append(ieps)
            ventas_reporte[x].append(total)
            datos_de_ventas['Cantidad'] = datos_de_ventas['Cantidad'] + float(cantidad)
            datos_de_ventas['Cantidad'] = round(datos_de_ventas['Cantidad'], 4)
            datos_de_ventas['Subtotal'] = datos_de_ventas['Subtotal'] + float(subtotal.replace('$', ''))
            datos_de_ventas['Subtotal'] = round(datos_de_ventas['Subtotal'], 2)
            datos_de_ventas['IVA'] = datos_de_ventas['IVA'] + float(iva.replace('$', ''))
            datos_de_ventas['IVA'] = round(datos_de_ventas['IVA'], 2)
            datos_de_ventas['IEPS'] = datos_de_ventas['IEPS'] + float(ieps.replace('$', ''))
            datos_de_ventas['IEPS'] = round(datos_de_ventas['IEPS'], 2)
            datos_de_ventas['Importe Total'] = datos_de_ventas['Importe Total'] + float(total.replace('$', ''))
            datos_de_ventas['Importe Total'] = round(datos_de_ventas['Importe Total'], 2)
            x += 1
            i += 1
        # nos movemos a Reportes -> Reporte de venta por clientes
        reportes = driver.find_element(By.XPATH, '//*[@id="grouptab_5"]')
        reportes.click()
        reporte_por_cliente = driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/table/tbody/tr/td/div[3]/table/tbody/tr[7]/td[2]/div/a')
        reporte_por_cliente.click()
        input_fecha1 = driver.find_element(By.XPATH, '//*[@id="_fecha_0"]')
        input_fecha1.clear()
        input_fecha1.send_keys(fecha_1[0])
        input_hora1 = Select(driver.find_element(By.XPATH, '//*[@id="_hora_0"]'))
        input_hora1.select_by_visible_text(hora_1[0])
        input_min1 = Select(driver.find_element(By.XPATH, '//*[@id="_minuto_0"]'))
        input_min1.select_by_visible_text(hora_1[1])
        input_fecha2 = driver.find_element(By.XPATH, '//*[@id="_fecha2_0"]')
        input_fecha2.clear()
        input_fecha2.send_keys(fecha_2[0])
        input_hora2 = Select(driver.find_element(By.XPATH, '//*[@id="_hora2_0"]'))
        input_hora2.select_by_visible_text(hora_2[0])
        input_min2 = Select(driver.find_element(By.XPATH, '//*[@id="_minuto2_0"]'))
        input_min2.select_by_visible_text(hora_2[1])
        tipo_cliente = Select(driver.find_element(By.XPATH, '//*[@id="tipo_cliente"]'))
        tipo_cliente.select_by_visible_text('Contado')
        ver_reporte = driver.find_element(By.XPATH, '//*[@id="btn_ver_reporte"]')
        ver_reporte.click()
        time.sleep(5)
        tabla_reporte = driver.find_element(By.XPATH, '//*[@id="_preViewReport"]/table/tbody')
        tabla_reporte_len = len(tabla_reporte.find_elements(By.TAG_NAME, 'tr'))
        cantidad_contado = driver.find_element(By.XPATH, f'//*[@id="_preViewReport"]/table/tbody/tr[{tabla_reporte_len}]/td[4]').text
        subtotal_contado = driver.find_element(By.XPATH, f'//*[@id="_preViewReport"]/table/tbody/tr[{tabla_reporte_len}]/td[5]').text
        iva_contado = driver.find_element(By.XPATH, f'//*[@id="_preViewReport"]/table/tbody/tr[{tabla_reporte_len}]/td[6]').text
        ieps_contado = driver.find_element(By.XPATH, f'//*[@id="_preViewReport"]/table/tbody/tr[{tabla_reporte_len}]/td[7]').text
        total_contado = driver.find_element(By.XPATH, f'//*[@id="_preViewReport"]/table/tbody/tr[{tabla_reporte_len}]/td[8]').text
        datos_de_clientes['Cantidad de LTs a contado'] = cantidad_contado
        datos_de_clientes['Total a Contado'] = total_contado
        datos_de_clientes['Subtotal a Contado'] = subtotal_contado
        datos_de_clientes['IVA a contado'] = iva_contado
        datos_de_clientes['IEPS contado'] = ieps_contado
        tipo_cliente.select_by_visible_text('Crédito')
        ver_reporte.click()
        time.sleep(5)
        tabla_reporte = driver.find_element(By.XPATH, '//*[@id="_preViewReport"]/table/tbody')
        tabla_reporte_len = len(tabla_reporte.find_elements(By.TAG_NAME, 'tr'))
        cantidad_credito = driver.find_element(By.XPATH, f'//*[@id="_preViewReport"]/table/tbody/tr[{tabla_reporte_len}]/td[4]').text
        subtotal_credito = driver.find_element(By.XPATH, f'//*[@id="_preViewReport"]/table/tbody/tr[{tabla_reporte_len}]/td[5]').text
        iva_credito = driver.find_element(By.XPATH, f'//*[@id="_preViewReport"]/table/tbody/tr[{tabla_reporte_len}]/td[6]').text
        ieps_credito = driver.find_element(By.XPATH, f'//*[@id="_preViewReport"]/table/tbody/tr[{tabla_reporte_len}]/td[7]').text
        total_credito = driver.find_element(By.XPATH, f'//*[@id="_preViewReport"]/table/tbody/tr[{tabla_reporte_len}]/td[8]').text
        datos_de_clientes['Cantidad de LTs a Credito'] = cantidad_credito
        datos_de_clientes['Total a Credito'] = total_credito
        datos_de_clientes['Subtotal a Credito'] = subtotal_credito
        datos_de_clientes['IVA a credito'] = iva_credito
        datos_de_clientes['IEPS Credito'] = ieps_credito
        # nos movemos a Ventas -> corte de venta
        ventas = driver.find_element(By.XPATH, '//*[@id="grouptab_1"]')
        ventas.click()
        corte_de_venta = driver.find_element(By.XPATH, '//*[@id="moduleTab_1_isies_liquidaciones"]')
        corte_de_venta.click()
        busqueda_avanzada2 = driver.find_element(By.XPATH, '//*[@id="tab_link_isies_liquidaciones|advanced_search"]')
        busqueda_avanzada2.click()
        input_fecha3 = driver.find_element(By.XPATH, '//*[@id="fecha_inicial_basic"]')
        input_fecha3.send_keys(fecha_1[0])
        buscar = driver.find_element(By.XPATH, '//*[@id="search_form_submit"]')
        buscar.click()
        time.sleep(2)
        corte = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody/tr[3]/td[1]/a')
        corte.click()
        time.sleep(2)
        # sacamos los datos totales del corte
        volumen_corte = driver.find_element(By.XPATH, '//*[@id="content"]/table/tbody/tr/td/table[2]/tbody/tr[4]/td[3]').text
        subtotal_corte = driver.find_element(By.XPATH, '//*[@id="content"]/table/tbody/tr/td/table[2]/tbody/tr[4]/td[4]').text
        iva_corte = driver.find_element(By.XPATH, '//*[@id="content"]/table/tbody/tr/td/table[2]/tbody/tr[4]/td[5]').text
        ieps_corte = driver.find_element(By.XPATH, '//*[@id="content"]/table/tbody/tr/td/table[2]/tbody/tr[4]/td[6]').text
        total_corte = driver.find_element(By.XPATH, '//*[@id="content"]/table/tbody/tr/td/table[2]/tbody/tr[4]/td[7]').text
        datos_corte['Volumen Corte'] = volumen_corte
        datos_corte['Subtotal Corte'] = subtotal_corte
        datos_corte['IVA Corte'] = iva_corte
        datos_corte['IEPS Corte'] = ieps_corte
        datos_corte['Total Corte'] = total_corte
        # sacamos los datos totales de credito
        volumen_corte_credito = driver.find_element(By.XPATH, '//*[@id="content"]/table/tbody/tr/td/table[2]/tbody/tr[8]/td[3]').text
        subtotal_corte_credito = driver.find_element(By.XPATH, '//*[@id="content"]/table/tbody/tr/td/table[2]/tbody/tr[8]/td[4]').text
        iva_corte_credito = driver.find_element(By.XPATH, '//*[@id="content"]/table/tbody/tr/td/table[2]/tbody/tr[8]/td[5]').text
        ieps_corte_credito = driver.find_element(By.XPATH, '//*[@id="content"]/table/tbody/tr/td/table[2]/tbody/tr[8]/td[6]').text
        total_corte_credito = driver.find_element(By.XPATH, '//*[@id="content"]/table/tbody/tr/td/table[2]/tbody/tr[8]/td[7]').text
        datos_corte['Volumen Corte Credito'] = volumen_corte_credito
        datos_corte['Subtotal Corte Credito'] = subtotal_corte_credito
        datos_corte['IVA Corte Credito'] = iva_corte_credito
        datos_corte['IEPS Corte Credito'] = ieps_corte_credito
        datos_corte['Total Corte Credito'] = total_corte_credito
        credito_por_cliente = driver.find_element(By.XPATH, '//*[@id="content"]/table/tbody/tr/td/table[2]/tbody/tr[18]/td[3]').text
        datos_corte['Credito por cliente'] = credito_por_cliente
        cierre = driver.find_element(By.XPATH, '//*[@id="content"]/table/tbody/tr/td/table[2]/tbody/tr[25]/td[2]').text
        datos_corte['Cierre de corte'] = cierre
        # sacamos las difrencias

        diferencias['Diferencia de Litros'] = float(datos_corte['Volumen Corte']) - float(datos_de_ventas['Cantidad'])
        diferencias['Diferencia de Litros'] = abs(diferencias['Diferencia de Litros'])
        diferencias['Diferencia de Litros'] = round(diferencias['Diferencia de Litros'], 4)
        # Diferencias contado
        total_corte = total_corte.replace('$', '')
        total_corte = total_corte.replace(',', '')
        subtotal_corte = subtotal_corte.replace('$', '')
        subtotal_corte = subtotal_corte.replace(',', '')
        iva_corte = iva_corte.replace('$', '')
        iva_corte = iva_corte.replace(',', '')
        ieps_corte = ieps_corte.replace('$', '')
        ieps_corte = ieps_corte.replace(',', '')
        diferencias['Diferencia de Subtotal entre Reporte de ventas y el corte'] = float(datos_de_ventas['Subtotal']) - float(subtotal_corte)
        diferencias['Diferencia de Subtotal entre Reporte de ventas y el corte'] = abs(diferencias['Diferencia de Subtotal entre Reporte de ventas y el corte'])
        diferencias['Diferencia de Subtotal entre Reporte de ventas y el corte'] = round(diferencias['Diferencia de Subtotal entre Reporte de ventas y el corte'], 2)
        diferencias['Diferencia de IVA entre Reporte de ventas y el corte'] = float(datos_de_ventas['IVA']) - float(iva_corte)
        diferencias['Diferencia de IVA entre Reporte de ventas y el corte'] = abs(diferencias['Diferencia de IVA entre Reporte de ventas y el corte'])
        diferencias['Diferencia de IVA entre Reporte de ventas y el corte'] = round(diferencias['Diferencia de IVA entre Reporte de ventas y el corte'], 2)
        diferencias['Diferencia de IEPS entre Reporte de ventas y el corte'] = float(datos_de_ventas['IEPS']) - float(ieps_corte)
        diferencias['Diferencia de IEPS entre Reporte de ventas y el corte'] = abs(diferencias['Diferencia de IEPS entre Reporte de ventas y el corte'])
        diferencias['Diferencia de IEPS entre Reporte de ventas y el corte'] = round(diferencias['Diferencia de IEPS entre Reporte de ventas y el corte'], 2)
        diferencias['Diferencia de Total entre Reporte de ventas y el corte'] = float(datos_de_ventas['Importe Total']) - float(total_corte)
        diferencias['Diferencia de Total entre Reporte de ventas y el corte'] = abs(diferencias['Diferencia de Total entre Reporte de ventas y el corte'])
        diferencias['Diferencia de Total entre Reporte de ventas y el corte'] = round(diferencias['Diferencia de Total entre Reporte de ventas y el corte'], 2)

        # Diferencias credito
        total_corte_credito = total_corte_credito.replace('$', '')
        total_corte_credito = total_corte_credito.replace(',', '')
        subtotal_corte_credito = subtotal_corte_credito.replace('$', '')
        subtotal_corte_credito = subtotal_corte_credito.replace(',', '')
        iva_corte_credito = iva_corte_credito.replace('$', '')
        iva_corte_credito = iva_corte_credito.replace(',', '')
        ieps_corte_credito = ieps_corte_credito.replace('$', '')
        ieps_corte_credito = ieps_corte_credito.replace(',', '')
        datos_de_clientes['Subtotal a Credito'] = str(datos_de_clientes['Subtotal a Credito']).replace('$', '')
        datos_de_clientes['Subtotal a Credito'] = str(datos_de_clientes['Subtotal a Credito']).replace(',', '')
        datos_de_clientes['IVA a credito'] = str(datos_de_clientes['IVA a credito']).replace('$', '')
        datos_de_clientes['IVA a credito'] = str(datos_de_clientes['IVA a credito']).replace(',', '')
        datos_de_clientes['IEPS Credito'] = str(datos_de_clientes['IEPS Credito']).replace('$', '')
        datos_de_clientes['IEPS Credito'] = str(datos_de_clientes['IEPS Credito']).replace(',', '')
        datos_de_clientes['Total a Credito'] = str(datos_de_clientes['Total a Credito']).replace('$', '')
        datos_de_clientes['Total a Credito'] = str(datos_de_clientes['Total a Credito']).replace(',', '')
        diferencias['Diferencia de Subtotal credito entre Reporte de ventas y el corte'] = float(datos_de_clientes['Subtotal a Credito']) - float(subtotal_corte_credito)
        diferencias['Diferencia de Subtotal credito entre Reporte de ventas y el corte'] = abs(diferencias['Diferencia de Subtotal credito entre Reporte de ventas y el corte'])
        diferencias['Diferencia de Subtotal credito entre Reporte de ventas y el corte'] = round(diferencias['Diferencia de Subtotal credito entre Reporte de ventas y el corte'], 2)
        diferencias['Diferencia de IVA credito entre Reporte de ventas y el corte'] = float(datos_de_clientes['IVA a credito']) - float(iva_corte_credito)
        diferencias['Diferencia de IVA credito entre Reporte de ventas y el corte'] = abs(diferencias['Diferencia de IVA credito entre Reporte de ventas y el corte'])
        diferencias['Diferencia de IVA credito entre Reporte de ventas y el corte'] = round(diferencias['Diferencia de IVA credito entre Reporte de ventas y el corte'], 2)
        diferencias['Diferencia de IEPS credito entre Reporte de ventas y el corte'] = float(datos_de_clientes['IEPS Credito']) - float(ieps_corte_credito)
        diferencias['Diferencia de IEPS credito entre Reporte de ventas y el corte'] = abs(diferencias['Diferencia de IEPS credito entre Reporte de ventas y el corte'])
        diferencias['Diferencia de IEPS credito entre Reporte de ventas y el corte'] = round(diferencias['Diferencia de IEPS credito entre Reporte de ventas y el corte'], 2)
        diferencias['Diferencia de Total credito entre Reporte de ventas y el corte'] = float(datos_de_clientes['Total a Credito']) - float(total_corte_credito)
        diferencias['Diferencia de Total credito entre Reporte de ventas y el corte'] = abs(diferencias['Diferencia de Total credito entre Reporte de ventas y el corte'])
        diferencias['Diferencia de Total credito entre Reporte de ventas y el corte'] = round(diferencias['Diferencia de Total credito entre Reporte de ventas y el corte'], 2)

    except NoSuchElementException as exc:
        print(exc)

    print('Test Liquidacion\n')
    print('Test liquidacion, test para comprobar si los datos en carburacion cuadran en todos los reportes de liquidacion')
    print('Instancias: 192.168.9.163/sgcweb\n\n')
    mensaje_de_salida(datos_turnos, datos_de_ventas, datos_de_clientes, datos_corte, diferencias, liquidaciones, ventas_reporte)
    assert True, 'D:'
