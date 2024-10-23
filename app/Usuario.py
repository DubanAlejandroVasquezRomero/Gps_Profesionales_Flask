<<<<<<< HEAD
from flask import (
    render_template,flash,request,url_for, session,Blueprint, g, jsonify
)
from app.db import get_db
from app.auth import login_logged_in_user, login_required
from datetime import timedelta, datetime

bp = Blueprint ("Usuario",__name__) 


@login_required
@bp.route ("/usuario")
def inicio ():
    return render_template ("usuario/inicio.html")

@bp.route("/api/obtener_profesionales", methods=['GET','POST'])
def ver_profesionales ():
    db, c = get_db ()
    c.execute ('''
    SELECT profesional.nombre, 
       profesional.especializacion, 
       profesional.telefono, 
       ubicacion.latitud, 
       ubicacion.longitud, 
       horarios.hora_inicio, 
       horarios.hora_fin
FROM profesional
INNER JOIN ubicacion ON profesional.id = ubicacion.profesional_id
INNER JOIN horarios ON profesional.id = horarios.profesional_id;
''')
    profesionales = c.fetchall ()
    return jsonify (profesionales)


@bp.route ("/ver_perfil")
def VerUsuario ():
    db,c = get_db ()
    c.execute ("SELECT usuario, nombre FROM usuarios WHERE ID = %s",(g.user['id'],))
    usuario = c.fetchone()
    return render_template ("usuario/ver_perfil.html", usuario=usuario)


@bp.route("/api/obtener_profesionales/<int:profesional_id>", methods=['POST','GET'])
def obtener_horas(profesional_id):
    db, c = get_db()
    c.execute("""
       SELECT profesional.nombre, profesional.telefono, profesional.email, profesional.especializacion, horarios.fecha, horarios.hora_inicio, horarios.hora_fin
        FROM profesional
        INNER JOIN horarios
        ON profesional.id = horarios.profesional_id
        WHERE profesional.id = %s;

    """, (profesional_id,))
    
    horarios = c.fetchone()
    return horarios
=======
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
    FROM profesional
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

@bp.route('/api/obtener_horas/<int:profesional_id>', methods=['POST','GET'])
def obtener_horas(profesional_id):
    db, c = get_db()

    # Selecciona las horas disponibles para el profesional dado
    c.execute("""
        SELECT p.id AS profesional_id, p.nombre, p.especializacion, p.telefono, u.latitud, u.longitud, h.dia, h.hora_inicio, h.hora_fin
    FROM GestionProfesionales.profesional p
    JOIN GestionProfesionales.ubicacion u ON p.id = u.profesional_id
    LEFT JOIN GestionProfesionales.horarios h ON p.id = h.profesional_id
    WHERE p.id = %s;
    """, (profesional_id,))
    
    horarios = c.fetchall()

    # Organiza las horas por días
    result = {}
    for horario in horarios:
        dia = horario['dia']  # Formato de fecha, si es necesario, puedes formatearlo con strftime
        hora = f"{horario['hora_inicio']} - {horario['hora_fin']}"
        
        if dia not in result:
            result[dia] = []
        result[dia].append(hora)

    # Devuelve el resultado como JSON
    return jsonify(result)

>>>>>>> 58b5dc9cd2df97652abfd36fb01f3263eb421fa0
