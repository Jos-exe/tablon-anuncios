from flask import render_template, request, redirect, url_for, flash, session
from . import bp
from ..extensions import db
from ..models import Anuncio, Categoria
from ..auth.routes import login_requerido


@bp.route("/")
@login_requerido
def listar():
    anuncios = Anuncio.query.order_by(Anuncio.fecha.desc()).all()
    return render_template("anuncios/listar.html", anuncios=anuncios)


@bp.route("/anuncios/nuevo", methods=["GET", "POST"])
@login_requerido
def nuevo():
    categorias = Categoria.query.order_by(Categoria.nombre).all()
    if request.method == "POST":
        a = Anuncio(
            titulo=request.form["titulo"].strip(),
            contenido=request.form["contenido"].strip(),
            categoria_id=int(request.form["categoria_id"]),
            usuario_id=session["usuario_id"],
        )
        db.session.add(a)
        db.session.commit()
        flash("Anuncio registrado")
        return redirect(url_for("anuncios.listar"))
    return render_template("anuncios/form.html", anuncio=None, categorias=categorias)


@bp.route("/anuncios/<int:id>/editar", methods=["GET", "POST"])
@login_requerido
def editar(id):
    anuncio = Anuncio.query.get_or_404(id)
    categorias = Categoria.query.order_by(Categoria.nombre).all()
    if request.method == "POST":
        anuncio.titulo = request.form["titulo"].strip()
        anuncio.contenido = request.form["contenido"].strip()
        anuncio.categoria_id = int(request.form["categoria_id"])
        db.session.commit()
        flash("Anuncio modificado")
        return redirect(url_for("anuncios.listar"))
    return render_template("anuncios/form.html", anuncio=anuncio, categorias=categorias)


@bp.route("/anuncios/<int:id>/eliminar", methods=["POST"])
@login_requerido
def eliminar(id):
    anuncio = Anuncio.query.get_or_404(id)
    db.session.delete(anuncio)
    db.session.commit()
    flash("Anuncio eliminado")
    return redirect(url_for("anuncios.listar"))