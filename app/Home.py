from flask import (
    render_template,flash,request,url_for, redirect, session, Blueprint,jsonify
)

from app.db import get_db

bp = Blueprint ('Home',__name__)
@bp.route ('/')
def inicio ():
   return render_template ("home/Home.html")


@bp.route ('/api/obtener_profesionales')
def ver_profesional ():
    db ,c = get_db ()
    c.execute ('''
        SELECT profesional.nombre, profesional.especializacion, profesional.telefono, 
               ubicacion.latitud, ubicacion.longitud
        FROM profesionales
        INNER JOIN ubicacion ON profesional.id = ubicacion.profesional_id
    ''')
    profesionales = c.fetchall ()
    return jsonify (profesionales)