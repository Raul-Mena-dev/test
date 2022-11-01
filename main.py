from crypt import methods
import datetime
from app import create_app, script_pytest
from flask import render_template, redirect, url_for, request, flash, session
import os
import webbrowser
from werkzeug.utils import secure_filename
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
# import MySQLdb.cursors

app = create_app()  
mysql = MySQL(cursorclass=DictCursor)
mysql.init_app(app)
app.config['UPLOAD_FOLDER'] ='app/static/pruebas_gasstation'
app.config['UPLOAD_FOLDER2'] ='app/static/pruebas_sgc'
app.config['SECRET_KEY'] = 'mysecret'
# base de datos
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'raul'
app.config['MYSQL_DATABASE_PASSWORD'] = '12345678'
app.config['MYSQL_DATABASE_DB'] = 'station'

    

@app.route('/')
def inicio():
    return render_template('inicio.html')    

#gasstation
@app.route('/reportes_gas')
def reportes_gas():
    reports = []
    for file in os.listdir('/home/rmenapc/Escritorio/test_station/app/static/reports_gasstation/'):
        if file.endswith('.html'):
            reports.append(file)
    return render_template('home.html', reports = reports)


@app.route('/<string:report>')
def mostrar(report):
    url = '/home/rmenapc/Escritorio/test_station/app/static/reports_gasstation/' + report
    webbrowser.open_new_tab(url)

    return redirect(url_for('inicio'))


@app.route('/test')
def test():
    tests = []
    descripcion = []
    for file in os.listdir('/home/rmenapc/Escritorio/test_station/app/static/pruebas_gasstation/'):
        if file.endswith('.py'):
            tests.append(file)
    for file in os.listdir('/home/rmenapc/Escritorio/test_station/app/static/pruebas_gasstation/'):
        if file.endswith('.txt'):
            texto = open(f'/home/rmenapc/Escritorio/test_station/app/static/pruebas_gasstation/{file}', 'r')
            texto = texto.read()
            descripcion.append(texto)
    return render_template('test.html', tests = tests, descripcion = descripcion)


@app.route('/test/<string:prueba>')
def ejecutar(prueba):
    try:
        script_pytest.script_pytest(prueba)
        return redirect(url_for('inicio'))
    except Exception as e:
        flash(str(e))
        return redirect(url_for('test'))

# SGC
@app.route('/carpetas_sgc')
def carpetas_sgc():
    reports = []
    for file in os.listdir('/home/rmenapc/Escritorio/test_station/app/static/reports_sgc/'):
        d = os.path.join('/home/rmenapc/Escritorio/test_station/app/static/reports_sgc/', file)
        if os.path.isdir(d):
            d = d.replace('/home/rmenapc/Escritorio/test_station/app/static/reports_sgc/', '')
            reports.append(d)
    return render_template('sgc_reportes.html', reports = reports)

@app.route('/reportes_sgc/<string:report>')
def reportes_sgc(report):
    reports = []
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT reporte.nombre_reporte, reporte.fecha, login.usuario FROM reporte INNER JOIN login on reporte.autor = login.id_login WHERE reporte.fecha = %s', (report))
    data = cursor.fetchall()
    for file in os.listdir(f'/home/rmenapc/Escritorio/test_station/app/static/reports_sgc/{report}'):
        if file.endswith('.html'):
            reports.append(file)
    return render_template('reportes.html', reports = reports, fecha = report, data = data)

@app.route('/mostrar_sgc', methods=['GET'])
def mostrar_sgc():
    reporte = request.args.get('reporte')
    folder = request.args.get('folder')
    url = f'/home/rmenapc/Escritorio/test_station/app/static/reports_sgc/{folder}/' + reporte
    webbrowser.open_new_tab(url)

    return redirect(url_for('reportes_sgc', report = folder))

@app.route('/test_sgc')
def test_sgc():
    tests = ''
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT pruebas.nombre_prueba, pruebas.fecha, descripciones.text, descripciones.nombre_descripcion, login.usuario FROM pruebas INNER JOIN descripciones ON descripciones.id_prueba = pruebas.id_prueba INNER JOIN login on login.id_login = pruebas.autor')
    data = cursor.fetchall()
    return render_template('test_sgc.html', tests = data)


@app.route('/test_sgc/<string:prueba>')
def ejecutar_sgc(prueba):
    try:
        f = datetime.datetime.now()
        f = f.strftime("%Y-%m-%d")
        if os.path.isdir(f'/home/rmenapc/Escritorio/test_station/app/static/reports_sgc/{f}'):
            d = datetime.datetime.now()
            d = d.strftime("%Y-%m-%d-%H-%M-%S")
            report_name = prueba.replace('.py', '')
            report_name = report_name + '-' + d + '.html'
            os.system(f'pytest /home/rmenapc/Escritorio/test_station/app/static/pruebas_sgc/{prueba}.py --html=/home/rmenapc/Escritorio/test_station/app/static/reports_sgc/{f}/{report_name}')
            cursor = mysql.get_db().cursor()
            cursor.execute('SELECT id_prueba FROM pruebas WHERE nombre_prueba = %s', (prueba.replace('.py', '')))
            data = cursor.fetchone()
            cursor = mysql.get_db().cursor()
            cursor.execute('INSERT INTO reporte(id_prueba, autor, nombre_reporte, fecha) VALUES (%s, %s, %s, %s)', (int(data['id_prueba']), int(session['id']), report_name, f,))
            mysql.get_db().commit()
        else:
            os.mkdir(f'/home/rmenapc/Escritorio/test_station/app/static/reports_sgc/{f}')
            d = datetime.datetime.now()
            d = d.strftime("%Y-%m-%d-%H-%M-%S")
            report_name = prueba.replace('.py', '')
            report_name = report_name + '-' + d + '.html'
            os.system(f'pytest /home/rmenapc/Escritorio/test_station/app/static/pruebas_sgc/{prueba}.py --html=/home/rmenapc/Escritorio/test_station/app/static/reports_sgc/{f}/{report_name}')
            cursor = mysql.get_db().cursor()
            cursor.execute('SELECT id_prueba FROM pruebas WHERE nombre_prueba = %s', (prueba.replace('.py', '')))
            data = cursor.fetchone()
            cursor = mysql.get_db().cursor()
            cursor.execute('INSERT INTO reporte(id_prueba, autor, nombre_reporte, fecha) VALUES (%s, %s, %s, %s)', (int(data['id_prueba']), int(session['id']), report_name, f,))
            mysql.get_db().commit()
            # script_pytest.script_pytest2(prueba)
        return redirect(url_for('carpetas_sgc'))
    except Exception as e:
        flash(str(e))
        return redirect(url_for('test_sgc'))

@app.route('/test_sgc/<string:prueba>/<string:fecha>')
def ejecutar_sgc2(prueba, fecha):
    try:
        f = datetime.datetime.now()
        f = f.strftime("%Y-%m-%d")
        if os.path.isdir(f'/home/rmenapc/Escritorio/test_station/app/static/reports_sgc/{f}'):
            d = datetime.datetime.now()
            d = d.strftime("%Y-%m-%d-%H-%M-%S")
            report_name = prueba.replace('.py', '')
            report_name = report_name + '-' + d + '.html'
            os.system(f'pytest /home/rmenapc/Escritorio/test_station/app/static/pruebas_sgc/{prueba}.py --fecha_test={fecha} --html=/home/rmenapc/Escritorio/test_station/app/static/reports_sgc/{f}/{report_name}')
            cursor = mysql.get_db().cursor()
            cursor.execute('SELECT id_prueba FROM pruebas WHERE nombre_prueba = %s', (prueba.replace('.py', '')))
            data = cursor.fetchone()
            cursor = mysql.get_db().cursor()
            cursor.execute('INSERT INTO reporte(id_prueba, autor, nombre_reporte, fecha) VALUES (%s, %s, %s, %s)', (int(data['id_prueba']), int(session['id']), report_name, f,))
            mysql.get_db().commit()
        else:
            os.mkdir(f'/home/rmenapc/Escritorio/test_station/app/static/reports_sgc/{f}')
            d = datetime.datetime.now()
            d = d.strftime("%Y-%m-%d-%H-%M-%S")
            report_name = prueba.replace('.py', '')
            report_name = report_name + '-' + d + '.html'
            os.system(f'pytest /home/rmenapc/Escritorio/test_station/app/static/pruebas_sgc/{prueba}.py --fecha_test={fecha} --html=/home/rmenapc/Escritorio/test_station/app/static/reports_sgc/{f}/{report_name}')
            cursor = mysql.get_db().cursor()
            cursor.execute('SELECT id_prueba FROM pruebas WHERE nombre_prueba = %s', (prueba.replace('.py', '')))
            data = cursor.fetchone()
            cursor = mysql.get_db().cursor()
            cursor.execute('INSERT INTO reporte(id_prueba, autor, nombre_reporte, fecha) VALUES (%s, %s, %s, %s)', (int(data['id_prueba']), int(session['id']), report_name, f,))
            mysql.get_db().commit()
            # script_pytest.script_pytest2(prueba)
        return redirect(url_for('carpetas_sgc'))
    except Exception as e:
        flash(str(e))
        return redirect(url_for('test_sgc'))

@app.route('/borrar_sgc', methods=['GET'])
def borrar_sgc():
    try:
        reporte = request.args.get('reporte')
        folder = request.args.get('folder')
        if os.path.exists(f'/home/rmenapc/Escritorio/test_station/app/static/reports_sgc/{folder}/' + reporte):
            os.remove(f'/home/rmenapc/Escritorio/test_station/app/static/reports_sgc/{folder}/' + reporte)
            cursor = mysql.get_db().cursor()
            cursor.execute('DELETE FROM reporte WHERE nombre_reporte = %s', (reporte))
            mysql.get_db().commit()
        return redirect(url_for('carpetas_sgc'))
    except Exception as e:
        flash(str(e))
        return redirect(url_for('carpetas_sgc'))

#subir
@app.route('/subir', methods=['GET', 'POST'])
def subir():
    msgU = ''
    try:
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('sin archivo')
                return redirect(url_for('subir', msgU = msgU))
            if 'option' not in request.form:
                flash('seleccione una opcion')
                return redirect(url_for('subir', msgU = msgU))
            f = request.files['file']
            texto = request.form['descripcion']
            nombre_descripcion = f.filename
            nombre_descripcion = str(nombre_descripcion)
            nombre_descripcion = nombre_descripcion.replace('.py', '')
            option = request.form['option']
            fecha = datetime.date.today()
            fecha = datetime.datetime.strftime(fecha, '%Y-%m-%d')
            if option == 'sgc':
                f.save(os.path.join(app.config['UPLOAD_FOLDER2'], secure_filename(f.filename)))
                cursor = mysql.get_db().cursor()
                cursor.execute('INSERT INTO pruebas(nombre_prueba, autor, projecto, fecha) VALUES (%s, %s, %s, %s)', (nombre_descripcion, int(session['id']), option, fecha,))
                mysql.get_db().commit()
                id = cursor.lastrowid
                cursor = mysql.get_db().cursor()
                cursor.execute('INSERT INTO descripciones(id_prueba, nombre_descripcion, text) VALUES (%s, %s, %s)', (id, nombre_descripcion, texto))
                mysql.get_db().commit()
                flash('Archivo guardado con exito en reportes de SGC')
                return redirect(url_for('subir' , msgU = msgU))
            elif option == 'gas':
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
                with open(f'app/static/pruebas_gasstation/{nombre_descripcion}.txt', 'w') as t:
                    t.write(str(texto))
                flash('Archivo guardado con exito en reportes de Gas Station')
                return redirect(url_for('subir' , msgU = msgU))
        return render_template('subir.html')
    except Exception as e:
        flash(str(e))
        return render_template('subir.html')


#credenciales
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    try:
        if request.method == 'POST' and 'usuario' in request.form and 'contra' in request.form:
            usuario = request.form['usuario']
            contra = request.form['contra']
            cursor = mysql.get_db().cursor()
            cursor.execute('SELECT * FROM login WHERE usuario = %s', (usuario))
            data = cursor.fetchone()
            if data != None:
                if usuario == data['usuario'] and contra == data['contra']:
                    session['id'] = data['id_login']
                    return redirect(url_for('inicio'))
                else:
                    return render_template('login.html')
            else:
                msg ='Usuario/contraseña no encontrados'
                flash(str(msg))
                return render_template('login.html')   
        return render_template('login.html')
    except Exception as e:
        flash(str(e))
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('id', None)
    session.clear()
    return redirect(url_for('inicio'))





