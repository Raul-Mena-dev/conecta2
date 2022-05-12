from datetime import date
from flask import render_template,request,session,redirect, url_for,flash
from app import create_app
from flask_mysqldb import MySQL
import modelo
from flask_bcrypt import Bcrypt
import MySQLdb.cursors
import re
from werkzeug.utils import secure_filename
import os
import pandas as pd

#CONFIGURACIONES
app = create_app()
app.config['SECRET_KEY'] = 'mysecret'

# app.config['MYSQL_HOST'] = 'RaulMena.mysql.pythonanywhere-services.com'
# app.config['MYSQL_USER'] = 'RaulMena'
# app.config['MYSQL_PASSWORD'] = 'Smersyc1+'
# app.config['MYSQL_DB'] = 'RaulMena$conectados'
# app.config['UPLOAD_FOLDER'] ='/home/RaulMena/conecta2/app/static/img'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'conecta2'
app.config['UPLOAD_FOLDER'] ='app\static\img'

mysql = MySQL(app)
bcrypt = Bcrypt(app)



#PRINCIPAL
@app.route('/')
def portada():
    return render_template('portada.html')

@app.route('/inicio')
def inicio():

    if 'id' in session:
        universidades = ['Guadalajara','Tlaquepaque', 'Zapopan']
        carreras = {}
        carreras['Guadalajara'] = ['Bachillerato','Derecho', 'Psicologia', 'Negocios Internacionales', 'Administracion', 'Mercadotecnia', 'Contaduria publica']
        carreras['Tlaquepaque'] = ['Bachillerato','Ingenieria en Computacion', 'Ingenieria en Electronica', 'Ingenieria Industrial','Ingenieria Civil']
        carreras['Zapopan'] = ['Bachillerato','Derecho', 'Gastronomia', 'Ingenieria Industrial','Quimica']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM banner")
        banners = cursor.fetchall()

        return render_template('home.html', universidades = universidades, carreras = carreras, banners = banners)
    return render_template('portada.html')

@app.route('/busqueda', methods=['POST'])
def buscar():
    if request.method == 'POST' and 'buscar' in request.form:
        buscar = request.form['buscar']
        mostrar = True

        if buscar == "":
            return redirect(url_for('inicio'))
        today = date.today()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT post.id_post, post.titulo, date(post.fecha) as fecha, post.fecha as tiempo, post.id_estado, login.usuario, nivel.id_nivel_estudio as nivel, nivel.nivel_estudio  FROM post  INNER JOIN usuarios on post.matricula = usuarios.matricula INNER JOIN login on usuarios.matricula = login.matricula INNER JOIN nivel on usuarios.id_nivel_estudio = nivel.id_nivel_estudio WHERE post.titulo LIKE '%{}%' OR post.contenido LIKE '%{}%';".format(buscar,buscar))
        posts = cursor.fetchall()

        if posts == ():
            mostrar = False

        print(posts)
        return render_template('resultadoBusqueda.html', posts=posts, mostrar = mostrar, today = today)
    
    return redirect(url_for('inicio'))

@app.route('/legal')
def legal():
    return render_template('legal.html')

@app.route('/reglas')
def reglas():
    return render_template('reglas.html')

@app.route('/tutorial')
def tutorial():
    return render_template('tuto.html')

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')


#perfil
@app.route('/perfil')
def profile():
    # Check if user is loggedin
    if 'id' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT a.nombre, a.apellido1, a.apellido2, a.fnac, a.matricula, a.correo, a.foto, b.plantel, c.carrera FROM usuarios as a INNER JOIN planteles as b ON a.id_plantel INNER JOIN carrera as c ON a.id_plantel WHERE a.matricula = %s AND a.id_plantel = b.id_plantel AND a.id_carrera = c.id_carrera', (session['id'],))
        account = cursor.fetchone()
        session['account'] = account
        # Show the profile page with account info
        return render_template('datos.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/cambioContraseña', methods=['GET', 'POST'])
def contra():
    if request.method == 'POST' and 'actual' in request.form and 'nueva' in request.form and 'repetir' in request.form:

        actual = request.form['actual']
        nueva = request.form['nueva']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM login WHERE matricula = %s;', (session['id'],))
        datos = cursor.fetchone()
        try:
            if bcrypt.check_password_hash(datos['pass'], actual):
                pw_hash = bcrypt.generate_password_hash(nueva, 10)
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('UPDATE login SET pass = %s WHERE login.matricula = %s' ,(pw_hash, session['id'],))
                mysql.connection.commit()
                flash('Cambio exitoso')
                return redirect(url_for('profile'))
            else:
                flash('error al cambiar su contraseña')
                return render_template('contra.html')
        except Exception as e:
            flash("Error: " + str(e))
            return render_template('contra.html')

    return render_template('contra.html')


#upload
@app.route('/', methods=['GET', 'POST'])
def upload():
    msgU = ''
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('sin archivo')
            return redirect(url_for('profile'))
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        filename = secure_filename(f.filename)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE usuarios SET foto = %s WHERE usuarios.matricula = %s', (filename, session['id']))
        mysql.connection.commit()
        return redirect(url_for('profile', msgU = msgU))
    return redirect(url_for('profile'))




#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    session.pop('id_plantel', None)
    session.pop('id_carrera', None)
    session.pop('nivel', None)
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
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM login WHERE matricula = %s;', (matricula,))
            datos = cursor.fetchone()
            # Check if account exists using MySQL
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            try:
                if(bcrypt.check_password_hash(datos['pass'], password)):
                    cursor.execute('SELECT a.nombre, a.apellido1, a.matricula, a.id_nivel_estudio FROM usuarios as a INNER JOIN login as b ON a.matricula = b.matricula WHERE b.matricula = %s;', (matricula,))
                    # Fetch one record and return result
                    usuario = cursor.fetchone()
                    session['id'] = usuario['matricula']
                    nombreUsuario = usuario['nombre'].capitalize() +' '+ usuario['apellido1'].capitalize()
                    session['usuario']= nombreUsuario
                    session['nivel'] = usuario['id_nivel_estudio']
                    return redirect(url_for('profile'))
                else:
                    msg = "Usuario y/o contraseña incorrecto"
                    return render_template('login.html', msg = msg)
            except Exception as e:
                msg = "Usuario y/o contraseña incorrecto"
                return render_template('login.html', msg = msg)
        else:
            return render_template('login.html')


#logout
@app.route('/login/logout')
def logout():
# Remove session data, this will log the user out
    session.pop('id', None)
    session.pop('usuario', None)
    session.clear()
    # Redirect to login page
    return redirect(url_for('inicio'))


@app.route('/login/registrar', methods=['POST'])
def registrar():

    try:
        if request.method == 'POST' and 'matriculaR' in request.form and 'email' in request.form and 'passwordR' in request.form:
            
            passwordR = request.form['passwordR']
            email = request.form['email']
            matriculaR = request.form['matriculaR']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM login WHERE matricula = %s', (matriculaR,))
            cuenta = cursor.fetchone()
            if cuenta:
                msg = 'Cuenta ya existe!'
                return render_template('login.html', msg=msg)
            else:
                cursor.execute('SELECT * FROM usuarios WHERE matricula = %s', (matriculaR,))
                usuario = cursor.fetchone()
                if not usuario:
                    flash('usuario no esta en la base de datos')
                    return render_template('login.html')

                if bcrypt.check_password_hash(usuario['pass'], passwordR):
                    if not usuario:
                        flash('usuario no esta en la base de datos')
                        return render_template('login.html')
                    elif not re.match('[^@]+[@conectados.edu.mx]', str(email)):
                        flash('Correo invalido!')
                        return render_template('login.html')
                    elif not re.match('[0-9]{9,11}', str(matriculaR)):
                        flash('La matricula incorrecta!')
                        return render_template('login.html')
                    elif not passwordR or not email or not matriculaR:
                        flash('Porfavor llena el formulario!')
                        return render_template('login.html')
                    else:
                        
                        nombreUsuario = usuario['nombre'] +' '+ usuario['apellido1']
                        cursor.execute('INSERT INTO login(matricula,pass,usuario) VALUES (%s, %s, %s)', (matriculaR, usuario['pass'] ,nombreUsuario))
                        mysql.connection.commit()
                        flash('Te has registrado satisfactoriamente')
                        session['id'] = usuario['matricula']
                        nombreUsuario = usuario['nombre'].capitalize() +' '+ usuario['apellido1'].capitalize()
                        session['usuario']= nombreUsuario
                        session['nivel'] = usuario['id_nivel_estudio']
                        return redirect(url_for('profile'))
                else:
                    flash('Porfavor llena el formulario!')
                    return render_template('login.html')
        elif request.method == 'POST':
            flash('Porfavor llena el formulario!')
            return render_template('login.html')
        else :
            return render_template('login.html')
    except Exception as e:
        flash(str(e))
        return render_template('login.html')



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




#ADMINISTRADOR
@app.route("/Admin")
def Admin():
    if session['nivel'] == 4 or session['nivel'] == 5:
        return render_template('Admin.html')
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


#Pagina donde se elige que tipo de usuario se registrara
@app.route("/Selec_usuario")
def Selec_usuario():
    if session['nivel'] == 4 or session['nivel'] == 5:
        return render_template('Selec_usuario.html')
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


#Pagina donde se hace el registro de un nuevo usuario
@app.route("/Alta_Alum")
def Alta_usuario():
    if session['nivel'] == 4 or session['nivel'] == 5:
        return render_template('Alta_Alum.html')
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route("/Alta_admin")
def Alta_admin():
    if session['nivel'] == 4 or session['nivel'] == 5:
        # We need all the account info for the user so we can display it on the profile page
        cur = mysql.connection.cursor()
        cur.execute('SELECT usuarios.matricula, usuarios.nombre, usuarios.apellido1, usuarios.apellido2, usuarios.fnac, usuarios.correo, login.usuario FROM usuarios INNER JOIN login ON usuarios.matricula = login.matricula where usuarios.id_nivel_estudio = 3')
        usuarios = cur.fetchall()
        # Show the profile page with account info
        return render_template('Alta_admin.html', usuarios = usuarios)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

#Dar privilegios de administrador
@app.route('/Dar_admin/<string:id>') 
def Dar_admin(id): 
    if session['nivel'] == 4 or session['nivel'] == 5:
        nivel = 4
        try:
            cur = mysql.connection.cursor()
            cur.execute('UPDATE usuarios SET id_nivel_estudio = %s WHERE matricula = %s',(nivel,id))
            mysql.connection.commit()
            return redirect(url_for('Alta_admin'))
        except Exception as e:
            print("Error"+ str(e))
            return redirect(url_for('Alta_admin'))
    return redirect(url_for('login'))

#Aqui se envian los datos de registro de admin a la bd
@app.route("/Registro_admin", methods=['POST'])
def Registro_admin():
    if session['nivel'] == 4 or session['nivel'] == 5:
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
    return redirect(url_for('login')) 


#Pagina donde se muestran los usuarios y para hacer la eliminacion de usuario
@app.route("/Baja_admin")
def Baja_admin():
    if session['nivel'] == 4 or session['nivel'] == 5:
        # We need all the account info for the user so we can display it on the profile page
        cur = mysql.connection.cursor()
        cur.execute('SELECT usuarios.matricula, usuarios.nombre, usuarios.apellido1, usuarios.apellido2, usuarios.fnac, usuarios.correo, login.usuario FROM usuarios INNER JOIN login ON usuarios.matricula = login.matricula where usuarios.id_nivel_estudio = 4')
        usuarios = cur.fetchall()

        return render_template('Baja_Alum.html',usuarios = usuarios, )
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

#Quitar privilegios de administrador
@app.route('/Quitar_admin/<string:id>')
def Quitar_admin(id):
    if session['nivel'] == 4 or session['nivel'] == 5:
        nivel = 3
        try:
            cur = mysql.connection.cursor()
            cur.execute('UPDATE usuarios SET id_nivel_estudio = %s WHERE matricula = %s AND usuarios.id_nivel_estudio = 4',(nivel,id))
            mysql.connection.commit()
            return redirect(url_for('Baja_admin'))
        except Exception as e:
            print("Error"+ str(e))
            return redirect(url_for('Baja_admin'))
    return redirect(url_for('login'))

#Se manda la instruccion de eliminar al usuario a la bd
@app.route("/deleteUser/<string:id>")
def deleteUser(id):
    if session['nivel'] == 4 or session['nivel'] == 5:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM respuestas where matricula = %s', (id,))
        mysql.connection.commit()

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM post where matricula = %s', (id,))
        publicaciones = cur.fetchall()

        for publicacion in publicaciones:
            print(publicacion)
            cur = mysql.connection.cursor()
            cur.execute('DELETE FROM archivos where id_post = %s', (publicacion[0],))
            mysql.connection.commit()

            cur = mysql.connection.cursor()
            cur.execute('DELETE FROM tageados where id_post = %s', (publicacion[0],))
            mysql.connection.commit()

            cur = mysql.connection.cursor()
            cur.execute('DELETE FROM respuestas where id_post = %s', (publicacion[0],))
            mysql.connection.commit()

            cur = mysql.connection.cursor()
            cur.execute('DELETE FROM post where id_post = %s', (publicacion[0],))
            mysql.connection.commit()

        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM login where matricula = %s', (id,))
        mysql.connection.commit()
        return redirect(url_for('Ver_usuarios'))
    return redirect(url_for('login'))

#Vista de los mensajes reportados
@app.route("/Reportes")
def Reportes():
    if session['nivel'] == 4 or session['nivel'] == 5:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM post WHERE id_estado = 2 or id_estado = 3')
        publicaciones = cur.fetchall()

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM respuestas WHERE id_estado = 2 or id_estado = 3')
        respuestas = cur.fetchall()
        return render_template('Reportes.html', publicaciones=publicaciones, respuestas = respuestas)
    return redirect(url_for('login'))

@app.route("/Restaurar_publi/<string:id>")
def Restaurar_publi(id):
    if session['nivel'] == 4 or session['nivel'] == 5:
        estado = 1
        try:
            cur = mysql.connection.cursor()
            cur.execute('UPDATE post SET id_estado = %s WHERE id_post = %s',(estado,id))
            mysql.connection.commit()
            return redirect(url_for('Reportes'))
        except Exception as e:
            print("Error"+ str(e))
            return redirect(url_for('Reportes'))
    return redirect(url_for('login'))

@app.route("/Restaurar_msj/<string:id>")
def Restaurar_msj(id):
    if session['nivel'] == 4 or session['nivel'] == 5:
        estado = 1
        try:
            cur = mysql.connection.cursor()
            cur.execute('UPDATE respuestas SET id_estado = %s WHERE id_respuesta = %s',(estado,id))
            mysql.connection.commit()
            return redirect(url_for('Reportes'))
        except Exception as e:
            print("Error"+ str(e))
            return redirect(url_for('Reportes'))
    return redirect(url_for('login'))


#Vista para ver los usuarios
@app.route("/Ver_usuarios")
def Ver_usuarios():
    if session['nivel'] == 4 or session['nivel'] == 5:
        cur = mysql.connection.cursor()
        cur.execute('SELECT usuarios.matricula, usuarios.nombre, usuarios.apellido1, usuarios.apellido2, usuarios.fnac, usuarios.correo, login.usuario FROM usuarios INNER JOIN login ON usuarios.matricula = login.matricula')
        datos = cur.fetchall()
        print(datos)
        return render_template('Ver_Usuarios.html',usuarios = datos)
    return redirect(url_for('login'))


#Se hace la busqueda de usuarios de a mostrar
@app.route("/Buscar_usuarios", methods=['POST','GET'])
def buscar_usuarios():
    if session['nivel'] == 4 or session['nivel'] == 5:
        if request.method == 'POST':
            dato = request.form['buscar']
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute('SELECT usuarios.matricula, usuarios.nombre, usuarios.apellido1, usuarios.apellido2, usuarios.fnac, usuarios.correo, login.usuario FROM usuarios INNER JOIN login ON usuarios.matricula = login.matricula WHERE usuarios.matricula = %s', (dato,))
            datos = cur.fetchone()
        return render_template('Ver_usuarios.html',datos = datos)
    return redirect(url_for('login'))


@app.route('/actu_banner')
def actu_banner():

    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('Select * FROM banner')
        banners = cur.fetchall()
        return render_template('actubanner.html', banners=banners)
    except Exception as e:
        flash('Error al cargar banner')
        return render_template('actubanner.html')

@app.route('/add_banner', methods = ['POST', 'GET'])
def add_banner():

    try:
        if request.method == 'POST':
            titulo = request.form['titulo']
            mensaje = request.form['mensaje']
            if 'imagen' not in request.files:
                flash('sin Imagen')
                return redirect(url_for('actu_banner'))
            f = request.files['imagen']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            filename = secure_filename(f.filename)
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute('INSERT INTO banner(imagen, titulo, texto) VALUES (%s, %s, %s)', (filename,titulo,mensaje))
            mysql.connection.commit()
            flash('Agregado satisafactoriamente')
            return redirect(url_for('actu_banner'))
    except Exception as e:
        msg = str(e)
        flash('Error al añadir al banner ' + msg)
        return redirect(url_for('actu_banner'))
    

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

    session['id_plantel'] = id_plantel
    session['id_carrera'] = id_carrera

    return redirect(url_for('listar'))

#Se muestra la lista de post
@app.route("/listar")
def listar():

    id_plantel = session['id_plantel']
    id_carrera = session['id_carrera']
    mostrar = True

    today = date.today()

    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT post.id_post, post.titulo, date(post.fecha) as fecha, post.fecha as tiempo, post.id_estado, login.usuario, nivel.id_nivel_estudio as nivel, nivel.nivel_estudio, usuarios.foto, tageados.id_tag, tags.tag, tags.id_tags, tags.id_tag as tg FROM post  INNER JOIN usuarios on post.matricula = usuarios.matricula INNER JOIN login on usuarios.matricula = login.matricula INNER JOIN nivel on usuarios.id_nivel_estudio = nivel.id_nivel_estudio LEFT JOIN tageados ON post.id_post = tageados.id_post INNER JOIN tags on tageados.id_tag = tags.id_tags WHERE post.id_plantel  = %s AND post.id_carrera = %s ORDER BY post.fecha DESC", (id_plantel,id_carrera,))
        posts = cur.fetchall()
        
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT planteles.id_plantel, planteles.plantel, carrera.carrera FROM planteles INNER JOIN carrera ON planteles.id_plantel = carrera.id_plantel WHERE carrera.id_plantel = %s AND carrera.id_carrera = %s', (id_plantel,id_carrera,))
        centroUni = cur.fetchall()

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM tags")
        tags = cur.fetchall()
    except Exception as e:
        msg=str(e)
        print(msg)
        return render_template('verpost.html',posts = posts, centroUni = centroUni, mostrar = mostrar, id_plantel = id_plantel, id_carrera = id_carrera, today = today, tags=tags)
    if posts == ():
        mostrar = False

    return render_template('verpost.html',posts = posts, centroUni = centroUni, mostrar = mostrar, id_plantel = id_plantel, id_carrera = id_carrera, today = today, tags=tags)

#Se accede a un post para ver el contenido
@app.route("/mostrarpost/<string:id>")
def mostrarpost(id):

    mostrar = False

    if 'nivel' not in session:
        session['nivel'] = 0
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT post.matricula, post.id_post, post.titulo, post.contenido, post.fecha ,login.usuario, carrera.carrera, usuarios.foto FROM post INNER JOIN usuarios ON post.matricula = usuarios.matricula INNER JOIN login ON usuarios.matricula = login.matricula INNER JOIN carrera ON post.id_carrera = carrera.id_carrera  WHERE post.id_post = %s', (id,))
    post = cur.fetchone()

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM archivos WHERE id_post = %s', (id,))
    archivos = cur.fetchall()

    print(archivos)
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT respuestas.matricula, respuestas.id_respuesta, respuestas.contenido, respuestas.fecha, respuestas.id_estado, usuarios.foto, login.usuario FROM respuestas INNER JOIN usuarios ON respuestas.matricula = usuarios.matricula INNER JOIN login ON usuarios.matricula = login.matricula WHERE id_post = %s ORDER BY fecha DESC', (id,))
    respuestas = cur.fetchall()

    for archivo in archivos:
        if not archivo['id_respuestas']:
            mostrar = True
            break
    
    return render_template('mostrarpost.html', post = post, respuestas = respuestas, archivos = archivos, mostrar = mostrar)


@app.route('/subirPrueba', methods = ['POST'])
def subirPrueba():
    files = request.files.getlist('file[]')
    for file in files:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        filename = secure_filename(file.filename)
        print(filename)
    return render_template("home.html")

#Se agrega una nueva publicacion
@app.route("/add_post",  methods=['POST'])
def add_post():
    msg=''
    id_plantel = session['id_plantel']
    id_carrera = session['id_carrera']
    try:
        
        matricula = session['id']
        if request.method == 'POST':
            estado = 1
            tag = request.form['tags']
            titulo = request.form['titulo']

            # Titulo de los post
            if modelo.prediccion([titulo]):
                flash('Tu titulo contiene lenguaje inapropiado')
                print(titulo)
                return redirect(url_for('listar'))
            

            #comprobaccion por diccionario
            df = pd.read_csv('app/model/malas_palabras.csv')
            liTitulo = list(titulo.split(" "))
            for palabra in liTitulo:
                for mala in df["MALA_PALABRA"]:
                    if palabra == mala:
                        print(modelo.prediccion_prob([contenido]))
                        flash('El contenido contiene lenguaje inapropiado')
                        return redirect(url_for('listar'))
            
            # Contenido de los post
            contenido = request.form['contenido']
            
            if modelo.prediccion([contenido]):
                print(modelo.prediccion_prob([contenido]))
                flash('El contenido contiene lenguaje inapropiado')
                return redirect(url_for('listar'))
            
            #comprobaccion por diccionario
            df = pd.read_csv('app/model/malas_palabras.csv')
            liContenido = list(contenido.split(" "))
            for palabra in liContenido:
                for mala in df["MALA_PALABRA"]:
                    if palabra == mala:
                        print(modelo.prediccion_prob([contenido]))
                        print("Funcino")
                        flash('El contenido contiene lenguaje inapropiado')
                        return redirect(url_for('listar'))
            
            #carga de archivos e insercion en la base de datos
            if 'file' in request.files:
                files = request.files.getlist('file')
                files_size = len(files)
                if files_size > 5:
                    flash('Maximo 5 archivos')
                    return redirect(url_for('listar'))
            if int(tag) > 0:
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute('INSERT INTO post(titulo, contenido, matricula, id_plantel, id_carrera, id_estado) VALUES(%s, %s, %s, %s, %s, %s)', (titulo, contenido, matricula, id_plantel, id_carrera, estado))
                mysql.connection.commit()
                id = cur.lastrowid
        
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute('INSERT INTO tageados(id_tag,id_post) VALUES(%s, %s)', (tag, id,))
                mysql.connection.commit()
            else:
                flash('Seleccione una etiqueta valida')
                return redirect(url_for('listar'))
            file = request.files['file']

            if file.filename != '':
                for file in request.files.getlist('file'):
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
                    filename = secure_filename(file.filename)
                    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cur.execute('INSERT INTO archivos(nombre_archivo,id_post) VALUES(%s, %s)', (filename, id,))
                    mysql.connection.commit()
            flash('Agregado exitosamente')
            return redirect(url_for('listar'))

    except Exception as e:
        msg = str(e)
        flash(msg)
        return redirect(url_for('listar'))

#Se agrega una respuesta a la publicacion
@app.route("/add_comentario/<string:id>/<string:matricula>",  methods=['POST'])
def add_comentario(id, matricula):
   #try:
    if request.method == 'POST':
        estado = 1
        contenido = request.form['texto']
        if modelo.prediccion([contenido]):
                print(modelo.prediccion_prob([contenido]))
                flash('El contenido contiene lenguaje inapropiado')
                return redirect(url_for('mostrarpost',id = id))
        #Contenido de la respuesta
        df = pd.read_csv('app/model/malas_palabras.csv')
        liContenido = list(contenido.split(" "))
        for palabra in liContenido:
            for mala in df["MALA_PALABRA"]:
                if palabra == mala:
                    print(modelo.prediccion_prob([contenido]))
                    flash('El contenido contiene lenguaje inapropiado')
                    return redirect(url_for('mostrarpost',id = id))
        if 'file' in request.files:
                files = request.files.getlist('file')
                files_size = len(files)
                if files_size > 5:
                    flash('Maximo 5 archivos')
                    return redirect(url_for('mostrarpost',id = id))
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('INSERT INTO respuestas(contenido, matricula, id_post, id_estado) VALUES(%s, %s, %s, %s)', (contenido, matricula, id, estado,))
        mysql.connection.commit()
        id_last = cur.lastrowid
            
        file = request.files['file']
        
        if file.filename != '':
            for file in request.files.getlist('file'):
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
                filename = secure_filename(file.filename)
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute('INSERT INTO archivos(nombre_archivo,id_post,id_respuestas) VALUES(%s, %s, %s)', (filename, id, id_last,))
                mysql.connection.commit()
        flash('Agregado exitosamente')
        return redirect(url_for('mostrarpost',id = id))
    # except Exception as e:
    #     msg = str(e)
    #     flash(msg)
    #     return redirect(url_for('mostrarpost',id = id))

#Se toman acciones al reportar una publicacion
@app.route('/reportar_publi/<string:id>')
def reportar_publi(id):
    estado = 3
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
    estado = 3
    try:
        cur = mysql.connection.cursor()
        cur.execute('UPDATE respuestas SET id_estado = %s WHERE id_respuesta = %s',(estado,id_msj))
        mysql.connection.commit()
        return redirect(url_for('mostrarpost',id=id_pub))
    except Exception as e:
        print("Error"+ str(e))
        return redirect(url_for('mostrarpost',id=id_pub))

@app.route('/reportar_publi_admin/<string:id>')
def reportar_publi_admin(id):
    estado = 2
    try:
        cur = mysql.connection.cursor()
        cur.execute('UPDATE post SET id_estado = %s WHERE id_post = %s',(estado,id))
        mysql.connection.commit()
        return redirect(url_for('listar'))
    except Exception as e:
        print("Error"+ str(e))
        return redirect(url_for('mostrarpost',id=id))

#Se toman acciones al reportar una respuesta
@app.route('/reportar_msj_admin/<string:id_pub>/<string:id_msj>')
def reportar_msj_admin(id_pub,id_msj):
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

@app.route('/actualiza_banner/<string:id_banner>', methods = ['POST'])
def actualiza_banner(id_banner):
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        filename = secure_filename(f.filename)
        titulo = request.form['titulo']
        contenido = request.form['texto']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE banner SET imagen = %s WHERE id_banner = %s', (filename, id_banner))
        mysql.connection.commit()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE banner SET titulo = %s WHERE id_banner = %s', (titulo, id_banner))
        mysql.connection.commit()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE banner SET texto = %s WHERE id_banner = %s', (contenido, id_banner))
        mysql.connection.commit()

        return redirect(url_for('actu_banner'))

@app.route('/eliminar_banner/<string:id_banner>')
def eliminar_banner(id_banner):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM banner where id_banner = %s', (id_banner))
        mysql.connection.commit()

        return redirect(url_for('actu_banner'))

@app.route('/editar_banner/<string:id_banner>')
def editar_banner(id_banner):   
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('Select * FROM banner where id_banner = %s', (id_banner,))
    banners = cur.fetchone() 
    return render_template('editar_banner.html', banners=banners)

