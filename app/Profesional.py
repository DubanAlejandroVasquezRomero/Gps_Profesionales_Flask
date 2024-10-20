from flask import (
    render_template,Blueprint,flash, url_for , request , session , g , redirect
)
from app.db import get_db
from app.auth import role_required
from app.auth import login_required
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint ("Profesional", __name__)


@bp.route ("/registro_profesionales")
def registro_profesionales ():
    return render_template ("auth/registro_pro.html")


@bp.route("/profesional", methods=['GET', 'POST'])
def registrar_profesional():
    if request.method == "POST":
        nombre = request.form['nombre']
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        correo = request.form['email']
        rol = request.form['rol']
        especialidad = request.form['especializacion']
        telefono = request.form['telefono']
        latitud = request.form['latitud']
        longitud = request.form['longitud']

        db, c = get_db()

        # Insertar usuario
        c.execute("""
            INSERT INTO usuarios (usuario, contraseña, rol)
            VALUES (%s, %s, %s)
        """, (usuario, generate_password_hash(contraseña), rol))

        id_usuario = c.lastrowid  # Obtener el id del usuario recién creado

        # Insertar profesional
        c.execute("""
            INSERT INTO profesional (nombre, especializacion, telefono, email, id_usuario)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, especialidad, telefono, correo, id_usuario))

        profesional_id = c.lastrowid  # Obtener el id del profesional recién creado

        # Insertar ubicación para el profesional
        c.execute("""
            INSERT INTO ubicacion (latitud, longitud, profesional_id)
            VALUES (%s, %s, %s)
        """, (latitud, longitud, profesional_id))

        # Guardar todos los cambios
        db.commit()

        flash("Usuario y profesional agregados con éxito")
        return redirect(url_for('auth.login'))

@bp.route ("/ver_perfil")
def perfil ():
    db, c = get_db ()
    c.execute ("SELECT usuario, nombre FROM usuarios WHERE ID = %s",(g.user['id'],))
    usuario = c.fetchone ()
    return render_template ("Profesional/perfil.html",usuario=usuario)

@login_required
@role_required ("Especialista")
@bp.route ("/panel_profesional")
def dashboard_profesional ():
    db, c = get_db()
    c.execute("""
        SELECT h.id, h.hora_inicio, h.hora_fin, h.dia
        FROM horarios h
        WHERE h.profesional_id = %s
    """, (g.user['profesional_id'],))  # Usa el profesional_id obtenido
    horarios = c.fetchall()
    return render_template ("Profesional/dashboard.html",horarios=horarios)



    
@bp.route("/crear_horario", methods=['POST', 'GET'])
def crear_horario():
    if request.method == "POST":
        dia = request.form['dia']
        hora_inicio = request.form['hora_inicio']
        hora_fin = request.form['hora_fin']
        profesional_id = g.user['profesional_id']  # Este valor proviene del formulario

        db, c = get_db()

        # Insertamos el horario en la tabla 'horarios', asociándolo al 'profesional_id'
        c.execute("""
            INSERT INTO horarios (dia, hora_inicio, hora_fin, profesional_id)
            VALUES (%s, %s, %s, %s)
        """, (dia, hora_inicio, hora_fin, profesional_id))

        db.commit()  # Guardamos los cambios en la base de datos

        flash("Horario creado con éxito")
        return redirect(url_for('Profesional.dashboard_profesional'))

    return render_template("Profesional/crear_horario.html")




@bp.route("/editar_horario/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("Especialista")
def editar_horario(id):
    db, c = get_db()

    if request.method == "POST":
        dia = request.form["dia"]
        hora_inicio = request.form["hora_inicio"]
        hora_fin = request.form["hora_fin"]

        c.execute("""
            UPDATE horarios SET dia = %s, hora_inicio = %s, hora_fin = %s
            WHERE id = %s AND profesional_id = %s
        """, (dia, hora_inicio, hora_fin, id, g.user["id"]))
        db.commit()

        flash("Horario actualizado con éxito")
        return redirect(url_for("Profesional.dashboard_profesional"))

    c.execute("SELECT * FROM horarios WHERE id = %s AND profesional_id = %s", (id, g.user["id"]))
    horario = c.fetchone()

    return render_template("Profesional/editar_horario.html", horario=horario)


@bp.route("/eliminar_horario/<int:id>", methods=["POST"])
@login_required
@role_required("Especialista")
def eliminar_horario(id):
    db, c = get_db()
    c.execute("DELETE FROM horarios WHERE id = %s AND profesional_id = %s", (id, g.user["id"]))
    db.commit()
    flash("Horario eliminado con éxito")
    return redirect(url_for("Profesional.dashboard_profesional"))


