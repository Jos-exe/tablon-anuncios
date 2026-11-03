from flask import render_template, request, redirect, url_for, flash
from . import bp
from ..extensions import db
from ..models import Categoria
from ..auth.routes import login_requerido

@bp.route("/")
@login_requerido
def listar():
    categorias = Categoria.query.order_by(Categoria.nombre).all()
    return render_template("categorias/listar.html", categorias=categorias)

@bp.route("/nueva", methods=["GET", "POST"])
@login_requerido
def nueva():
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        if Categoria.query.filter_by(nombre=nombre).first():
            flash("Esa categoria ya existe")
        else:
            db.session.add(Categoria(nombre=nombre))
            db.session.commit()
            flash("Categoria registrada")
            return redirect(url_for("categorias.listar"))
    return render_template("categorias/form.html", categoria=None)

@bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_requerido
def editar(id):
    categoria = Categoria.query.get_or_404(id)
    if request.method == "POST":
        categoria.nombre = request.form["nombre"].strip()
        db.session.commit()
        flash("Categoria modificada")
        return redirect(url_for("categorias.listar"))
    return render_template("categorias/form.html", categoria=categoria)

@bp.route("/<int:id>/eliminar", methods=["POST"])
@login_requerido
def eliminar(id):
    categoria = Categoria.query.get_or_404(id)
    if categoria.anuncios:
        flash("No se puede eliminar: la categoria tiene anuncios")
    else:
        db.session.delete(categoria)
        db.session.commit()
        flash("Categoria eliminada")
    return redirect(url_for("categorias.listar"))