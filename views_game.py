from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app, db
from models import Jogos
from helpers import recupera_imagem, deleta_arquivo, FormularioJogo
import time

@app.route("/")
def index():
    lista_jogos = Jogos.query.order_by(Jogos.id)

    lista_jogos_com_imagem = []
    for jogo in lista_jogos:
        capa_jogo = recupera_imagem(jogo.id)
        lista_jogos_com_imagem.append({
            "id":jogo.id,
            "nome":jogo.nome,
            "categoria":jogo.categoria,
            "console":jogo.console,
            "imagem":capa_jogo
        })

    return render_template("lista.html", titulo="Jogos", jogos=lista_jogos_com_imagem)

@app.route("/novo")
def novo():
    if "usuario_logado" not in session or session["usuario_logado"] == None:
        return redirect(url_for("login", proxima=url_for("novo")))
    form = FormularioJogo()
    return render_template("novo.html", titulo="Novo Jogo", form=form)

@app.route("/criar", methods=["POST",])
def criar():
    form = FormularioJogo(request.form)

    if not form.validate_on_submit():
        return redirect(url_for("novo"))

    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data
    
    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo:
        flash("Jogo já existente!", "alert alert-warning")
        return redirect(url_for("index"))
    
    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()

    arquivo = request.files["arquivo"]
    if arquivo.filename != "":
        upload_path = app.config["UPLOAD_PATH"]
        timestamp = time.time()
        arquivo.save(f"{upload_path}/capa_{novo_jogo.id}-{timestamp}.jpg")

    return redirect(url_for("index"))

@app.route("/editar/<int:id>")
def editar(id):
    if "usuario_logado" not in session or session["usuario_logado"] == None:
        return redirect(url_for("login", proxima=url_for("editar", id=id)))
    jogo = Jogos.query.filter_by(id=id).first()
    form = FormularioJogo()
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console
    capa_jogo = recupera_imagem(id)
    return render_template("editar.html", titulo="Editando Jogo", id=id, capa_jogo=capa_jogo, form=form)

@app.route("/atualizar", methods=["POST",])
def atualizar():
    form = FormularioJogo(request.form)

    if form.validate_on_submit():
        jogo = Jogos.query.filter_by(id=request.form["id"]).first()
        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data
        jogo.console = form.console.data

        db.session.add(jogo)
        db.session.commit()

        arquivo = request.files["arquivo"]
        if arquivo.filename != "":
            upload_path = app.config["UPLOAD_PATH"]
            timestamp = time.time()
            deleta_arquivo(jogo.id)
            arquivo.save(f"{upload_path}/capa_{jogo.id}-{timestamp}.jpg")

    return redirect(url_for("index"))

@app.route("/deletar/<int:id>")
def deletar(id):
    if "usuario_logado" not in session or session["usuario_logado"] == None:
        return redirect(url_for("login"))
    
    jogo = Jogos.query.filter_by(id=id).first()
    nome_jogo = jogo.nome

    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    deleta_arquivo(jogo.id)
    flash(f"O jogo {nome_jogo} foi deletado com sucesso!", "alert alert-success")

    return redirect(url_for("index"))

@app.route("/uploads/<nome_arquivo>")
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)