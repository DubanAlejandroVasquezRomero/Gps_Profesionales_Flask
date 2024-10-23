<<<<<<< HEAD
from flask import (
    render_template,flash,request,url_for, Blueprint, g,jsonify,redirect
)
from app.db import get_db
from app.auth import login_required,role_required

bp = Blueprint ('admin',__name__)

@login_required
@role_required ("Administrador")
@bp.route ('/administrador')
def Admin_Inicio ():
    return render_template ("Admin/vista_admin.html")

@bp.route ('/ver_profesionales')
@role_required ('Administrador')
def ver_profesional ():
    db , c = get_db ()
    c.execute ('''
        SELECT profesional.id, profesional.nombre, profesional.especializacion, profesional.telefono, 
               ubicacion.latitud, ubicacion.longitud, profesional.email
        FROM profesional
        INNER JOIN ubicacion ON profesional.id = ubicacion.profesional_id
    ''')
    profesionales = c.fetchall ()
    return render_template ('Admin/ver_profesionales.html',profesionales=profesionales)

@bp.route ('/crear_profesional',methods = ["POST","GET"])
@login_required
def agregar_profesional ():
    if request.method == "POST":
        nombre = request.form ['nombre']
        especialidad = request.form ['especializacion']
        telefono = request.form ['telefono']
        latitud = request.form ['latitud']
        longitud = request.form ['longitud']
        db, c = get_db ()
        c.execute ("INSERT INTO profesional (nombre,especializacion,telefono) VALUES (%s,%s,%s)",(
            nombre,especialidad,telefono
        ))
        profesional_id = c.lastrowid 
        c.execute ("INSERT INTO ubicacion (latitud,longitud,profesional_id) VALUES (%s,%s,%s)",(
            latitud,longitud,profesional_id
        ))
        db.commit ()
        flash ("Usuario agregado con exito")
        return redirect (url_for('admin.Admin_Inicio'))
    return render_template ("Admin/agregar_pro.html")


@bp.route ("/api/obtener_profesionales")
def ver_profesionales ():
    db, c = get_db ()
    c.execute ('''
        SELECT profesional.nombre, profesional.especializacion, profesional.telefono, 
               ubicacion.latitud, ubicacion.longitud
        FROM profesional
        INNER JOIN ubicacion ON profesional.id = ubicacion.profesional_id
    ''')
    profesionales = c.fetchall ()
    return jsonify (profesionales)

@bp.route("/actualizar_profesional/<int:id>", methods=["POST", "GET"])
def actualizar_profesionales(id):
    db, c = get_db()
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        especialización = request.form['especializacion']
        telefono = request.form['telefono']
        latitud = request.form['latitud']
        longitud = request.form['longitud']
        
        # Actualizar la tabla `profesional`
        c.execute('''
            UPDATE profesional 
            SET nombre = %s, especializacion = %s, telefono = %s 
            WHERE id = %s
        ''', (nombre, especialización, telefono, id))
        
        # Actualizar la tabla `ubicacion`
        c.execute('''
            UPDATE ubicacion 
            SET latitud = %s, longitud = %s 
            WHERE profesional_id = %s
        ''', (latitud, longitud, id))
        db.commit()
        flash("Usuario y ubicación actualizados con éxito")
        return redirect(url_for("admin.Admin_Inicio"))
    
    c.execute('SELECT * FROM profesional WHERE id = %s', (id,))
    profesional = c.fetchone()
    c.execute('SELECT * FROM ubicacion WHERE profesional_id = %s', (id,))
    ubicacion = c.fetchone()
    
    return render_template("Admin/actualizar_pro.html", profesional=profesional, ubicacion=ubicacion)



@bp.route("/eliminar_profesional/<int:id>", methods=['POST'])
def eliminar_profesional(id):
    db, c = get_db()
    c.execute ("DELETE FROM ubicacion WHERE profesional_id = %s",(id,))
    c.execute("DELETE FROM profesional WHERE id = %s", (id,))
    db.commit()
    flash("Profesional eliminado con éxito")
=======
from flask import (
    render_template,flash,request,url_for, Blueprint, g,jsonify,redirect
)
from app.db import get_db
from app.auth import login_required,role_required

bp = Blueprint ('admin',__name__)

@login_required
@role_required ("Administrador")
@bp.route ('/administrador')
def Admin_Inicio ():
    return render_template ("Admin/vista_admin.html")

@bp.route ('/ver_profesionales')
@role_required ('Administrador')
def ver_profesional ():
    db , c = get_db ()
    c.execute ('''
        SELECT profesional.id, profesional.nombre, profesional.especializacion, profesional.telefono, 
               ubicacion.latitud, ubicacion.longitud, profesional.email
        FROM profesional
        INNER JOIN ubicacion ON profesional.id = ubicacion.profesional_id
    ''')
    profesionales = c.fetchall ()
    return render_template ('Admin/ver_profesionales.html',profesionales=profesionales)

@bp.route ('/crear_profesional',methods = ["POST","GET"])
@login_required
def agregar_profesional ():
    if request.method == "POST":
        nombre = request.form ['nombre']
        especialidad = request.form ['especializacion']
        telefono = request.form ['telefono']
        latitud = request.form ['latitud']
        longitud = request.form ['longitud']
        db, c = get_db ()
        c.execute ("INSERT INTO profesional (nombre,especializacion,telefono) VALUES (%s,%s,%s)",(
            nombre,especialidad,telefono
        ))
        profesional_id = c.lastrowid 
        c.execute ("INSERT INTO ubicacion (latitud,longitud,profesional_id) VALUES (%s,%s,%s)",(
            latitud,longitud,profesional_id
        ))
        db.commit ()
        flash ("Usuario agregado con exito")
        return redirect (url_for('admin.Admin_Inicio'))
    return render_template ("Admin/agregar_pro.html")


@bp.route ("/api/obtener_profesionales")
def ver_profesionales ():
    db, c = get_db ()
    c.execute ('''
        SELECT profesional.nombre, profesional.especializacion, profesional.telefono, 
               ubicacion.latitud, ubicacion.longitud
        FROM profesional
        INNER JOIN ubicacion ON profesional.id = ubicacion.profesional_id
    ''')
    profesionales = c.fetchall ()
    return jsonify (profesionales)

@bp.route("/actualizar_profesional/<int:id>", methods=["POST", "GET"])
def actualizar_profesionales(id):
    db, c = get_db()
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        especialización = request.form['especializacion']
        telefono = request.form['telefono']
        latitud = request.form['latitud']
        longitud = request.form['longitud']
        
        # Actualizar la tabla `profesional`
        c.execute('''
            UPDATE profesional 
            SET nombre = %s, especializacion = %s, telefono = %s 
            WHERE id = %s
        ''', (nombre, especialización, telefono, id))
        
        # Actualizar la tabla `ubicacion`
        c.execute('''
            UPDATE ubicacion 
            SET latitud = %s, longitud = %s 
            WHERE profesional_id = %s
        ''', (latitud, longitud, id))
        db.commit()
        flash("Usuario y ubicación actualizados con éxito")
        return redirect(url_for("admin.Admin_Inicio"))
    
    c.execute('SELECT * FROM profesional WHERE id = %s', (id,))
    profesional = c.fetchone()
    c.execute('SELECT * FROM ubicacion WHERE profesional_id = %s', (id,))
    ubicacion = c.fetchone()
    
    return render_template("Admin/actualizar_pro.html", profesional=profesional, ubicacion=ubicacion)



@bp.route("/eliminar_profesional/<int:id>", methods=['POST'])
def eliminar_profesional(id):
    db, c = get_db()
    c.execute ("DELETE FROM ubicacion WHERE profesional_id = %s",(id,))
    c.execute("DELETE FROM profesional WHERE id = %s", (id,))
    db.commit()
    flash("Profesional eliminado con éxito")
>>>>>>> 58b5dc9cd2df97652abfd36fb01f3263eb421fa0
    return redirect(url_for("admin.ver_profesional"))