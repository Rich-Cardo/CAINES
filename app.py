#Librerías generales

from flask import Flask
from flask import render_template,request,redirect, flash, make_response
from flaskext.mysql import MySQL

#Librerías para la generación de PDF

import jinja2
import pdfkit
import json

#Librería para enviar solicitudes al servidor
from flask import jsonify

#Librería para servidor de producción
from waitress import serve

#Librería para el manejo de sesiones activas de los usuarios
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user



#Código general de Flask

app = Flask(__name__,static_folder='static')
app.secret_key="Caines"

mysql = MySQL()
app.config['MYSQL_DATABASE_URL'] = 'mysql://root:EGbhqZ172cup7cdvvTgn@containers-us-west-210.railway.app:5983/railway'
app.config['MYSQL_DATABASE_HOST'] = 'containers-us-west-210.railway.app'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 5983
app.config['MYSQL_DATABASE_PASSWORD'] = 'EGbhqZ172cup7cdvvTgn'
app.config['MYSQL_DATABASE_DB']='railway'
mysql.init_app(app)


#Codigo para gestionar el login con Flask_Login

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


#Clase Usuario para el manejo de sesiones activas

class User(UserMixin):
    def __init__(self, id, cedula, nombre, rol):
        self.id = id
        self.cedula = cedula
        self.nombre = nombre
        self.rol = rol

    @staticmethod
    def get(id):
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT * FROM usuarios WHERE id_usuario = %s"
        cursor.execute(sql, (id,))
        user_data = cursor.fetchone()
        if user_data:
            return User(id=user_data[0], rol=user_data[1], cedula=user_data[2], nombre=user_data[3])
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






# Funciones para rellenar los inputs
# en la plantilla create_factura.html

#Codigo para llenar los inputs del representante en create_factura

@app.route('/verificar_cedula', methods=['POST'])
def verificar_cedula():

    cedula = request.form['txtCedula']
    print(cedula)

    # Hacemos la conexión a la base de datos
    conn = mysql.connect() 
    cursor = conn.cursor() 

    # Ejecutamos la consulta SQL
    cursor.execute("SELECT nombre, apellido, direccion FROM usuarios WHERE cedula = %s", (cedula,))

    resultado = cursor.fetchone()

    # Cerramos la conexión a la base de datos
    conn.close()

    if resultado:
        nombre, apellido, direccion = resultado
    else:
        nombre, apellido, direccion = "", "", ""

    response = {
        'nombre': nombre,
        'apellido': apellido,
        'direccion': direccion
    }

    return jsonify(response)


#Codigo para rellenar el input Precio de create_factura.html

@app.route('/verificar_terapia', methods=['POST'])
def verificar_terapia():

    terapia = request.form['txtTerapia']
    print(terapia)

    # Hacemos la conexión a la base de datos
    conn = mysql.connect() 
    cursor = conn.cursor() 

    # Ejecutamos la consulta SQL
    cursor.execute("SELECT precio FROM terapias WHERE terapia = %s", (terapia,))

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
        return render_template('caines/principal.html')
    else:
        flash('Cédula o contraseña incorrecta.')
        return render_template('caines/login.html')





#Funciones para acceder a las rutas de la página

@app.route('/cerrar_sesion', methods=['GET'])
@login_required
def cerrar_sesion():

    logout_user()  # Función de Flask-Login para cerrar sesión
    flash('¡Has cerrado sesión exitosamente!')  # Mostramos un mensaje personalizado

    return redirect('/login')  # Redirigir al inicio de sesión



@app.route('/menu')
@login_required
def menu():
    return render_template('/caines/menu.html')

@app.route('/recuperar_contrasena')
def recuperar_contrasena():
    return render_template('/caines/contrasena.html')

@app.route('/factura')
def factura():
    return render_template('/factura.html')

@app.route('/create_factura')
def create_factura():
    return render_template('/caines/create_factura.html')

@app.route('/login')
def login():
    return render_template('caines/login.html')

@app.route('/principal')
def principal():
    return render_template('caines/principal.html')

@app.route('/registro')
def registro():
    return render_template('caines/registro.html')



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

#Ir a la página principal de director

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
        flash('El usuario ya existe', 'error')
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
        return redirect(redireccionamiento(_tipo_usuario)) 

    return redirect(redireccionamiento(_tipo_usuario))



#Funcion para buscar un usuario en la base de datos a partir de los 
# caracteres ingresados en el input Buscar

@app.route('/buscar_usuario', methods=['POST'])
def buscar_usuario():
    _busqueda = request.form['buscar']
    _tipo_usuario = request.form['tipo_usuario']  # Add this line to get the user type from the form

    # Construct the SQL query with a parameter for 'tipo_usuario'
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



#Funcion para guardar los cambios en el usuario editado

@app.route('/update_user', methods=['POST'])
def update_user():
    _cedula = request.form['txtCedula']
    _nombre = request.form['txtNombre']
    _apellido = request.form['txtApellido']
    _direccion = request.form['txtDireccion']
    _correo = request.form['txtCorreo']
    usuario_id = request.form['txtID']
    _password = request.form['txtPassword']


    # Update los datos del usuario en la tabla 'usuarios'
    sql_usuario = "UPDATE usuarios SET cedula=%s, nombre=%s, apellido=%s, direccion=%s, correo=%s, clave=%s WHERE id_usuario=%s"
    datos_usuario = (_cedula, _nombre, _apellido, _direccion, _correo, _password, usuario_id)
  
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

        if current_user.rol == 'director':

            return redirect(redireccionamiento(_tipo_usuario))
        
        else:
            return redirect('/menu')
  
    except Exception as e:
        conn.rollback()
        return str(e)
  
    finally:
        cursor.close()
        conn.close()

#Fin del código para manipular los usuarios




# #Comienzo del código para la gestión de los Niños

#Ir a la página principal de ninos

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
    
        return render_template('caines/ninos.html', ninos=ninos)
    

    #Sino, que muestre todos los niños totales registrados.
    else: 
        cursor.execute("SELECT * FROM ninos")
    
        ninos = cursor.fetchall() 
    
        conn.commit() 
    
        return render_template('caines/ninos.html', ninos=ninos)

#Ir a la plantilla HTML crear_nino
@app.route('/create_nino')
def create_nino():
    return render_template('caines/create_nino.html')


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


#Funcion para eliminar niño
@app.route('/destroy_nino/<int:id>')
def destroy_nino(id):
    conn = mysql.connect()
    cursor = conn.cursor()


    # Delete the user from the database
    cursor.execute("DELETE FROM ninos WHERE id_nino = %s", (id,))

    conn.commit()


    return redirect('/ninos')

#Funcion para editar niño
@app.route('/edit_nino/<int:id>') 
def edit_nino(id): 
 
    conn = mysql.connect() 
    cursor = conn.cursor()
 
    # Consulta para obtener los datos del niño
    cursor.execute("SELECT * FROM ninos WHERE id_nino = %s ",(id)) 
    ninos = cursor.fetchall()
 
    conn.commit()

    return render_template("caines/edit_nino.html", ninos=ninos)

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

 
    return render_template('caines/ninos.html', ninos=ninos)


#Inicio del codigo de Facturacion



#Funcion para la generacion de PDF
@app.route('/generar_pdf/<table_data_json>')
def pdf_template(table_data_json):

    table_data = json.loads(table_data_json)
    rendered = render_template('/factura.html',table_data=table_data)
    pdf = pdfkit.from_string(rendered,False,css='static/css/style.css', options={"enable-local-file-access": ""})

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

    return response




# if __name__ == '__main__':
#     app.run(debug=True)

mode = "dev"

if __name__ == '__main__':
     
    if mode == "dev":
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        serve(app,host='0.0.0.0',port=5000,threads=2)

