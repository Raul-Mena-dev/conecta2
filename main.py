from pickle import TRUE
from flask import render_template,request,session,redirect, url_for,flash
from app import create_app
from flask_socketio import SocketIO, emit
from flask_login import current_user, logout_user
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from werkzeug.utils import secure_filename
import os
import modelo
import sys
import pandas as pd
from pprint import pprint

#CONFIGURACIONES
app = create_app()
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'conecta2'
app.config['UPLOAD_FOLDER'] ='app\static\img'

mysql = MySQL(app)


@socketio.on('disconnect')
def disconnect_user():
    logout_user()
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    
#PRINCIPAL  
@app.route('/')
def inicio():
    
    universidades = ['Tlajomulco','Rio Nilo','Lazaro Cardenas', 'Campus','Americas', 'Zapopan', 'Pedro Moreno', 'Olimpica']
    carreras = {}
    carreras['Tlajomulco'] = ['Derecho', 'Psicologia', 'Negocios Internacionales', 'Administracion', 'Mercadotecnia', 'Contaduria publica']
    carreras['Rio Nilo'] = ['Derecho', 'Administracion', 'Negocios Internacionales','Mercadotecnia', 'Contaduria publica']
    carreras['Lazaro Cardenas'] = ['Derecho', 'Carrera de abogado']
    carreras['Campus'] = ['Nutricion', 'Cultura Fisica y deporte', 'Psicologia', 'Enfermeria','Quimico farmaceutico biologo','Cirujano Dentista', 'Negocios Internacionales','Administracion', 'Mercadotecnia', 'Contaduria publica','Gestion de recursos humanos']
    carreras['Americas'] = ['Trabajo Social', 'Carrera de abogado', 'Derecho', 'Gastronimia', 'Diseño de modas', 'Diseño para la comunicacion grafica','Diseño de interiores','Arquitectura', 'Negocios Internacionales', 'Administracion', 'Mercadotecnia', 'Contaduria publica' ]
    carreras['Zapopan'] = ['Carrera de abogado', 'Derecho', 'Psicologia', 'Negocios Internacionales','Administracion', 'Mercadotecnia', 'Contaduria publica', 'Gestion recursos humanos']
    carreras['Pedro Moreno'] = ['Trabajo social', 'Derecho', 'Gastronomia', 'Negocios Internacionales', 'Administracion', 'Mercadotecnia', 'Contaduria publica']
    carreras['Olimpica'] = ['Comunicacion y Electronica', 'Industrial', 'Computacion', 'Civil']

    return render_template('home.html', universidades = universidades, carreras = carreras)


#perfil
@app.route('/perfil')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuarios WHERE MATRICULA = %s', (session['id'],))
        account = cursor.fetchone()
        session['account'] = account
        # Show the profile page with account info
        return render_template('datos.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


#upload
@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('sin archivo')
            return redirect(url_for('profile'))
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        filename = secure_filename(f.filename)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE usuarios SET FOTO = %s WHERE usuarios.MATRICULA = %s', (filename, session['id']))
        mysql.connection.commit()
    return redirect(url_for('profile'))


#login
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if session:
        return redirect(url_for('inicio'))
    else:    
        # Output message if something goes wrong...
        msg = ''
        # Check if "username" and "password" POST requests exist (user submitted form)
        if request.method == 'POST' and 'matricula' in request.form and 'passwordA' in request.form:
            # Create variables for easy access
            matricula = request.form['matricula']
            password = request.form['passwordA']
            # Check if account exists using MySQL
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            try:
                cursor.execute('SELECT * FROM login WHERE matricula = %s AND pass = %s', (matricula, password))
                # Fetch one record and return result
                account = cursor.fetchone()
                session['id']= account['matricula']
                session['usuario']= account['usuario']
            except Exception as e:
                return "Error: " + str(e) 
        return redirect(url_for('inicio'))


#logout
@app.route('/login/logout')
def logout():
# Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('level', None)
    session.clear()
    # Redirect to login page
    return redirect(url_for('login'))



# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/login/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'enrollment' in request.form and 'name' in request.form and 'birthday' in request.form and 'phone' in request.form:
        # Create variables for easy access
        username = request.form['username'].lower()
        password = request.form['password'].lower()
        email = request.form['email'].lower()
        name = request.form['name'].lower()
        enrollment = request.form['enrollment']
        birthday = request.form['birthday']
        phone = request.form['phone']


        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuarios WHERE MATRICULA = %s', (enrollment,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Cuenta ya existe!'
        elif not re.match('[^@]+[@alumnos.uteg.edu.mx]', str(email)):
            msg = 'Correo invalido!'
        elif not re.match('[A-Za-z0-9]+', str(username)):
            msg = 'El usuario no puede tener caracteres especiales!'
        elif not re.match('[A-Za-z\\s]+', str(name)):
            msg = 'El nombre solo debe tener letras!'
        elif not re.match('[0-9]{10}', str(enrollment)):
            msg = 'La matricula incorrecta!'
        elif not re.match('[0-9]+', str(phone)):
            msg = 'El telefono incorrecto!'
        elif not username or not password or not email or not name or not enrollment or not birthday or not phone:
            msg = 'Porfavor llena el formulario!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO usuarios(MATRICULA, NOMBRE, FNAC, TELEFONO) VALUES (%s, %s, %s, %s)', (enrollment, name, birthday, phone))
            mysql.connection.commit()
            cursor.execute('INSERT INTO login(ID_LOGIN, USUARIO, CONTRA, CORREO) VALUES (%s, %s, %s, %s)', (enrollment, username, password, email))
            mysql.connection.commit()
            msg = 'Te has registrado satisfactoriamente!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Porfavor llena el formulario!'
    # Show registration form with message (if any)
    return render_template('registro.html', msg=msg)


@app.route('/publicaciones')
def publicaciones():
    account=session['account']
    cur = mysql.connection.cursor()
    mat = session['id']
    cur.execute('SELECT * FROM post WHERE Matricula = %s ', (mat,))
    posts = cur.fetchall()
    context={
    'posts':posts,
    'account':account
    }

    return render_template('publicaciones.html', **context)


# @app.route('/mensajes')
# def mensajes():
#     print('hola')
#     # cur = mysql.connection.cursor()
#     # cur.execute(''' SELECT * FROM chat WHERE ID_RECEPTOR = 25  ''')
#     # enviado=cur.fetchall()
#     # cur.execute(''' SELECT * FROM chat WHERE ID_EMISOR = 25  ''')
#     # recibido=cur.fetchall()
#     # return render_template("mensajes.html", enviado=enviado, recibido=recibido )



#ADMINISTRADOR
@app.route("/Admin")
def Admin():
    #if 'loggedin' in session:
        
    return render_template('Admin.html')
    # User is not loggedin redirect to login page
    #return redirect(url_for('login'))


#Pagina donde se elige que tipo de usuario se registrara
@app.route("/Selec_usuario")
def Selec_usuario():
    if 'loggedin' in session:
        return render_template('Selec_usuario.html')
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


#Pagina donde se hace el registro de un nuevo usuario
@app.route("/Alta_Alum")
def Alta_usuario():
    if 'loggedin' in session:
        return render_template('Alta_Alum.html')
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route("/Alta_Admin")
def Alta_admin():
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuarios WHERE MATRICULA = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('Alta_admin.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

#Aqui se envian los datos de registro de admin a la bd
@app.route("/Registro_admin", methods=['POST'])
def Registro_admin():
    if request.method == 'POST':
        matricula = request.form['matricula']
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO administradores (ID_Admin, Nombre, Apellidos, Pass) VALUES(%s, %s, %s, %s)',
        (matricula, nombre, apellidos, password))
        mysql.connection.commit()
        return redirect(url_for('Alta_admin'))


#Pagina donde se muestran los usuarios y para hacer la eliminacion de usuario
@app.route("/Baja_Alum")
def baja_alum():
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios')
        usuarios = cur.fetchall()
        return render_template('Baja_Alum.html',usuarios = usuarios, )
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
    
#Se manda la instruccion de eliminar al usuario a la bd
@app.route("/deleteUser/<string:id>")
def deleteUser(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM login where ID_LOGIN = {0}'.format(id))
    mysql.connection.commit()
    cur.execute('DELETE FROM usuarios where MATRICULA = {0}'.format(id))
    mysql.connection.commit()
    return redirect(url_for('baja_alum'))

#Vista de los mensajes reportados
@app.route("/Reportes")
def reportes():

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM post WHERE ID_Estado = 2')
    datos = cur.fetchall()
    return render_template('Reportes.html',mensajes = datos)

#Vista para ver los usuarios
@app.route("/Ver_usuarios")
def ver_usuarios():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios')
    datos = cur.fetchall()
    return render_template('Ver_usuarios.html',usuarios = datos)

#Se hace la busqueda de usuarios de a mostrar
@app.route("/Buscar_usuarios", methods=['POST','GET'])
def buscar_usuarios():
    if request.method == 'POST':
        dato = request.form['buscar']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM usuarios WHERE NOMBRE  = %s OR MATRICULA = %s', (dato,dato))
        datos = cur.fetchone()
    return render_template('Ver_usuarios.html',datos = datos)

#Seccion de post  

#****** NUEVO ******
@app.route("/obtenerID/<string:plantel>/<string:carrera>")
def obtenerID(plantel,carrera):
    cur = mysql.connection.cursor()
    cur.execute('SELECT id_plantel FROM planteles WHERE plantel = %s',(plantel,))
    id_plantel = cur.fetchone()

    cur = mysql.connection.cursor()
    cur.execute('SELECT id_carrera FROM carrera WHERE carrera = %s AND id_plantel = %s',(carrera,id_plantel))
    id_carrera = cur.fetchone()
    
    return redirect(url_for('listar',id_plantel = id_plantel, id_carrera = id_carrera))

#Se muestra la lista de post
@app.route("/listar/<string:id_plantel>/<string:id_carrera>")
def listar(id_plantel,id_carrera):

    mostrar = True

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT post.id_post, post.titulo, post.fecha, post.id_estado, login.usuario FROM post  INNER JOIN usuarios on post.matricula = usuarios.matricula INNER JOIN login on usuarios.matricula = login.matricula WHERE post.id_plantel  = %s AND post.id_carrera = %s ORDER BY fecha DESC', (id_plantel,id_carrera))
    posts = cur.fetchall()

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT planteles.plantel, carrera.carrera FROM planteles INNER JOIN carrera ON planteles.id_plantel = carrera.id_plantel WHERE carrera.id_plantel = %s AND carrera.id_carrera = %s', (id_plantel,id_carrera))
    centroUni = cur.fetchall()

    if posts == ():
        mostrar = False


    return render_template('verpost.html',posts = posts, centroUni = centroUni, mostrar = mostrar, id_plantel = id_plantel, id_carrera = id_carrera)

#Se accede a un post para ver el contenido
@app.route("/mostrarpost/<string:id>")
def mostrarpost(id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT post.id_post, post.titulo, post.contenido, post.fecha ,login.usuario FROM post INNER JOIN usuarios ON post.matricula = usuarios.matricula INNER JOIN login ON usuarios.matricula = login.matricula WHERE id_post = %s', (id,))
    post = cur.fetchone()

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT respuestas.id_respuesta, respuestas.contenido, respuestas.fecha, respuestas.id_estado, login.usuario FROM respuestas INNER JOIN usuarios ON respuestas.matricula = usuarios.matricula INNER JOIN login ON usuarios.matricula = login.matricula WHERE id_post = %s ORDER BY fecha DESC', (id,))
    respuestas = cur.fetchall()
    return render_template('mostrarpost.html', post = post, respuestas = respuestas)

#Se agrega una nueva publicacion
@app.route("/add_post/<string:id_carrera>/<string:id_plantel>/<string:matricula>",  methods=['POST'])
def add_post(id_carrera, id_plantel, matricula):
    if request.method == 'POST':
        #Linea de matricula a borrar, ajusta cuando exista sesion
        titulo = request.form['titulo']
        contenido = request.form['contenido']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('INSERT INTO post(titulo, contenido, matricula, id_plantel, id_carrera) VALUES(%s, %s, %s, %s, %s)', (titulo, contenido, matricula, id_plantel, id_carrera))
        mysql.connection.commit()
        return redirect(url_for('listar',id_plantel=id_plantel,id_carrera=id_carrera))

#Se agrega una respuesta a la publicacion
@app.route("/add_comentario//<string:matricula>",  methods=['POST'])
def add_comentario(id, matricula):
    if request.method == 'POST':
        contenido = request.form['texto']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('INSERT INTO respuestas(contenido, matricula, id_post) VALUES(%s, %s, %s)', (contenido, matricula, id))
        mysql.connection.commit()
        return redirect(url_for('mostrarpost',id = id))

#Se toman acciones al reportar una publicacion
@app.route('/reportar_publi/<string:id>')
def reportar_publi(id):
    estado = 2
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT id_carrera FROM post WHERE id_post = %s',(id,))
        id_carrera = cur.fetchone()
        cur = mysql.connection.cursor()
        cur.execute('SELECT id_plantel FROM post WHERE id_post = %s',(id,))
        id_plantel = cur.fetchone()
        cur = mysql.connection.cursor()
        cur.execute('UPDATE post SET id_estado = %s WHERE id_post = %s',(estado,id))
        mysql.connection.commit()
        return redirect(url_for('listar',id_plantel=id_plantel,id_carrera=id_carrera)) 
    except Exception as e:
        print("Error"+ str(e)) 
        return redirect(url_for('mostrarpost',id=id)) 

#Se toman acciones al reportar una respuesta
@app.route('/reportar_msj/<string:id_pub>/<string:id_msj>')
def reportar_msj(id_pub,id_msj):
    estado = 2
    try:
        cur = mysql.connection.cursor()
        cur.execute('UPDATE respuestas SET id_estado = %s WHERE id_respuesta = %s',(estado,id_msj))
        mysql.connection.commit()
        return redirect(url_for('mostrarpost',id=id_pub))
    except Exception as e:
        print("Error"+ str(e))
        return redirect(url_for('mostrarpost',id=id_pub))

@app.route('/actualiza_publi/<string:id>')
def actualizar_publi(id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT post.id_post, post.titulo, post.contenido, post.fecha ,login.usuario FROM post INNER JOIN usuarios ON post.matricula = usuarios.matricula INNER JOIN login ON usuarios.matricula = login.matricula WHERE id_post = %s', (id,))
    post = cur.fetchone()

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT respuestas.id_respuesta, respuestas.contenido, respuestas.fecha, respuestas.id_estado, login.usuario FROM respuestas INNER JOIN usuarios ON respuestas.matricula = usuarios.matricula INNER JOIN login ON usuarios.matricula = login.matricula WHERE id_post = %s ORDER BY fecha DESC', (id,))
    respuestas = cur.fetchall()
    return render_template('actualiza_publi.html', post = post, respuestas = respuestas)


@app.route('/actualizacion/<string:id>', methods = ['POST'])
def actualizacion(id):
    if request.method == 'POST':
        titulo = request.form['titulo']
        contenido = request.form['texto']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('UPDATE post SET titulo = %s, contenido = %s WHERE id_post = %s',(titulo,contenido,id,))
        mysql.connection.commit()
        return redirect(url_for('mostrarpost',id=id))

@app.route('/actualiza_msj/<string:id_post>/<string:id_msj>')
def actualiza_msj(id_post,id_msj):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT post.id_post, post.titulo, post.contenido, post.fecha ,login.usuario FROM post INNER JOIN usuarios ON post.matricula = usuarios.matricula INNER JOIN login ON usuarios.matricula = login.matricula WHERE id_post = %s', (id_post,))
    post = cur.fetchone()

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT respuestas.id_respuesta, respuestas.contenido, respuestas.fecha, respuestas.id_estado, login.usuario FROM respuestas INNER JOIN usuarios ON respuestas.matricula = usuarios.matricula INNER JOIN login ON usuarios.matricula = login.matricula WHERE id_post = %s ORDER BY fecha DESC', (id_post,))
    respuestas = cur.fetchall()

    return render_template('actualiza_coment.html', post = post, respuestas = respuestas, id_validar = id_msj)

@app.route('/actualizacion_msj/<string:id_post>/<string:id_msj>', methods = ['POST'])
def actualziacion_msj(id_post,id_msj):
    if request.method == 'POST':
        print(id_msj)
        contenido = request.form['texto']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('UPDATE respuestas SET contenido = %s WHERE id_respuesta = %s',(contenido,id_msj,))
        mysql.connection.commit()
        return redirect(url_for('mostrarpost',id=id_post))