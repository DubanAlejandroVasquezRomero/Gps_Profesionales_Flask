from flask import (
    render_template,flash,request,url_for, session,Blueprint, g, jsonify
)
from app.db import get_db
from app.auth import login_logged_in_user, login_required

bp = Blueprint ("Usuario",__name__) 


@login_required
@bp.route ("/usuario")
def inicio ():
    return render_template ("usuario/inicio.html")


@bp.route ("/api/obtener_profesionales")
def ver_profesionales ():
    db, c = get_db ()
    c.execute ('''
        SELECT profesional.nombre, profesional.especializacion, profesional.telefono, 
               ubicacion.latitud, ubicacion.longitud
        FROM profesionales
        INNER JOIN ubicacion ON profesional.id = ubicacion.profesional_id
    ''')
    profesionales = c.fetchall ()
    return jsonify (profesionales)


@bp.route ("/ver_perfil")
def VerUsuario ():
    db,c = get_db ()
    c.execute ("SELECT usuario, nombre FROM usuarios WHERE ID = %s",(g.user['id'],))
    usuario = c.fetchone()
    return render_template ("usuario/ver_perfil.html", usuario=usuario)