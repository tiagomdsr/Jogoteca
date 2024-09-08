from jogoteca import app, db
from flask import render_template, request, redirect, session, flash, url_for
from models import Usuarios
from helpers import FormularioUsuario, FormularioNovoUsuario
from flask_bcrypt import check_password_hash, generate_password_hash

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

@app.route("/cadastro")
def cadastro():
    form = FormularioNovoUsuario()
    return render_template("cadastro.html", form=form)

@app.route("/cadastrar", methods=["POST",])
def cadastrar():
    form = FormularioNovoUsuario(request.form)

    if not form.validate_on_submit():
        return redirect(url_for("cadastro"))

    nome = form.nome.data
    nickname = form.nickname.data
    senha = generate_password_hash(form.senha.data).decode("utf-8")
    
    nickname_escolhido = Usuarios.query.filter_by(nickname=nickname).first()

    if nickname_escolhido:
        flash("Nickname já está em uso!", "alert alert-warning")
        return redirect(url_for("cadastro"))
    
    novo_usuario = Usuarios(nome=nome, nickname=nickname, senha=senha)
    db.session.add(novo_usuario)
    db.session.commit()

    flash(f"Usuário {nickname} cadastrado com sucesso!", "alert alert-success")
    return redirect(url_for("login"))