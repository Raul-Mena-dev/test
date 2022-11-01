import os
import datetime


def test_todos(fecha_test):
    lista = [
        'test_inventario_unificado',
        'test_json_diario',
        'test_salidas_almacen_vs_json'
        

    ]
    fecha = fecha_test
    for prueba in lista:
        f = datetime.datetime.now()
        f = f.strftime("%Y-%m-%d")
        if os.path.isdir(f'/home/rmenapc/Escritorio/test_station/app/static/reports_sgc/{f}'):
            report_name = prueba.replace('.py', '')
            os.system(
                f'pytest /home/rmenapc/Escritorio/test_station/app/static/pruebas_sgc/{prueba}.py --fecha_test={fecha} --html=/home/rmenapc/Escritorio/test_station/app/static/reports_sgc/{f}/{report_name}-"`date +"%d-%m-%Y-%H-%M-%S"`".html')
        else:
            os.mkdir(f'/home/rmenapc/Escritorio/test_station/app/static/reports_sgc/{f}')
            report_name = prueba.replace('.py', '')
            os.system(
                f'pytest /home/rmenapc/Escritorio/test_station/app/static/pruebas_sgc/{prueba}.py --fecha_test={fecha} --html=/home/rmenapc/Escritorio/test_station/app/static/reports_sgc/{f}/{report_name}-"`date +"%d-%m-%Y-%H-%M-%S"`".html')


assert True, ':D'
