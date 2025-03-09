#Librerías generales

import os
from flask import Flask
from flask import render_template,request,redirect, flash, make_response, url_for
from flaskext.mysql import MySQL

#Librerías para la generación de PDF

import jinja2
import pdfkit
import json
from weasyprint import HTML

#Librería para enviar solicitudes al servidor
from flask import  jsonify

#Librería para servidor de producción
from waitress import serve

#Librería para el manejo de sesiones activas de los usuarios
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

from datetime import datetime


#Código general de Flask

app = Flask(__name__,static_folder='static')
app.secret_key="Caines"

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB']='caines'
mysql.init_app(app)


#Codigo para gestionar el login con Flask_Login

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


#Clase Usuario para el manejo de sesiones activas

class User(UserMixin):
    def __init__(self, id, cedula, nombre, apellido, rol):
        self.id = id
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.rol = rol

    @staticmethod
    def get(id):
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT * FROM usuarios WHERE id_usuario = %s"
        cursor.execute(sql, (id,))
        user_data = cursor.fetchone()
        if user_data:
            return User(id=user_data[0], rol=user_data[1], cedula=user_data[2], nombre=user_data[3], apellido=user_data[4])
        return None

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


#Clase Citas para el manejo de datos de las Citas
class Citas():
    def __init__(self, id, id_representante, id_nino, fecha, estado, nueva_fecha, hora):
        self.id = id
        self.representante = id_representante
        self.id_nino = id_nino
        self.fecha = fecha
        self.estado = estado
        self.nueva_fecha = nueva_fecha
        self.hora = hora

    #Obtener los datos de la cita
    def get(id):
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT * FROM citas WHERE id_cita = %s"
        cursor.execute(sql, (id,))
        cita = cursor.fetchone()
        if cita:
            return cita(id=cita[0], id_representante=cita[1], id_nino=cita[2], fecha=cita[3], estado=cita[4], nueva_fecha=cita[5], hora=cita[6])
        return None


#Clase Niño para el manejo de datos de los niños
class Nino():
    def __init__(self, id, representante, nombre, apellido, edad, fecha_nac):
        self.id = id
        self.reprsentante = representante
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.fecha_nac = fecha_nac

    #Obtener los datos del niño
    def get(id):
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT * FROM ninos WHERE id_nino = %s"
        cursor.execute(sql, (id,))
        nino = cursor.fetchone()
        if nino:
            return Nino(id=nino[0], representante=nino[1], nombre=nino[2], apellido=nino[3],edad=nino[4], fecha_nac=nino[5])
        return None

#Clase Representante para el manejo de datos
class Representante():
    def __init__(self, id, cedula, nombre, apellido, direccion, correo, telefono):
        self.id = id
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
        self.correo = correo
        self.telefono = telefono

        # Obtener los hijos del representante
        # self.hijos = self.get_hijos()



    #Obtener los datos del representante
    def get(id):
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = """
            SELECT u.*, t.telefono 
            FROM usuarios u 
            LEFT JOIN telefonos_usuario t ON u.id_usuario = t.id_usuario 
            WHERE u.id_usuario = %s
        """
        cursor.execute(sql, (id,))
        representante = cursor.fetchone()
        print(representante)
        if representante:
            return Representante(id=representante[0], cedula=representante[2], nombre=representante[3], apellido=representante[4], direccion=representante[5], correo=representante[6], telefono=representante[8])
        return None


#Clase Especialista para el manejo de datos de los mismos
class Especialista():
    def __init__(self, id, cedula, nombre, apellido, direccion, correo):
        self.id = id
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
        self.correo = correo


    #Obtener los datos del especialista
    def get(id):
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT * FROM usuarios WHERE id_usuario = %s"
        cursor.execute(sql, (id,))
        especialista = cursor.fetchone()
        if especialista:
            return Especialista(id=especialista[0],
                                cedula=especialista[2],
                                nombre=especialista[3],
                                apellido=especialista[4],
                                direccion=especialista[5],
                                correo=especialista[6])
        return None
    

### Vistas Generales ###
@app.route('/')
def index():
    return render_template('general/principal.html')


@app.route('/login')
def login():
    return render_template('general/login.html')

@app.route('/registro')
def registro():
    return render_template('general/registro.html')

@app.route('/recuperar_contrasena')
def recuperar_contrasena():
    return render_template('/general/contrasena.html')


@app.route('/menu')
@login_required
def menu():
    return render_template('/caines/menu.html')

### Vistas de la Gestión de Niños ###
@app.route('/ninos') 
@login_required
def ninos(): 
    conn = mysql.connect() 
    cursor = conn.cursor()

    #Condición para que muestre solamente los niños asociados al representante
    if current_user.rol == 'representante':
        cursor.execute("SELECT * FROM ninos WHERE id_usuario = %s", (current_user.id,))
    
        ninos = cursor.fetchall()
    
        conn.commit() 
    
        return render_template('ninos/ninos.html', ninos=ninos)
    
    elif current_user.rol == 'especialista': 
        cursor.execute("""
            SELECT DISTINCT n.*
            FROM ninos n
            INNER JOIN aux_horarios h ON n.id_nino = h.id_nino
            WHERE h.id_especialista = %s
        """, (current_user.id,))
    
        ninos = cursor.fetchall()  
        print(ninos)
    
        conn.commit()  
    
        return render_template('ninos/ninos.html', ninos=ninos)
    

    #Sino, que muestre todos los niños totales registrados.
    else: 
        cursor.execute("SELECT * FROM ninos")
    
        ninos = cursor.fetchall() 
    
        conn.commit() 
    
        return render_template('ninos/ninos.html', ninos=ninos)

#Registrar Niño
@app.route('/create_nino')
def create_nino():

    conn = mysql.connect() 
    cursor = conn.cursor() 

    cursor.execute("SELECT id_usuario, cedula, nombre, apellido FROM usuarios WHERE tipo_usuario = 'representante'")

    representantes = cursor.fetchall()

    return render_template('ninos/create_nino.html', clientes = representantes)

# Funciones para rellenar los inputs
# en la plantilla create_ffactura.html

#Codigo para llenar los inputs del representante en create_factura

@app.route('/verificar_cedula', methods=['POST'])
def verificar_cedula():

    cedula = request.form['txtCedula']


    # Hacemos la conexión a la base de datos
    conn = mysql.connect() 
    cursor = conn.cursor() 

    # Ejecutamos la consulta SQL
    cursor.execute("SELECT nombre, apellido, direccion, id_usuario FROM usuarios WHERE cedula = %s", (cedula,))

    resultado = cursor.fetchone()

    # Cerramos la conexión a la base de datos
    conn.close()

    if resultado:
        nombre, apellido, direccion, id_usuario = resultado
    else:
        nombre, apellido, direccion, id_usuario = "", "", "", ""

    response = {
        'nombre': nombre,
        'apellido': apellido,
        'direccion': direccion,
        'id': id_usuario
    }

    return jsonify(response)

#Funcion para editar niño
@app.route('/edit_nino/<int:id>') 
def edit_nino(id): 
 
    conn = mysql.connect() 
    cursor = conn.cursor()
 
    # Consulta para obtener los datos del niño
    cursor.execute("SELECT * FROM ninos WHERE id_nino = %s ",(id)) 
    ninos = cursor.fetchall()
 
    conn.commit()

    return render_template("ninos/edit_nino.html", ninos=ninos)

#Funcion para eliminar niño
@app.route('/destroy_nino/<int:id>')
def destroy_nino(id):
    conn = mysql.connect()
    cursor = conn.cursor()


    # Delete the user from the database
    cursor.execute("DELETE FROM ninos WHERE id_nino = %s", (id,))

    conn.commit()

    return redirect('/ninos')

@app.route('/eliminar_ninos', methods=['POST', 'DELETE'])
@login_required
def eliminar_ninos():
    ids = request.json.get('ids', [])
    
    if not ids:
        return jsonify(success=False, message='No IDs provided'), 400

    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        # Eliminar los clientes y sus facturas de las tablas originales
        cursor.execute("DELETE FROM ninos WHERE id_nino IN %s", (tuple(ids),))

        conn.commit()
        return jsonify(success=True)
    
    except Exception as e:
        conn.rollback()
        return jsonify(success=False, message=str(e)), 500
    
    finally:
        cursor.close()
        conn.close()


@app.route('/eliminar_pagos', methods=['POST', 'DELETE'])
@login_required
def eliminar_pagos():
    ids = request.json.get('ids', [])
    
    if not ids:
        return jsonify(success=False, message='No IDs provided'), 400

    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM facturas WHERE id_factura IN %s", (tuple(ids),))

        conn.commit()
        return jsonify(success=True)
    
    except Exception as e:
        conn.rollback()
        return jsonify(success=False, message=str(e)), 500
    
    finally:
        cursor.close()
        conn.close()


@app.route('/eliminar_usuarios', methods=['POST', 'DELETE'])
@login_required
def eliminar_usuarios():
    ids = request.json.get('ids', [])
    
    if not ids:
        return jsonify(success=False, message='No IDs provided'), 400

    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        # Eliminar los clientes y sus facturas de las tablas originales
        cursor.execute("DELETE FROM usuarios WHERE id_usuario IN %s", (tuple(ids),))

        conn.commit()
        return jsonify(success=True)
    
    except Exception as e:
        conn.rollback()
        return jsonify(success=False, message=str(e)), 500
    
    finally:
        cursor.close()
        conn.close()

#Codigo para rellenar el input Precio de create_factura.html

@app.route('/verificar_terapia', methods=['POST'])
def verificar_terapia():

    terapia = request.form['txtTerapia']


    # Hacemos la conexión a la base de datos
    conn = mysql.connect() 
    cursor = conn.cursor() 

    # Ejecutamos la consulta SQL
    cursor.execute("SELECT precio FROM terapias WHERE nombre = %s", (terapia,))

    resultado = cursor.fetchone()

    # Cerramos la conexión a la base de datos
    conn.close()

    if resultado:
        precio = resultado
    else:
        precio = "", "", ""

    response = {
        'precio': precio,
    }

    return jsonify(response)












@app.route('/entrar', methods=['POST'])
def entrar():
    cedula = request.form['txtCedula']
    contrasena = request.form['txtContrasena']

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT id_usuario FROM usuarios WHERE cedula=%s AND clave=%s", (cedula, contrasena))
    user_id = cursor.fetchone()

    if user_id:
        user = User.get(user_id[0])
        login_user(user)  # Funcion de Flask_Login para Iniciar sesión del usuario actual
        return render_template('general/principal.html')
    else:
        flash('Cédula o contraseña incorrecta.')
        return render_template('general/login.html')





#Funciones para acceder a las rutas de la página

@app.route('/cerrar_sesion', methods=['GET'])
@login_required
def cerrar_sesion():

    logout_user()  # Función de Flask-Login para cerrar sesión
    flash('¡Has cerrado sesión exitosamente!')  # Mostramos un mensaje personalizado

    return redirect('/login')  # Redirigir al inicio de sesión

@app.route('/ag_citas/<int:id>')
def agendar_citas(id):

    representante = Representante.get(id)

    conn = mysql.connect()
    cursor = conn.cursor()

    # Obtener las citas de la base de datos
    cursor.execute("SELECT * FROM citas WHERE id_representante = %s", (id,))
    cita = cursor.fetchone()


    if cita is not None:
        print("Cita es: ", cita)

    # La cita ya existe, mostrar mensaje de flash y redirigir a la página anterior

        return render_template('/caines/ag_citas.html', representante = representante, cita = cita)
    
    return render_template('/caines/ag_citas.html', representante = representante)

@app.route('/eliminar_citas', methods=['POST', 'DELETE'])
@login_required
def eliminar_citas():
    ids = request.json.get('ids', [])
    
    if not ids:
        return jsonify(success=False, message='No IDs provided'), 400

    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        # Eliminar los clientes y sus facturas de las tablas originales
        cursor.execute("DELETE FROM citas WHERE id_cita IN %s", (tuple(ids),))

        conn.commit()
        return jsonify(success=True)
    
    except Exception as e:
        conn.rollback()
        return jsonify(success=False, message=str(e)), 500
    
    finally:
        cursor.close()
        conn.close()


#Metodo para eliminar cita (usuario representante)
@app.route('/eliminar_cita/<int:id>')
def eliminar_cita(id):

    conn = mysql.connect()
    cursor = conn.cursor()
 


    # Consultar las terapias existentes en el día y hora para eliminarlos
    sql = "DELETE FROM citas WHERE id_cita = %s"


    cursor.execute("DELETE FROM citas WHERE id_cita = %s",(id))


    conn.commit()

    conn.close()

    if current_user.rol == 'representante':

        flash('¡Su cita fue anulada exitosamente!', 'error')

        return redirect('/menu')
    
    #Si es el director o cualquier otro rol entonces vuelve a la pagina de Citas
    return redirect('/citas')


@app.route('/gestfacturas')
@login_required
def gestfacturas():

    conn = mysql.connect() 
    cursor = conn.cursor()

    #Condición para que muestre solamente las facturas asociadas al representante
    if current_user.rol == 'representante':
        cursor.execute("SELECT * FROM facturas WHERE id_usuario = %s", (current_user.id,))
    
        facturas = cursor.fetchall() 
    
        conn.commit() 
    
        return render_template('caines/gestfacturas.html', facturas=facturas)
    

    #Sino, que muestre todas las facturas registradas.
    else: 
        cursor.execute('''
                SELECT
                    facturas.id_factura,
                    usuarios.nombre,
                    facturas.fecha,                    
                    usuarios.apellido,
                    facturas.total
                FROM
                    facturas
                INNER JOIN
                    usuarios ON facturas.id_usuario = usuarios.id_usuario
                WHERE
                    usuarios.tipo_usuario = "representante"''')
    
        facturas = cursor.fetchall() 
    
        conn.commit() 
    
        return render_template('caines/gestfacturas.html', facturas=facturas)




#Pasar los datos de los horarios del niño seleccionado a horario.html

@app.route('/horario/<int:id>')
def horario(id):

    conn = mysql.connect()
    cursor = conn.cursor()

    nino = Nino.get(id)

    # Obtener terapias desde la base de datos
    cursor.execute("SELECT id_terapia, nombre FROM terapias")
    terapias = cursor.fetchall()

    # Obtener los especialistas desde la base de datos
    cursor.execute("SELECT id_usuario, nombre FROM usuarios WHERE tipo_usuario = 'especialista' ")
    especialistas = cursor.fetchall()


    return render_template('/caines/horario.html', especialistas = especialistas,  terapias = terapias, nino = nino)

@app.route('/datos_horario/<int:id>')
def datos_horario(id):

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT aux_horarios.*, usuarios.nombre AS nombre_especialista, terapias.nombre AS nombre_terapia
        FROM aux_horarios
        JOIN usuarios ON aux_horarios.id_especialista = usuarios.id_usuario
        JOIN terapias ON aux_horarios.id_terapia = terapias.id_terapia
        WHERE aux_horarios.id_nino = %s
    """, (id,))

    ninos = cursor.fetchall()
    # print("Niños es: ", ninos)

    # cursor.execute("""
    # SELECT * FROM aux_horarios WHERE id_especialista = %s
    # """, (id,))

    # ninos = cursor.fetchall()

    conn.close()

    # Convertir los datos a formato JSON y devolverlos
    return jsonify(ninos)



@app.route('/horario_pdf/<int:id>', methods=['GET'])
def horario_pdf(id):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT
            aux_horarios.*,
            usuarios.nombre AS nombre_especialista,
            terapias.nombre AS nombre_terapia
        FROM
            aux_horarios
        JOIN
            usuarios ON aux_horarios.id_especialista = usuarios.id_usuario
        JOIN
            terapias ON aux_horarios.id_terapia = terapias.id_terapia
        WHERE
            aux_horarios.id_nino = %s
    ''', (id,))

    rows = cursor.fetchall()
    print("Rows es: ", rows)

    conn.close()

    # Crear una estructura para el horario escolar
    horario = {}
    for hora in range(7, 17):
        for minuto in [0, 30]:
            key = f"{hora:02}:{minuto:02}"
            horario[key] = {"Lunes": "", "Martes": "", "Miércoles": "", "Jueves": "", "Viernes": ""}

    # Poner los datos en el horario
    for row in rows:
        dia = row[2].capitalize() # Convertir a título por si acaso
        hora_inicio = row[4][:5]
        duracion = int(row[6])
        especialidad_terapia = f"{row[9]}<br>({row[8]})"
        if hora_inicio in horario:
            horario[hora_inicio][dia] = {
                "especialidad_terapia": especialidad_terapia,
                "rowspan": 3 if duracion == 60 else 2
            }

    # Renderizar el template con los datos agrupados y el total
    rendered = render_template('ninos/reporte_horario.html', horario=horario)

    # Generar el PDF con WeasyPrint
    html = HTML(string=rendered)
    pdf = html.write_pdf()

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=reporte_horario.pdf'

    return response





#Pasar los datos de los horarios del especialista seleccionado a horario_esp.html

@app.route('/horario_esp/<int:id>')
def horario_esp(id):

    conn = mysql.connect()
    cursor = conn.cursor()

    sql = '''SELECT aux_horarios.id_nino, ninos.nombre, ninos.apellido
                        FROM aux_horarios
                        JOIN ninos ON aux_horarios.id_nino = ninos.id_nino
                        WHERE aux_horarios.id_especialista = %s;
                    '''
    
    cursor.execute(sql,(id))
    ninos = cursor.fetchall()
    print(ninos)
    especialista = Especialista.get(id)

    # Obtener terapias desde la base de datos
    cursor.execute("SELECT id_terapia, nombre FROM terapias")
    terapias = cursor.fetchall()

    # Obtener los niños desde la base de datos
    cursor.execute("SELECT id_nino, nombre, apellido, escolaridad FROM ninos ORDER BY nombre ASC")
    ninos = cursor.fetchall()
    print(ninos)


    return render_template('/caines/horario_esp.html', ninos = ninos, terapias = terapias, especialista = especialista)

@app.route('/datos_horario_esp/<int:id>')
def datos_horario_esp(id):

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT aux_horarios.*, 
            usuarios.nombre AS nombre_especialista, 
            terapias.nombre AS nombre_terapia, 
            ninos.nombre AS nombre_nino
        FROM aux_horarios 
        JOIN usuarios ON aux_horarios.id_especialista = usuarios.id_usuario 
        JOIN terapias ON aux_horarios.id_terapia = terapias.id_terapia 
        JOIN ninos ON aux_horarios.id_nino = ninos.id_nino
        WHERE aux_horarios.id_especialista = %s
    """, (id,))

    ninos = cursor.fetchall()

    conn.close()

    # Convertir los datos a formato JSON y devolverlos
    return jsonify(ninos)











@app.route('/agregar_cita', methods=['POST'])  
def agregar_cita():

    _fecha = request.form['txtFecha']
    _fechacita = request.form['txtFechaCita']
    _hora = request.form['txtHora']
    _id = request.form['txtID']

    conn = mysql.connect() 
    cursor = conn.cursor() 

    # Consultar si la cita ya existe en la base de datos

    sql = "SELECT * FROM citas WHERE id_representante = %s"
    cursor.execute(sql, (_id,))
    result = cursor.fetchone()
    if result is not None:

        # La cita ya existe, mostrar mensaje de flash y redirigir a la página anterior
        flash('Ya posee una cita en proceso', 'error')
        return redirect(request.referrer)

    # La cita no existe, insertar el nuevo registro (por ahora, sin niño)
    sql = "INSERT INTO citas (id_cita, id_representante, fecha, estado, fecha_cita, hora) VALUES (NULL, %s,  %s, 'pendiente', %s, %s);" 

    datos=(_id,_fecha, _fechacita, _hora) 

    cursor.execute(sql,datos) 
    conn.commit() 

    flash('¡Su cita fue agendada exitosamente!', 'error')

    return redirect('/menu')


@app.route('/agregar_terapia', methods=['POST'])
def agregar_terapia():
    _id_nino = request.form['txtId']
    _dia = request.form['txtDia']
    _hora = request.form['txtHora']
    _especialista = request.form['txtEspecialista']
    _terapia = request.form['txtTerapia']
    _duracion = request.form['txtDuracion']

    # CODIGO PARA CALCULAR LA HORA FIN:

    # Dividir la cadena de la hora en horas y minutos
    horas, minutos = _hora.split(':')

    # Convertir horas y minutos en enteros
    horas = int(horas)
    minutos = int(minutos)

    # Sumar 30 minutos
    minutos += 30

    # Verificar si se ha excedido el límite de 60 minutos
    if minutos >= 60:
        minutos -= 60
        horas += 1

    # Verificar si se ha excedido el límite de 12 horas
    if horas >= 13:
        horas -= 12

    # Ajustar el formato de horas y minutos (agregar un cero si es necesario)
    horas = str(horas)
    minutos = str(minutos).zfill(2)

    # Crear la hora modificada en formato de cadena 'HH:MM'
    _hora_fin = f"{horas}:{minutos}"

    # print("La hora de fin es: ", _hora_fin)

    #FIN DEL CODIGO PARA CALCULAR LA HORA FIN


    conn = mysql.connect()
    cursor = conn.cursor()



    if _duracion == '60':

        # Consultar las terapias existentes en el día y hora modificados
        sql = "SELECT COUNT(*) FROM aux_horarios WHERE dia = %s AND hora = %s"
        datos = (_dia, _hora_fin)
        cursor.execute(sql, datos)
        cantidad_terapias = cursor.fetchone()[0]

        if cantidad_terapias > 0:
            flash("No se puede insertar la terapia en ese horario debido a una colisión.")
            return redirect('/horario/' + _id_nino)
        
    print("Especialista: ", _especialista, "\nDia: ", _dia, "\nHora: ", _hora, "Hora Fin: ", _hora_fin)

    # Verificar si el especialista está disponible a esa hora
    sql_especialista_disponible = """
        SELECT COUNT(*) 
        FROM aux_horarios 
        WHERE id_especialista = %s 
        AND dia = %s 
        AND hora = %s AND hora_fin = %s
    """

    datos_especialista = (_especialista, _dia, _hora, _hora_fin)
    cursor.execute(sql_especialista_disponible, datos_especialista)

    especialista_ocupado = cursor.fetchone()[0]

    if especialista_ocupado > 0:
        flash("El especialista no está disponible en la hora seleccionada.")
        return redirect('/horario/' + _id_nino)
            
    
    #Introducir los datos

    sql = "INSERT INTO aux_horarios (id_nino, dia, id_especialista, hora, hora_fin, id_terapia, duracion) VALUES (%s, %s, %s, %s, %s, %s, %s);"
    datos = (_id_nino, _dia, _especialista, _hora, _hora_fin, _terapia, _duracion)
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/horario/' + _id_nino)


@app.route('/eliminar_terapia', methods=['POST'])
def eliminar_terapia():
    _id_nino = request.form['txtId_ocupado']
    _dia = request.form['txtDia_ocupado']
    _hora = request.form['txtHora_ocupado']

    conn = mysql.connect()
    cursor = conn.cursor()

    # Consultar las terapias existentes en el día y hora para eliminarlos
    sql = "DELETE FROM aux_horarios WHERE id_nino = %s AND dia = %s AND hora = %s"
    datos = (_id_nino, _dia, _hora)

    cursor.execute(sql, datos)
    conn.commit()
    conn.close() 

    return redirect('/horario/' + _id_nino)

@app.route('/eliminar_terapia_esp', methods=['POST'])
def eliminar_terapia_esp():
    _id_nino = request.form['txtId_ocupado']
    _dia = request.form['txtDia_ocupado']
    _hora = request.form['txtHora_ocupado']

    conn = mysql.connect()
    cursor = conn.cursor()

    # Consultar las terapias existentes en el día y hora para eliminarlos
    sql = "DELETE FROM aux_horarios WHERE id_nino = %s AND dia = %s AND hora = %s"
    datos = (_id_nino, _dia, _hora)

    cursor.execute(sql, datos)
    conn.commit()
    conn.close() 

    return redirect('/horario/' + _id_nino)


@app.route('/create_factura')
def create_factura():

    conn = mysql.connect()
    cursor = conn.cursor()

    # Consultar las terapias existentes en el día y hora para eliminarlos
    sql = "SELECT id_usuario, cedula, nombre, apellido, direccion FROM usuarios WHERE tipo_usuario = 'representante'"

    cursor.execute(sql)
    representantes = cursor.fetchall()

    conn.commit()
    conn.close()    

    return render_template('/caines/create_factura.html', clientes = representantes)


@app.route('/citas')
def citas():

    conn = mysql.connect() 
    cursor = conn.cursor() 
    cursor.execute("""
                   
        SELECT citas.*, usuarios.nombre, usuarios.apellido, usuarios.cedula, telefonos_usuario.telefono 
        FROM citas 
        INNER JOIN usuarios ON citas.id_representante = usuarios.id_usuario 
        INNER JOIN telefonos_usuario ON usuarios.id_usuario = telefonos_usuario.id_usuario;

                   
                   """)
 
    citas = cursor.fetchall()
    print(citas)
 
    conn.commit() 

    return render_template('caines/citas.html', citas = citas)

# @app.route('/citas')
# def citas():

#     citas = Citas.get(id)

#     conn = mysql.connect() 
#     cursor = conn.cursor() 

#     # cursor.execute("""
                   
#     #     SELECT citas.*, usuarios.nombre, usuarios.apellido, usuarios.cedula, telefonos_usuario.telefono 
#     #     FROM citas 
#     #     INNER JOIN usuarios ON citas.id_representante = usuarios.id_usuario 
#     #     INNER JOIN telefonos_usuario ON usuarios.id_usuario = telefonos_usuario.id_usuario;
                   
#     #                """)
 
#     # citas = cursor.fetchall()
#     print(citas)
 
#     conn.commit() 

#     return render_template('caines/citas.html', citas = citas)







#Ir a la pagina principal de representantes

@app.route('/representantes') 
def representantes(): 
    conn = mysql.connect() 
    cursor = conn.cursor() 
    cursor.execute("SELECT r.*, t.telefono FROM usuarios r LEFT JOIN telefonos_usuario t ON r.id_usuario = t.id_usuario WHERE r.tipo_usuario = 'representante'")
 
    usuarios = cursor.fetchall() 
 
    conn.commit() 
 
    return render_template('caines/representantes.html', usuarios=usuarios)


#Ir a la página principal de especialistas

@app.route('/especialistas') 
def especialistas(): 
    conn = mysql.connect() 
    cursor = conn.cursor() 
    cursor.execute("SELECT r.*, t.telefono FROM usuarios r LEFT JOIN telefonos_usuario t ON r.id_usuario = t.id_usuario WHERE r.tipo_usuario = 'especialista'")
 
    usuarios = cursor.fetchall() 
 
    conn.commit() 
 
    return render_template('caines/especialistas.html', usuarios=usuarios)

#Ir a la página principal de administradores

@app.route('/administradores') 
def administradores(): 
    conn = mysql.connect() 
    cursor = conn.cursor() 
    cursor.execute("SELECT r.*, t.telefono FROM usuarios r LEFT JOIN telefonos_usuario t ON r.id_usuario = t.id_usuario WHERE r.tipo_usuario = 'administrador'")
 
    usuarios = cursor.fetchall() 
 
    conn.commit() 
 
    return render_template('caines/administradores.html', usuarios=usuarios)

#Ir a la página principal de secretaria

@app.route('/secretarias') 
def secretarias(): 
    conn = mysql.connect() 
    cursor = conn.cursor() 
    cursor.execute("SELECT r.*, t.telefono FROM usuarios r LEFT JOIN telefonos_usuario t ON r.id_usuario = t.id_usuario WHERE r.tipo_usuario = 'secretaria'")
 
    usuarios = cursor.fetchall() 
 
    conn.commit() 
 
    return render_template('caines/secretarias.html', usuarios=usuarios)

#Ir a la página principal de directores

@app.route('/directores') 
def directores(): 
    conn = mysql.connect() 
    cursor = conn.cursor() 
    cursor.execute("SELECT r.*, t.telefono FROM usuarios r LEFT JOIN telefonos_usuario t ON r.id_usuario = t.id_usuario WHERE r.tipo_usuario = 'director'")
 
    usuarios = cursor.fetchall() 
 
    conn.commit() 
 
    return render_template('caines/directores.html', usuarios=usuarios)

#Comienzo del código para manipular los Usuarios

#Funcion para ahorrar código y redirigir al usuario correcto

def redireccionamiento(_tipo_usuario):
    # Seleccionar la plantilla HTML apropiada segun el tipo de usuario
    if _tipo_usuario == 'especialista':
        template = '/especialistas'
    elif _tipo_usuario == 'administrador':
        template = '/administradores'
    elif _tipo_usuario == 'representante':
        template = '/representantes'
    elif _tipo_usuario == 'secretaria':
        template = '/secretarias'
    elif _tipo_usuario == 'director':
        template = '/directores'
    
    else:
        # Mensaje de error que no creo que ocurra
        return 'Invalid user type'

    return template

#Ir a la ventana "Registrar Usuario"
@app.route('/create_user')
def create_user():
    return render_template('caines/create_user.html')

#Función para insertar un usuario en la base de datos

@app.route('/store_user/<from_page>', methods=['POST'])  
def store_user(from_page):  

    _cedula = request.form['txtCedula'] 
    _nombre = request.form['txtNombre'] 
    _apellido = request.form['txtApellido'] 
    _direccion = request.form['txtDireccion'] 
    _correo = request.form['txtCorreo'] 
    _telefono = request.form['txtTelefono'] 
    _cod_numero = request.form['cod_numero'] 
    _tipo_usuario = request.form['tipo_usuario'] 
    _clave = request.form['txtPassword'] 

    conn = mysql.connect() 
    cursor = conn.cursor() 

    # Consultar si la cedula ya existe en la base de datos

    sql = "SELECT id_usuario FROM usuarios WHERE cedula = %s"
    cursor.execute(sql, (_cedula,))
    result = cursor.fetchone()
    if result is not None:
        # La cedula ya existe, mostrar mensaje de flash y redirigir a la página anterior
        flash('La cédula ya está registrada', 'error')

        return redirect(request.referrer)

    # La cedula no existe, insertar el nuevo registro
    sql = "INSERT INTO usuarios (id_usuario, tipo_usuario, cedula, nombre, apellido, direccion, correo, clave) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s);" 

    datos=(_tipo_usuario, _cedula, _nombre, _apellido, _direccion, _correo, _clave) 

    cursor.execute(sql,datos) 
    conn.commit() 

    # Obtener el ID del usuario insertado 
    id_usuario = cursor.lastrowid 

    # Insertar el número de teléfono en la tabla "telefonos_usuario" 
    telefono_completo = "{}{}".format(_cod_numero, _telefono) 
    sql = "INSERT INTO telefonos_usuario (id_usuario, telefono) VALUES (%s, %s);" 
    datos = (id_usuario, telefono_completo) 
    cursor.execute(sql, datos) 
    conn.commit() 

    if from_page == 'registro':
        flash('¡Registro exitoso!') 
        return redirect('/login') 
    elif from_page == 'create_user':
        flash('¡Usuario registrado exitosamente!') 
        return redirect(redireccionamiento(_tipo_usuario)) 
    
    flash('¡Usuario registrado exitosamente!')
    return redirect(redireccionamiento(_tipo_usuario))



#Funcion para buscar un usuario en la base de datos a partir de los 
# caracteres ingresados en el input Buscar

@app.route('/buscar_usuario', methods=['POST'])
def buscar_usuario():
    _busqueda = request.form['buscar']
    _tipo_usuario = request.form['tipo_usuario']  # Saber que tipo de usuario es
    _tipo_usuario = request.form['tipo_usuario']  # Saber que tipo de usuario es

    sql = "SELECT r.*, t.telefono FROM usuarios r LEFT JOIN telefonos_usuario t ON r.id_usuario = t.id_usuario WHERE r.tipo_usuario = %s AND r.nombre LIKE %s ORDER BY r.id_usuario DESC;"

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, (_tipo_usuario, _busqueda + "%"))  # Pass _tipo_usuario as a parameter

    usuarios = cursor.fetchall()

    conn.commit()

    #   En esta parte se concatena la ruta con la funcion redireccionamiento para poder reutilizar el código
    #tanto en la función buscar_user como en destroy_user y las demás que necesiten hacer
    #un 'redirect' al final y no un 'render_template'
    return render_template('caines' + redireccionamiento(_tipo_usuario) + '.html', usuarios=usuarios)



# Codigo para Eliminar Usuario

@app.route('/destroy_user/<int:id>')
def destroy_user(id):
    conn = mysql.connect()
    cursor = conn.cursor()

    # Get the user's tipo_usuario from the database
    cursor.execute("SELECT tipo_usuario FROM usuarios WHERE id_usuario = %s", (id,))
    _tipo_usuario = cursor.fetchone()[0]  # Access the first element of the tuple

    # Delete the user from the database
    cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id,))

    conn.commit()


    return redirect(redireccionamiento(_tipo_usuario))

# Codigo para Editar Usuario

@app.route('/edit_user/<int:id>')  
def edit_user(id):  
    conn = mysql.connect()  
    cursor = conn.cursor() 
  
    # Consulta para obtener los datos del usuario y sus teléfonos 
    cursor.execute("SELECT r.*, t.telefono FROM usuarios r LEFT JOIN telefonos_usuario t ON r.id_usuario = t.id_usuario WHERE r.id_usuario=%s",(id))  
    usuarios = cursor.fetchall() 
  
    conn.commit() 

    return render_template("caines/edit_user.html", usuarios=usuarios)

@app.route('/edit_password/<int:id>')  
def edit_password(id):  
    conn = mysql.connect()  
    cursor = conn.cursor() 
  
    # Consulta para obtener los datos del usuario y sus teléfonos 
    cursor.execute("SELECT r.*, t.telefono FROM usuarios r LEFT JOIN telefonos_usuario t ON r.id_usuario = t.id_usuario WHERE r.id_usuario=%s",(id))  
    usuarios = cursor.fetchall() 
  
    conn.commit() 

    return render_template("caines/edit_password.html", usuarios=usuarios)



#Funcion para guardar los cambios en el usuario editado

@app.route('/update_user', methods=['POST'])
def update_user():
    _cedula = request.form['txtCedula']
    _nombre = request.form['txtNombre']
    _apellido = request.form['txtApellido']
    _direccion = request.form['txtDireccion']
    _correo = request.form['txtCorreo']
    usuario_id = request.form['txtID']
    # _password = request.form['txtPassword']


    # Update los datos del usuario en la tabla 'usuarios'
    sql_usuario = "UPDATE usuarios SET cedula=%s, nombre=%s, apellido=%s, direccion=%s, correo=%s WHERE id_usuario=%s"
    datos_usuario = (_cedula, _nombre, _apellido, _direccion, _correo, usuario_id)
  
    # Actualizar los teléfonos en la tabla 'telefonos_usuario'
    telefonos = []
    for key, value in request.form.items():
        if key.startswith('txtTelefono'):
            codigo_area = request.form['cod_numero_' + key[12:]]
            telefono_completo = codigo_area + value
            telefonos.append((telefono_completo, usuario_id))
  
    conn = mysql.connect()
    cursor = conn.cursor()

    # Get the user's tipo_usuario from the database
    cursor.execute("SELECT tipo_usuario FROM usuarios WHERE id_usuario = %s", (usuario_id,))
    _tipo_usuario = cursor.fetchone()[0]
  
    try:
        cursor.execute(sql_usuario, datos_usuario)
  
        # Actualizar los teléfonos existentes del usuario
        sql_update_telefonos = "UPDATE telefonos_usuario SET telefono=%s WHERE id_usuario=%s"
        cursor.executemany(sql_update_telefonos, telefonos)
  
        conn.commit()
        flash('¡Usuario actualizado exitosamente!')


        return redirect('/menu')
  
    except Exception as e:
        conn.rollback()
        return str(e)
  
    finally:
        cursor.close()
        conn.close()



@app.route('/update_password', methods=['POST'])
def update_password():
    conn = mysql.connect()
    cursor = conn.cursor()

    usuario_id = request.form['txtID']
    old_password = request.form['txtOldPassword']
    new_password = request.form['txtPassword']
    confirm_password = request.form['txtPassword2']

    # Consulta para obtener la contraseña actual del usuario
    cursor.execute("SELECT clave FROM usuarios WHERE id_usuario=%s", (usuario_id,))
    user = cursor.fetchone()

    if user and old_password == user[0]:
        if new_password == confirm_password:
            # Actualizar la contraseña en la base de datos
            sql_usuario = "UPDATE usuarios SET clave=%s WHERE id_usuario=%s"
            datos_usuario = (new_password, usuario_id)
            cursor.execute(sql_usuario, datos_usuario)
            conn.commit()

            flash('¡Contraseña modificada exitosamente!', 'success')
            return redirect('/menu')
        else:
            flash('Las contraseñas nuevas no coinciden.', 'error')
    else:
        flash('La contraseña actual es incorrecta.', 'error')
    
    # Si hay un error, volver a la página de cambio de contraseña
    return redirect(url_for('edit_password', id=usuario_id))

  

#Fin del código para manipular los usuarios




# #Comienzo del código para la gestión de los Niños

#Ir a la página principal de ninos


    
#Ir a la plantilla HTML crear_nino



#Funcion para agregar niño 
@app.route('/agregar_nino', methods=['POST']) 
def agregar_nino(): 
 
    _nombre = request.form['txtNombre'] 
    _apellido = request.form['txtApellido'] 
    _fecha_nac = request.form['txtFecha_Nac'] 
    _edad = request.form['txtEdad'] 
    _escolaridad = request.form['txtEscolaridad'] 
    _lugar_nac = request.form['txtLugar_Nac'] 
    _num_hermanos = request.form['txtNum_Hermanos'] 
    _cedula = request.form['txtCedula'] 
 
    conn = mysql.connect() 
    cursor = conn.cursor() 
 
    # Consultar si la cedula ya existe en la base de datos 
 
    sql = "SELECT id_usuario FROM usuarios WHERE cedula = %s" 
    cursor.execute(sql, (_cedula,)) 
    result = cursor.fetchone() 
    if not result:

        # La cedula no existe, mostrar mensaje de flash y redirigir a la página anterior 
        flash('El representante no existe', 'error') 
        return redirect(request.referrer) 
 
    # La cedula si existe, insertar los datos en la tabla "ninos"
    _cedula = result #La cedula ahora es el ID del usuario. Esto no es lo mas optimo. Lo mas óptimo sería colocar id_usuario en la tabla niños como clave foránea de la tabla usuarios(cedula). Queda pendiente actualizarlo.
 
    sql = "INSERT INTO ninos (id_nino, id_usuario, nombre, apellido, edad, fecha_nacimiento, lugar_nacimiento, num_hermanos, escolaridad) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s);" 
 
    datos=(_cedula, _nombre, _apellido, _edad, _fecha_nac, _lugar_nac, _num_hermanos, _escolaridad) 
 
    cursor.execute(sql,datos) 
    conn.commit() 
 
    return redirect('/ninos')






#Funcion para actualizar niño después de su edición

@app.route('/update_nino', methods=['POST'])
def update_nino():

    _nombre = request.form['txtNombre']
    _apellido = request.form['txtApellido']
    _fecha_nac = request.form['txtFecha_Nac']
    _edad = request.form['txtEdad']
    _escolaridad = request.form['txtEscolaridad']
    _lugar_nac = request.form['txtLugar_Nac']
    _num_hermanos = request.form['txtNum_Hermanos']
    usuario_id = request.form['txtID']  

    sql = "UPDATE ninos SET nombre = %s, apellido = %s, edad = %s, fecha_nacimiento = %s, lugar_nacimiento = %s, num_hermanos = %s, escolaridad = %s WHERE id_nino = %s;"

    datos=(_nombre, _apellido, _edad, _fecha_nac, _lugar_nac, _num_hermanos, _escolaridad, usuario_id)   

  
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()

    return redirect('/ninos')

#Funcion para buscar niño

@app.route('/buscar_ninos', methods=['POST'])
def buscar_ninos():
    _busqueda = request.form['buscar']
 


    sql = "SELECT * FROM ninos WHERE nombre LIKE %s ORDER BY id_nino DESC;"

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, (_busqueda + "%"))  # Pass _tipo_usuario as a parameter

    ninos = cursor.fetchall()

    conn.commit()

 
    return render_template('ninos/ninos.html', ninos=ninos)

@app.route('/avances/<int:id>') 
@login_required
def avances(id): 
    
    conn = mysql.connect() 
    cursor = conn.cursor()
    

    cursor.execute(" SELECT * FROM avances WHERE id_nino = %s",(id,))
    avances = cursor.fetchall()  

    conn.commit()

    print(id)
    
    nino = Nino.get(id)

    print(nino.id)

    
    return render_template('caines/avances.html', avances=avances, nino = nino)


#Funcion para eliminar avance
@app.route('/destroy_avance/<int:id>')
def destroy_avance(id):
    conn = mysql.connect()
    cursor = conn.cursor()


    # Delete the user from the database
    cursor.execute("DELETE FROM avances WHERE id_avance = %s", (id,))

    conn.commit()


    return redirect('/ninos')

#Formulario de Edicion de avances
@app.route('/edit_avance/<int:id>')  
def edit_avance(id):  


    conn = mysql.connect()  
    cursor = conn.cursor() 
  
    # Consulta para obtener los datos de avances de un niño especifico
    cursor.execute("SELECT * FROM avances WHERE id_avance=%s",(id))  
    avance = cursor.fetchall() 
  
    conn.commit() 

    # nino = Nino.get(id)

    return render_template("caines/edit_avance.html", avance=avance)


#Funcion para actualizar avance después de su edición

@app.route('/update_avance', methods=['POST'])
def update_avance():


    _id_avance = request.form['txtID']
    _fecha_in = request.form['txtFecha_In']
    _fecha_fin = request.form['txtFecha_Fin']
    _objetivo = request.form['txtObjetivo'] 
    _resultado = request.form['txtResultado'] 
    _observacion = request.form['txtObservacion'] 
    _recomendacion = request.form['txtRecomendacion'] 

    sql = "UPDATE avances SET fecha_inicio = %s, fecha_fin = %s, objetivos = %s, resultados = %s, observaciones = %s, recomendaciones = %s WHERE id_avance = %s;"

    datos=(_fecha_in, _fecha_fin, _objetivo, _resultado, _observacion, _recomendacion, _id_avance)   

  
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()

    return redirect('/ninos')

#Funcion para registrar avance
@app.route('/registrar_avance/<int:id>') 
def registrar_avance(id): 
 
    conn = mysql.connect() 
    cursor = conn.cursor()
 
    # Consulta para obtener los datos del niño
    cursor.execute("SELECT * FROM ninos WHERE id_nino = %s ",(id)) 
    ninos = cursor.fetchall()
 
    conn.commit()

    return render_template("caines/create_avance.html", ninos=ninos)

#Funcion para agregar avance
@app.route('/agregar_avance', methods=['POST']) 
def agregar_avance(): 

    _id_especialista = current_user.id

    _id_nino = request.form['txtID']

    # _nombre = request.form['txtNombre'] 
    # _apellido = request.form['txtApellido'] 

    _fecha_in = request.form['txtFecha_In']
    _fecha_fin = request.form['txtFecha_Fin']
    _objetivo = request.form['txtObjetivo'] 
    _resultado = request.form['txtResultado'] 
    _observacion = request.form['txtObservacion'] 
    _recomendacion = request.form['txtRecomendacion'] 

 
    conn = mysql.connect() 
    cursor = conn.cursor() 
 
    sql = "INSERT INTO avances (id_avance, id_especialista, id_nino, fecha_inicio, fecha_fin, objetivos, observaciones, resultados, recomendaciones) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s);" 
 
    datos=(_id_especialista, _id_nino, _fecha_in, _fecha_fin, _objetivo, _observacion, _resultado, _recomendacion) 
 
    cursor.execute(sql,datos) 
    conn.commit() 
 
    return redirect('/ninos')


#Inicio del codigo de Facturacion

@app.route('/generar_pdf/<table_data_json>', methods=['GET'])
def generar_pdf(table_data_json):
    # Parsear los datos de la tabla
    table_data = json.loads(table_data_json)

    # Renderizar la plantilla HTML con los datos de la tabla
    rendered = render_template('factura.html', table_data=table_data)

    # Generar el PDF con WeasyPrint
    html = HTML(string=rendered)
    pdf = html.write_pdf(stylesheets=['static/css/style2.css'])

    # Crear la respuesta
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=factura.pdf'

    # Guardar la factura en la base de datos
    terapias = []
    cantidades = []
    precios = []
    subtotales = []
    total_a_pagar = table_data[0]['total_a_pagar']
    representante = table_data[0]['representante']
    id_usuario = representante['id_representante']
    cedula = representante['cedula']
    fecha = representante['fecha']

    for item in table_data:
        cantidad = item['cantidad']
        cantidades.append(cantidad)
        producto = item['producto']
        terapias.append(producto)
        precio = item['precio']
        precios.append(precio)
        subtotal = item['subtotal']
        subtotales.append(subtotal)

    conn = mysql.connect()
    cursor = conn.cursor()

    # Guardar los datos en la tabla facturas
    sql = "INSERT INTO facturas (id_factura, id_usuario, fecha, total) VALUES (NULL, %s, %s, %s);"
    datos = (id_usuario, fecha, total_a_pagar)
    cursor.execute(sql, datos)
    conn.commit()

    # Obtener el id_factura generado por el autoincrementable
    id_factura = cursor.lastrowid

    # Guardar los datos en la tabla aux_facturas
    for i in range(len(terapias)):
        sql = "INSERT INTO aux_facturas (id_factura, terapia, cantidad, precio, subtotal) VALUES (%s, %s, %s, %s, %s);"
        datos = (id_factura, terapias[i], cantidades[i], precios[i], subtotales[i])
        cursor.execute(sql, datos)
        conn.commit()

    return response



# #Funcion para la generacion de PDF
# @app.route('/generar_pdf/<table_data_json>')
# def pdf_template(table_data_json):

#     table_data = json.loads(table_data_json)
#     rendered = render_template('/factura.html',table_data=table_data)
#     pdf = pdfkit.from_string(rendered,False,css='static/css/style2.css', options={"enable-local-file-access": ""})

#     response = make_response(pdf)
#     response.headers['Content-Type'] = 'application/pdf'
#     response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

#     # #Guardar la factura en la base de datos

#     print("Table data es: ", table_data)

#     terapias = []
#     cantidades = []
#     precios = []
#     subtotales = []

#     for item in table_data:
#         cantidad = item["cantidad"]
#         cantidades.append(cantidad)
#         producto = item["producto"]
#         terapias.append(producto)
#         precio = item["precio"]
#         precios.append(precio)
#         subtotal = item["subtotal"]
#         subtotales.append(subtotal)
#         total_a_pagar = item["total_a_pagar"]

#         representante = item["representante"]
#         id_usuario = representante["id_representante"]
#         cedula = representante["cedula"]
#         fecha = representante["fecha"]


    
#     # Aquí puedes procesar los datos como necesites

#     print("cantidad es: ", cantidades[0],
#           "producto es: ", terapias[0],
#           "precio es: ", precio,
#           "subtotal es: ", subtotales[0],
#           "total_a_pagar es: ", total_a_pagar,
#           "cedula es: ", cedula,
#           "id es: ", id_usuario)


 
#     conn = mysql.connect() 
#     cursor = conn.cursor() 
 
#     #Guardar los datos en la tabla facturas

#     sql = "INSERT INTO facturas (id_factura, id_usuario, fecha, total) VALUES (NULL, %s, %s, %s);" 
 
#     datos=(id_usuario, fecha, total_a_pagar)
#     cursor.execute(sql,datos)
#     # conn.commit()

#     # Obtener el id_factura generado por el autoincrementable
#     id_factura = cursor.lastrowid

#     #Guardar los datos en la tabla aux_facturas

#     # Iterar sobre las terapias y cantidades y guardar cada registro en la tabla aux_facturas
#     for i in range(len(terapias)):
#         sql = "INSERT INTO aux_facturas (id_factura, terapia, cantidad, precio, subtotal) VALUES (%s, %s, %s, %s, %s);"
#         datos = (id_factura, terapias[i], cantidades[i], precios[i] ,subtotales[i])
#         cursor.execute(sql, datos)
#         conn.commit()

#     return response

#Funcion para eliminar factura
@app.route('/destroy_factura/<int:id>')
def destroy_factura(id):
    conn = mysql.connect()
    cursor = conn.cursor()


    # Delete the user from the database
    cursor.execute("DELETE FROM facturas WHERE id_factura = %s", (id,))

    conn.commit()


    return redirect('/gestfacturas')

@app.route('/ver_factura/<int:id_factura>')
def ver_factura(id_factura):
    conn = mysql.connect()
    cursor = conn.cursor()

    # Obtener los datos de la factura desde la base de datos
    sql = "SELECT * FROM facturas WHERE id_factura = %s"
    cursor.execute(sql, (id_factura,))
    factura = cursor.fetchone()

    # Obtener los detalles de la factura desde la tabla aux_facturas
    sql = "SELECT * FROM aux_facturas WHERE id_factura = %s"
    cursor.execute(sql, (id_factura,))
    detalles_factura = cursor.fetchall()

    # Crear una lista con los datos de cada terapia
    terapias = []
    cantidades = []
    precios = []
    subtotales = []
    for detalle in detalles_factura:
        terapias.append(detalle[1])
        cantidades.append(detalle[2])
        precios.append(detalle[3])
        subtotales.append(int(detalle[4]))

    # Calcular el total a pagar
    total_a_pagar = sum(subtotales)

    # Obtener los datos del representante asociado a la factura
    sql = "SELECT * FROM usuarios WHERE id_usuario = %s"
    cursor.execute(sql, (factura[1],))
    representante = cursor.fetchone()

    # Crear un diccionario con todos los datos necesarios para la plantilla
    terapias_detalles = list(zip(cantidades, terapias, precios, subtotales))
    data = {
        'representante': representante,
        'fecha': factura[2],
        'cedula': representante[2],
        'nombre': representante[3],
        'apellido': representante[4],
        'direccion': representante[5],
        'terapias_detalles': terapias_detalles,
        'total_a_pagar': total_a_pagar
    }

    # Generar el PDF a partir de la plantilla y los datos
    rendered = render_template('ver_factura.html', table_data=data)
    html = HTML(string=rendered)
    pdf = html.write_pdf(stylesheets=['static/css/style2.css'])

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=factura_{}.pdf'.format(id_factura)

    return response


#Funcion para actualizar cita después de aprobarla

@app.route('/actualizar_cita', methods=['POST'])
def actualizar_cita():

    _idCita = request.form['txtId']
    # _fecha = request.form['txtFecha']
    # _cedula = request.form['txtCedula']
    # _nombre = request.form['txtNombre']
    # _apellido = request.form['txtApellido']
    # _telefono = request.form['txtTelefono']
    _estado = 'aprobado'
    _nuevaFecha = request.form['txtNuevaFecha']
    _hora = request.form['txtHora']

    sql = "UPDATE citas SET estado = %s, fecha_cita = %s, hora = %s WHERE id_cita = %s;"

    datos=(_estado, _nuevaFecha, _hora, _idCita)   

  
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()

    return redirect('/citas')

#Funcion para buscar una cita en la base de datos a partir de los 
# caracteres ingresados en el input Buscar

@app.route('/buscar_cita', methods=['POST']) 
def buscar_cita(): 
    _busqueda = '%' + request.form['buscar'] + '%'  # Agregar % alrededor del valor de búsqueda
    # _tipo_usuario = request.form['tipo_usuario']  # Saber que tipo de usuario es 
 
    #Buscar por nombre o por cedula 

    #ATENCION: Este codigo se puede mejorar en un futuro ya que no se utilizan los datos de la tabla telefonos.
    #Sin embargo, se colocó para que devuelva exactamente los mismos valores en el mismo orden que en la funcion Citas()
    #y la funcion Buscar_Cita() los devuelva igual. Sino, se alteran los valores en la tabla de Citas.html.
    
    sql = """  
    SELECT citas.*, usuarios.nombre, usuarios.apellido, usuarios.cedula, telefonos_usuario.telefono 
    FROM citas   
    INNER JOIN usuarios ON citas.id_representante = usuarios.id_usuario   
    INNER JOIN telefonos_usuario ON usuarios.id_usuario = telefonos_usuario.id_usuario
    WHERE usuarios.cedula LIKE %s OR usuarios.nombre LIKE %s;  
    """

 
    conn = mysql.connect() 
    cursor = conn.cursor() 
    cursor.execute(sql, (_busqueda, _busqueda))  # Pasar una tupla con los valores de búsqueda
 
    citas = cursor.fetchall()
 
    conn.commit() 

    return render_template('caines/citas.html', citas = citas)


@app.route('/pagos_pdf', methods=['POST'])
def facturas_pdf():
    conn = mysql.connect()
    cursor = conn.cursor()

    # Obtener el término de búsqueda del formulario
    search_term = request.form.get('searchInput', '').strip()
    search_pattern = f"%{search_term}%"  # Formato para LIKE

    # Consulta base para representantes
    if current_user.rol == 'representante':
        sql = '''
            SELECT
                f.fecha AS FechaPago,
                u.nombre AS NombreUsuario,
                u.apellido AS ApellidoUsuario,
                f.total AS MontoFactura
            FROM
                facturas f
            JOIN
                usuarios u ON f.id_usuario = u.id_usuario
            WHERE
                u.tipo_usuario = 'representante' 
                AND u.id_usuario = %s
        '''
        params = [current_user.id]

        # Agregar filtro de búsqueda si hay término
        if search_term:
            sql += '''
                AND (
                    f.fecha LIKE %s 
                    OR u.nombre LIKE %s 
                    OR u.apellido LIKE %s 
                    OR CAST(f.total AS CHAR) LIKE %s
                )
            '''
            params.extend([search_pattern] * 4)

    # Consulta base para otros roles
    else:
        sql = '''
            SELECT
                f.fecha AS FechaPago,
                u.nombre AS NombreUsuario,
                u.apellido AS ApellidoUsuario,
                f.total AS MontoFactura
            FROM
                facturas f
            JOIN
                usuarios u ON f.id_usuario = u.id_usuario
            WHERE
                u.tipo_usuario = 'representante'
        '''
        params = []

        # Agregar filtro de búsqueda si hay término
        if search_term:
            sql += '''
                AND (
                    f.fecha LIKE %s 
                    OR u.nombre LIKE %s 
                    OR u.apellido LIKE %s 
                    OR CAST(f.total AS CHAR) LIKE %s
                )
            '''
            params.extend([search_pattern] * 4)

    # Ordenar y ejecutar la consulta
    sql += " ORDER BY f.fecha ASC"
    cursor.execute(sql, params)
    rows = cursor.fetchall()

    # Agregar correlativo a cada fila
    datos = [(i + 1, *row) for i, row in enumerate(rows)]
    conn.close()

    # Generar el PDF
    rendered = render_template('reportes/reporte_pagos.html', datos=datos)
    html = HTML(string=rendered)
    pdf = html.write_pdf()

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=reporte_facturas.pdf'

    return response




@app.route('/ninos_pdf', methods=['POST'])
def ninos_pdf():
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT
            nombre,
            apellido,
            edad,
            escolaridad            
        FROM
            ninos
        ORDER BY
            nombre ASC
    ''')

    rows = cursor.fetchall()

    # Agregar un correlativo a cada fila
    datos = [(i + 1, *row) for i, row in enumerate(rows)] 

    conn.close()

    # Renderizar el template con los datos agrupados y el total
    rendered = render_template('ninos/reporte_ninos.html', datos=datos)

    # Generar el PDF con WeasyPrint
    html = HTML(string=rendered)
    pdf = html.write_pdf()

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=reporte_inventario.pdf'

    return response


@app.route('/representantes_pdf', methods=['POST'])
def representantes_pdf():
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute('''
            SELECT r.*, t.telefono FROM usuarios r
            LEFT JOIN telefonos_usuario t ON r.id_usuario = t.id_usuario
            WHERE r.tipo_usuario = 'representante'
    ''')

    rows = cursor.fetchall()

    # Agregar un correlativo a cada fila
    datos = [(i + 1, *row) for i, row in enumerate(rows)] 
    
    print(datos)

    conn.close()

    # Renderizar el template con los datos agrupados y el total
    rendered = render_template('reportes/reporte_representantes.html', datos=datos)

    # Generar el PDF con WeasyPrint
    html = HTML(string=rendered)
    pdf = html.write_pdf()

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=reporte_inventario.pdf'

    return response

@app.route('/especialistas_pdf', methods=['POST'])
def especialistas_pdf():
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute('''
            SELECT r.*, t.telefono FROM usuarios r
            LEFT JOIN telefonos_usuario t ON r.id_usuario = t.id_usuario
            WHERE r.tipo_usuario = 'especialista'
    ''')

    rows = cursor.fetchall()

    # Agregar un correlativo a cada fila
    datos = [(i + 1, *row) for i, row in enumerate(rows)] 
    
    print(datos)

    conn.close()

    # Renderizar el template con los datos agrupados y el total
    rendered = render_template('reportes/reporte_especialistas.html', datos=datos)

    # Generar el PDF con WeasyPrint
    html = HTML(string=rendered)
    pdf = html.write_pdf()

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=reporte_inventario.pdf'

    return response


@app.route('/contadores_pdf', methods=['POST'])
def contadores_pdf():
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute('''
            SELECT r.*, t.telefono FROM usuarios r
            LEFT JOIN telefonos_usuario t ON r.id_usuario = t.id_usuario
            WHERE r.tipo_usuario = 'administrador'
    ''')

    rows = cursor.fetchall()

    # Agregar un correlativo a cada fila
    datos = [(i + 1, *row) for i, row in enumerate(rows)] 
    
    print(datos)

    conn.close()

    # Renderizar el template con los datos agrupados y el total
    rendered = render_template('reportes/reporte_contadores.html', datos=datos)

    # Generar el PDF con WeasyPrint
    html = HTML(string=rendered)
    pdf = html.write_pdf()

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=reporte_inventario.pdf'

    return response


@app.route('/secretarias_pdf', methods=['POST'])
def secretarias_pdf():
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute('''
            SELECT r.*, t.telefono FROM usuarios r
            LEFT JOIN telefonos_usuario t ON r.id_usuario = t.id_usuario
            WHERE r.tipo_usuario = 'secretaria'
    ''')

    rows = cursor.fetchall()

    # Agregar un correlativo a cada fila
    datos = [(i + 1, *row) for i, row in enumerate(rows)] 
    
    print(datos)

    conn.close()

    # Renderizar el template con los datos agrupados y el total
    rendered = render_template('reportes/reporte_secretarias.html', datos=datos)

    # Generar el PDF con WeasyPrint
    html = HTML(string=rendered)
    pdf = html.write_pdf()

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=reporte_inventario.pdf'

    return response





mode = "prod"

if __name__ == '__main__':
     
    if mode == "prod":
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        serve(app,host='0.0.0.0',port=5000,threads=6)
        serve(app,host='0.0.0.0',port=5000,threads=6)

