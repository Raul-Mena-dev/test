import os
import datetime


def script_pytest(prueba):
    report_name = prueba.replace('.py', '')
    os.system(f'pytest /home/rmenapc/Escritorio/test_station/app/static/pruebas_gasstation/{prueba} --html=/home/rmenapc/Escritorio/test_station/app/static/reports_gasstation/{report_name}-"`date +"%d-%m-%Y-%H-%M-%S"`".html')


def script_pytest2(prueba):
    f = datetime.datetime.now()
    f = f.strftime("%Y-%m-%d")
    if os.path.isdir(f'/home/rmenapc/Escritorio/test_station/app/static/reports_sgc/{f}'):
        report_name = prueba.replace('.py', '')
        os.system(f'pytest /home/rmenapc/Escritorio/test_station/app/static/pruebas_sgc/{prueba}.py --html=/home/rmenapc/Escritorio/test_station/app/static/reports_sgc/{f}/{report_name}-"`date +"%d-%m-%Y-%H-%M-%S"`".html')
    else:
        os.mkdir(f'/home/rmenapc/Escritorio/test_station/app/static/reports_sgc/{f}')
        report_name = prueba.replace('.py', '')
        os.system(f'pytest /home/rmenapc/Escritorio/test_station/app/static/pruebas_sgc/{prueba}.py --html=/home/rmenapc/Escritorio/test_station/app/static/reports_sgc/{f}/{report_name}-"`date +"%d-%m-%Y-%H-%M-%S"`".html')
    


def script_pytest3(prueba, fecha):
    f = datetime.datetime.now()
    f = f.strftime("%Y-%m-%d")
    if os.path.isdir(f'/home/rmenapc/Escritorio/test_station/app/static/reports_sgc/{f}'):
        report_name = prueba.replace('.py', '')
        os.system(f'pytest /home/rmenapc/Escritorio/test_station/app/static/pruebas_sgc/{prueba}.py --fecha_test={fecha} --html=/home/rmenapc/Escritorio/test_station/app/static/reports_sgc/{f}/{report_name}-"`date +"%d-%m-%Y-%H-%M-%S"`".html')
    else:
        os.mkdir(f'/home/rmenapc/Escritorio/test_station/app/static/reports_sgc/{f}')
        report_name = prueba.replace('.py', '')
        os.system(f'pytest /home/rmenapc/Escritorio/test_station/app/static/pruebas_sgc/{prueba}.py --fecha_test={fecha} --html=/home/rmenapc/Escritorio/test_station/app/static/reports_sgc/{f}/{report_name}-"`date +"%d-%m-%Y-%H-%M-%S"`".html')
    

