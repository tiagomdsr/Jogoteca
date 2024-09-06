from jogoteca import app
from flask import render_template, request, redirect, session, flash, url_for
from models import Usuarios
from helpers import FormularioUsuario
from flask_bcrypt import check_password_hash

@app.route("/login")
def login():
    proxima = request.args.get("proxima") if request.args.get("proxima") is not None else url_for("index")
    form = FormularioUsuario()
    return render_template("login.html", proxima=proxima, form=form)

@app.route("/autenticar", methods=["POST",])
def autenticar():
    form = FormularioUsuario(request.form)
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    senha = check_password_hash(usuario.senha, form.senha.data)
    if usuario and senha:
        session["usuario_logado"] = usuario.nickname
        flash(usuario.nickname + " logado com sucesso!", "alert alert-success")
        proxima_pagina = request.form["proxima"]
        return redirect(proxima_pagina)
    else:
        flash("Usuário ou senha incorretos!", "alert alert-danger")
        return redirect(url_for("login", proxima=request.form["proxima"]))
    
@app.route("/logout")
def logout():
    session["usuario_logado"] = None
    flash("Logout efetuado com sucesso!", "alert alert-success")
    return redirect(url_for("index"))