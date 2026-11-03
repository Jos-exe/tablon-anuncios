from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
from . import bp
from ..extensions import db
from ..models import Usuario
from ..auth.routes import login_requerido


@bp.route("/usuarios")
@login_requerido
def listar():
    usuarios = Usuario.query.order_by(Usuario.nombre).all()
    return render_template("usuarios/listar.html", usuarios=usuarios)


@bp.route("/usuarios/nuevo", methods=["GET", "POST"])
@login_requerido
def nuevo():
    if request.method == "POST":
        email = request.form["email"].strip()
        if Usuario.query.filter_by(email=email).first():
            flash("Ese correo ya está registrado")
        else:
            u = Usuario(
                nombre=request.form["nombre"].strip(),
                email=email,
                password_hash=generate_password_hash(request.form["password"]),
            )
            db.session.add(u)
            db.session.commit()
            flash("Usuario registrado")
            return redirect(url_for("usuarios.listar"))
    return render_template("usuarios/form.html", usuario=None)


@bp.route("/usuarios/<int:id>/editar", methods=["GET", "POST"])
@login_requerido
def editar(id):
    usuario = Usuario.query.get_or_404(id)
    if request.method == "POST":
        usuario.nombre = request.form["nombre"].strip()
        usuario.email = request.form["email"].strip()
        if request.form["password"]:  # solo cambia si escribió una nueva
            usuario.password_hash = generate_password_hash(request.form["password"])
        db.session.commit()
        flash("Usuario modificado")
        return redirect(url_for("usuarios.listar"))
    return render_template("usuarios/form.html", usuario=usuario)


@bp.route("/usuarios/<int:id>/eliminar", methods=["POST"])
@login_requerido
def eliminar(id):
    usuario = Usuario.query.get_or_404(id)
    if usuario.id == session["usuario_id"]:
        flash("No puedes eliminar tu propio usuario")
    elif usuario.anuncios:
        flash("No se puede eliminar: el usuario tiene anuncios")
    else:
        db.session.delete(usuario)
        db.session.commit()
        flash("Usuario eliminado")
    return redirect(url_for("usuarios.listar"))