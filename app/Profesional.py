from flask import (
    render_template,Blueprint,flash, url_for , request , session , g , redirect
)
from app.db import get_db
from app.auth import login_required

bp = Blueprint ("Profesional", __name__)


@bp.route ("/registro_profesionales")
def registro_profesionales ():
    return render_template ("auth/registro_pro.html")

@bp.route ("/profesional",methods = ['GET','POST'])
def registrar_profesional ():
    db,c = get_db ()

    if request.method == 'GET':
        c.execute ("SELECT id, nombre FROM comuna")

        comunas = c.fetchall ()
        return render_template ("registro_pro.html", comunas=comunas)


    if request.method == 'POST':
        usuario = request.form ['usuario']
        nombre = request.form ['nombre']
        email = request.form ['email']
        especialidad = request.form ['especializacion']
        telefono = request.form ['telefono']
        latitud = request.form ['latitud']
        longitud = request.form ['longitud']

        c.execute ("INSERT INTO profesional (nombre,especializacion,telefono) VALUES (%s,%s,%s)",(
            nombre,especialidad,telefono
        ))

        profesional_id = c.lastrowid 


        c.execute ("INSERT INTO ubicacion (latitud,longitud,profesional_id) VALUES (%s,%s,%s)",(
            latitud,longitud,profesional_id
        ))
        
        flash ("Usuario agregado con exito")
        return redirect (url_for('auth.login'))

