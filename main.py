from crypt import methods
from app import create_app, script_pytest
from flask import render_template, redirect, url_for, request, flash, session
import os
import webbrowser
from werkzeug.utils import secure_filename

app = create_app()  
app.config['UPLOAD_FOLDER'] ='app/static/pruebas_gasstation'
app.config['UPLOAD_FOLDER2'] ='app/static/pruebas_sgc'
app.config['SECRET_KEY'] = 'mysecret'

    

#gasstation
@app.route('/')
def inicio():
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
    for file in os.listdir(f'/home/rmenapc/Escritorio/test_station/app/static/reports_sgc/{report}'):
        if file.endswith('.html'):
            reports.append(file)
    return render_template('reportes.html', reports = reports, fecha = report)

@app.route('/mostrar_sgc', methods=['GET'])
def mostrar_sgc():
    reporte = request.args.get('reporte')
    folder = request.args.get('folder')
    url = f'/home/rmenapc/Escritorio/test_station/app/static/reports_sgc/{folder}/' + reporte
    webbrowser.open_new_tab(url)

    return redirect(url_for('reportes_sgc', report = folder))

@app.route('/test_sgc')
def test_sgc():
    tests = []
    descripcion = {}
    for file in os.listdir('/home/rmenapc/Escritorio/test_station/app/static/pruebas_sgc/'):
        if file.endswith('.py'):
            file = file.replace('.py', '')
            tests.append(file)
    for file in os.listdir('/home/rmenapc/Escritorio/test_station/app/static/pruebas_sgc/'):
        if file.endswith('.txt'):
            texto = open(f'/home/rmenapc/Escritorio/test_station/app/static/pruebas_sgc/{file}', 'r')
            texto = texto.read()
            file = file.replace('.txt', '')
            descripcion[file] = texto
    tests.sort()
    return render_template('test_sgc.html', tests = tests, descripcion = descripcion)


@app.route('/test_sgc/<string:prueba>')
def ejecutar_sgc(prueba):
    try:
        script_pytest.script_pytest2(prueba)
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
            if option == 'sgc':
                f.save(os.path.join(app.config['UPLOAD_FOLDER2'], secure_filename(f.filename)))
                with open(f'app/static/pruebas_sgc/{nombre_descripcion}.txt', 'w') as t:
                    t.write(str(texto))
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
    try:
        if request.method == 'POST' and 'usuario' in request.form and 'contra' in request.form:
            usuario = request.form['usuario']
            contra = request.form['contra']

            if usuario == 'raul' and contra == '12345678':
                session['id'] = '1'
                return redirect(url_for('inicio'))
            else:
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





