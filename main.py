from flask import Flask,render_template,request,session,redirect, url_for,flash
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
mysql = MySQL(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'conecta2'
app.config['UPLOAD_FOLDER'] ='app\static\img'


@socketio.on('disconnect')
def disconnect_user():
    logout_user()
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    
#PRINCIPAL  
@app.route('/')
def inicio():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM carrera')
    carreras = cur.fetchall()

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM tema')
    temas = cur.fetchall()
    return render_template('home.html',carreras = carreras, temas = temas)


@app.route('/verpost/<carrera_id>/<tema_id>')
def grados(carrera_id,tema_id):
    estado = 1
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM post WHERE ID_Carrera = %s AND ID_Tema = %s AND ID_Estado = %s', (carrera_id,tema_id,estado))
    posts = cur.fetchall()

    return render_template('verpost.html',posts = posts)

@app.route('/login')
def principal():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuarios WHERE MATRICULA = %s', (session['id'],))
        account = cursor.fetchone()
        if account['NIVEL'] == 1:
            return redirect(url_for('Admin', account=account))
        else:
            return render_template('datos.html', account=account)
    return render_template("login.html")


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
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            # Create variables for easy access
            username = request.form['username']
            password = request.form['password']
            # Check if account exists using MySQL
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM login WHERE USUARIO = %s AND CONTRA = %s', (username, password,))
            # Fetch one record and return result
            account = cursor.fetchone()
            # If account exists in accounts table in out database
            if  account['NIVEL'] == 0:
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['ID_LOGIN']
                session['username'] = account['USUARIO'].capitalize()
                
                # Redirect to home page
                return redirect(url_for('profile'))
            elif  account['NIVEL'] == 1:
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['ID_LOGIN']
                session['username'] = account['USUARIO'].capitalize()
                session['level'] = account['NIVEL']
                # Redirect to home page
                return redirect(url_for('Admin'))
            else:
                # Account doesnt exist or username/password incorrect
                msg = 'Usuario\Contraseña incorrecta!'
        # Show the login form with message (if any)
        return render_template('login.html', msg=msg)


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
    if 'loggedin' in session:
        
        return render_template('Admin.html')
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


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
        print (datos)
    return render_template('Ver_usuarios.html',datos = datos)

@app.route('/post')
def post():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM carrera')
    carreras = cur.fetchall()

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM tema')
    grados = cur.fetchall()

    return render_template('post.html',carreras=carreras , grados=grados)

@app.route('/mostrarpost/<string:id>')
def mostrarpost(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM comentarios WHERE ID_Post = {0}'.format(id))
    comentarios = cur.fetchall()

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM post WHERE ID_Post = {0}'.format(id))
    contenido = cur.fetchone()

    return render_template('mostrarpost.html',comentarios=comentarios , contenido=contenido)

@app.route('/add_post' , methods=['POST'])
def add_post():
    if request.method == 'POST':
        titulo=request.form['titulo']
        texto=request.form['texto']
        carrera=request.form['carrera']
        tema=request.form['grado']
        matricula=session['id']
        like=0
        estado=1
        grado=1
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO post(Titulo,MeGusta,Texto,ID_Carrera,ID_Tema,ID_Estado,Matricula,id_grado) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',(titulo, like, texto, carrera,tema, estado,matricula, grado))
        mysql.connection.commit()
        flash('Se ha agregado su post')
        return redirect(url_for('inicio'))    

@app.route('/add_comentario/<string:id>' , methods=['POST'])
def add_comentario(id):
    if request.method == 'POST':
        texto=request.form['texto']
        cadena = texto.split()
        valor = modelo.prediccion_prob([texto])
        palabras = pd.read_csv('app/model/malas_palabras.csv', encoding = 'utf-8')
        pal = palabras['MALA_PALABRA'].tolist()
        
        if modelo.prediccion([texto]) == 1:
            print(valor, file=sys.stderr)
            print(cadena, file=sys.stdout)
            print(pal, file=sys.stdout)
            return redirect(url_for('mostrarpost',id=id))
        elif any(item in cadena for item in pal):
            print(valor, file=sys.stderr)
            return redirect(url_for('mostrarpost',id=id))
        else:
            estado=1
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO comentarios(Texto,ID_Post,ID_Estado) VALUES (%s, %s, %s)',(texto, id, estado))
            mysql.connection.commit()
            print(valor, file=sys.stderr)
            print(cadena, file=sys.stdout)
            print(pal, file=sys.stdout)
            return redirect(url_for('mostrarpost',id=id))

@app.route('/edit/<string:id>')
def get_comentario(id):
  cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
  cur.execute('SELECT * FROM comentarios WHERE ID_Comentario = {0} '.format(id))
  data = cur.fetchone()

  return render_template('editar.html', contact = data )

@app.route('/update', methods=['POST'])
def editar_comentario2():
  if request.method == 'POST':
      id = request.form['ide']
      texto = request.form['texto']
      cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      cur.execute('UPDATE comentarios SET Texto = %s WHERE ID_Comentario = %s ',(texto,id))
      mysql.connection.commit()
      flash('comentario editado con exito')
      return redirect(url_for('inicio'))

@app.route('/edita/<string:id>')
def get_comentario2(id):
  cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
  cur.execute('SELECT * FROM post WHERE ID_Post = {0} '.format(id))
  data = cur.fetchone()
  return render_template('editar2.html', contact = data )

@app.route('/update2', methods=['POST'])
def editar_comentario():
  if request.method == 'POST':
      id = request.form['ide']
      titulo = request.form['titulo']
      texto = request.form['texto']
      cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
      cur.execute('UPDATE post SET Titulo = %s, Texto = %s WHERE ID_Post = %s ',(titulo,texto,id))
      mysql.connection.commit()
      flash('POST editado con exito')
      return redirect(url_for('inicio'))

@app.route('/borrar/<string:id>')
def borrar_comentario(id):
  cur = mysql.connection.cursor()
  cur.execute('DELETE FROM comentarios WHERE ID_Comentario = {0} '.format(id))
  mysql.connection.commit()
  flash('comentario eliminado')
  return redirect(url_for('inicio'))

@app.route('/delete/<string:id>')
def borrar_post(id):
  cur = mysql.connection.cursor()
  cur.execute('DELETE FROM post WHERE ID_Post = {0} '.format(id))
  mysql.connection.commit()
  flash('post eliminado')
  return redirect(url_for('inicio'))  

@app.route('/nosotros')
def nosotros():
  return render_template('nosotros.html')

@app.route('/credito')
def creditos():
  return render_template('creditos.html')

@app.route('/busqueda')
def busqueda():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM grados')
    grados = cur.fetchall()

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM post')
    data = cur.fetchall()

    context={
      'grados':grados,
      'comentario':data
    }
    return render_template("buscar.html",**context)

@app.route('/busquedabtn', methods=['POST'])
def busquedabtn():
  if request.method == 'POST':
      grado = request.form['grado']

      cur = mysql.connection.cursor()
      cur.execute('SELECT * FROM post WHERE id_grado = %s', grado)
      busqueda= cur.fetchall() 

      cur = mysql.connection.cursor()
      cur.execute('SELECT * FROM grados')
      grados = cur.fetchall()

      context={
       'grados':grados,
       'comentario':busqueda,
      }
    
      return render_template('buscar.html',**context)

@app.route('/busqueda2')
def busqueda2():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM carrera')
    carreras = cur.fetchall()

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM post')
    data = cur.fetchall()

    context={
      'carreras':carreras,
      'comentario':data
    }
    return render_template("buscar2.html",**context)

@app.route('/busquedabtn2', methods=['POST'])
def busquedabtn2():
  if request.method == 'POST':
      carrera = request.form['carrera']
    
      cur = mysql.connection.cursor()
      cur.execute('SELECT * FROM post WHERE ID_Carrera = %s', carrera)
      busqueda= cur.fetchall() 

      cur = mysql.connection.cursor()
      cur.execute('SELECT * FROM carrera')
      carreras = cur.fetchall()

      context={
       'carreras':carreras,
       'comentario':busqueda,
      }
    
      return render_template('buscar2.html',**context)   

@app.route('/reportado_post/<string:id>')
def reportado_post(id):
    estado = 2
    cur = mysql.connection.cursor()
    cur.execute('UPDATE post SET ID_Estado = %s WHERE ID_Post = %s',(estado,id))
    mysql.connection.commit()
    return redirect(url_for('inicio'))     

@app.route('/reportado_msj/<string:id>')
def reportado_msj(id):
    estado = 2
    cur = mysql.connection.cursor()
    cur.execute('UPDATE comentarios SET ID_Estado = %s WHERE ID_Post = %s ',(estado,id))
    mysql.connection.commit()
    return redirect(url_for('inicio'))