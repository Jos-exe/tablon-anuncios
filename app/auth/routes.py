from functools import wraps
from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from . import bp
from ..models import Usuario

def login_requerido(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if not session.get("usuario_id"):
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorada

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.password_hash, password):
            session["usuario_id"] = usuario.id
            session["usuario_nombre"] = usuario.nombre
            return redirect(url_for("anuncios.listar"))

        flash("Correo o contraseña incorrectos")
    return render_template("login.html")

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))