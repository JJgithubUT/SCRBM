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

@app.route ("/")
def login():
    return render_template('index.html')

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
        nombre = request.form['username']
        apellidos = request.form['apellidos']
        correo = request.form['correo']
        password = request.form['password']
        password = generate_password_hash(password)
        conn = get_db_conection()
        cur = conn.cursor()
        cur.execute('INSERT INTO public.usuarios(nombre, apellidos, correo_usuario, password) VALUES (%s, %s, %s, %s);',
                    (nombre, apellidos, correo, password))
        conn.commit()
        cur.close()
        conn.close()
        return render_template('index.html')
    return render_template('index.html')
########################## FIN REGISTRARSE ####################################

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

#==========================================LISTAR OfICIOS=============================================================

def listar_oficios():
    conn = get_db_conection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM oficios WHERE visibilidad IS true')
    oficios= cur.fetchall()
    cur.close()
    conn.close()
    return oficios
  
#==========================================FIN LISTAR OfICIOS=============================================================


############################################################################################
############################################################################################
############################################################################################

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
@login_required
def maquinaria():
    sql_count='SELECT COUNT(*) FROM maquinaria where visibilidad=true'
    sql_lim='SELECT maquinaria.id_maquina, maquinaria.nombre_maquina, maquinaria.costo_maquina, maquinaria.vida_util, unidades.nombre_unidad FROM maquinaria INNER JOIN unidades ON fk_unidad = id_unidad WHERE  visibilidad IS true LIMIT %s OFFsET %s'
    paginado = paginador(sql_count,sql_lim, 1, 7)
    return render_template('maquinaria.html', maquinaria = paginado[0],
                           page = paginado[1],
                           per_page = paginado[2], 
                           total_items = paginado[3],
                           total_pages = paginado[4])

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
    sql_lim = 'SELECT id_oficio, nombre_oficio, unidades.nombre_unidad, costo_oficio, visibilidad FROM oficios INNER JOIN unidades ON oficios.fk_unidad = unidades.id_unidad WHERE visibilidad = true LIMIT %s OFFSET %s;'
    paginado = paginador(sql_count, sql_lim,1,7)
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
#------------------INICIO BASICOS INICIO BASICOS INICIO BASICOS INICIO BASICOS INICIO BASICOS-----------------
#-------------------------------------------------------------------------------------------------------------

#===================================INICIO LEER BASICOS====================================================
@app.route('/basicos')
def basicos():
    conn = get_db_conection()
    cur = conn.cursor()
    cur.execute('SELECT id_unidad, nombre_unidad FROM unidades WHERE visibilidad_unidad=true;')
    unidades = cur.fetchall()
    cur.close()
    conn.close()

    sql_count = 'SELECT COUNT (*) FROM basicos WHERE visible_basico=true;' 
    sql_lim = 'SELECT id_basico, nombre_basico, un.nombre_unidad, porcentaje_basico, fk_cuadrilla_basico, cantidad_cuad_basico, visible_basico FROM basicos ba INNER JOIN unidades un ON ba.fk_unidad_basico = un.id_unidad WHERE ba.visible_basico=true LIMIT %s OFFSET %s;'
    paginado = paginador(sql_count, sql_lim,1,8)
    return render_template('basicos.html', basicos = paginado[0],
                           page = paginado[1],
                           per_page = paginado[2],
                           total_items = paginado[3],
                           total_pages = paginado[4],
                           unidades=unidades)
#===================================FIN LEER BASICOS====================================================

#===================================INICIO REGISTRAR BASICO====================================================
@app.route('/basico/registrar', methods=('GET', 'POST'))
def registrar_basico():
    if request.method == 'POST':

        nombre_basico = request.form['nombre_basico']
        fk_unid_basico = request.form['fk_unid_basico']
        porcentmaqyeq_bas = request.form['porcentmaqyeq_bas']

        conn = get_db_conection()
        cur = conn.cursor()

        cur.execute('INSERT INTO basicos(nombre_basico, fk_unidad_basico, porcentaje_basico) VALUES(%s,%s,%s) RETURNING id_basico', (nombre_basico, fk_unid_basico, porcentmaqyeq_bas,))
        id_basico_nuevo = cur.fetchone()[0]
        conn.commit()

        cur.execute('INSERT INTO cuadrillas(porcentaje_cuadrilla, fk_unidad_cuadrilla) VALUES (0, %s) RETURNING id_cuadrilla;', (fk_unid_basico,))
        id_cuadrilla_nuevo = cur.fetchone()[0]
        conn.commit()

        cur.execute('UPDATE basicos SET fk_cuadrilla_basico=%s, cantidad_cuad_basico=1 WHERE id_basico=%s;', (id_cuadrilla_nuevo, id_basico_nuevo))
        conn.commit()

        cur.close()
        conn.close()

        return redirect(url_for('basicos'))
    return redirect(url_for('basicos'))
#===================================FIN REGISTRAR BASICO====================================================

#===================================INICIO EDITAR BASICO====================================================
@app.route('/basico/editar/<string:id_basico>', methods=('GET', 'POST'))
def editar_basico(id_basico):
    if request.method == 'POST':
        nombre_basico = request.form['nombre_basico']
        fk_unid_basico = request.form['fk_unid_basico']
        porcentmaqyeq_bas = request.form['porcentmaqyeq_bas']
        conn = get_db_conection()
        cur = conn.cursor()
        cur.execute('UPDATE basicos SET nombre_basico=%s, fk_unidad_basico=%s, porcentaje_basico=%s WHERE id_basico=%s;',
                    (nombre_basico, fk_unid_basico, porcentmaqyeq_bas, id_basico,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('detalles_basico', id_basico=id_basico))
    return redirect(url_for('detalles_basico', id_basico=id_basico))
#===================================FIN EDITAR BASICO====================================================

#===================================INICIO ELIMINAR BASICO====================================================
@app.route('/basico/eliminar/<string:id_basico>')
def eliminar_basico(id_basico):
    conn = get_db_conection()
    cur = conn.cursor()
    valor = False
    cur.execute('UPDATE basicos SET visible_basico=%s WHERE id_basico=%s;',
                (valor, id_basico,))
    cur.close()
    conn.close()
    return redirect(url_for('basicos'))
#===================================FIN ELIMINAR BASICO====================================================

#===================================INICIO DETALLES BASICO====================================================
@app.route('/basico/detalles/<string:id_basico>')
def detalles_basico(id_basico):
    conn = get_db_conection()
    cur = conn.cursor()

    cur.execute('SELECT id_unidad, nombre_unidad FROM unidades WHERE visibilidad_unidad=true;')
    unidades = cur.fetchall()

    cur.execute('SELECT id_basico, nombre_basico, un.nombre_unidad, porcentaje_basico, fk_cuadrilla_basico, cantidad_cuad_basico, visible_basico, fk_unidad_basico FROM basicos ba INNER JOIN unidades un ON ba.fk_unidad_basico = un.id_unidad WHERE id_basico = %s;',
                (id_basico,))
    basicon = cur.fetchone()
    fk_cuadrilla_basico_concepton = int(basicon[4])

    ########## SUMAS / CONTADORES PARA COSTES

    cur.execute('SELECT SUM(cant_basmat * costo_material) as costo_materiales_basico FROM basicosmateriales WHERE fk_id_basico = %s',
                (id_basico,))
    resultado = cur.fetchone()
    if resultado is not None and resultado[0] is not None:
        conteo_materiales_basico = resultado[0]
    else:
        conteo_materiales_basico = 0

    cur.execute('SELECT SUM(cuof.cant_cuadofi * cuof.costo_oficio) AS pretotal, cuad.porcentaje_cuadrilla, SUM(cuof.cant_cuadofi * cuof.costo_oficio) * (1 + (cuad.porcentaje_cuadrilla / 100)) AS total_oficios FROM cuadrillasoficios cuof INNER JOIN cuadrillas cuad ON cuof.fk_id_cuadrilla = cuad.id_cuadrilla WHERE cuad.id_cuadrilla=%s GROUP BY cuad.porcentaje_cuadrilla;',
                (fk_cuadrilla_basico_concepton,))
    resultado = cur.fetchone()
    if resultado is not None:
        conteo_oficios_basico = tuple(resultado)
    else:
        conteo_oficios_basico = (0, 0, 0)

    # Asegúrate de que conteo_oficios_basico[2] no sea None
    if conteo_oficios_basico[2] is None:
        conteo_oficios_basico = (conteo_oficios_basico[0], conteo_oficios_basico[1], 0)

    # Calcula el costo total de básico
    costo_total_de_basico = conteo_materiales_basico + conteo_oficios_basico[2]

    ########## SELECTS DE MATERIALES

    cur.execute('SELECT id_material, nombre_material, un.nombre_unidad, costo_material FROM materiales ma INNER JOIN unidades un ON ma.fk_unidad = un.id_unidad WHERE visibilidad_material=true;')
    materiales = cur.fetchall()

    cur.execute('SELECT id_basmat, ma.nombre_material, un.nombre_unidad, bm.costo_material, bm.cant_basmat, (cant_basmat * bm.costo_material) AS importe FROM basicosmateriales bm INNER JOIN materiales ma ON bm.fk_id_material = ma.id_material INNER JOIN basicos ba ON bm.fk_id_basico = ba.id_basico INNER JOIN unidades un ON ma.fk_unidad = un.id_unidad WHERE fk_id_basico=%s ORDER BY bm.id_basmat;',
                (id_basico,))
    materialones = cur.fetchall()

    ########## SELECTS DE OFICIOS y CUADRILLAS

    cur.execute('SELECT id_oficio, nombre_oficio, uni.nombre_unidad, costo_oficio, visibilidad FROM oficios ofi INNER JOIN unidades uni ON ofi.fk_unidad = uni.id_unidad;')
    oficios = cur.fetchall()

    cur.execute('SELECT ofi.id_oficio, ofi.nombre_oficio, uni.nombre_unidad, cuof.costo_oficio, cuof.cant_cuadofi, (cuof.costo_oficio * cuof.cant_cuadofi) AS importeoficio, cuof.id_cuadofi FROM cuadrillasoficios cuof INNER JOIN oficios ofi ON cuof.fk_id_oficio = ofi.id_oficio INNER JOIN cuadrillas cuad ON cuof.fk_id_cuadrilla = cuad.id_cuadrilla INNER JOIN basicos bas ON cuof.fk_id_cuadrilla = bas.fk_cuadrilla_basico INNER JOIN unidades uni ON ofi.fk_unidad = uni.id_unidad WHERE bas.fk_cuadrilla_basico = %s ORDER BY cuof.id_cuadofi;',
                (fk_cuadrilla_basico_concepton,))
    oficiones = cur.fetchall()

    ##########

    cur.close()
    conn.close()
    return render_template('detalles_basico.html',
                           basicon=basicon, materiales=materiales,
                           oficios=oficios, unidades=unidades,
                           materialones=materialones,
                           oficiones=oficiones,
                           fk_cuadrilla_basico_concepton=fk_cuadrilla_basico_concepton,
                           conteo_materiales_basico=conteo_materiales_basico,
                           conteo_oficios_basico=conteo_oficios_basico,
                           costo_total_de_basico=costo_total_de_basico)
#===================================FIN DETALLES BASICO====================================================

#===================================INICIO DETALLES BASICO - REGISTRAR MATERIAL====================================================
@app.route('/basico/detalles/<string:id_basico>/registrarmaterial')
def registrar_material_basico(id_basico):
    fk_id_basico = request.args.get('fk_id_basico')
    fk_id_material = request.args.get('fk_id_material')
    costo_material = request.args.get('costo_material')
    conn = get_db_conection()
    cur = conn.cursor()
    cur.execute('INSERT INTO public.basicosmateriales(fk_id_basico, fk_id_material, cant_basmat, costo_material) VALUES (%s, %s, 1, %s);',(fk_id_basico, fk_id_material, costo_material,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('detalles_basico', id_basico=id_basico))

#===================================FIN DETALLES BASICO - REGISTRAR MATERIAL====================================================

#===================================INICIO DETALLES BASICO - EDITAR MATERIAL====================================================
@app.route('/basico/detalles/<string:id_basico>/editarmaterial', methods=('GET', 'POST'))
def editar_material_basico(id_basico):
    id_basmat= request.form['id_basmat']
    cant_basmat = request.form['cant_basmat']
    if request.method == 'POST':
        conn = get_db_conection()
        cur = conn.cursor()
        cur.execute('UPDATE basicosmateriales SET cant_basmat=%s WHERE id_basmat=%s;', (cant_basmat, id_basmat))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('detalles_basico', id_basico=id_basico))
    return redirect(url_for('detalles_basico', id_basico=id_basico))
#===================================FIN DETALLES BASICO - EDITAR MATERIALES====================================================

#===================================INICIO DETALLES BASICO - ELIMINAR MATERIAL====================================================
@app.route('/basico/detalles/<string:id_basico>/eliminarmaterial/<string:id_basmat>', methods=('GET', 'POST'))
def eliminar_material_basico(id_basico, id_basmat):
    conn = get_db_conection()
    cur = conn.cursor()
    cur.execute('DELETE FROM basicosmateriales WHERE id_basmat=%s;', (id_basmat,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('detalles_basico', id_basico=id_basico))
#===================================FIN DETALLES BASICO - ELIMINAR MATERIAL====================================================

#===================================INICIO DETALLES BASICO - REGISTRAR OFICIO (a cuadrilla)====================================================
@app.route('/basico/detalles/<string:id_basico>/registraroficio')
def registrar_oficio_basico(id_basico):
    fk_id_cuadrilla = request.args.get('fk_id_cuadrilla')
    fk_id_oficio = request.args.get('fk_id_oficio')
    costo_oficio = request.args.get('costo_oficio')
    conn = get_db_conection()
    cur = conn.cursor()
    cur.execute('INSERT INTO public.cuadrillasoficios(fk_id_cuadrilla, fk_id_oficio, cant_cuadofi, costo_oficio) VALUES (%s, %s, 1, %s);',
                (fk_id_cuadrilla, fk_id_oficio, costo_oficio))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('detalles_basico', id_basico=id_basico))
#===================================FIN DETALLES BASICO - REGISTRAR OFICIO (a cuadrilla)====================================================

#===================================INICIO DETALLES BASICO - EDITAR MATERIAL====================================================
@app.route('/basico/detalles/<string:id_basico>/editaroficio', methods=('GET', 'POST'))
def editar_oficio_basico(id_basico):
    id_cuadofi = request.form['id_cuadofi']
    cant_cuadofi = request.form['cant_cuadofi']
    if request.method == 'POST':
        conn = get_db_conection()
        cur = conn.cursor()
        cur.execute('UPDATE public.cuadrillasoficios SET cant_cuadofi=%s WHERE id_cuadofi=%s;',
                    (cant_cuadofi, id_cuadofi,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('detalles_basico', id_basico=id_basico))
    return redirect(url_for('detalles_basico', id_basico=id_basico))
#===================================FIN DETALLES BASICO - EDITAR MATERIALES====================================================

#===================================FIN DETALLES BASICO - EDITAR MATERIALES====================================================
@app.route('/basico/detalles/<string:id_basico>/editar_cuadrilla', methods=('GET', 'POST'))
def editar_cuadrilla_basico(id_basico):
    id_cuadrilla = request.form['id_cuadrilla']
    porcentaje_cuadrilla = request.form['porcentaje_cuadrilla']
    print(f'----------id_cuadrilla:{id_cuadrilla}--------porcentaje_cuadrilla:{porcentaje_cuadrilla}----------')
    if request.method == 'POST':
        conn = get_db_conection()
        cur = conn.cursor()
        cur.execute('UPDATE cuadrillas SET porcentaje_cuadrilla=%s WHERE id_cuadrilla=%s;',
                    (porcentaje_cuadrilla, id_cuadrilla,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('detalles_basico', id_basico=id_basico))
    return redirect(url_for('detalles_basico', id_basico=id_basico))
#===================================FIN DETALLES BASICO - EDITAR MATERIALES====================================================

#===================================INICIO DETALLES BASICO - ELIMINAR OFICIO====================================================
@app.route('/basico/detalles/<string:id_basico>/eliminaroficio/<string:id_cuadofi>', methods=('GET', 'POST'))
def eliminar_oficio_basico(id_basico, id_cuadofi):
    conn = get_db_conection()
    cur = conn.cursor()
    cur.execute('DELETE FROM cuadrillasoficios WHERE id_cuadofi=%s;', (id_cuadofi,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('detalles_basico', id_basico=id_basico))
#===================================FIN DETALLES BASICO - ELIMINAR OFICIO====================================================

#-------------------------------------------------------------------------------------------------------------
#-------------------------FIN BASICOS FIN BASICOS FIN BASICOS FIN BASICOS FIN BASICOS-------------------------
#-------------------------------------------------------------------------------------------------------------


#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------
#----------------------------PROYECTO PROYECTO PROYECTO PROYECTO PROYECTO PROYECTO----------------------------
#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------

#-=============================================DASHBOARD===========================================================

@app.route ("/dashboard")
@login_required
def dashboard():
    sql_count = 'SELECT COUNT(*) FROM proyectos WHERE visible_proyecto = true' 
    sql_lim = 'SELECT * FROM public.proyectos WHERE visible_proyecto=true;'
    paginado = paginador(sql_count, sql_lim,1,10)
    
    return render_template('dashboard.html',
                           proyectos= paginado[0],
                           page = paginado[1],
                           per_page = paginado[2],
                           total_items = paginado[3],
                           total_pages = paginado[4])

#-=============================================FIN DASHBOARD===========================================================

#=========================================== Inicio Create Proyecto ==============================================

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
        return redirect(url_for('dashboard'))
    return redirect(url_for('bashboard'))

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
    cur.execute('SELECT id_concepto, nombre_concepto, co.fk_proy_con, uni.nombre_unidad, cantidad_concepto, fk_cuadrilla_con, cant_cuadrilla_con, porcentaje_con, indirectos_con, financiamiento_con, utilidad_con, visible_con FROM conceptos co INNER JOIN unidades uni ON co.fk_unid_con = uni.id_unidad WHERE co.visible_con=true AND co.fk_proy_con=%s;', (id_proyecto,))
    conceptos=cur.fetchall()
    conn.commit()
    cur.execute('SELECT id_unidad, nombre_unidad FROM public.unidades WHERE visibilidad_unidad=true;')
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
                    porcentaje_con, indirectos_con, financiamiento_con, utilidad_con
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

    sqlconceptos = "SELECT id_concepto, nombre_concepto, pr.nombre_proyecto, un.nombre_unidad, co.porcentaje_con, co.indirectos_con, financiamiento_con, utilidad_con, fk_proy_con FROM conceptos co INNER JOIN unidades un ON co.fk_unid_con = un.id_unidad INNER JOIN proyectos pr ON co.fk_proy_con = pr.id_proyecto WHERE visible_con = true AND id_concepto = %s;"
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

    sqlmaquinariaconcepto = "SELECT mq.id_maquina, mq.nombre_maquina, cq.costo_maq, cq.cant_conmaq, (cq.costo_maq*cq.cant_conmaq) AS importe, mq.vida_util, mq.visibilidad, un.nombre_unidad, cq.id_conmaq, cq.fk_id_con, (mq.costo_maquina / mq.vida_util) FROM maquinaria mq INNER JOIN unidades un ON mq.fk_unidad = un.id_unidad INNER JOIN conceptosmaquinaria cq ON mq.id_maquina = cq.fk_id_maq WHERE cq.fk_id_con = %s;"
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


def acceso_no_autorizado(error):
    return render_template('error_401.html')

if __name__ =='__main__':
    csrf.init_app(app)
    app.register_error_handler(404, pagina_no_encontrada)
    app.register_error_handler(401, acceso_no_autorizado)
    app.run(debug=True, port = 5)