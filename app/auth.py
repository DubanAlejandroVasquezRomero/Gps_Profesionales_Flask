import functools
from functools import wraps

from flask import (
    Blueprint,render_template, request, redirect,url_for, flash, session, g 
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

bp = Blueprint ('auth',__name__)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        Usuario = request.form['Usuario']
        Nombre = request.form['Nombre']
        Contraseña = request.form['Contraseña']
        Correo = request.form ['Correo']
        db, c = get_db()
        error = None

        c.execute('SELECT id FROM usuarios WHERE usuario = %s', (Usuario,))
        if not Nombre:
            error = 'Nombre es requerido'
        elif not Contraseña:
            error = 'Contraseña es requerida'
        elif c.fetchone() is not None:
            error = 'Usuario {} se encuentra registrado'.format(Nombre)

        if error is None:
            c.execute(
                'INSERT INTO usuarios (Usuario,Nombre,Contraseña,Correo) VALUES (%s, %s, %s)',
                (Usuario,Nombre, Correo,generate_password_hash(Contraseña),)
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('Usuario')
        contraseña = request.form.get('Contraseña')
        db, c = get_db()
        error = None
        c.execute(
            'SELECT * FROM usuarios WHERE usuario = %s', (usuario,)
        )
        user = c.fetchone()

        if user is None:
            error = 'Usuario y/o contraseña inválida'
        elif not check_password_hash(user['contraseña'], contraseña):
            error = 'Usuario y/o contraseña inválida'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['user_role'] = user['rol']
            if user['rol'] == 'Administrador':
                return redirect(url_for('admin.Admin_Inicio'))
            else:
                return redirect(url_for('Usuario.inicio'))

        
        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def login_logged_in_user ():
    user_id = session.get ('user_id')

    if user_id is None:
        g.user = None
    else:
        db,c = get_db ()
        c.execute ('SELECT * FROM usuarios WHERE ID = %s',(user_id,))
        g.user = c.fetchone()

@bp.route ('/logout')
def logout ():
    session.clear ()
    return redirect (url_for('auth.login'))

def role_required(role):
    def decorator(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if g.user is None or g.user['rol'] != role:
                return redirect(url_for('auth.login'))
            return view(**kwargs)
        return wrapped_view
    return decorator

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes estar logueado para acceder a esta página.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
