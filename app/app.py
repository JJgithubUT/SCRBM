import os
import uuid
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from flask import Flask, render_template, url_for, redirect, request, flash, Blueprint, jsonify
from flask_wtf.csrf import CSRFProtect

from werkzeug.security import generate_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from Models.ModelUser import ModuleUser
from Models.entities.user import User


'''
SE AÑADIO IMPORT LOGGIN ADVERTENCIA SE AÑADIO IMPORT LOGGIN ADVERTENCIA SE AÑADIO IMPORT LOGGIN ADVERTENCIA SE AÑADIO IMPORT LOGGIN ADVERTENCIA
'''
import logging


app = Flask(__name__)
csrf = CSRFProtect()

#LLAMAR A LA BASE DE DATOS

def get_db_conection():
    try:
        conn=psycopg2.connect(host='localhost',
                              dbname='SCRBMpruebas',
                              port= '1940',
                              user = os.environ['DB_USERNAME'],
                              password =os.environ['DB_PASSWORD'],
                              )
        return conn
    except psycopg2.Error as error:
        print(f"Base de datos no encontrada {error}")
        return None

#FIN LLAMADA DE BASE DE DATOS

app.secret_key='mysecretkey'

########################## INICIO L O G I N #################################
Login_manager_app=LoginManager(app)

@Login_manager_app.user_loader
def load_user(idusuarios):
    return ModuleUser.get_by_id(get_db_conection(), idusuarios)

@app.route('/loguear', methods=('GET', 'POST'))
def loguear():
    if request.method == 'POST':
        correo = request.form['Correo']
        password = request.form['Password']
        user = User(None, None, None, correo, password, None, None)
        loged_user = ModuleUser.login(get_db_conection(), user)
        
        if loged_user != None:
            if loged_user.password:
                login_user(loged_user)
                print('Exito en el ACCCC')
                return redirect(url_for('dashboard'))
            else:
                print('Nombre de usuario y/o contraseña incorrecta.')
                return redirect(url_for('login'))
        else:
            print('Nombre de usuario y/o contraseña incorrecta.')
            return redirect(url_for('login'))
    else:
        print('Nombre de usuario y/o contraseña incorrecta.')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    logout_user()
    return render_template('index.html')
########################## FIN L O G I N ####################################

########################## INICIO REGISTRARSE ####################################
@app.route('/registrarte')
def registrarte():
    return render_template('registrarte.html')

@app.route('/registrate/proceso', methods=('GET', 'POST'))
def proceso_registro():
    if request.method == 'POST':
        username = request.form['username']
        apellidos = request.form['apellidos']
        correo = request.form['correo']
        password = request.form['password']
        password = generate_password_hash(password)
        conn = get_db_conection()
        cur = conn.cursor()
        cur.execute('INSERT INTO public.usuarios(username, apellidos, correo_usuario, password) VALUES (%s, %s, %s, %s);',
                    (username, apellidos, correo, password))
        conn.commit()
        cur.close()
        conn.close()
        return render_template('index.html')
    return render_template('index.html')
########################## FIN REGISTRARSE ####################################

@app.route ("/")
def login():
    return render_template('index.html')



@app.route ("/dashboard")
def dashboard():
    return render_template('dashboard.html')

#-----------------------------------------------inicio PAGINADOR-------------------------------------------------------

def paginador(sql_count,sql_lim,in_page,per_pages):
    page = request.args.get('page', in_page, type=int)
    per_page = request.args.get('per_page', per_pages, type=int)

    offset = (page - 1) * per_page

    conn = get_db_conection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    cursor.execute(sql_count)
    total_items = cursor.fetchone()['count']

    cursor.execute(sql_lim,(per_page, offset))
    items = cursor.fetchall()

    cursor.close()
    conn.close()

    total_pages = (total_items + per_page - 1) // per_page

    return items, page, per_page, total_items, total_pages

#-----------------------------------------------fin PAGINADOR----------------------------------------------------------

#=============================================LISTAR MATERIAL=================================================
def  listar_materiales():
    conn= get_db_conection()
    cur=conn.cursor()
    cur.execute('SELECT * FROM materiales WHERE visibilidad_material = true ORDER BY nombre_material ASC')
    materiales=cur.fetchall()
    cur.close
    conn.close
    return materiales
#=========================================FIN LISTAR UNIDADES=====================================================

#=====================================================LISTAR UNIDAD=============================================
def listar_unidad():
    conn = get_db_conection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM unidades WHERE visibilidad_unidad IS true ORDER BY nombre_unidad ASC')
    unidades= cur.fetchall()
    cur.close()
    conn.close()
    return unidades

#=======================================FIN LISTAR UNIDAD===========================================================

#=============================================LISTAR MATERIAL=================================================
def  listar_materiales():
    conn= get_db_conection()
    cur=conn.cursor()
    cur.execute('SELECT id_material, nombre_material, costo_material, visibilidad_material, fk_unidad FROM materiales WHERE visibilidad_material = true ORDER BY nombre_material ASC')
    materiales=cur.fetchall()
    cur.close
    conn.close
    return materiales
#=========================================FIN LISTAR MATERIAL=====================================================




#-----------------------------------------------INICIO READ UNIDAD------------------------------------------------------

@app.route("/unidades")
@login_required
def unidades():
    sql_count= 'SELECT COUNT(*) FROM unidades where visibilidad_unidad=true'
    sql_lim = 'SELECT * FROM public.unidades WHERE visibilidad_unidad = true ORDER BY id_unidad ASC LIMIT %s OFFSET %s'
    paginado = paginador(sql_count, sql_lim, 1, 7)
    print(paginado[0])
    return render_template('unidades.html',
                           unidades = paginado[0],
                           page = paginado[1],
                           per_page = paginado[2],
                           total_items = paginado[3],
                           total_pages = paginado[4])

#-----------------------------------------------FIN READ UNIDAD ------------------------------------------------------

#-------------------------INICIO REGISTRO UNIDAD------------------------------------------------------------------


@app.route("/unidades/registrar")
@login_required
def form_regis_unidad():
    return render_template('registrar_unidad.html')


@app.route("/unidades/registrar/regitrando", methods=('GET', 'POST'))
@login_required
def registrando_unidad():
    if request.method == 'POST':
        unidad = request.form['unidad']
        
        conn = get_db_conection()
        cur = conn.cursor()
        cur.execute('INSERT INTO unidades(nombre_unidad)'
                    'VALUES (%s)',
                    (unidad,))
        conn.commit()
        cur.close()
        conn.close()
        flash('Unidad registrada correctamente')
        return redirect(url_for('unidades'))
    return redirect(url_for('unidades'))

#-------------------------FIN REGISTRO UNIDAD------------------------------------------------------------------
         
#----------------------------INICIO UPDATE UNIDADES-----------------------------------------------------------------
@app.route('/unidades/editar/<string:id_unidad>')
@login_required
def editar_unidad(id_unidad):
    conn = get_db_conection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM unidades WHERE id_unidad ={0}'.format(id_unidad))
    unidad = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return render_template('unidades_editar.html', unidad = unidad[0])

@app.route('/unidad/editar/proceso/<string:id_unidad>', methods =['POST'] )
@login_required
def editar_unidad_proceso(id_unidad):
    if request.method == 'POST':
        nombre_unidad = request.form['nombre_unidad']
        
        conn = get_db_conection()
        cur = conn.cursor()
        sql = "UPDATE unidades SET nombre_unidad=%s WHERE id_unidad =%s;"
        valores = (nombre_unidad, id_unidad)
        cur.execute(sql, valores)
        conn.commit()
        cur.close()
        conn.close()
        flash('Unidad editada')
        return redirect (url_for('unidades'))
    return redirect (url_for('unidades'))

#----------------------------FIN UBDATE UNIDADE-----------------------------------------------------------------

#========================================= INICIO ELIMINAR UNIDADES ============================================

@app.route('/unidad/eliminar/<string:id_unidad>')
@login_required
def eliminar_unidad(id_unidad):
    activo = False
    conn = get_db_conection()
    cur = conn.cursor()
    sql = 'UPDATE unidades SET visibilidad_unidad=%s WHERE id_unidad=%s'
    valores = (activo, id_unidad) 
    cur.execute(sql, valores)
    conn.commit()
    cur.close()
    conn.close()
    flash('Se elimino la unidad')
    return redirect (url_for('unidades'))

#========================================= FIN ELIMINAR UNIDADES ============================================

#===========================================INICIO READ MATERIALES=============================================

@app.route('/materiales')
@login_required
def materiales():
    sql_count= 'SELECT COUNT(*) FROM materiales where visibilidad_material=true'
    sql_lim = 'SELECT materiales.id_material, materiales.nombre_material, materiales.costo_material, unidades.nombre_unidad FROM materiales INNER JOIN unidades ON materiales.fk_unidad = unidades.id_unidad WHERE visibilidad_material = true ORDER BY nombre_material ASC LIMIT %s OFFSET %s'     
    paginado = paginador(sql_count, sql_lim,1,7) 
   
    return render_template('materiales.html', 
                           materiales = paginado[0],
                           page = paginado[1],
                           per_page = paginado[2], 
                           total_items = paginado[3],
                           total_pages = paginado[4])


#=======================================+FIN READ MATERIALES===================================================


#-------------------------INICIO REGISTRO MATERIAL------------------------------------------------------------------


@app.route("/materiales/registrar")
def registrar_material():
    return render_template('registrar_material.html', unidades = listar_unidad())


@app.route("/materiales/registrar/proceso", methods=('GET', 'POST'))
def registrar_material_proceso():
    if request.method == 'POST':
        nombre_material = request.form['nombre_material']
        costo_material = request.form['costo_material']
        fk_unidad = request.form['fk_unidad']
        
        conn = get_db_conection()
        cur = conn.cursor()
        cur.execute('INSERT INTO public.materiales(nombre_material, costo_material,  fk_unidad) '
	                'VALUES (%s, %s, %s);',
                    (nombre_material, costo_material, fk_unidad,))
        conn.commit()
        cur.close()
        conn.close()
        flash('Material registrado correctamente')
        return redirect(url_for('materiales'))
    return redirect(url_for('materiales'))

#-------------------------FIN REGISTRO MATERIAL------------------------------------------------------------------
    
#===============================INICIO UPDATE MATERIAL-============================================================
@app.route('/material/editar/<string:id_material>')
def editar_material(id_material):
    conn = get_db_conection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM materiales WHERE id_material ={0}'.format(id_material))
    materiales = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return render_template('editar_material.html', materiales = materiales[0], unidades = listar_unidad())

@app.route('/material/editar/proceso/<string:id_material>', methods =['POST'] )
def editar_material_proceso(id_material):
    if request.method == 'POST':
        nombre_material = request.form['nombre_material']
        costo_material = request.form['costo_material']
        fk_unidad = request.form['fk_unidad']
        
        conn = get_db_conection()
        cur = conn.cursor()
        sql = "UPDATE materiales SET nombre_material=%s, costo_material=%s, fk_unidad = %s WHERE id_material =%s;"
        valores = (nombre_material, costo_material, fk_unidad, id_material)
        cur.execute(sql, valores)
        conn.commit()
        cur.close()
        conn.close()
        flash('Material editado')
        return redirect (url_for('materiales'))
    return redirect (url_for('materiales'))
#================================FIN UPDATE MATERIAL============================================================

#===================================INICIO ELIMINAR MATERIAL====================================================

@app.route('/material/eliminar/<string:id_material>')
def eliminar_material(id_material):
    activo = False
    conn = get_db_conection()
    cur = conn.cursor()
    sql = 'UPDATE materiales SET visibilidad_material=%s WHERE id_material=%s'
    valores = (activo, id_material) 
    cur.execute(sql, valores)
    conn.commit()
    cur.close()
    conn.close()
    flash('Se elimino el material')
    return redirect (url_for('materiales'))

#=======================================FIN ELIMINAR MATERIAL===================================================

#=======================================MAQUINARIA==============================================================

#---------------------------------------------READ MAQUINARIA---------------------------------------------------

@app.route("/maquinaria")
def maquinaria():
    conn = get_db_conection()
    cur = conn.cursor()
    cur.execute('SELECT maquinaria.id_maquina, maquinaria.nombre_maquina, maquinaria.costo_maquina, ' 
	            'maquinaria.vida_util, unidades.nombre_unidad FROM maquinaria INNER JOIN unidades ' 
	            'ON fk_unidad = id_unidad WHERE  visibilidad IS true ')
    maquinaria = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return render_template('maquinaria.html', maquinaria = maquinaria)

#--------------------------------------------REGISTRO MAQUINARIA----------------------------------------------------

@app.route("/maquinaria/registrar")
def registrar_maquinaria():
    return render_template('registrar_maquinaria.html', unidades = listar_unidad())


@app.route("/maquinaria/registrar/proceso", methods=('GET', 'POST'))
def registrar_maquinaria_proceso():
    if request.method == 'POST':
        nombre_maquina = request.form['nombre_maquina']
        costo_maquina = request.form['costo_maquina']
        vida_util = request.form['vida_util']
        fk_unidad =  request.form['fk_unidad']
        
        conn = get_db_conection()
        cur = conn.cursor()
        cur.execute('INSERT INTO public.maquinaria(nombre_maquina, costo_maquina, vida_util, fk_unidad) '
	                'VALUES (%s, %s, %s, %s);',
                    (nombre_maquina, costo_maquina, vida_util, fk_unidad,))
        conn.commit()
        cur.close()
        conn.close()
        flash('Maquina registrada correctamente')
        return redirect(url_for('maquinaria'))
    return redirect(url_for('maquinaria'))

#------------------------------------------UPDATE MAQUINARIA---------------------------------------------------------

@app.route('/maquina/editar/<int:id_maquina>')
def editar_maquina(id_maquina):
    conn = get_db_conection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM maquinaria WHERE id_maquina = %s;', (id_maquina,))
    maquinaria = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return render_template('editar_maquinaria.html', maquinaria=maquinaria[0], unidades=listar_unidad())

@app.route('/maquina/editar/proceso/<string:id_maquina>', methods =['POST'] )
def editar_maquina_proceso(id_maquina):
    if request.method == 'POST':
        nombre_maquina = request.form['nombre_maquina']
        costo_maquina = request.form['costo_maquina']
        vida_util = request.form['vida_util']
        
        conn = get_db_conection()
        cur = conn.cursor()
        sql = "UPDATE maquinaria SET nombre_maquina=%s, costo_maquina=%s, vida_util = %s WHERE id_maquina =%s;"
        valores = (nombre_maquina, costo_maquina, vida_util, id_maquina)
        cur.execute(sql, valores)
        conn.commit()
        cur.close()
        conn.close()
        flash('Maquina editada')
        return redirect (url_for('maquinaria'))
    return redirect (url_for('maquinaria'))

#--------------------------------------------------ELIMINAR MAQUINARIA------------------------------------------------

@app.route('/maquinaria/eliminar/<string:id_maquina>')
def eliminar_maquinaria(id_maquina):
    activo = False
    conn = get_db_conection()
    cur = conn.cursor()
    sql = 'UPDATE maquinaria SET visibilidad=%s WHERE id_maquina=%s'
    valores = (activo, id_maquina) 
    cur.execute(sql, valores)
    conn.commit()
    cur.close()
    conn.close()
    flash('Se elimino la maquina')
    return redirect (url_for('maquinaria'))

#---------------------------------------------------------------------------------------------------------------------

#======================================= OFICIOS ===================================================

#=======================================INICIO READ OFICIOS==========================================================

@app.route('/oficios')
@login_required
def oficios():
    sql_count = 'SELECT COUNT(*) FROM oficios where visibilidad = true;'
    sql_lim = 'SELECT id_oficio, nombre_oficio, unidades.nombre_unidad AS unitts, costo_oficio, visibilidad FROM oficios INNER JOIN unidades ON oficios.fk_unidad = unidades.id_unidad WHERE visibilidad = true ORDER BY id_oficio LIMIT %s OFFSET %s;'
    paginado = paginador(sql_count, sql_lim,1,10)
    return render_template('oficios.html', oficios = paginado[0],
                           page = paginado[1],
                           per_page = paginado[2],
                           total_items = paginado[3],
                           total_pages = paginado[4])

#======================================= FIN READ OFICIOS ===========================================================

#-------------------------INICIO REGISTRO OFICIO------------------------------------------------------------------

@app.route("/oficios/registrar")
def registrar_oficio():
    return render_template('registrar_oficio.html', unidades = listar_unidad())


@app.route("/oficios/registrar/proceso", methods=('GET', 'POST'))
def registrar_oficio_proceso():
    if request.method == 'POST':
        nombre_oficio = request.form['nombre_oficio']
        costo_oficio = request.form['costo_oficio']
        fk_unidad = request.form['fk_unidad']
        
        conn = get_db_conection()
        cur = conn.cursor()
        cur.execute('INSERT INTO public.oficios(nombre_oficio, costo_oficio, fk_unidad) VALUES (%s, %s, %s)', (nombre_oficio, costo_oficio, fk_unidad))
        conn.commit()
        cur.close()
        conn.close()
        flash('Oficio registrado correctamente')
        return redirect(url_for('oficios'))
    return redirect(url_for('oficios'))

#-------------------------FIN REGISTRO OFICIO------------------------------------------------------------------

#===============================INICIO UPDATE OFICIO-============================================================

@app.route('/oficio/editar/<string:id_oficio>')
def editar_oficio(id_oficio):
    conn = get_db_conection()
    cur = conn.cursor()

    cur.execute('SELECT id_oficio, nombre_oficio, unidades.nombre_unidad, costo_oficio, visibilidad '
                'FROM oficios '
                'INNER JOIN unidades '
                'ON oficios.fk_unidad = unidades.id_unidad '
                'WHERE id_oficio ={0}'.format(id_oficio))
    oficios = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return render_template('editar_oficio.html', oficios=oficios[0], unidades = listar_unidad())

@app.route('/oficio/editar/proceso/<string:id_oficio>', methods =['POST'] )
def editar_oficio_proceso(id_oficio):
    if request.method == 'POST':
        nombre_oficio = request.form['nombre_oficio']
        costo_oficio = request.form['costo_oficio']
        fk_unidad = request.form['fk_unidad']

        conn = get_db_conection()
        cur = conn.cursor()
        sql = "UPDATE public.oficios SET nombre_oficio=%s, costo_oficio=%s, fk_unidad=%s WHERE id_oficio=%s"
        valores = (nombre_oficio, costo_oficio, fk_unidad, id_oficio)
        cur.execute(sql, valores)
        conn.commit()
        cur.close()
        conn.close()
        flash('Oficio editado')
        return redirect (url_for('oficios'))
    return redirect (url_for('oficios'))

#================================FIN UPDATE OFICIO============================================================

#===================================INICIO ELIMINAR OFICIO====================================================

@app.route('/oficio/eliminar/<string:id_oficio>')
def eliminar_oficio(id_oficio):
    activo = False
    conn = get_db_conection()
    cur = conn.cursor()
    sql = 'UPDATE oficios SET visibilidad=%s WHERE id_oficio=%s'
    valores = (activo, id_oficio) 
    cur.execute(sql, valores)
    conn.commit()
    cur.close()
    conn.close()
    flash('Se elimino el oficio')
    return redirect (url_for('oficios'))

#=======================================FIN ELIMINAR OFICIO===================================================


#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------
#----------------------------PROYECTO PROYECTO PROYECTO PROYECTO PROYECTO PROYECTO----------------------------
#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------

#=========================================== Inicio Read Proyecto ===========================================

@app.route('/proyectos')
def proyectos():
    conn = get_db_conection()
    cur = conn.cursor()
    cur.execute('SELECT id_proyecto, fk_creador_proyecto, nombre_proyecto, titulo_proyecto, colonia_proyecto, municipio_proyecto, estado_proyecto, nombrecliente_proyecto, visible_proyecto, gubernamental_proyecto FROM public.proyectos WHERE visible_proyecto=true;')
    proyectos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('proyectos.html', proyectos=proyectos)

#=========================================== Fin Read Proyecto ==============================================

#=========================================== Inicio Create Proyecto ==============================================

@app.route('/proyecto/registrar')
def registrar_proyecto():
    return render_template('registrar_proyecto.html')

@app.route('/proyecto/registrar/proceso', methods=('GET', 'POST'))
def registrar_proyecto_proceso():
    if request.method == 'POST':
        #fk_creador_proyecto = request.form['fk_creador_proyecto']
        nombre_proyecto = request.form['nombre_proyecto']
        titulo_proyecto = request.form['titulo_proyecto']
        colonia_proyecto = request.form['colonia_proyecto']
        municipio_proyecto = request.form['municipio_proyecto']
        estado_proyecto = request.form['estado_proyecto']
        nombrecliente_proyecto = request.form['nombrecliente_proyecto']
        gubernamental_proyecto = 'gubernamental_proyecto' in request.form

        conn = get_db_conection()
        cur = conn.cursor()
        cur.execute('INSERT INTO proyectos(nombre_proyecto, titulo_proyecto, colonia_proyecto, municipio_proyecto, estado_proyecto, nombrecliente_proyecto, gubernamental_proyecto) '
                    'VALUES (%s,%s,%s,%s,%s,%s,%s);',
                    (nombre_proyecto, titulo_proyecto, colonia_proyecto, municipio_proyecto, estado_proyecto, nombrecliente_proyecto, gubernamental_proyecto,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('proyectos'))
    return redirect(url_for('proyectos'))

#=========================================== Fin Create Proyecto ==============================================

#=========================================== Inicio Editar Proyecto ==============================================

@app.route('/proyecto/editar/<string:id_proyecto>', methods =['POST'] )
def editar_proyecto_proceso(id_proyecto):
    if request.method == 'POST':
        nombre_proyecto = request.form['nombre_proyecto']
        titulo_proyecto = request.form['titulo_proyecto']
        colonia_proyecto = request.form['colonia_proyecto']
        municipio_proyecto = request.form['municipio_proyecto']
        estado_proyecto = request.form['estado_proyecto']
        nombrecliente_proyecto = request.form['nombrecliente_proyecto']
        gubernamental_proyecto = request.form['gubernamental_proyecto']
        conn = get_db_conection()
        cur = conn.cursor()
        valores = (nombre_proyecto, titulo_proyecto, colonia_proyecto, municipio_proyecto, estado_proyecto, nombrecliente_proyecto, gubernamental_proyecto, id_proyecto)
        sql = 'UPDATE proyectos SET nombre_proyecto=%s, titulo_proyecto=%s, colonia_proyecto=%s, municipio_proyecto=%s, estado_proyecto=%s, nombrecliente_proyecto=%s, gubernamental_proyecto=%s WHERE id_proyecto=%s;'
        cur.execute(sql, valores)
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('detalles_proyecto', id_proyecto=id_proyecto))
    return redirect(url_for('detalles_proyecto', id_proyecto=id_proyecto))

#=========================================== Fin Editar Proyecto ==============================================

#=========================================== Inicio Eliminar Proyecto ==============================================

@app.route('/proyecto/eliminar/<string:id_proyecto>')
def eliminar_proyecto(id_proyecto):
    conn = get_db_conection()
    cur = conn.cursor()
    sql = "UPDATE proyectos SET visible_proyecto=false WHERE id_proyecto=%s;"
    cur.execute(sql, id_proyecto)
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('proyectos'))

#=========================================== Fin Eliminar Proyecto ==============================================

#=========================================== Inicio LEER DETALLES Proyecto (CONCEPTOS DE PROYECTO) ==============================================

@app.route('/proyecto/detalles/<string:id_proyecto>')
def detalles_proyecto(id_proyecto):
    conn = get_db_conection()
    cur = conn.cursor()
    cur.execute('SELECT id_proyecto, fk_creador_proyecto, nombre_proyecto, titulo_proyecto, colonia_proyecto, municipio_proyecto, estado_proyecto, nombrecliente_proyecto, visible_proyecto, gubernamental_proyecto FROM proyectos WHERE id_proyecto=%s;', (id_proyecto,))
    proyectaso = cur.fetchall()
    conn.commit()
    cur.execute('SELECT id_concepto, nombre_concepto, co.fk_proy_con, uni.nombre_unidad, cantidad_concepto, fk_cuad_con, cantcuad_con, porcentajemaqyeq_con, indirectos_con, financiamiento_con, utilidad_con, visible_con FROM conceptos co INNER JOIN unidades uni ON co.fk_unid_con = uni.id_unidad WHERE co.visible_con=true AND co.fk_proy_con=%s;', (id_proyecto,))
    conceptos=cur.fetchall()
    conn.commit()
    cur.execute('SELECT id_unidad, nombre_unidad FROM public.unidades;')
    unidades=cur.fetchall()
    conn.commit()   
    cur.close()
    conn.close()
    return render_template('detalles_proyecto.html', proyectaso=proyectaso[0], conceptos=conceptos, unidades=unidades)

#=========================================== Fin LEER DETALLES Proyecto (CONCEPTOS DE PROYECTO) ==============================================

#=========================================== Inicio REGISTRAR CONCEPTO DETALLES Proyecto (CONCEPTOS DE PROYECTO) ==============================================

@app.route('/proyecto/detalles/<string:id_proyecto>/registrarconcepto', methods=('GET', 'POST'))
def registrar_concepto(id_proyecto):
    if request.method == 'POST':
        try:
            nombre_concepto = request.form['nombre_concepto']
            fk_proy_con = request.form['fk_proy_con']
            fk_unid_con = request.form['fk_unid_con']
            cantidad_concepto = request.form['cantidad_concepto']
            porcentajemaqyeq_con = request.form['porcentajemaqyeq_con']
            indirectos_con = request.form['indirectos_con']
            financiamiento_con = request.form['financiamiento_con']
            utilidad_con = request.form['utilidad_con']

            conn = get_db_conection()
            cur = conn.cursor()
            sql = '''
                INSERT INTO public.conceptos(
                    nombre_concepto, fk_proy_con, fk_unid_con, cantidad_concepto, 
                    porcentajemaqyeq_con, indirectos_con, financiamiento_con, utilidad_con
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            '''
            valores = (nombre_concepto, fk_proy_con, fk_unid_con, cantidad_concepto, 
                       porcentajemaqyeq_con, indirectos_con, financiamiento_con, utilidad_con)
            cur.execute(sql, valores)
            conn.commit()  # Asegúrate de hacer commit para guardar los cambios
            cur.close()
            conn.close()

            return redirect(url_for('detalles_proyecto', id_proyecto=id_proyecto))
        except Exception as e:
            logging.error(f"Error al registrar concepto: {e}")
            return "Error al registrar concepto", 500
    return redirect(url_for('detalles_proyecto', id_proyecto=id_proyecto))


#=========================================== Fin CREAR CONCEPTO DETALLES Proyecto (CONCEPTOS DE PROYECTO) ==============================================

#=========================================== Inicio ELIMINAR CONCEPTO DETALLES Proyecto (CONCEPTOS DE PROYECTO) ==============================================

@app.route('/proyecto/detalles/<string:id_proyecto>/eliminarconcepto/<string:id_concepto>')
def eliminar_concepto(id_proyecto, id_concepto):
    conn = get_db_conection()
    cur = conn.cursor()
    activo = False
    sql = 'UPDATE public.conceptos SET visible_con=%s WHERE id_concepto=%s;'
    cur.execute(sql, (activo, id_concepto))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('detalles_proyecto', id_proyecto=id_proyecto))

#=========================================== Fin ELIMINAR CONCEPTO DETALLES Proyecto (CONCEPTOS DE PROYECTO) ==============================================

#=========================================== Inicio DETALLES CONCEPTO Proyecto =====================================
@app.route('/proyecto/detalles/concepto/<string:id_concepto>/detalles/')
def detalles_concepto(id_concepto):
    conn = get_db_conection()
    cur = conn.cursor()

    sqlconceptos = "SELECT id_concepto, nombre_concepto, pr.nombre_proyecto, un.nombre_unidad, co.porcentajemaqyeq_con, co.indirectos_con, financiamiento_con, utilidad_con, fk_proy_con FROM conceptos co INNER JOIN unidades un ON co.fk_unid_con = un.id_unidad INNER JOIN proyectos pr ON co.fk_proy_con = pr.id_proyecto WHERE visible_con = true AND id_concepto = %s;"
    cur.execute(sqlconceptos, (id_concepto,))
    concepton = cur.fetchone()
    conn.commit()

    sqlmaterialesconcepto = "SELECT ma.id_material, ma.nombre_material, cm.costo_mat, cm.cant_conmat, (cm.cant_conmat * cm.costo_mat) AS importe, ma.visibilidad_material, un.nombre_unidad, cm.id_conmat, cm.fk_id_con FROM materiales ma INNER JOIN unidades un ON ma.fk_unidad = un.id_unidad INNER JOIN conceptosmateriales cm ON ma.id_material = cm.fk_id_mat WHERE cm.fk_id_con = %s;"
    cur.execute(sqlmaterialesconcepto, (id_concepto,))
    materialon = cur.fetchall()
    conn.commit()

    sqlmateriales = "SELECT id_material, nombre_material, costo_material, visibilidad_material, nombre_unidad FROM materiales INNER JOIN unidades ON materiales.fk_unidad = unidades.id_unidad WHERE visibilidad_material = true;"
    cur.execute (sqlmateriales)
    materiales = cur.fetchall()
    conn.commit()

    sqlmaquinariaconcepto = "SELECT mq.id_maquina, mq.nombre_maquina, cq.costo_maq, cq.cant_conmaq, (cq.costo_maq*cq.cant_conmaq) AS importe, mq.vida_util, mq.visibilidad, un.nombre_unidad, cq.id_conmaq, cq.fk_id_con FROM maquinaria mq INNER JOIN unidades un ON mq.fk_unidad = un.id_unidad INNER JOIN conceptosmaquinaria cq ON mq.id_maquina = cq.fk_id_maq WHERE cq.fk_id_con = %s;"
    cur.execute(sqlmaquinariaconcepto, (id_concepto,))
    maquinon = cur.fetchall()
    conn.commit()

    sqlmaquinaria = "SELECT id_maquina, nombre_maquina, costo_maquina, vida_util, visibilidad, nombre_unidad FROM maquinaria INNER JOIN unidades ON maquinaria.fk_unidad = unidades.id_unidad WHERE maquinaria.visibilidad = true;"
    cur.execute(sqlmaquinaria)
    maquinaria = cur.fetchall()

    cur.close()
    conn.close()
    return render_template('detalles_concepto.html', concepton=concepton,
                           materialon=materialon, materiales=materiales,
                           maquinon=maquinon, maquinaria=maquinaria
                           )
#=========================================== Fin DETALLES CONCEPTO Proyecto ========================================

#=========================================== Inicio DETALLES CONCEPTO Proyecto - REGISTRAR MATERIAL A CONCEPTO =====================================
@app.route('/concepto/<string:fk_id_con>/detalles/material/<string:fk_id_mat>-costo-<string:costo_mat>/registrar')
def registrar_material_concepto(fk_id_con, fk_id_mat, costo_mat):
    conn = get_db_conection()
    cur = conn.cursor()
    sql = "INSERT INTO public.conceptosmateriales(fk_id_con, fk_id_mat, cant_conmat, costo_mat) VALUES (%s, %s, 1, %s);"
    cur.execute(sql, (fk_id_con, fk_id_mat, costo_mat,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('detalles_concepto', id_concepto=fk_id_con))
#=========================================== Fin DETALLES CONCEPTO Proyecto - REGISTRAR MATERIAL A CONCEPTO =====================================

#=========================================== Inicio DETALLES CONCEPTO Proyecto - EDITAR MATERIAL A CONCEPTO =====================================
@app.route('/concepto/<string:id_concepto>/detalles/material/editar/', methods=('GET', 'POST'))
def editar_material_concepto(id_concepto):
    if request.method == 'POST':
        id_conmat = request.form['id_conmat']
        cant_conmat = request.form['cant_conmat']
        conn = get_db_conection()
        cur = conn.cursor()
        cur.execute('UPDATE public.conceptosmateriales SET cant_conmat=%s WHERE id_conmat=%s;', (cant_conmat, id_conmat,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('detalles_concepto', id_concepto=id_concepto))
    return redirect(url_for('detalles_concepto', id_concepto=id_concepto))
#=========================================== Fin DETALLES CONCEPTO Proyecto - EDITAR MATERIAL A CONCEPTO =====================================

#=========================================== Inicio DETALLES CONCEPTO Proyecto - ELIMINAR MATERIAL A CONCEPTO =====================================
@app.route('/concepto/<string:id_concepto>/detalles/material/eliminar/<string:id_conmat>')
def eliminar_material_concepto(id_conmat, id_concepto):
    conn = get_db_conection()
    cur = conn.cursor()
    sql = "DELETE FROM public.conceptosmateriales WHERE id_conmat=%s;"
    cur.execute(sql, (id_conmat,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('detalles_concepto', id_concepto=id_concepto))
#=========================================== Inicio DETALLES CONCEPTO Proyecto - ELIMINAR MATERIAL A CONCEPTO =====================================

#=========================================== Inicio DETALLES CONCEPTO Proyecto - Registrar MAQUINARIA A CONCEPTO =====================================
@app.route('/concepto/<string:fk_id_con>/detalles/maquinaria/<string:fk_id_maq>-costo-<string:costo_maq>/registrar')
def registrar_maquinaria_concepto(fk_id_con, fk_id_maq, costo_maq):
    conn = get_db_conection()
    cur = conn.cursor()
    sql = "INSERT INTO public.conceptosmaquinaria(fk_id_con, fk_id_maq, cant_conmaq, costo_maq) VALUES (%s, %s, 1, %s);"
    cur.execute(sql, (fk_id_con, fk_id_maq, costo_maq,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('detalles_concepto', id_concepto=fk_id_con))
#=========================================== Fin DETALLES CONCEPTO Proyecto - Registrar MAQUINARIA A CONCEPTO =====================================

#=========================================== Inicio DETALLES CONCEPTO Proyecto - EDITAR MAQUINARIA A CONCEPTO =====================================
@app.route('/concepto/<string:id_concepto>/detalles/maquinaria/editar/', methods=('GET', 'POST'))
def editar_maquinaria_concepto(id_concepto):
    if request.method == 'POST':
        id_conmaq = request.form['id_conmaq']
        cant_conmaq = request.form['cant_conmaq']
        conn = get_db_conection()
        cur = conn.cursor()
        cur.execute('UPDATE public.conceptosmaquinaria SET cant_conmaq=%s WHERE id_conmaq=%s;', (cant_conmaq, id_conmaq,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('detalles_concepto', id_concepto=id_concepto))
    return redirect(url_for('detalles_concepto', id_concepto=id_concepto))
#=========================================== Fin DETALLES CONCEPTO Proyecto - EDITAR MAQUINARIA A CONCEPTO =====================================

#=========================================== Inicio DETALLES CONCEPTO Proyecto - ELIMINAR MAQUINARIA A CONCEPTO =====================================
@app.route('/concepto/<string:id_concepto>/detalles/maquinaria/eliminar/<string:id_conmaq>')
def eliminar_maquinaria_concepto(id_conmaq, id_concepto):
    conn = get_db_conection()
    cur = conn.cursor()
    sql = "DELETE FROM public.conceptosmaquinaria WHERE id_conmaq=%s;"
    cur.execute(sql, (id_conmaq,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('detalles_concepto', id_concepto=id_concepto))
#=========================================== Inicio DETALLES CONCEPTO Proyecto - ELIMINAR MAQUINARIA A CONCEPTO =====================================

#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------
#----------------------------PROYECTO PROYECTO PROYECTO PROYECTO PROYECTO PROYECTO----------------------------
#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------

#======================================INICIO PAPELERA============================================================
         
@app.route('/papelera')
def papelera():
    conn = get_db_conection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM public.unidades '
	            'WHERE visibilidad_unidad = false '
                'ORDER BY id_unidad ASC')
    unidades = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    
    conn = get_db_conection()
    cur = conn.cursor()
    cur.execute('SELECT materiales.id_material, materiales.nombre_material, materiales.costo_material, unidades.nombre_unidad' 
	            ' FROM materiales INNER JOIN unidades ON materiales.fk_unidad = unidades.id_unidad '
                'WHERE visibilidad_material = false '
                'ORDER BY nombre_material')
    materiales = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    
    conn = get_db_conection()
    cur = conn.cursor()
    cur.execute('SELECT id_oficio, nombre_oficio, unidades.nombre_unidad, costo_oficio, visibilidad '
                'FROM oficios '
                'INNER JOIN unidades '
                'ON oficios.fk_unidad = unidades.id_unidad '
                'WHERE visibilidad = false '
                'ORDER BY nombre_oficio ASC ')
    oficios = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    
    conn = get_db_conection()
    cur = conn.cursor()
    cur.execute('SELECT maquinaria.id_maquina, maquinaria.nombre_maquina, maquinaria.costo_maquina, ' 
	            'maquinaria.vida_util, unidades.nombre_unidad FROM maquinaria INNER JOIN unidades ' 
	            'ON fk_unidad = id_unidad WHERE visibilidad = false ')
    maquinaria = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    
    
    return render_template('papelera.html', unidades = unidades, materiales = materiales, oficios=oficios, maquinaria=maquinaria)

#======================================FIN PAPELERA============================================================

@app.route('/perfil')
def perfil():
    return render_template(url_for('perfil'))

    

def pagina_no_encontrada(error):
    return render_template('error404.html')

if __name__ =='__main__':
    csrf.init_app(app)
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, port = 5)