import os
from datetime import datetime
from functools import wraps
from re import fullmatch

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__, static_folder="static")
app.secret_key = os.environ.get("SECRET_KEY", "chave-dev-membresia-igreja-viva")

PERFIS_USUARIO = ["Administrador", "Pastor", "Secretaria", "Líder", "Financeiro"]
STATUS_USUARIO = ["Ativo", "Bloqueado", "Inativo"]
SITUACOES_MEMBRO = ["Ativo", "Inativo", "Visitante", "Afastado"]
STATUS_MINISTERIO = ["Ativo", "Inativo"]
ESTADOS_CIVIS = ["Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viúvo(a)", "União estável"]
DIAS_REUNIAO = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
TIPOS_HISTORICO = [
    "Batismo",
    "Conversão",
    "Profissão de fé",
    "Transferência de igreja",
    "Desligamento",
    "Discipulado",
    "Acompanhamento pastoral",
    "Pedido de oração",
    "Testemunho",
    "Aconselhamento",
    "Observação espiritual",
]

EMAIL_PATTERN = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
TELEFONE_PATTERN = r"^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$"
CPF_PATTERN = r"^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$"


USUARIOS = [
    {
        "id": 1,
        "nome": "Administrador Igreja Viva",
        "email": "admin@igreja.org",
        "senha_hash": generate_password_hash("admin123"),
        "perfil": "Administrador",
        "status": "Ativo",
        "ultimo_acesso": None,
        "excluido": False,
    },
    {
        "id": 2,
        "nome": "Ana Paula Lima",
        "email": "ana@igreja.org",
        "senha_hash": generate_password_hash("secretaria123"),
        "perfil": "Secretaria",
        "status": "Ativo",
        "ultimo_acesso": "07/05/2026 18:20",
        "excluido": False,
    },
    {
        "id": 3,
        "nome": "Carlos Mendes",
        "email": "carlos@igreja.org",
        "senha_hash": generate_password_hash("financeiro123"),
        "perfil": "Financeiro",
        "status": "Ativo",
        "ultimo_acesso": "07/05/2026 09:45",
        "excluido": False,
    },
    {
        "id": 4,
        "nome": "Fernanda Alves",
        "email": "fernanda@igreja.org",
        "senha_hash": generate_password_hash("pastoral123"),
        "perfil": "Pastor",
        "status": "Ativo",
        "ultimo_acesso": "06/05/2026 21:10",
        "excluido": False,
    },
]

MINISTERIOS = [
    {
        "id": 201,
        "nome": "Louvor",
        "lider": "Débora Martins",
        "dia_reuniao": "Quinta",
        "vagas": 4,
        "status": "Ativo",
        "participantes": [101, 105],
        "atividades": ["Escala do culto de domingo", "Ensaio geral"],
        "excluido": False,
    },
    {
        "id": 202,
        "nome": "Infantil",
        "lider": "Rafaela Costa",
        "dia_reuniao": "Sábado",
        "vagas": 2,
        "status": "Ativo",
        "participantes": [],
        "atividades": ["Classe infantil", "Treinamento de voluntários"],
        "excluido": False,
    },
    {
        "id": 203,
        "nome": "Intercessão",
        "lider": "André Silva",
        "dia_reuniao": "Terça",
        "vagas": 6,
        "status": "Ativo",
        "participantes": [102],
        "atividades": ["Relógio de oração", "Vigília mensal"],
        "excluido": False,
    },
    {
        "id": 204,
        "nome": "Recepção",
        "lider": "Paulo Henrique",
        "dia_reuniao": "Domingo",
        "vagas": 3,
        "status": "Ativo",
        "participantes": [103],
        "atividades": ["Acolhimento no culto", "Integração de visitantes"],
        "excluido": False,
    },
    {
        "id": 205,
        "nome": "Mídia",
        "lider": "Juliana Rocha",
        "dia_reuniao": "Sexta",
        "vagas": 1,
        "status": "Ativo",
        "participantes": [105],
        "atividades": ["Transmissão ao vivo", "Captação de fotos"],
        "excluido": False,
    },
]

CELULAS = [
    {
        "id": 301,
        "nome": "Célula Jardim",
        "lider": "Patrícia Souza",
        "bairro": "Jardim América",
        "dia_reuniao": "Quarta",
        "membros": [101, 102],
        "visitantes": 2,
        "crescimento_percentual": 12,
        "status": "Ativo",
        "reunioes": [
            {"data": "2026-05-06", "presentes": 8, "visitantes": 1},
            {"data": "2026-04-29", "presentes": 7, "visitantes": 1},
        ],
    },
    {
        "id": 302,
        "nome": "Célula Centro",
        "lider": "Ricardo Nunes",
        "bairro": "Centro",
        "dia_reuniao": "Sexta",
        "membros": [103, 105],
        "visitantes": 1,
        "crescimento_percentual": 8,
        "status": "Ativo",
        "reunioes": [
            {"data": "2026-05-01", "presentes": 10, "visitantes": 0},
            {"data": "2026-04-24", "presentes": 9, "visitantes": 1},
        ],
    },
]

MEMBROS = [
    {
        "id": 101,
        "nome": "Marcos Pereira",
        "cpf": "123.456.789-10",
        "email": "marcos@exemplo.com",
        "telefone": "(14) 99911-1001",
        "whatsapp": "(14) 99911-1001",
        "data_nascimento": "1984-03-12",
        "endereco": "Rua das Oliveiras, 120",
        "estado_civil": "Casado(a)",
        "profissao": "Professor",
        "data_entrada": "2018-02-04",
        "data_batismo": "2018-06-10",
        "ministerios": ["Louvor"],
        "celula": "Célula Jardim",
        "cargo_funcao": "Vocal",
        "situacao": "Ativo",
        "excluido": False,
        "historico_espiritual": [
            {
                "id": 1,
                "tipo": "Batismo",
                "data": "2018-06-10",
                "descricao": "Batizado em culto público.",
                "responsavel": "Pastor Daniel",
            }
        ],
    },
    {
        "id": 102,
        "nome": "Patrícia Souza",
        "cpf": "234.567.890-21",
        "email": "patricia@exemplo.com",
        "telefone": "(14) 99822-2002",
        "whatsapp": "(14) 99822-2002",
        "data_nascimento": "1990-08-21",
        "endereco": "Av. Esperança, 45",
        "estado_civil": "Solteiro(a)",
        "profissao": "Enfermeira",
        "data_entrada": "2020-09-13",
        "data_batismo": "2021-01-17",
        "ministerios": ["Intercessão"],
        "celula": "Célula Jardim",
        "cargo_funcao": "Líder de oração",
        "situacao": "Ativo",
        "excluido": False,
        "historico_espiritual": [
            {
                "id": 1,
                "tipo": "Discipulado",
                "data": "2021-02-05",
                "descricao": "Concluiu trilha inicial de discipulado.",
                "responsavel": "Ana Paula Lima",
            }
        ],
    },
    {
        "id": 103,
        "nome": "Ricardo Nunes",
        "cpf": "345.678.901-32",
        "email": "ricardo@exemplo.com",
        "telefone": "(14) 99733-3003",
        "whatsapp": "(14) 99733-3003",
        "data_nascimento": "1978-11-02",
        "endereco": "Rua Central, 900",
        "estado_civil": "Casado(a)",
        "profissao": "Comerciante",
        "data_entrada": "2016-04-24",
        "data_batismo": "2016-08-14",
        "ministerios": ["Recepção"],
        "celula": "Célula Centro",
        "cargo_funcao": "Diácono",
        "situacao": "Ativo",
        "excluido": False,
        "historico_espiritual": [],
    },
    {
        "id": 104,
        "nome": "Sandra Oliveira",
        "cpf": "456.789.012-43",
        "email": "sandra@exemplo.com",
        "telefone": "(14) 99644-4004",
        "whatsapp": "(14) 99644-4004",
        "data_nascimento": "1995-01-30",
        "endereco": "Rua Ipê, 28",
        "estado_civil": "Solteiro(a)",
        "profissao": "Designer",
        "data_entrada": "2026-04-12",
        "data_batismo": "",
        "ministerios": [],
        "celula": "",
        "cargo_funcao": "",
        "situacao": "Visitante",
        "excluido": False,
        "historico_espiritual": [
            {
                "id": 1,
                "tipo": "Acompanhamento pastoral",
                "data": "2026-04-20",
                "descricao": "Primeiro contato após visita ao culto.",
                "responsavel": "Fernanda Alves",
            }
        ],
    },
    {
        "id": 105,
        "nome": "Tiago Ferreira",
        "cpf": "567.890.123-54",
        "email": "tiago@exemplo.com",
        "telefone": "(14) 99555-5005",
        "whatsapp": "(14) 99555-5005",
        "data_nascimento": "1989-12-18",
        "endereco": "Rua dos Cedros, 310",
        "estado_civil": "Casado(a)",
        "profissao": "Analista de sistemas",
        "data_entrada": "2019-07-07",
        "data_batismo": "2019-10-20",
        "ministerios": ["Mídia", "Louvor"],
        "celula": "Célula Centro",
        "cargo_funcao": "Operador de transmissão",
        "situacao": "Afastado",
        "excluido": False,
        "historico_espiritual": [],
    },
]

PRESENCAS = [
    {"id": 401, "data": "2026-05-03", "tipo": "Culto", "referencia": "Culto de celebração", "membro_id": 101, "presente": True},
    {"id": 402, "data": "2026-05-03", "tipo": "Culto", "referencia": "Culto de celebração", "membro_id": 102, "presente": True},
    {"id": 403, "data": "2026-05-03", "tipo": "Culto", "referencia": "Culto de celebração", "membro_id": 105, "presente": False},
    {"id": 404, "data": "2026-05-06", "tipo": "Célula", "referencia": "Célula Jardim", "membro_id": 101, "presente": True},
    {"id": 405, "data": "2026-05-06", "tipo": "Célula", "referencia": "Célula Jardim", "membro_id": 102, "presente": True},
]

EVENTOS = [
    {
        "id": 501,
        "nome": "Conferência de Famílias",
        "data": "2026-06-14",
        "status": "Agendado",
        "inscritos_membros": [101, 102, 103],
        "inscritos_visitantes": ["Sandra Oliveira"],
        "presentes": 0,
    },
    {
        "id": 502,
        "nome": "Treinamento de líderes",
        "data": "2026-05-30",
        "status": "Agendado",
        "inscritos_membros": [102, 103],
        "inscritos_visitantes": [],
        "presentes": 0,
    },
]

LANCAMENTOS_FINANCEIROS = [
    {"id": 601, "data": "2026-05-01", "tipo": "Entrada", "categoria": "Dízimo", "membro_id": 101, "conta": "Conta principal", "valor": 350.00},
    {"id": 602, "data": "2026-05-02", "tipo": "Entrada", "categoria": "Oferta", "membro_id": None, "conta": "Conta principal", "valor": 720.00},
    {"id": 603, "data": "2026-05-04", "tipo": "Saída", "categoria": "Manutenção", "membro_id": None, "conta": "Conta principal", "valor": 180.50},
    {"id": 604, "data": "2026-05-05", "tipo": "Entrada", "categoria": "Contribuição fixa", "membro_id": 103, "conta": "Conta missionária", "valor": 120.00},
]

MENSAGENS = [
    {"id": 701, "canal": "WhatsApp", "destino": "Célula Jardim", "assunto": "Lembrete de reunião", "enviada_em": "2026-05-06 10:00", "status": "Enviada"},
    {"id": 702, "canal": "E-mail", "destino": "Ministério de Louvor", "assunto": "Escala de domingo", "enviada_em": "2026-05-05 15:30", "status": "Enviada"},
    {"id": 703, "canal": "Interna", "destino": "Aniversariantes", "assunto": "Mensagem de aniversário", "enviada_em": "2026-05-01 09:00", "status": "Agendada"},
]

CONFIGURACOES = {
    "nome_igreja": "Igreja Viva",
    "logo": "static/imgs/logo_church.png",
    "backup": "Diário às 02:00",
    "mensagem_aniversario": "Que Deus abençoe sua vida neste novo ciclo!",
    "parametros": "Paginação: 20 registros por página; baixa frequência: menos de 50% no mês",
}


def registros_visiveis(lista):
    return [item for item in lista if not item.get("excluido")]


def encontrar_por_id(lista, item_id, incluir_excluidos=False):
    return next(
        (
            item
            for item in lista
            if item.get("id") == item_id and (incluir_excluidos or not item.get("excluido"))
        ),
        None,
    )


def proximo_id(lista):
    if not lista:
        return 1
    return max(item.get("id", 0) for item in lista) + 1


def obter_opcoes_ministerio():
    return [
        ministerio["nome"]
        for ministerio in registros_visiveis(MINISTERIOS)
        if ministerio["status"] == "Ativo"
    ]


def obter_opcoes_celula():
    return [celula["nome"] for celula in CELULAS if celula["status"] == "Ativo"]


def email_em_uso(email, usuario_id=None):
    email_normalizado = email.lower()
    return any(
        usuario["email"].lower() == email_normalizado
        and usuario["id"] != usuario_id
        and not usuario.get("excluido")
        for usuario in USUARIOS
    )


def validar_email(email):
    return bool(fullmatch(EMAIL_PATTERN, email))


def validar_telefone(telefone):
    return bool(fullmatch(TELEFONE_PATTERN, telefone))


def validar_cpf(cpf):
    return not cpf or bool(fullmatch(CPF_PATTERN, cpf))


def filtrar_registros(registros, termo, campos):
    if not termo:
        return registros

    termo_normalizado = termo.lower()
    return [
        registro
        for registro in registros
        if any(termo_normalizado in str(registro.get(campo, "")).lower() for campo in campos)
    ]


def filtrar_membros(membros, termo="", situacao="", apenas_visitantes=False):
    resultado = registros_visiveis(membros)

    if apenas_visitantes:
        resultado = [membro for membro in resultado if membro["situacao"] == "Visitante"]
    elif situacao:
        resultado = [membro for membro in resultado if membro["situacao"] == situacao]

    if not termo:
        return resultado

    termo_normalizado = termo.lower()
    campos = ["nome", "telefone", "whatsapp", "email", "cpf", "situacao", "celula", "cargo_funcao"]
    return [
        membro
        for membro in resultado
        if any(termo_normalizado in str(membro.get(campo, "")).lower() for campo in campos)
        or any(termo_normalizado in ministerio.lower() for ministerio in membro.get("ministerios", []))
    ]


def obter_usuario_por_email(email):
    return next(
        (
            usuario
            for usuario in USUARIOS
            if usuario["email"].lower() == email.lower() and not usuario.get("excluido")
        ),
        None,
    )


def obter_nome_membro(membro_id):
    membro = encontrar_por_id(MEMBROS, membro_id)
    return membro["nome"] if membro else "Visitante/Não vinculado"


def gerar_metricas():
    membros_visiveis = registros_visiveis(MEMBROS)
    ministerios_visiveis = registros_visiveis(MINISTERIOS)
    entradas = sum(item["valor"] for item in LANCAMENTOS_FINANCEIROS if item["tipo"] == "Entrada")
    saidas = sum(item["valor"] for item in LANCAMENTOS_FINANCEIROS if item["tipo"] == "Saída")
    presentes = sum(1 for presenca in PRESENCAS if presenca["presente"])
    ausentes = sum(1 for presenca in PRESENCAS if not presenca["presente"])

    return {
        "usuarios_ativos": sum(1 for usuario in registros_visiveis(USUARIOS) if usuario["status"] == "Ativo"),
        "membros_ativos": sum(1 for membro in membros_visiveis if membro["situacao"] == "Ativo"),
        "membros_inativos": sum(1 for membro in membros_visiveis if membro["situacao"] == "Inativo"),
        "visitantes": sum(1 for membro in membros_visiveis if membro["situacao"] == "Visitante"),
        "afastados": sum(1 for membro in membros_visiveis if membro["situacao"] == "Afastado"),
        "ministerios": sum(1 for ministerio in ministerios_visiveis if ministerio["status"] == "Ativo"),
        "vagas": sum(ministerio["vagas"] for ministerio in ministerios_visiveis if ministerio["status"] == "Ativo"),
        "celulas": sum(1 for celula in CELULAS if celula["status"] == "Ativo"),
        "eventos": sum(1 for evento in EVENTOS if evento["status"] != "Cancelado"),
        "presencas": presentes,
        "ausencias": ausentes,
        "entradas": entradas,
        "saidas": saidas,
        "saldo": entradas - saidas,
        "mensagens": len(MENSAGENS),
    }


def montar_modulos_dashboard():
    return [
        {"titulo": "Membros", "descricao": "Cadastro, edição, status e histórico espiritual.", "rota": "listar_membros", "valor": gerar_metricas()["membros_ativos"]},
        {"titulo": "Visitantes", "descricao": "Acompanhamento de visitantes e integração.", "rota": "listar_visitantes", "valor": gerar_metricas()["visitantes"]},
        {"titulo": "Ministérios", "descricao": "Líderes, participantes, atividades e relatórios.", "rota": "listar_ministerios", "valor": gerar_metricas()["ministerios"]},
        {"titulo": "Células", "descricao": "Grupos pequenos, reuniões, presença e crescimento.", "rota": "listar_celulas", "valor": gerar_metricas()["celulas"]},
        {"titulo": "Presença", "descricao": "Frequência por culto, evento, célula e membro.", "rota": "listar_presencas", "valor": gerar_metricas()["presencas"]},
        {"titulo": "Eventos", "descricao": "Inscrições, participantes e listas de presença.", "rota": "listar_eventos", "valor": gerar_metricas()["eventos"]},
        {"titulo": "Financeiro", "descricao": "Dízimos, ofertas, contribuições, contas e relatórios.", "rota": "listar_financeiro", "valor": f"R$ {gerar_metricas()['saldo']:.2f}"},
        {"titulo": "Comunicação", "descricao": "WhatsApp, e-mail, listas e histórico de mensagens.", "rota": "listar_comunicacao", "valor": gerar_metricas()["mensagens"]},
        {"titulo": "Relatórios", "descricao": "Indicadores pastorais, financeiros e de crescimento.", "rota": "listar_relatorios", "valor": "10+"},
        {"titulo": "Usuários", "descricao": "Perfis, permissões, bloqueio e auditoria.", "rota": "listar_usuarios", "valor": gerar_metricas()["usuarios_ativos"]},
        {"titulo": "Configurações", "descricao": "Dados da igreja, logo, cargos, backups e parâmetros.", "rota": "listar_configuracoes", "valor": "OK"},
    ]


def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not session.get("usuario_logado"):
            flash("Por favor, realize o login para continuar.", "warning")
            return redirect(url_for("login"))
        return function(*args, **kwargs)

    return wrapper


@app.template_filter("data_br")
def data_br(valor):
    if not valor:
        return "-"
    try:
        return datetime.strptime(valor[:10], "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        return valor


@app.template_filter("moeda_br")
def moeda_br(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


@app.context_processor
def inject_layout_context():
    return {
        "usuario_logado": session.get("usuario_logado"),
        "usuario_nome": session.get("usuario_nome"),
        "usuario_perfil": session.get("usuario_perfil"),
        "metricas_layout": gerar_metricas(),
    }


@app.route("/")
def index():
    return render_template("index.html", metricas=gerar_metricas())


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        metricas=gerar_metricas(),
        modulos=montar_modulos_dashboard(),
        membros_recentes=registros_visiveis(MEMBROS)[-3:],
        eventos=EVENTOS[:3],
    )


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

        usuario = obter_usuario_por_email(email)
        if not usuario or not check_password_hash(usuario["senha_hash"], senha):
            flash("Credenciais inválidas.", "danger")
            return redirect(url_for("login"))

        if usuario["status"] != "Ativo":
            flash("Usuário bloqueado ou inativo. Procure um administrador.", "danger")
            return redirect(url_for("login"))

        usuario["ultimo_acesso"] = datetime.now().strftime("%d/%m/%Y %H:%M")
        session["usuario_logado"] = usuario["email"]
        session["usuario_nome"] = usuario["nome"]
        session["usuario_perfil"] = usuario["perfil"]
        flash("Login realizado com sucesso!", "success")
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/recuperar-senha", methods=["GET", "POST"])
def recuperar_senha():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        if not email or not validar_email(email):
            flash("Informe um e-mail válido para recuperação de senha.", "danger")
            return redirect(url_for("recuperar_senha"))

        flash("Se o e-mail estiver cadastrado, as instruções de recuperação serão enviadas.", "info")
        return redirect(url_for("login"))

    return render_template("recuperar_senha.html")


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

        if email_em_uso(email):
            flash("Já existe um usuário com este e-mail.", "danger")
            return redirect(url_for("cadastro"))

        if len(senha) < 8:
            flash("A senha deve ter pelo menos 8 caracteres.", "danger")
            return redirect(url_for("cadastro"))

        if senha != confirmar_senha:
            flash("A confirmação de senha não confere.", "danger")
            return redirect(url_for("cadastro"))

        USUARIOS.append(
            {
                "id": proximo_id(USUARIOS),
                "nome": nome,
                "email": email,
                "senha_hash": generate_password_hash(senha),
                "perfil": "Secretaria",
                "status": "Ativo",
                "ultimo_acesso": None,
                "excluido": False,
            }
        )
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
    usuarios = filtrar_registros(
        registros_visiveis(USUARIOS),
        busca,
        ["nome", "email", "perfil", "status", "ultimo_acesso"],
    )
    return render_template("usuarios/listar_usuarios.html", usuarios=usuarios, busca=busca, total=len(registros_visiveis(USUARIOS)))


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

        USUARIOS.append(
            {
                "id": proximo_id(USUARIOS),
                "nome": nome,
                "email": email,
                "senha_hash": generate_password_hash("Mudar@123"),
                "perfil": perfil,
                "status": "Ativo",
                "ultimo_acesso": None,
                "excluido": False,
            }
        )
        flash("Usuário cadastrado com sucesso! Senha inicial: Mudar@123", "success")
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

    usuario["status"] = "Inativo"
    usuario["excluido"] = True
    flash("Usuário inativado por exclusão lógica.", "success")
    return redirect(url_for("listar_usuarios"))


@app.route("/membros/listar")
@login_required
def listar_membros():
    busca = request.args.get("q", "").strip()
    situacao = request.args.get("status", "").strip()
    if situacao not in SITUACOES_MEMBRO:
        situacao = ""
    membros = filtrar_membros(MEMBROS, busca, situacao)
    return render_template(
        "membros/listar_membros.html",
        membros=membros,
        busca=busca,
        status_atual=situacao,
        status_opcoes=SITUACOES_MEMBRO,
        total=len(registros_visiveis(MEMBROS)),
        metricas=gerar_metricas(),
        titulo_lista="Membros da igreja",
        descricao_lista="Acompanhe dados pessoais, vínculo ministerial, célula e situação de cada pessoa.",
        novo_label="Novo membro",
        novo_url=url_for("inserir_membro"),
        modo_visitantes=False,
    )


@app.route("/visitantes/listar")
@login_required
def listar_visitantes():
    busca = request.args.get("q", "").strip()
    membros = filtrar_membros(MEMBROS, busca, apenas_visitantes=True)
    return render_template(
        "membros/listar_membros.html",
        membros=membros,
        busca=busca,
        status_atual="Visitante",
        status_opcoes=["Visitante"],
        total=len(membros),
        metricas=gerar_metricas(),
        titulo_lista="Visitantes",
        descricao_lista="Acompanhe visitantes, contatos e encaminhamento para integração.",
        novo_label="Novo visitante",
        novo_url=url_for("inserir_membro", situacao="Visitante"),
        modo_visitantes=True,
    )


def obter_dados_membro_form():
    ministerios_form = request.form.getlist("ministerios")
    ministerio_legado = request.form.get("ministerio", "").strip()
    if ministerio_legado and ministerio_legado not in ministerios_form:
        ministerios_form.append(ministerio_legado)

    ministerios_validos = set(obter_opcoes_ministerio())
    ministerios = [ministerio for ministerio in ministerios_form if ministerio in ministerios_validos]

    return {
        "nome": request.form.get("nome", "").strip(),
        "cpf": request.form.get("cpf", "").strip(),
        "email": request.form.get("email", "").strip().lower(),
        "telefone": request.form.get("telefone", "").strip(),
        "whatsapp": request.form.get("whatsapp", "").strip(),
        "data_nascimento": request.form.get("data_nascimento", "").strip(),
        "endereco": request.form.get("endereco", "").strip(),
        "estado_civil": request.form.get("estado_civil", "").strip(),
        "profissao": request.form.get("profissao", "").strip(),
        "data_entrada": request.form.get("data_entrada", "").strip(),
        "data_batismo": request.form.get("data_batismo", "").strip(),
        "ministerios": ministerios,
        "celula": request.form.get("celula", "").strip(),
        "cargo_funcao": request.form.get("cargo_funcao", "").strip(),
        "situacao": request.form.get("situacao", "Ativo").strip(),
    }


def validar_dados_membro(dados, rota, **kwargs):
    if not dados["nome"] or not dados["telefone"] or not dados["situacao"]:
        flash("Nome, telefone e situação são obrigatórios.", "danger")
        return redirect(url_for(rota, **kwargs))

    if not validar_telefone(dados["telefone"]):
        flash("Informe um telefone válido com DDD.", "danger")
        return redirect(url_for(rota, **kwargs))

    if dados["whatsapp"] and not validar_telefone(dados["whatsapp"]):
        flash("Informe um WhatsApp válido com DDD.", "danger")
        return redirect(url_for(rota, **kwargs))

    if dados["email"] and not validar_email(dados["email"]):
        flash("Informe um e-mail válido.", "danger")
        return redirect(url_for(rota, **kwargs))

    if not validar_cpf(dados["cpf"]):
        flash("Informe um CPF válido.", "danger")
        return redirect(url_for(rota, **kwargs))

    if dados["situacao"] not in SITUACOES_MEMBRO:
        flash("Selecione uma situação válida.", "danger")
        return redirect(url_for(rota, **kwargs))

    if dados["estado_civil"] and dados["estado_civil"] not in ESTADOS_CIVIS:
        flash("Selecione um estado civil válido.", "danger")
        return redirect(url_for(rota, **kwargs))

    if dados["celula"] and dados["celula"] not in obter_opcoes_celula():
        flash("Selecione uma célula válida.", "danger")
        return redirect(url_for(rota, **kwargs))

    return None


@app.route("/membros/inserir", methods=["GET", "POST"])
@login_required
def inserir_membro():
    situacao_padrao = request.args.get("situacao", "Ativo")
    if situacao_padrao not in SITUACOES_MEMBRO:
        situacao_padrao = "Ativo"

    if request.method == "POST":
        dados = obter_dados_membro_form()
        erro = validar_dados_membro(dados, "inserir_membro", situacao=situacao_padrao)
        if erro:
            return erro

        MEMBROS.append(
            {
                "id": proximo_id(MEMBROS),
                **dados,
                "historico_espiritual": [],
                "excluido": False,
            }
        )
        flash("Pessoa cadastrada com sucesso!", "success")
        return redirect(url_for("listar_visitantes" if dados["situacao"] == "Visitante" else "listar_membros"))

    return render_template(
        "membros/inserir_membro.html",
        ministerios=obter_opcoes_ministerio(),
        celulas=obter_opcoes_celula(),
        situacoes=SITUACOES_MEMBRO,
        situacao_padrao=situacao_padrao,
        estados_civis=ESTADOS_CIVIS,
    )


@app.route("/membros/editar/<int:membro_id>", methods=["GET", "POST"])
@login_required
def editar_membro(membro_id):
    membro = encontrar_por_id(MEMBROS, membro_id)
    if not membro:
        flash("Membro não encontrado.", "danger")
        return redirect(url_for("listar_membros"))

    if request.method == "POST":
        dados = obter_dados_membro_form()
        erro = validar_dados_membro(dados, "editar_membro", membro_id=membro_id)
        if erro:
            return erro

        membro.update(dados)
        flash("Cadastro atualizado com sucesso.", "success")
        return redirect(url_for("listar_visitantes" if membro["situacao"] == "Visitante" else "listar_membros"))

    return render_template(
        "membros/editar_membro.html",
        membro=membro,
        ministerios=obter_opcoes_ministerio(),
        celulas=obter_opcoes_celula(),
        situacoes=SITUACOES_MEMBRO,
        estados_civis=ESTADOS_CIVIS,
    )


@app.route("/membros/inativar/<int:membro_id>")
@login_required
def inativar_membro(membro_id):
    membro = encontrar_por_id(MEMBROS, membro_id)
    if not membro:
        flash("Membro não encontrado.", "danger")
        return redirect(url_for("listar_membros"))

    membro["situacao"] = "Inativo"
    flash("Membro inativado com sucesso.", "success")
    return redirect(url_for("listar_membros"))


@app.route("/membros/excluir/<int:membro_id>")
@login_required
def excluir_membro(membro_id):
    membro = encontrar_por_id(MEMBROS, membro_id)
    if not membro:
        flash("Membro não encontrado.", "danger")
        return redirect(url_for("listar_membros"))

    membro["situacao"] = "Inativo"
    membro["excluido"] = True
    flash("Membro removido da listagem por exclusão lógica.", "success")
    return redirect(url_for("listar_membros"))


@app.route("/membros/historico/<int:membro_id>", methods=["GET", "POST"])
@login_required
def historico_membro(membro_id):
    membro = encontrar_por_id(MEMBROS, membro_id)
    if not membro:
        flash("Membro não encontrado.", "danger")
        return redirect(url_for("listar_membros"))

    if request.method == "POST":
        tipo = request.form.get("tipo", "").strip()
        data = request.form.get("data", "").strip()
        descricao = request.form.get("descricao", "").strip()

        if tipo not in TIPOS_HISTORICO or not data or not descricao:
            flash("Tipo, data e descrição são obrigatórios para registrar o histórico.", "danger")
            return redirect(url_for("historico_membro", membro_id=membro_id))

        membro.setdefault("historico_espiritual", []).append(
            {
                "id": proximo_id(membro.get("historico_espiritual", [])),
                "tipo": tipo,
                "data": data,
                "descricao": descricao,
                "responsavel": session.get("usuario_nome") or session.get("usuario_logado"),
            }
        )
        flash("Histórico espiritual registrado com sucesso.", "success")
        return redirect(url_for("historico_membro", membro_id=membro_id))

    return render_template("membros/historico_membro.html", membro=membro, tipos_historico=TIPOS_HISTORICO)


@app.route("/ministerios/listar")
@login_required
def listar_ministerios():
    busca = request.args.get("q", "").strip()
    status = request.args.get("status", "").strip()
    ministerios = registros_visiveis(MINISTERIOS)
    if status in STATUS_MINISTERIO:
        ministerios = [ministerio for ministerio in ministerios if ministerio["status"] == status]
    ministerios = filtrar_registros(ministerios, busca, ["nome", "lider", "dia_reuniao", "vagas", "status"])
    return render_template(
        "ministerios/listar_ministerios.html",
        ministerios=ministerios,
        busca=busca,
        status_atual=status,
        status_opcoes=STATUS_MINISTERIO,
        total=len(registros_visiveis(MINISTERIOS)),
        metricas=gerar_metricas(),
    )


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

        MINISTERIOS.append(
            {
                "id": proximo_id(MINISTERIOS),
                "nome": nome,
                "lider": lider,
                "dia_reuniao": dia_reuniao,
                "vagas": vagas,
                "status": "Ativo",
                "participantes": [],
                "atividades": [],
                "excluido": False,
            }
        )
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
        status = request.form.get("status", "Ativo").strip()

        if not nome or not lider or not dia_reuniao or not vagas_raw:
            flash("Preencha todos os campos.", "danger")
            return redirect(url_for("editar_ministerio", ministerio_id=ministerio_id))

        try:
            vagas = int(vagas_raw)
        except ValueError:
            flash("Informe uma quantidade de vagas válida.", "danger")
            return redirect(url_for("editar_ministerio", ministerio_id=ministerio_id))

        if dia_reuniao not in DIAS_REUNIAO or vagas < 0 or status not in STATUS_MINISTERIO:
            flash("Revise os dados informados antes de salvar.", "danger")
            return redirect(url_for("editar_ministerio", ministerio_id=ministerio_id))

        ministerio.update({"nome": nome, "lider": lider, "dia_reuniao": dia_reuniao, "vagas": vagas, "status": status})
        flash("Ministério atualizado com sucesso.", "success")
        return redirect(url_for("listar_ministerios"))

    return render_template("ministerios/editar_ministerio.html", ministerio=ministerio, dias=DIAS_REUNIAO, status_opcoes=STATUS_MINISTERIO)


@app.route("/ministerios/excluir/<int:ministerio_id>")
@login_required
def excluir_ministerio(ministerio_id):
    ministerio = encontrar_por_id(MINISTERIOS, ministerio_id)
    if not ministerio:
        flash("Ministério não encontrado.", "danger")
        return redirect(url_for("listar_ministerios"))

    ministerio["status"] = "Inativo"
    ministerio["excluido"] = True
    flash("Ministério inativado por exclusão lógica.", "success")
    return redirect(url_for("listar_ministerios"))


@app.route("/celulas/listar")
@login_required
def listar_celulas():
    linhas = [
        [
            f"#{celula['id']}",
            celula["nome"],
            celula["lider"],
            celula["bairro"],
            celula["dia_reuniao"],
            len(celula["membros"]),
            celula["visitantes"],
            f"{celula['crescimento_percentual']}%",
        ]
        for celula in CELULAS
    ]
    return render_template(
        "modulos/resumo.html",
        titulo="Células e grupos pequenos",
        subtitulo="Controle líderes, membros vinculados, reuniões, presença, visitantes e crescimento.",
        cards=[
            {"label": "Células ativas", "valor": gerar_metricas()["celulas"]},
            {"label": "Membros vinculados", "valor": sum(len(celula["membros"]) for celula in CELULAS)},
            {"label": "Visitantes em células", "valor": sum(celula["visitantes"] for celula in CELULAS)},
        ],
        cabecalhos=["ID", "Nome", "Líder", "Bairro", "Dia", "Membros", "Visitantes", "Crescimento"],
        linhas=linhas,
    )


@app.route("/presencas/listar")
@login_required
def listar_presencas():
    data = request.args.get("data", "").strip()
    membro_busca = request.args.get("membro", "").strip().lower()
    presencas = PRESENCAS
    if data:
        presencas = [presenca for presenca in presencas if presenca["data"] == data]
    if membro_busca:
        presencas = [
            presenca
            for presenca in presencas
            if membro_busca in obter_nome_membro(presenca["membro_id"]).lower()
        ]

    linhas = [
        [
            f"#{presenca['id']}",
            data_br(presenca["data"]),
            presenca["tipo"],
            presenca["referencia"],
            obter_nome_membro(presenca["membro_id"]),
            "Presente" if presenca["presente"] else "Ausente",
        ]
        for presenca in presencas
    ]
    return render_template(
        "modulos/resumo.html",
        titulo="Controle de presença",
        subtitulo="Registre e filtre presença por culto, evento, célula, data e membro.",
        cards=[
            {"label": "Presenças", "valor": gerar_metricas()["presencas"]},
            {"label": "Ausências", "valor": gerar_metricas()["ausencias"]},
            {"label": "Baixa frequência", "valor": 1},
        ],
        filtros=[
            {"name": "data", "label": "Data", "type": "date", "value": data},
            {"name": "membro", "label": "Membro", "type": "search", "value": membro_busca, "placeholder": "Buscar membro"},
        ],
        cabecalhos=["ID", "Data", "Tipo", "Referência", "Membro", "Status"],
        linhas=linhas,
    )


@app.route("/eventos/listar")
@login_required
def listar_eventos():
    linhas = [
        [
            f"#{evento['id']}",
            evento["nome"],
            data_br(evento["data"]),
            evento["status"],
            len(evento["inscritos_membros"]),
            len(evento["inscritos_visitantes"]),
            evento["presentes"],
        ]
        for evento in EVENTOS
    ]
    return render_template(
        "modulos/resumo.html",
        titulo="Eventos",
        subtitulo="Cadastre eventos, inscrições, visitantes, presença e relatórios de participantes.",
        cards=[
            {"label": "Eventos ativos", "valor": gerar_metricas()["eventos"]},
            {"label": "Membros inscritos", "valor": sum(len(evento["inscritos_membros"]) for evento in EVENTOS)},
            {"label": "Visitantes inscritos", "valor": sum(len(evento["inscritos_visitantes"]) for evento in EVENTOS)},
        ],
        cabecalhos=["ID", "Evento", "Data", "Status", "Membros", "Visitantes", "Presentes"],
        linhas=linhas,
    )


@app.route("/financeiro/listar")
@login_required
def listar_financeiro():
    linhas = [
        [
            f"#{lancamento['id']}",
            data_br(lancamento["data"]),
            lancamento["tipo"],
            lancamento["categoria"],
            obter_nome_membro(lancamento["membro_id"]) if lancamento["membro_id"] else "-",
            lancamento["conta"],
            moeda_br(lancamento["valor"]),
        ]
        for lancamento in LANCAMENTOS_FINANCEIROS
    ]
    return render_template(
        "modulos/resumo.html",
        titulo="Financeiro",
        subtitulo="Controle entradas, saídas, dízimos, ofertas, contribuições, categorias, contas e exportações.",
        cards=[
            {"label": "Entradas", "valor": moeda_br(gerar_metricas()["entradas"])},
            {"label": "Saídas", "valor": moeda_br(gerar_metricas()["saidas"])},
            {"label": "Saldo", "valor": moeda_br(gerar_metricas()["saldo"])},
        ],
        cabecalhos=["ID", "Data", "Tipo", "Categoria", "Membro", "Conta", "Valor"],
        linhas=linhas,
    )


@app.route("/comunicacao/listar")
@login_required
def listar_comunicacao():
    linhas = [
        [
            f"#{mensagem['id']}",
            mensagem["canal"],
            mensagem["destino"],
            mensagem["assunto"],
            mensagem["enviada_em"],
            mensagem["status"],
        ]
        for mensagem in MENSAGENS
    ]
    return render_template(
        "modulos/resumo.html",
        titulo="Comunicação",
        subtitulo="Envie avisos por WhatsApp, e-mail e notificações internas para listas, ministérios e células.",
        cards=[
            {"label": "Mensagens", "valor": len(MENSAGENS)},
            {"label": "Canais", "valor": 3},
            {"label": "Listas", "valor": 4},
        ],
        cabecalhos=["ID", "Canal", "Destino", "Assunto", "Enviado em", "Status"],
        linhas=linhas,
    )


@app.route("/relatorios/listar")
@login_required
def listar_relatorios():
    linhas = [
        ["Membros ativos", "Pessoas", gerar_metricas()["membros_ativos"], "Disponível"],
        ["Membros inativos", "Pessoas", gerar_metricas()["membros_inativos"], "Disponível"],
        ["Visitantes", "Pessoas", gerar_metricas()["visitantes"], "Disponível"],
        ["Aniversariantes", "Pessoas", "Por mês", "Planejado"],
        ["Batizados", "Eclesiástico", "Por período", "Disponível via histórico"],
        ["Novos membros", "Crescimento", "Por período", "Disponível"],
        ["Membros por ministério", "Ministérios", gerar_metricas()["ministerios"], "Disponível"],
        ["Membros por célula", "Células", gerar_metricas()["celulas"], "Disponível"],
        ["Presença", "Frequência", gerar_metricas()["presencas"], "Disponível"],
        ["Financeiro", "Financeiro", moeda_br(gerar_metricas()["saldo"]), "Disponível"],
        ["Crescimento da igreja", "Indicadores", "+8%", "Planejado"],
    ]
    return render_template(
        "modulos/resumo.html",
        titulo="Relatórios",
        subtitulo="Consultas operacionais e pastorais para secretaria, liderança e administração.",
        cards=[
            {"label": "Relatórios mapeados", "valor": len(linhas)},
            {"label": "Disponíveis", "valor": sum(1 for linha in linhas if "Disponível" in linha[3])},
            {"label": "Exportações", "valor": "PDF/Excel"},
        ],
        cabecalhos=["Relatório", "Módulo", "Indicador", "Status"],
        linhas=linhas,
    )


@app.route("/configuracoes/listar")
@login_required
def listar_configuracoes():
    linhas = [
        ["Dados da igreja", CONFIGURACOES["nome_igreja"], "Ativo"],
        ["Logo da igreja", CONFIGURACOES["logo"], "Ativo"],
        ["Cargos e funções", ", ".join(PERFIS_USUARIO), "Ativo"],
        ["Tipos de membro", ", ".join(SITUACOES_MEMBRO), "Ativo"],
        ["Mensagens padrão", CONFIGURACOES["mensagem_aniversario"], "Ativo"],
        ["Backups", CONFIGURACOES["backup"], "Ativo"],
        ["Parâmetros gerais", CONFIGURACOES["parametros"], "Ativo"],
    ]
    return render_template(
        "modulos/resumo.html",
        titulo="Configurações",
        subtitulo="Parâmetros administrativos da igreja, permissões, mensagens, backups e regras gerais.",
        cards=[
            {"label": "Igreja", "valor": CONFIGURACOES["nome_igreja"]},
            {"label": "Backup", "valor": "Diário"},
            {"label": "Perfis", "valor": len(PERFIS_USUARIO)},
        ],
        cabecalhos=["Configuração", "Valor", "Status"],
        linhas=linhas,
    )


@app.route("/sobre-equipe")
def equipe():
    return render_template("sobre_equipe.html")


if __name__ == "__main__":
    app.run(debug=True)
