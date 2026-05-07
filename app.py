import os
from functools import wraps
from re import fullmatch

from flask import Flask, flash, redirect, render_template, request, session, url_for

app = Flask(__name__, static_folder="static")
app.secret_key = os.environ.get("SECRET_KEY", "chave-dev-membresia-igreja-viva")

USUARIOS = [
    {"id": 1, "nome": "Ana Paula Lima", "email": "ana@igreja.org", "perfil": "Secretaria", "status": "Ativo"},
    {"id": 2, "nome": "Carlos Mendes", "email": "carlos@igreja.org", "perfil": "Tesouraria", "status": "Ativo"},
    {"id": 3, "nome": "Fernanda Alves", "email": "fernanda@igreja.org", "perfil": "Pastoral", "status": "Ativo"},
    {"id": 4, "nome": "João Ribeiro", "email": "joao@igreja.org", "perfil": "Comunicação", "status": "Inativo"},
    {"id": 5, "nome": "Luciana Gomes", "email": "luciana@igreja.org", "perfil": "Voluntária", "status": "Ativo"},
]

MEMBROS = [
    {"id": 101, "nome": "Marcos Pereira", "telefone": "(14) 99911-1001", "ministerio": "Louvor", "situacao": "Ativo"},
    {"id": 102, "nome": "Patrícia Souza", "telefone": "(14) 99822-2002", "ministerio": "Intercessão", "situacao": "Ativo"},
    {"id": 103, "nome": "Ricardo Nunes", "telefone": "(14) 99733-3003", "ministerio": "Recepção", "situacao": "Ativo"},
    {"id": 104, "nome": "Sandra Oliveira", "telefone": "(14) 99644-4004", "ministerio": "Infantil", "situacao": "Visitante"},
    {"id": 105, "nome": "Tiago Ferreira", "telefone": "(14) 99555-5005", "ministerio": "Mídia", "situacao": "Ativo"},
]

MINISTERIOS = [
    {"id": 201, "nome": "Louvor", "lider": "Débora Martins", "dia_reuniao": "Quinta", "vagas": 4},
    {"id": 202, "nome": "Infantil", "lider": "Rafaela Costa", "dia_reuniao": "Sábado", "vagas": 2},
    {"id": 203, "nome": "Intercessão", "lider": "André Silva", "dia_reuniao": "Terça", "vagas": 6},
    {"id": 204, "nome": "Recepção", "lider": "Paulo Henrique", "dia_reuniao": "Domingo", "vagas": 3},
    {"id": 205, "nome": "Mídia", "lider": "Juliana Rocha", "dia_reuniao": "Sexta", "vagas": 1},
]

PERFIS_USUARIO = ["Secretaria", "Tesouraria", "Pastoral", "Comunicação", "Voluntária"]
STATUS_USUARIO = ["Ativo", "Inativo"]
SITUACOES_MEMBRO = ["Ativo", "Visitante", "Inativo"]
DIAS_REUNIAO = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
EMAIL_PATTERN = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
TELEFONE_PATTERN = r"^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$"


def encontrar_por_id(lista, item_id):
    return next((item for item in lista if item.get("id") == item_id), None)


def proximo_id(lista):
    if not lista:
        return 1
    return max(item.get("id", 0) for item in lista) + 1


def obter_opcoes_ministerio():
    return [ministerio["nome"] for ministerio in MINISTERIOS]


def email_em_uso(email, usuario_id=None):
    email_normalizado = email.lower()
    return any(
        usuario["email"].lower() == email_normalizado and usuario["id"] != usuario_id
        for usuario in USUARIOS
    )


def validar_email(email):
    return bool(fullmatch(EMAIL_PATTERN, email))


def validar_telefone(telefone):
    return bool(fullmatch(TELEFONE_PATTERN, telefone))


def filtrar_registros(registros, termo, campos):
    if not termo:
        return registros

    termo_normalizado = termo.lower()
    return [
        registro
        for registro in registros
        if any(termo_normalizado in str(registro.get(campo, "")).lower() for campo in campos)
    ]


def gerar_metricas():
    return {
        "usuarios_ativos": sum(1 for usuario in USUARIOS if usuario["status"] == "Ativo"),
        "membros_ativos": sum(1 for membro in MEMBROS if membro["situacao"] == "Ativo"),
        "visitantes": sum(1 for membro in MEMBROS if membro["situacao"] == "Visitante"),
        "ministerios": len(MINISTERIOS),
        "vagas": sum(ministerio["vagas"] for ministerio in MINISTERIOS),
    }


def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not session.get("usuario_logado"):
            flash("Por favor, realize o login para continuar.", "warning")
            return redirect(url_for("login"))
        return function(*args, **kwargs)

    return wrapper


@app.context_processor
def inject_layout_context():
    return {"usuario_logado": session.get("usuario_logado"), "metricas_layout": gerar_metricas()}


@app.route("/")
def index():
    return render_template("index.html", metricas=gerar_metricas())


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "").strip()

        if not email or not senha:
            flash("Por favor, preencha o e-mail e a senha.", "danger")
            return redirect(url_for("login"))

        if not validar_email(email):
            flash("Informe um e-mail válido para acessar o sistema.", "danger")
            return redirect(url_for("login"))

        session["usuario_logado"] = email
        flash("Login realizado com sucesso!", "success")
        return redirect(url_for("listar_membros"))

    return render_template("login.html")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "").strip()
        confirmar_senha = request.form.get("confirma_senha", "").strip()

        if not nome or not email or not senha or not confirmar_senha:
            flash("Por favor, preencha todos os campos.", "danger")
            return redirect(url_for("cadastro"))

        if not validar_email(email):
            flash("Informe um e-mail válido.", "danger")
            return redirect(url_for("cadastro"))

        if len(senha) < 8:
            flash("A senha deve ter pelo menos 8 caracteres.", "danger")
            return redirect(url_for("cadastro"))

        if senha != confirmar_senha:
            flash("A confirmação de senha não confere.", "danger")
            return redirect(url_for("cadastro"))

        flash("Cadastro realizado com sucesso! Agora realize o login para acessar o sistema.", "success")
        return redirect(url_for("login"))

    return render_template("cadastro.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logout realizado com sucesso!", "info")
    return redirect(url_for("login"))


@app.route("/usuarios/listar")
@login_required
def listar_usuarios():
    busca = request.args.get("q", "").strip()
    usuarios = filtrar_registros(USUARIOS, busca, ["nome", "email", "perfil", "status"])
    return render_template("usuarios/listar_usuarios.html", usuarios=usuarios, busca=busca, total=len(USUARIOS))


@app.route("/usuarios/inserir", methods=["GET", "POST"])
@login_required
def inserir_usuario():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        perfil = request.form.get("perfil", "").strip()

        if not nome or not email or not perfil:
            flash("Nome, e-mail e perfil são obrigatórios.", "danger")
            return redirect(url_for("inserir_usuario"))

        if not validar_email(email):
            flash("Informe um e-mail válido.", "danger")
            return redirect(url_for("inserir_usuario"))

        if perfil not in PERFIS_USUARIO:
            flash("Selecione um perfil válido.", "danger")
            return redirect(url_for("inserir_usuario"))

        if email_em_uso(email):
            flash("Já existe um usuário com este e-mail.", "danger")
            return redirect(url_for("inserir_usuario"))

        USUARIOS.append({"id": proximo_id(USUARIOS), "nome": nome, "email": email, "perfil": perfil, "status": "Ativo"})
        flash("Usuário cadastrado com sucesso!", "success")
        return redirect(url_for("listar_usuarios"))

    return render_template("usuarios/inserir_usuario.html", perfis=PERFIS_USUARIO)


@app.route("/usuarios/editar/<int:usuario_id>", methods=["GET", "POST"])
@login_required
def editar_usuario(usuario_id):
    usuario = encontrar_por_id(USUARIOS, usuario_id)
    if not usuario:
        flash("Usuário não encontrado.", "danger")
        return redirect(url_for("listar_usuarios"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        perfil = request.form.get("perfil", "").strip()
        status = request.form.get("status", "").strip()

        if not nome or not email or not perfil or not status:
            flash("Preencha todos os campos.", "danger")
            return redirect(url_for("editar_usuario", usuario_id=usuario_id))

        if not validar_email(email) or perfil not in PERFIS_USUARIO or status not in STATUS_USUARIO:
            flash("Revise os dados informados antes de salvar.", "danger")
            return redirect(url_for("editar_usuario", usuario_id=usuario_id))

        if email_em_uso(email, usuario_id):
            flash("Já existe outro usuário com este e-mail.", "danger")
            return redirect(url_for("editar_usuario", usuario_id=usuario_id))

        usuario.update({"nome": nome, "email": email, "perfil": perfil, "status": status})
        flash("Usuário atualizado com sucesso.", "success")
        return redirect(url_for("listar_usuarios"))

    return render_template("usuarios/editar_usuario.html", usuario=usuario, perfis=PERFIS_USUARIO, status_opcoes=STATUS_USUARIO)


@app.route("/usuarios/excluir/<int:usuario_id>")
@login_required
def excluir_usuario(usuario_id):
    usuario = encontrar_por_id(USUARIOS, usuario_id)
    if not usuario:
        flash("Usuário não encontrado.", "danger")
        return redirect(url_for("listar_usuarios"))

    USUARIOS.remove(usuario)
    flash("Usuário excluído com sucesso.", "success")
    return redirect(url_for("listar_usuarios"))


@app.route("/membros/listar")
@login_required
def listar_membros():
    busca = request.args.get("q", "").strip()
    membros = filtrar_registros(MEMBROS, busca, ["nome", "telefone", "ministerio", "situacao"])
    return render_template("membros/listar_membros.html", membros=membros, busca=busca, total=len(MEMBROS), metricas=gerar_metricas())


@app.route("/membros/inserir", methods=["GET", "POST"])
@login_required
def inserir_membro():
    ministerios = obter_opcoes_ministerio()
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        telefone = request.form.get("telefone", "").strip()
        ministerio = request.form.get("ministerio", "").strip()

        if not nome or not telefone or not ministerio:
            flash("Nome, telefone e ministério são obrigatórios.", "danger")
            return redirect(url_for("inserir_membro"))

        if not validar_telefone(telefone):
            flash("Informe um telefone válido com DDD.", "danger")
            return redirect(url_for("inserir_membro"))

        if ministerio not in ministerios:
            flash("Selecione um ministério válido.", "danger")
            return redirect(url_for("inserir_membro"))

        MEMBROS.append({"id": proximo_id(MEMBROS), "nome": nome, "telefone": telefone, "ministerio": ministerio, "situacao": "Ativo"})
        flash("Membro cadastrado com sucesso!", "success")
        return redirect(url_for("listar_membros"))

    return render_template("membros/inserir_membro.html", ministerios=ministerios)


@app.route("/membros/editar/<int:membro_id>", methods=["GET", "POST"])
@login_required
def editar_membro(membro_id):
    membro = encontrar_por_id(MEMBROS, membro_id)
    if not membro:
        flash("Membro não encontrado.", "danger")
        return redirect(url_for("listar_membros"))

    ministerios = obter_opcoes_ministerio()
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        telefone = request.form.get("telefone", "").strip()
        ministerio = request.form.get("ministerio", "").strip()
        situacao = request.form.get("situacao", "").strip()

        if not nome or not telefone or not ministerio or not situacao:
            flash("Preencha todos os campos.", "danger")
            return redirect(url_for("editar_membro", membro_id=membro_id))

        if not validar_telefone(telefone) or ministerio not in ministerios or situacao not in SITUACOES_MEMBRO:
            flash("Revise os dados informados antes de salvar.", "danger")
            return redirect(url_for("editar_membro", membro_id=membro_id))

        membro.update({"nome": nome, "telefone": telefone, "ministerio": ministerio, "situacao": situacao})
        flash("Membro atualizado com sucesso.", "success")
        return redirect(url_for("listar_membros"))

    return render_template("membros/editar_membro.html", membro=membro, ministerios=ministerios, situacoes=SITUACOES_MEMBRO)


@app.route("/membros/excluir/<int:membro_id>")
@login_required
def excluir_membro(membro_id):
    membro = encontrar_por_id(MEMBROS, membro_id)
    if not membro:
        flash("Membro não encontrado.", "danger")
        return redirect(url_for("listar_membros"))

    MEMBROS.remove(membro)
    flash("Membro excluído com sucesso.", "success")
    return redirect(url_for("listar_membros"))


@app.route("/ministerios/listar")
@login_required
def listar_ministerios():
    busca = request.args.get("q", "").strip()
    ministerios = filtrar_registros(MINISTERIOS, busca, ["nome", "lider", "dia_reuniao", "vagas"])
    return render_template("ministerios/listar_ministerios.html", ministerios=ministerios, busca=busca, total=len(MINISTERIOS), metricas=gerar_metricas())


@app.route("/ministerios/inserir", methods=["GET", "POST"])
@login_required
def inserir_ministerio():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        lider = request.form.get("lider", "").strip()
        dia_reuniao = request.form.get("dia_reuniao", "").strip()
        vagas_raw = request.form.get("vagas", "0").strip()

        if not nome or not lider or not dia_reuniao or not vagas_raw:
            flash("Nome, líder, dia de reunião e vagas são obrigatórios.", "danger")
            return redirect(url_for("inserir_ministerio"))

        if dia_reuniao not in DIAS_REUNIAO:
            flash("Selecione um dia de reunião válido.", "danger")
            return redirect(url_for("inserir_ministerio"))

        try:
            vagas = int(vagas_raw)
        except ValueError:
            flash("Informe uma quantidade de vagas válida.", "danger")
            return redirect(url_for("inserir_ministerio"))

        if vagas < 0:
            flash("Vagas não pode ser negativo.", "danger")
            return redirect(url_for("inserir_ministerio"))

        MINISTERIOS.append({"id": proximo_id(MINISTERIOS), "nome": nome, "lider": lider, "dia_reuniao": dia_reuniao, "vagas": vagas})
        flash("Ministério cadastrado com sucesso!", "success")
        return redirect(url_for("listar_ministerios"))

    return render_template("ministerios/inserir_ministerio.html", dias=DIAS_REUNIAO)


@app.route("/ministerios/editar/<int:ministerio_id>", methods=["GET", "POST"])
@login_required
def editar_ministerio(ministerio_id):
    ministerio = encontrar_por_id(MINISTERIOS, ministerio_id)
    if not ministerio:
        flash("Ministério não encontrado.", "danger")
        return redirect(url_for("listar_ministerios"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        lider = request.form.get("lider", "").strip()
        dia_reuniao = request.form.get("dia_reuniao", "").strip()
        vagas_raw = request.form.get("vagas", "0").strip()

        if not nome or not lider or not dia_reuniao or not vagas_raw:
            flash("Preencha todos os campos.", "danger")
            return redirect(url_for("editar_ministerio", ministerio_id=ministerio_id))

        try:
            vagas = int(vagas_raw)
        except ValueError:
            flash("Informe uma quantidade de vagas válida.", "danger")
            return redirect(url_for("editar_ministerio", ministerio_id=ministerio_id))

        if dia_reuniao not in DIAS_REUNIAO or vagas < 0:
            flash("Revise os dados informados antes de salvar.", "danger")
            return redirect(url_for("editar_ministerio", ministerio_id=ministerio_id))

        ministerio.update({"nome": nome, "lider": lider, "dia_reuniao": dia_reuniao, "vagas": vagas})
        flash("Ministério atualizado com sucesso.", "success")
        return redirect(url_for("listar_ministerios"))

    return render_template("ministerios/editar_ministerio.html", ministerio=ministerio, dias=DIAS_REUNIAO)


@app.route("/ministerios/excluir/<int:ministerio_id>")
@login_required
def excluir_ministerio(ministerio_id):
    ministerio = encontrar_por_id(MINISTERIOS, ministerio_id)
    if not ministerio:
        flash("Ministério não encontrado.", "danger")
        return redirect(url_for("listar_ministerios"))

    MINISTERIOS.remove(ministerio)
    flash("Ministério excluído com sucesso.", "success")
    return redirect(url_for("listar_ministerios"))


@app.route("/sobre-equipe")
def equipe():
    return render_template("sobre_equipe.html")


if __name__ == "__main__":
    app.run(debug=True)
