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


@bp.route ("/actualizar_profesional/<int:id>",methods= ["POST"])
def actualizar_profesionales (id):
    if request.method == 'POST':
        nombre = request.form ['nombre']
        especialización = request.form ['especilizacion']
        telefono = request.form ['telefono']
        latitud = request.form ['latitud']
        longitud = request.form ['longitud']
        db,c = get_db ()
        c.execute('UPDATE profesional SET nombre = %s, especializacion = %s, telefono = %s, latitud = %s, longitud = %s WHERE id = %s',
                   (nombre, especialización, telefono, latitud,longitud, id))
        db.commit()
        flash ("Usuario Actualizado con exito")
        return redirect (url_for("admin.Admin_Inicio"))
    return render_template ("Admin/agregar_pro.html")

@bp.route ("/eliminar_profesional/<int:id>",methods = ['POST'])
def eliminar_profesional (id):
    db, c = get_db ()
    c.execute ("DELETE FROM profesional WHERE id = %s",(id))
    return redirect(url_for("admin.Admin_Inicio"))