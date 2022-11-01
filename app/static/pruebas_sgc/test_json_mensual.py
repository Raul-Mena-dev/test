import time
import os
import json
import datetime
from calendar import monthrange
from tabulate import tabulate
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from zipfile import ZipFile
from funciones.function import login, login_web, check_exists_by_xpath, convertir_fecha_24
from selenium.common.exceptions import NoSuchElementException


class Venta:
    numero_de_registro = ''
    fecha = ''
    volumen_entregado = ''
    estado = ''
    cfdi = ''
    tipo_cfdi = ''
    estatus = ''
    valor_numerico = ''


class Venta2:
    cfdi = ''
    tipo_cfdi = ''
    fecha = ''
    valornumerico = ''


class Recepcion:
    cfdi = ''
    tipo_cfdi = ''


def mensaje_de_salida(datos_inventario, datos_inventario_ventas, recepciones, datos_descarga, facturados_sin_complemento, datos_ventas, ventas, datos_json, recepciones_json):
    print('-------------------------------------------')
    print('-------------------------------------------')
    print('Datos y diferencias: \n')
    print('-------------------------------------------')
    print('Datos en inventario:\n')
    print('----------------Recepciones----------------')
    for dato, valor in datos_inventario.items():
        print(dato + ': ' + str(valor))
    print('-------------------------------------------')
    print('------------------Ventas-------------------')
    for dato, valor in datos_inventario_ventas.items():
        print(dato + ': ' + str(valor))
    print('-------------------------------------------')
    print('Datos en SGC Ventas:\n')
    for dato, valor in datos_ventas.items():
        if dato == 'Entregas en nodo entregas en JSON':
            print('-------------------------------------------')
            print('-------------------------------------------')
            print('Datos en JSON:\n')
            print('--------------Recepciones JSON-------------')
            for key, value in recepciones.items():
                print(key + ': ' + str(value))
            print('---------------Entregas JSON---------------')
        if dato == 'Diferencia en entregas vs nodo Total entregas JSON':
            print('-------------------------------------------')
            print('-------------------------------------------')
            print('Diferencias:\n')
        print(dato, ': ', valor)

    print('-------------------------------------------')
    # columnas = ['Servicio', 'CFDI', 'FECHA']
    # print('Ventas que no aparecen en el json: \n')
    # print(tabulate(ventas_que_no_aparecen, headers=columnas, tablefmt="fancy_grid"))
    print('-------------------------------------------')
    columnas = ['Folio', 'Folio Fiscal', 'Estado', 'Volumen Compensado', 'Fecha']
    print('Datos de Servicios de descarga: \n')
    print(tabulate(datos_descarga, headers=columnas, tablefmt="fancy_grid"))
    print('-------------------------------------------')
    print('-------------------------------------------')
    columnas = ['Num.registro', 'Fecha', 'Volumen entregado', 'Estado', 'CFDI', 'Tipo CFDI', 'Estatus', 'Valor numerico']
    print('Datos de ventas: \n')
    print(tabulate(ventas, headers=columnas, tablefmt="fancy_grid"))
    print('-------------------------------------------')
    print('-------------------------------------------')
    columnas2 = ['CFDIs', 'Tipo de CFDI', 'Fecha']
    print('Datos de JSON(Entregas): \n')
    print(tabulate(datos_json, headers=columnas2, tablefmt="fancy_grid"))
    print('-------------------------------------------')
    print('-------------------------------------------')
    columnas3 = ['Num.registro', 'Fecha', 'CFDI', 'Tipo CFDI']
    print('Datos de JSON(Recepciones): \n')
    print(tabulate(recepciones_json, headers=columnas3, tablefmt="fancy_grid"))
    print('-------------------------------------------')
    print('-------------------------------------------')
    columnas = ['Servicio', 'CFDI', 'Fecha', 'Estatus']
    print('Facturados sin complementos: \n')
    print(tabulate(facturados_sin_complemento, headers=columnas, tablefmt="fancy_grid"))
    print('-------------------------------------------')


def test_ventas_vs_json(driver, fecha_test, name='admin', password='Z76U4CFIx#', name_web='admin', password_web='Ku8L08iEsb86'):
    datos_inventario = {}
    datos_inventario_ventas = {}
    datos_descarga = []
    datos_ventas = {}
    recepciones = {}
    ventas = []
    facturados_sin_complemento = []
    lista_aux = []
    lista_aux2 = []
    lista_aux3 = []
    fecha_inicio = ''
    fecha_final = ''
    try:
        login(driver, name, password)
        time.sleep(2)
        # sacar fechas del inventario
        boton_inventario = driver.find_element(By.XPATH, '//*[@id="grouptab_7"]')
        boton_inventario.click()
        hora = datetime.datetime.now()
        dia_inventario = datetime.date.today()
        mes_inventario = dia_inventario - datetime.timedelta(days=1)
        mes_inventario = mes_inventario.strftime("%Y-%m")
        datos_inventario['Fecha Inventario'] = mes_inventario
        fecha = driver.find_element(By.XPATH, '//*[@id="inventario_basic"]')
        fecha.send_keys(mes_inventario)
        fecha.send_keys(Keys.ENTER)
        time.sleep(1)
        # sacamos el JSON
        # controles_volumetricos = driver.find_element(By.XPATH, '//*[@id="grouptab_8"]')
        # controles_volumetricos.click()
        # generar_reportes = driver.find_element(By.XPATH, '//*[@id="ul_shortcuts"]/li[6]/a')
        # generar_reportes.click()
        # seleccion = Select(driver.find_element(By.XPATH, '//*[@id="json"]'))
        # seleccion.select_by_value('Mensual')
        # seleccion_mes = Select(driver.find_element(By.XPATH, '//*[@id="mes"]'))
        # seleccion_mes.select_by_visible_text(mes_inventario)
        # generar = driver.find_element(By.XPATH, '//*[@id="Generar"]/input')
        # generar.click()
        # time.sleep(420)
        # json_vntad = driver.find_element(By.XPATH, '//*[@id="mnsj_generado"]/a[1]')
        # json_d = driver.find_element(By.XPATH, '//*[@id="mnsj_generado"]/a[2]')
        nombre_json_vntad = 'VNTAM_2022-10-31.json'
        # nombre_json_d = 'M_2022-09-30.json'
        # json_vntad.click()
        # json_d.click()
        # with ZipFile(f'/home/rmenapc/Descargas/{nombre_json_vntad}', 'r') as z:
        #     z.extractall('/home/rmenapc/Descargas/')
        # os.remove(f'/home/rmenapc/Descargas/{nombre_json_vntad}')
        # with ZipFile(f'/home/rmenapc/Descargas/{nombre_json_d}', 'r') as z:
        #     z.extractall('/home/rmenapc/Descargas/')
        # os.remove(f'/home/rmenapc/Descargas/{nombre_json_d}')
        boton_descarga = driver.find_element(By.XPATH, '/html[1]/body[1]/div[3]/div[10]/ul[1]/li[6]/span[2]/a[1]')
        boton_descarga.click()
        sub_boton_descarga = driver.find_element(By.XPATH, '/html[1]/body[1]/div[3]/div[12]/span[5]/ul[1]/li[1]/a[1]')
        sub_boton_descarga.click()
        boton_descargas_documento = driver.find_element(By.XPATH, '/html[1]/body[1]/div[4]/div[2]/div[1]/ul[1]/li[2]/a[1]')
        boton_descargas_documento.click()
        fecha1 = driver.find_element(By.XPATH, '/html[1]/body[1]/div[4]/div[3]/table[1]/tbody[1]/tr[1]/td[1]/form[1]/div[1]/table[1]/tbody[1]/tr[1]/td[2]/input[1]')
        fecha2 = driver.find_element(By.XPATH, '/html[1]/body[1]/div[4]/div[3]/table[1]/tbody[1]/tr[1]/td[1]/form[1]/div[1]/table[1]/tbody[1]/tr[1]/td[2]/input[2]')
        time.sleep(2)
        fecha1.clear()
        fecha2.clear()
        mes_inventario_1 = mes_inventario
        primer_dia_mes = mes_inventario_1 + '-01'
        fecha1.send_keys(primer_dia_mes)
        mes_inventario_2 = mes_inventario
        mes_inventario_2 = mes_inventario_2.split('-')
        year = mes_inventario_2[0]
        mes = mes_inventario_2[1]
        ultimo_dia = monthrange(int(year), int(mes))
        ultimo_dia_mes = year + '-' + mes + '-' + str(ultimo_dia[1])
        fecha2.send_keys(ultimo_dia_mes)
        fecha2.send_keys(Keys.ENTER)
        time.sleep(1)
        unidades_de_medida = driver.find_element(By.XPATH, '/html[1]/body[1]/div[4]/div[3]/table[1]/tbody[1]/tr[1]/td[1]/form[1]/div[1]/table[1]/tbody[1]/tr[6]/td[2]/input[1]')
        unidades_de_medida.click()
        time.sleep(3)
        tabla_descargas = driver.find_element(By.XPATH, '//*[@id="content"]/table/tbody/tr/td/table[4]/tbody')
        tabla_descargas_len = len(tabla_descargas.find_elements(By.TAG_NAME, 'tr'))
        # tabla_descargas_len -= 1
        i = 2
        x = 0
        if check_exists_by_xpath(driver, '/html[1]/body[1]/div[4]/div[3]/table[1]/tbody[1]/tr[1]/td[1]/table[4]/tbody[1]/tr[3]/td[2]'):
            total = driver.find_element(By.XPATH, '//*[@id="tTotales"]/tbody/tr[2]/td[1]').text
            datos_inventario['Total de cargas'] = total
            datos_inventario['Volumen Compensado'] = '0'
            while i < tabla_descargas_len:
                datos_descarga.append([])
                compensado = driver.find_element(By.XPATH, f'//*[@id="content"]/table/tbody/tr/td/table[4]/tbody/tr[{i}]/td[13]').text
                compensado = compensado.replace(',', '')
                compensado = compensado.replace('kg', '')
                compensado = compensado.replace('lt', '')
                compensado = compensado.replace(' ', '', 10)
                datos_inventario['Volumen Compensado'] = str(float(datos_inventario['Volumen Compensado']) + float(compensado))
                folio_link = driver.find_element(By.XPATH, f'//*[@id="content"]/table/tbody/tr/td/table[4]/tbody/tr[{i}]/td[1]/a')
                datos_descarga[x].append(folio_link.text)
                folio_link.click()
                time.sleep(3)
                folio_fiscal = driver.find_element(By.XPATH, '//*[@id="detailpanel_2"]/tbody/tr[3]/td[2]').text
                datos_descarga[x].append(folio_fiscal)
                estado = driver.find_element(By.XPATH, '//*[@id="detailpanel_1"]/tbody/tr[4]/td[2]').text
                datos_descarga[x].append(estado)
                volumen_compensado = driver.find_element(By.XPATH, '//*[@id="detailpanel_4"]/tbody/tr[7]/td[4]').text
                datos_descarga[x].append(volumen_compensado)
                fecha = driver.find_element(By.XPATH, '//*[@id="detailpanel_1"]/tbody/tr[1]/td[4]').text
                datos_descarga[x].append(fecha)
                x += 1
                i += 1
                boton_descarga = driver.find_element(By.XPATH, '/html[1]/body[1]/div[3]/div[10]/ul[1]/li[6]/span[2]/a[1]')
                boton_descarga.click()
                sub_boton_descarga = driver.find_element(By.XPATH, '/html[1]/body[1]/div[3]/div[12]/span[5]/ul[1]/li[1]/a[1]')
                sub_boton_descarga.click()
                boton_descargas_documento = driver.find_element(By.XPATH, '/html[1]/body[1]/div[4]/div[2]/div[1]/ul[1]/li[2]/a[1]')
                boton_descargas_documento.click()
                fecha1 = driver.find_element(By.XPATH, '/html[1]/body[1]/div[4]/div[3]/table[1]/tbody[1]/tr[1]/td[1]/form[1]/div[1]/table[1]/tbody[1]/tr[1]/td[2]/input[1]')
                fecha2 = driver.find_element(By.XPATH, '/html[1]/body[1]/div[4]/div[3]/table[1]/tbody[1]/tr[1]/td[1]/form[1]/div[1]/table[1]/tbody[1]/tr[1]/td[2]/input[2]')
                time.sleep(2)
                fecha1.clear()
                fecha2.clear()
                fecha1.send_keys(primer_dia_mes)
                fecha2.send_keys(ultimo_dia_mes)
                fecha2.send_keys(Keys.ENTER)
                time.sleep(1)
                unidades_de_medida = driver.find_element(By.XPATH, '/html[1]/body[1]/div[4]/div[3]/table[1]/tbody[1]/tr[1]/td[1]/form[1]/div[1]/table[1]/tbody[1]/tr[6]/td[2]/input[1]')
                unidades_de_medida.click()
                time.sleep(3)
        else:
            datos_inventario['Total de cargas'] = '0'
            datos_inventario['Volumen Compensado'] = '0'
        # nos logeamos en sgc ventas
        login_web(driver, name_web, password_web)
        time.sleep(1)
        principal = driver.current_window_handle
        # nos movemos a la pestaña necesaria
        driver.execute_script('''window.open("https://testventas.sgcweb.com.mx/index.php?module=isies_reportes_generales&action=DetailView&record=2ef1e97a-0954-03df-6c18-4e933561657a","_blank");''')
        chld = driver.window_handles[1]
        driver.switch_to.window(chld)
        time.sleep(10)
        version = driver.find_element(By.XPATH, '//*[@id="footer"]').text
        version = version.replace(' ', '')
        version = version.split('|')
        version = version[1]
        version = version.replace('v', '')
        version = version.replace('.', '')
        # se mandan las fechas necesarias
        time.sleep(3)
        fecha1 = driver.find_element(By.XPATH, '//*[@id="_fecha_0"]')
        hora1 = Select(driver.find_element(By.XPATH, '//*[@id="_hora_0"]'))
        fecha1.clear()
        hora = '23'
        minuto = '59'
        fecha1.send_keys(primer_dia_mes)
        time.sleep(1)
        hora1.select_by_visible_text(hora)
        fecha2 = driver.find_element(By.XPATH, '//*[@id="_fecha2_0"]')
        hora2 = Select(driver.find_element(By.XPATH, '//*[@id="_hora2_0"]'))
        min2 = Select(driver.find_element(By.XPATH, '//*[@id="_minuto2_0"]'))
        fecha2.clear()
        fecha_inicio = mes_inventario
        fecha2.send_keys(ultimo_dia_mes)
        time.sleep(1)
        hora2.select_by_visible_text(hora)
        min2.select_by_visible_text(minuto)
        datos_ventas['Mes del reporte'] = fecha_inicio
        ver_reporte = driver.find_element(By.XPATH, '//*[@id="btn_ver_reporte"]')
        ver_reporte.click()
        time.sleep(20)
        # se saca la cantidad de servicios que existen en el rango de fechas y horas correspondientes
        lista_servicios = driver.find_element(By.XPATH, '//*[@id="_preViewReport"]/table/tbody')
        lista_servicios_len = len(lista_servicios.find_elements(By.TAG_NAME, 'tr'))
        datos_ventas['Cantidad de servicios'] = lista_servicios_len - 2
        i = 2
        facturados = 0
        # creamos los objetos necesarios por cada venta con la mitad de informacion (folio, fecha, estado, cantidad de lt)
        while i < lista_servicios_len:
            folio = driver.find_element(By.XPATH, f'//*[@id="_preViewReport"]/table/tbody/tr[{i}]/td[1]').text
            fecha = driver.find_element(By.XPATH, f'//*[@id="_preViewReport"]/table/tbody/tr[{i}]/td[3]').text
            estado = driver.find_element(By.XPATH, f'//*[@id="_preViewReport"]/table/tbody/tr[{i}]/td[10]').text
            cantidad_lt = driver.find_element(By.XPATH, f'//*[@id="_preViewReport"]/table/tbody/tr[{i}]/td[4]').text
            venta = Venta()
            venta.numero_de_registro = folio
            venta.fecha = fecha
            venta.estado = estado
            if estado == 'Facturado':
                facturados += 1
            venta.volumen_entregado = cantidad_lt
            venta.valor_numerico = cantidad_lt
            i += 1
            ventas.append(venta)

        ventas.sort(key=lambda numero: numero.numero_de_registro)
        datos_ventas['Servicios Facturados'] = 0
        for dato in ventas:
            if dato.estado == 'Facturado':
                datos_ventas['Servicios Facturados'] = int(datos_ventas['Servicios Facturados']) + 1
        datos_ventas['Servicios Terminados'] = 0
        # nos movemos a servicios para buscar cada servicio y ver si tiene factura si tiene sacara los datos necesarios
        if int(version) >= 802:
            driver.execute_script(''f'window.open("https://testventas.sgcweb.com.mx/index.php?module=isies_reportes_generales&action=ReporteServiciosFactura&fecha_inicial={primer_dia_mes}&fecha_final={ultimo_dia_mes}","_blank");''')
            time.sleep(5)
            chld2 = driver.window_handles[2]
            driver.switch_to.window(chld2)
            tabla_servicios = driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/table/tbody/tr/td/div[2]/table/tbody')
            tabla_servicios_len = len(tabla_servicios.find_elements(By.TAG_NAME, 'tr'))
            i = 1
            # for dato in ventas:
            #     i = 1
            #     if dato.estado == 'Facturado':
            #         while i < tabla_servicios_len:
            #             folio_servicio = driver.find_element(By.XPATH, f'/html/body/div[4]/div[3]/table/tbody/tr/td/div[2]/table/tbody/tr[{i}]/td[1]').text
            #             if dato.numero_de_registro == folio_servicio:
            #                 tabla_cfdi = driver.find_element(By.XPATH, f'/html/body/div[4]/div[3]/table/tbody/tr/td/div[2]/table/tbody/tr[{i}]/td[6]').text
            #                 dato.cfdi = tabla_cfdi
            #                 tabla_estatus = driver.find_element(By.XPATH, f'/html/body/div[4]/div[3]/table/tbody/tr/td/div[2]/table/tbody/tr[{i}]/td[8]').text
            #                 dato.estatus = tabla_estatus
            #                 tabla_tipo = driver.find_element(By.XPATH, f'/html/body/div[4]/div[3]/table/tbody/tr/td/div[2]/table/tbody/tr[{i}]/td[9]').text
            #                 dato.tipo_cfdi = tabla_tipo
            #                 break
            #             else:
            #                 i += 1
            #     else:
            #         datos_ventas['Servicios Terminados'] = datos_ventas['Servicios Terminados'] + 1
            #         dato.cfdi = 'N/A'
            #         dato.tipo_cfdi = 'N/A'
            #         dato.estatus = 'N/A'
            #         dato.valor_numerico = 'N/A'
            lista = []
            while i < tabla_servicios_len:
                x = Venta()
                folio_servicio = driver.find_element(By.XPATH, f'/html/body/div[4]/div[3]/table/tbody/tr/td/div[2]/table/tbody/tr[{i}]/td[1]').text
                x.numero_de_registro = folio_servicio
                tabla_cfdi = driver.find_element(By.XPATH, f'/html/body/div[4]/div[3]/table/tbody/tr/td/div[2]/table/tbody/tr[{i}]/td[6]').text
                x.cfdi = tabla_cfdi
                tabla_estatus = driver.find_element(By.XPATH, f'/html/body/div[4]/div[3]/table/tbody/tr/td/div[2]/table/tbody/tr[{i}]/td[8]').text
                x.estatus = tabla_estatus
                tabla_tipo = driver.find_element(By.XPATH, f'/html/body/div[4]/div[3]/table/tbody/tr/td/div[2]/table/tbody/tr[{i}]/td[9]').text
                x.tipo_cfdi = tabla_tipo
                lista.append(x)
                i += 1

            for dato in ventas:
                if dato.estado == 'Facturado':
                    for y in lista:
                        if y.numero_de_registro == dato.numero_de_registro:
                            dato.cfdi = y.cfdi
                            dato.tipo_cfdi = y.tipo_cfdi
                            dato.estatus = y.estatus
                else:
                    datos_ventas['Servicios Terminados'] = datos_ventas['Servicios Terminados'] + 1
                    dato.cfdi = 'N/A'
                    dato.tipo_cfdi = 'N/A'
                    dato.estatus = 'N/A'
                    dato.valor_numerico = 'N/A'

        else:
            for dato in ventas:
                time.sleep(1)
                if dato.estado == 'Facturado':
                    servicios = driver.find_element(By.XPATH, '//*[@id="grouptab_3"]')
                    servicios.click()
                    folio_interno = driver.find_element(By.XPATH, '//*[@id="folio_interno_basic"]')
                    folio_interno.send_keys(dato.numero_de_registro)
                    folio_interno.send_keys(Keys.ENTER)
                    time.sleep(1)
                    acceder = driver.find_element(By.XPATH, '//*[@id="MassUpdate"]/table/tbody/tr[3]/td[2]/a')
                    acceder.click()
                    if check_exists_by_xpath(driver, '/html/body/div[4]/div[3]/table/tbody/tr/td/div[4]/table/tbody/tr[4]/td[4]/a'):
                        factura = driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/table/tbody/tr/td/div[4]/table/tbody/tr[4]/td[4]/a')
                        factura.click()
                        time.sleep(1)
                    elif check_exists_by_xpath(driver, '/html/body/div[4]/div[3]/table/tbody/tr/td/div[4]/table/tbody/tr[5]/td[4]/a'):
                        comprobacion = driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/table/tbody/tr/td/div[4]/table/tbody/tr[5]/td[4]/a').text
                        if comprobacion.isnumeric():
                            factura = driver.find_element(By.XPATH, '//*[@id="detailpanel_3"]/tbody/tr[5]/td[4]/a')
                            factura.click()
                            time.sleep(1)
                        else:
                            factura = driver.find_element(By.XPATH, '//*[@id="detailpanel_3"]/tbody/tr[3]/td[4]/a')
                            factura.click()
                            time.sleep(1)
                    if check_exists_by_xpath(driver, '//*[@id="timbre_uuid"]'):
                        uuid = driver.find_element(By.XPATH, '//*[@id="timbre_uuid"]').text
                        tipo = driver.find_element(By.XPATH, '//*[@id="detailpanel_1"]/tbody/tr[7]/td[4]').text
                        estatus = driver.find_element(By.XPATH, '//*[@id="detailpanel_1"]/tbody/tr[7]/td[2]').text
                        dato.cfdi = uuid
                        dato.tipo_cfdi = tipo
                        dato.estatus = estatus
                    else:
                        dato.cfdi = 'N/A'
                        dato.tipo_cfdi = 'N/A'
                        dato.valor_numerico = 'N/A'
                else:
                    datos_ventas['Servicios Terminados'] = datos_ventas['Servicios Terminados'] + 1
                    dato.cfdi = 'N/A'
                    dato.tipo_cfdi = 'N/A'
                    dato.estatus = 'N/A'
                    dato.valor_numerico = 'N/A'

        # sacamos los datos del json
        # nombre_json_vntad = nombre_json_vntad.replace('.zip', '.json')
        # nombre_json_d = nombre_json_d.replace('.zip', '.json')
        with open(f'/home/rmenapc/Descargas/{nombre_json_vntad}', 'r') as json_file:
            json_load = json.load(json_file)

        datos_json = []
        num_entregas = json_load['ControlesVolumetricos']['Producto'][0]['ReporteDeVolumenMensual']['Entregas']['TotalEntregasMes']
        if int(num_entregas) > 0:
            data = json_load['ControlesVolumetricos']['Producto'][0]['ReporteDeVolumenMensual']['Entregas']['Complemento']

            aux = 0

            data_len = len(data)

            id_interno = 1
            for dato in data:
                v = Venta2()
                if 'CFDIs' in dato['Nacional'][0]:
                    v.cfdi = dato['Nacional'][0]['CFDIs']['Cfdi']
                    v.tipo_cfdi = dato['Nacional'][0]['CFDIs']['TipoCfdi']
                    v.valor_numerico = str(dato['Nacional'][0]['CFDIs']['VolumenDocumentado']['ValorNumerico'])
                    fecha = str(dato['Nacional'][0]['CFDIs']['FechaYHoraTransaccion']).replace('T', ' ')
                    fecha = fecha.split(' ')
                    sfecha = fecha[0]
                    shora = fecha[1]
                    shora = shora.split('-')
                    fecha = sfecha + ' ' + shora[0]
                    fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
                    fecha = fecha - datetime.timedelta(hours=5)
                    v.fecha = fecha
                    aux += 1
                else:
                    v.cfdi = f'ID interno = {id_interno}'
                    id_interno += 1
                    v.tipo_cfdi = 'Venta sin complemento'
                    v.valor_numerico = '0'
                    v.fecha = datos_ventas['Mes del reporte']
                datos_json.append(v)

            aux2 = 0
            for venta in ventas:
                if not any(obj.cfdi == venta.cfdi for obj in datos_json):
                    if venta.cfdi != 'N/A':
                        facturados_sin_complemento.append([])
                        facturados_sin_complemento[aux2].append(venta.numero_de_registro)
                        facturados_sin_complemento[aux2].append(venta.cfdi)
                        facturados_sin_complemento[aux2].append(venta.fecha)
                        facturados_sin_complemento[aux2].append(venta.estatus)
                        aux2 += 1

            json_entregas = int(num_entregas)
            json_documentos = int(json_load['ControlesVolumetricos']['Producto'][0]['ReporteDeVolumenMensual']['Entregas']['TotalDocumentosMes'])
            datos_ventas['Entregas en nodo entregas en JSON'] = json_entregas
            datos_ventas['Documentos en nodo entregas en JSON'] = json_documentos
            datos_ventas['Conteo Entregas en JSON'] = data_len
            datos_ventas['Conteo Facturados en JSON'] = aux
            datos_ventas['Total entregas JSON'] = int(datos_ventas['Conteo Entregas en JSON']) + int(datos_ventas['Conteo Facturados en JSON'])
            datos_ventas['Facturas sin Complementos'] = aux2
            datos_ventas['Diferencia en entregas vs nodo Total entregas JSON'] = int(datos_ventas['Entregas en nodo entregas en JSON']) - int(datos_ventas['Conteo Entregas en JSON'])
            datos_ventas['Diferencia en Documentos vs nodo Total Documentos JSON'] = int(datos_ventas['Documentos en nodo entregas en JSON']) - int(datos_ventas['Conteo Facturados en JSON'])
            datos_ventas['Diferencia en Documentos vs nodo Total Documentos JSON'] = abs(datos_ventas['Diferencia en Documentos vs nodo Total Documentos JSON'])
            datos_ventas['Diferencia de servicios'] = int(datos_ventas['Cantidad de servicios']) - (int(datos_ventas['Conteo Entregas en JSON']) + int(datos_ventas['Conteo Facturados en JSON']))
            datos_ventas['Diferencia de servicios'] = abs(datos_ventas['Diferencia de servicios'])
            datos_ventas['Diferencia facturas en JSON'] = int(datos_ventas['Servicios Facturados']) - int(datos_ventas['Conteo Facturados en JSON'])
            datos_ventas['Diferencia facturas en JSON'] = abs(datos_ventas['Diferencia facturas en JSON'])
            i = 0
            for venta in ventas:
                lista_aux.append([])
                lista_aux[i].append(venta.numero_de_registro)
                lista_aux[i].append(venta.fecha)
                lista_aux[i].append(venta.volumen_entregado)
                lista_aux[i].append(venta.estado)
                lista_aux[i].append(venta.cfdi)
                lista_aux[i].append(venta.tipo_cfdi)
                lista_aux[i].append(venta.estatus)
                lista_aux[i].append(venta.valor_numerico)
                i += 1

            i = 0
            for entrega in datos_json:
                lista_aux2.append([])
                lista_aux2[i].append(entrega.cfdi)
                lista_aux2[i].append(entrega.tipo_cfdi)
                lista_aux2[i].append(entrega.fecha)
                i += 1
        else:
            json_entregas = int(json_load['ControlesVolumetricos']['Producto'][0]['Tanque'][0]['Entregas']['TotalEntregas'])
            json_documentos = int(json_load['ControlesVolumetricos']['Producto'][0]['Tanque'][0]['Entregas']['TotalDocumentos'])
            datos_ventas['Entregas en nodo entregas en JSON'] = json_entregas
            datos_ventas['Documentos en nodo entregas en JSON'] = json_documentos
            # datos_json.append(f'Sin datos de ventas en el JSON de ventas, archivo: {nombre_json_vntad}')

        recepciones['Total Recepciones'] = json_load['ControlesVolumetricos']['Producto'][0]['ReporteDeVolumenMensual']['Recepciones']['TotalRecepcionesMes']
        recepciones_json = []
        if int(recepciones['Total Recepciones']) > 0:
            data2 = json_load['ControlesVolumetricos']['Producto'][0]['ReporteDeVolumenMensual']['Recepciones']['Complemento']
            for dato in data2:
                r = Recepcion()
                r.tipo_cfdi = dato['Nacional'][0]['CFDIs']['TipoCfdi']
                r.cfdi = dato['Nacional'][0]['CFDIs']['Cfdi']
                recepciones_json.append(r)
            i = 0
            for r in recepciones_json:
                lista_aux3.append([])
                lista_aux3[i].append(r.cfdi)
                lista_aux3[i].append(r.tipo_cfdi)
                i += 1

        # mensaje_de_salida(facturados_sin_complemento, datos_ventas, lista_aux, lista_aux2)
        # assert True, 'D:'
    except NoSuchElementException as exc:
        print(exc)
        assert False, 'not ok D:'

    # os.remove(f'/home/rmenapc/Descargas/{nombre_json_vntad}')
    # os.remove(f'/home/rmenapc/Descargas/{nombre_json_d}')
    print('Test JSON Mensual\n')
    print('Test JSON Mensual, Compara los datos en todas las ventas del mes en SGC(Informe de ventas) contra el JSON Mensual,\n'
          ' comprueba si las facturas aparecen en el JSON o no.\n'
          'Instancias: http://192.168.9.164/sgcweb, http://testventas.sgcweb.com.mx/')
    print('\n\n')
    mensaje_de_salida(datos_inventario, datos_inventario_ventas, recepciones, datos_descarga, facturados_sin_complemento, datos_ventas, lista_aux, lista_aux2, lista_aux3)
    assert True, 'D:'
