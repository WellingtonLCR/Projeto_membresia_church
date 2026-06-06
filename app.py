import os
from io import BytesIO
from datetime import date, datetime
from functools import wraps
from re import fullmatch

from flask import Flask, Response, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from db import execute_one, execute_query, get_connection


app = Flask(__name__, static_folder="static")
app.secret_key = os.environ.get("SECRET_KEY", "chave-dev-membresia-igreja-viva")

PERFIS_ADMINISTRATIVOS = ["Administrador", "Pastor", "Secretaria", "Líder", "Financeiro"]
PERFIL_VISITANTE = "Visitante"
PERFIS_USUARIO = PERFIS_ADMINISTRATIVOS + [PERFIL_VISITANTE]
PERFIL_DB = {
    "Administrador": "ADMINISTRADOR",
    "Pastor": "PASTOR",
    "Secretaria": "SECRETARIA",
    "Líder": "LIDER",
    "Financeiro": "FINANCEIRO",
    PERFIL_VISITANTE: "VISITANTE",
}
PERFIL_TELA = {valor: chave for chave, valor in PERFIL_DB.items()}

STATUS_USUARIO = ["Ativo", "Bloqueado", "Inativo"]
SITUACOES_MEMBRO = ["Ativo", "Inativo", "Visitante", "Afastado"]
STATUS_MINISTERIO = ["Ativo", "Inativo"]
STATUS_DOACAO = ["Recebida", "Pendente", "Cancelada"]
TIPOS_DOACAO = ["Dizimo", "Oferta", "Contribuicao", "Campanha", "Missao"]
FORMAS_RECEBIMENTO = ["Dinheiro", "PIX", "Cartao", "Transferencia", "Boleto"]
STATUS_MURAL = ["Rascunho", "Publicado", "Arquivado"]
STATUS_PEDIDO_ORACAO = ["Pendente", "Em oracao", "Respondido", "Arquivado"]
ORACAO_CATEGORIAS = ["Saude", "Familia", "Trabalho", "Vida espiritual", "Outro"]
ORACAO_REACOES = {
    "orando": "Estou orando",
    "amem": "Amém",
    "forca": "Força",
}
ESTADOS_CIVIS = ["Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viúvo(a)", "União estável"]
DIAS_REUNIAO = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
TIPOS_HISTORICO = [
    "Batismo",
    "Conversão",
    "Profissão de fé",
    "Transferência",
    "Desligamento",
    "Discipulado",
    "Acompanhamento pastoral",
    "Pedido de oração",
    "Testemunho",
    "Aconselhamento",
    "Observação",
]

EMAIL_PATTERN = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
TELEFONE_PATTERN = r"^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$"
CPF_PATTERN = r"^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$"
BANNER_EXTENSOES = {"jpg", "jpeg", "png", "webp"}

ROTULOS_TELA = {
    "Dizimo": "Dízimo",
    "Contribuicao": "Contribuição",
    "Missao": "Missão",
    "Cartao": "Cartão",
    "Transferencia": "Transferência",
    "Saida": "Saída",
    "Em oracao": "Em oração",
    "Saude": "Saúde",
    "Familia": "Família",
    "Responsavel": "Responsável",
    "Ministerio": "Ministério",
    "Celula": "Célula",
    "Email": "E-mail",
}

MENU_LATERAL = [
    {
        "itens": [
            {"label": "Dashboard", "rota": "dashboard", "ativos": ["dashboard"]},
        ],
    },
    {
        "titulo": "Financeiro",
        "itens": [
            {"label": "Painel", "rota": "painel_financeiro", "ativos": ["painel_financeiro"]},
            {"label": "Receitas", "rota": "listar_receitas", "ativos": ["listar_receitas"]},
            {"label": "Despesas", "rota": "listar_despesas", "ativos": ["listar_despesas"]},
            {"label": "Doações", "rota": "listar_doacoes", "ativos": ["listar_doacoes", "inserir_doacao"]},
            {
                "label": "Movimentações",
                "rota": "listar_financeiro",
                "ativos": ["listar_financeiro", "inserir_lancamento_financeiro"],
            },
            {"label": "Cadastros", "rota": "cadastros_financeiros", "ativos": ["cadastros_financeiros"]},
            {"label": "Fornecedores", "rota": "listar_fornecedores", "ativos": ["listar_fornecedores", "inserir_fornecedor"]},
        ],
    },
    {
        "titulo": "Pessoas",
        "itens": [
            {"label": "Painel", "rota": "painel_pessoas", "ativos": ["painel_pessoas"]},
            {
                "label": "Membros",
                "rota": "listar_membros",
                "ativos": ["listar_membros", "inserir_membro", "editar_membro", "historico_membro"],
            },
            {"label": "Visitantes", "rota": "listar_visitantes", "ativos": ["listar_visitantes"]},
            {"label": "Aniversários", "rota": "listar_aniversarios", "ativos": ["listar_aniversarios"]},
            {"label": "Famílias", "rota": "listar_familias", "ativos": ["listar_familias", "inserir_familia"]},
        ],
    },
    {
        "titulo": "Ministérios",
        "itens": [
            {"label": "Painel", "rota": "painel_ministerios", "ativos": ["painel_ministerios"]},
            {
                "label": "Gerenciamento",
                "rota": "listar_ministerios",
                "ativos": ["listar_ministerios", "inserir_ministerio", "editar_ministerio"],
            },
        ],
    },
    {
        "titulo": "Células",
        "itens": [
            {"label": "Painel", "rota": "painel_celulas", "ativos": ["painel_celulas"]},
            {"label": "Gerenciamento", "rota": "listar_celulas", "ativos": ["listar_celulas", "inserir_celula"]},
            {"label": "Presença", "rota": "listar_presencas", "ativos": ["listar_presencas", "inserir_presenca"]},
        ],
    },
    {
        "titulo": "Comunicação",
        "itens": [
            {"label": "Painel", "rota": "painel_comunicacao", "ativos": ["painel_comunicacao"]},
            {"label": "Feed", "rota": "listar_mural", "ativos": ["listar_mural", "inserir_mural"]},
            {"label": "Comunicados", "rota": "listar_comunicacao", "ativos": ["listar_comunicacao", "inserir_mensagem"]},
            {"label": "Devocional", "rota": "listar_mural", "ativos": ["listar_mural", "inserir_mural"]},
        ],
    },
    {
        "titulo": "Intercessão",
        "itens": [
            {"label": "Painel", "rota": "painel_intercessao", "ativos": ["painel_intercessao"]},
            {
                "label": "Pedidos de oração",
                "rota": "listar_intercessao",
                "ativos": ["listar_intercessao", "inserir_intercessao"],
            },
            {"label": "Testemunhos", "rota": "listar_testemunhos", "ativos": ["listar_testemunhos"]},
        ],
    },
    {
        "titulo": "Relatórios",
        "itens": [
            {"label": "Indicadores", "rota": "listar_relatorios", "ativos": ["listar_relatorios"]},
        ],
    },
    {
        "titulo": "Configurações",
        "itens": [
            {"label": "Painel", "rota": "listar_configuracoes", "ativos": ["listar_configuracoes"]},
            {"label": "Igreja", "rota": "configuracoes_igreja", "ativos": ["configuracoes_igreja"]},
            {"label": "História", "rota": "configuracoes_historia", "ativos": ["configuracoes_historia"]},
            {"label": "Informações", "rota": "configuracoes_informacoes", "ativos": ["configuracoes_informacoes"]},
            {"label": "Permissões", "rota": "configuracoes_permissoes", "ativos": ["configuracoes_permissoes"]},
            {"label": "Programação", "rota": "configuracoes_programacao", "ativos": ["configuracoes_programacao"]},
            {"label": "App", "rota": "configuracoes_app", "ativos": ["configuracoes_app"]},
            {"label": "Módulos", "rota": "configuracoes_modulos", "ativos": ["configuracoes_modulos"]},
            {"label": "Equipe", "rota": "equipe", "ativos": ["equipe"]},
        ],
    },
]


def validar_email(email):
    return bool(fullmatch(EMAIL_PATTERN, email))


def validar_telefone(telefone):
    return bool(fullmatch(TELEFONE_PATTERN, telefone))


def validar_cpf(cpf):
    return not cpf or bool(fullmatch(CPF_PATTERN, cpf))


def valor_ou_none(valor):
    valor = (valor or "").strip()
    return valor or None


def perfil_para_tela(perfil_db):
    return PERFIL_TELA.get((perfil_db or "").upper(), perfil_db or "Secretaria")


def perfil_para_db(perfil):
    return PERFIL_DB.get(perfil, (perfil or "").upper())


def perfil_eh_visitante(perfil):
    return perfil_para_db(perfil) == "VISITANTE"


def status_usuario(row):
    if row.get("excluido_em") or not row.get("ativo"):
        return "Inativo"
    if row.get("bloqueado"):
        return "Bloqueado"
    return "Ativo"


def aplicar_status_usuario(status):
    return {
        "Ativo": (1, 0),
        "Bloqueado": (1, 1),
        "Inativo": (0, 0),
    }.get(status, (1, 0))


def db_select(sql, params=None):
    try:
        return execute_query(sql, params, fetch=True)
    except Exception as erro:
        app.logger.error("Erro MySQL SELECT: %s", erro)
        return []


def db_one(sql, params=None):
    try:
        return execute_one(sql, params)
    except Exception as erro:
        app.logger.error("Erro MySQL SELECT ONE: %s", erro)
        return None


def db_scalar(sql, params=None, default=0):
    row = db_one(sql, params)
    if not row:
        return default
    return row.get("valor", default) or default


def db_write(sql, params=None):
    return execute_query(sql, params, fetch=False)


def usuario_from_row(row):
    if not row:
        return None
    usuario = dict(row)
    usuario["perfil"] = perfil_para_tela(usuario.get("perfil_db"))
    usuario["status"] = status_usuario(usuario)
    ultimo = usuario.get("ultimo_login_em")
    usuario["ultimo_acesso"] = data_hora_br(ultimo) if ultimo else None
    return usuario


def obter_usuario(usuario_id):
    row = db_one(
        """
        SELECT u.*, p.nome AS perfil_db
        FROM usuarios u
        LEFT JOIN usuario_perfil up ON up.usuario_id = u.id
        LEFT JOIN perfis p ON p.id = up.perfil_id
        WHERE u.id = %s AND u.excluido_em IS NULL
        LIMIT 1
        """,
        (usuario_id,),
    )
    return usuario_from_row(row)


def obter_usuario_por_email(email):
    row = db_one(
        """
        SELECT u.*, p.nome AS perfil_db
        FROM usuarios u
        LEFT JOIN usuario_perfil up ON up.usuario_id = u.id
        LEFT JOIN perfis p ON p.id = up.perfil_id
        WHERE u.email = %s AND u.excluido_em IS NULL
        LIMIT 1
        """,
        (email.lower(),),
    )
    return usuario_from_row(row)


def email_em_uso(email, usuario_id=None):
    sql = "SELECT id FROM usuarios WHERE email = %s AND excluido_em IS NULL"
    params = [email.lower()]
    if usuario_id:
        sql += " AND id <> %s"
        params.append(usuario_id)
    return db_one(sql, params) is not None


def criar_usuario(nome, email, senha, perfil):
    perfil_db = perfil_para_db(perfil)
    with get_connection() as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO usuarios (nome, email, senha_hash, ativo, bloqueado)
                VALUES (%s, %s, %s, 1, 0)
                """,
                (nome, email.lower(), generate_password_hash(senha)),
            )
            usuario_id = cursor.lastrowid
            cursor.execute(
                """
                INSERT INTO usuario_perfil (usuario_id, perfil_id)
                SELECT %s, id FROM perfis WHERE nome = %s
                """,
                (usuario_id, perfil_db),
            )
            connection.commit()
            return usuario_id
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()


def atualizar_usuario(usuario_id, nome, email, perfil, status):
    perfil_db = perfil_para_db(perfil)
    ativo, bloqueado = aplicar_status_usuario(status)
    with get_connection() as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                UPDATE usuarios
                SET nome = %s, email = %s, ativo = %s, bloqueado = %s
                WHERE id = %s AND excluido_em IS NULL
                """,
                (nome, email.lower(), ativo, bloqueado, usuario_id),
            )
            cursor.execute("DELETE FROM usuario_perfil WHERE usuario_id = %s", (usuario_id,))
            cursor.execute(
                """
                INSERT INTO usuario_perfil (usuario_id, perfil_id)
                SELECT %s, id FROM perfis WHERE nome = %s
                """,
                (usuario_id, perfil_db),
            )
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()


def listar_usuarios_db(busca=""):
    sql = """
        SELECT u.*, p.nome AS perfil_db
        FROM usuarios u
        LEFT JOIN usuario_perfil up ON up.usuario_id = u.id
        LEFT JOIN perfis p ON p.id = up.perfil_id
        WHERE u.excluido_em IS NULL
    """
    params = []
    if busca:
        sql += """
            AND (
                u.nome LIKE %s OR u.email LIKE %s OR p.nome LIKE %s
                OR CASE
                    WHEN u.ativo = 0 THEN 'Inativo'
                    WHEN u.bloqueado = 1 THEN 'Bloqueado'
                    ELSE 'Ativo'
                END LIKE %s
            )
        """
        termo = f"%{busca}%"
        params.extend([termo, termo, termo, termo])
    sql += " ORDER BY u.nome"
    return [usuario_from_row(row) for row in db_select(sql, params)]


def obter_ministerios_membro(membro_id):
    rows = db_select(
        """
        SELECT mi.nome
        FROM membro_ministerio mm
        JOIN ministerios mi ON mi.id = mm.ministerio_id
        WHERE mm.membro_id = %s
          AND mm.ativo = 1
          AND mi.excluido_em IS NULL
        ORDER BY mi.nome
        """,
        (membro_id,),
    )
    return [row["nome"] for row in rows]


def obter_historico_membro(membro_id):
    return db_select(
        """
        SELECT h.id,
               h.tipo,
               h.data_registro AS data,
               h.descricao,
               COALESCE(u.nome, 'Sistema') AS responsavel
        FROM historico_espiritual h
        LEFT JOIN usuarios u ON u.id = h.responsavel_usuario_id
        WHERE h.membro_id = %s
        ORDER BY h.data_registro DESC, h.id DESC
        """,
        (membro_id,),
    )


def membro_from_row(row, incluir_historico=False):
    if not row:
        return None
    membro = dict(row)
    membro["situacao"] = membro.pop("status")
    membro["celula"] = membro.get("celula") or ""
    membro["ministerios"] = obter_ministerios_membro(membro["id"])
    if incluir_historico:
        membro["historico_espiritual"] = obter_historico_membro(membro["id"])
    return membro


def obter_membro(membro_id, incluir_historico=False):
    row = db_one(
        """
        SELECT m.*, c.nome AS celula
        FROM membros m
        LEFT JOIN celulas c ON c.id = m.celula_id
        WHERE m.id = %s AND m.excluido_em IS NULL
        LIMIT 1
        """,
        (membro_id,),
    )
    return membro_from_row(row, incluir_historico)


def listar_membros_db(busca="", situacao="", apenas_visitantes=False):
    sql = """
        SELECT DISTINCT m.*, c.nome AS celula
        FROM membros m
        LEFT JOIN celulas c ON c.id = m.celula_id
        LEFT JOIN membro_ministerio mm ON mm.membro_id = m.id AND mm.ativo = 1
        LEFT JOIN ministerios mi ON mi.id = mm.ministerio_id
        WHERE m.excluido_em IS NULL
    """
    params = []
    if apenas_visitantes:
        sql += " AND m.status = 'Visitante'"
    elif situacao:
        sql += " AND m.status = %s"
        params.append(situacao)
    if busca:
        termo = f"%{busca}%"
        sql += """
            AND (
                m.nome LIKE %s OR m.telefone LIKE %s OR m.whatsapp LIKE %s
                OR m.email LIKE %s OR m.cpf LIKE %s OR m.status LIKE %s
                OR c.nome LIKE %s OR m.cargo_funcao LIKE %s OR mi.nome LIKE %s
            )
        """
        params.extend([termo] * 9)
    sql += " ORDER BY m.nome"
    return [membro_from_row(row) for row in db_select(sql, params)]


def obter_opcoes_ministerio():
    rows = db_select(
        """
        SELECT nome
        FROM ministerios
        WHERE ativo = 1 AND excluido_em IS NULL
        ORDER BY nome
        """
    )
    return [row["nome"] for row in rows]


def obter_opcoes_celula():
    rows = db_select(
        """
        SELECT nome
        FROM celulas
        WHERE ativo = 1 AND excluido_em IS NULL
        ORDER BY nome
        """
    )
    return [row["nome"] for row in rows]


def obter_celula_id(nome):
    if not nome:
        return None
    row = db_one(
        "SELECT id FROM celulas WHERE nome = %s AND ativo = 1 AND excluido_em IS NULL",
        (nome,),
    )
    return row["id"] if row else None


def salvar_vinculos_ministerio(cursor, membro_id, ministerios):
    cursor.execute("DELETE FROM membro_ministerio WHERE membro_id = %s", (membro_id,))
    for nome in ministerios:
        cursor.execute(
            """
            INSERT INTO membro_ministerio (membro_id, ministerio_id, ativo)
            SELECT %s, id, 1
            FROM ministerios
            WHERE nome = %s AND ativo = 1 AND excluido_em IS NULL
            """,
            (membro_id, nome),
        )


def obter_dados_membro_form():
    return {
        "nome": request.form.get("nome", "").strip(),
        "cpf": request.form.get("cpf", "").strip(),
        "email": request.form.get("email", "").strip().lower(),
        "telefone": request.form.get("telefone", "").strip(),
        "whatsapp": request.form.get("whatsapp", "").strip(),
        "data_nascimento": valor_ou_none(request.form.get("data_nascimento")),
        "endereco": request.form.get("endereco", "").strip(),
        "estado_civil": request.form.get("estado_civil", "").strip(),
        "profissao": request.form.get("profissao", "").strip(),
        "data_entrada": valor_ou_none(request.form.get("data_entrada")),
        "data_batismo": valor_ou_none(request.form.get("data_batismo")),
        "ministerios": request.form.getlist("ministerios") or request.form.getlist("ministerio"),
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


def inserir_membro_db(dados):
    celula_id = obter_celula_id(dados["celula"])
    with get_connection() as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO membros (
                    nome, cpf, data_nascimento, endereco, telefone, whatsapp,
                    email, estado_civil, profissao, data_entrada, data_batismo,
                    celula_id, cargo_funcao, status
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    dados["nome"],
                    valor_ou_none(dados["cpf"]),
                    dados["data_nascimento"],
                    valor_ou_none(dados["endereco"]),
                    valor_ou_none(dados["telefone"]),
                    valor_ou_none(dados["whatsapp"]),
                    valor_ou_none(dados["email"]),
                    valor_ou_none(dados["estado_civil"]),
                    valor_ou_none(dados["profissao"]),
                    dados["data_entrada"],
                    dados["data_batismo"],
                    celula_id,
                    valor_ou_none(dados["cargo_funcao"]),
                    dados["situacao"],
                ),
            )
            membro_id = cursor.lastrowid
            salvar_vinculos_ministerio(cursor, membro_id, dados["ministerios"])
            connection.commit()
            return membro_id
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()


def atualizar_membro_db(membro_id, dados):
    celula_id = obter_celula_id(dados["celula"])
    with get_connection() as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                UPDATE membros
                SET nome = %s,
                    cpf = %s,
                    data_nascimento = %s,
                    endereco = %s,
                    telefone = %s,
                    whatsapp = %s,
                    email = %s,
                    estado_civil = %s,
                    profissao = %s,
                    data_entrada = %s,
                    data_batismo = %s,
                    celula_id = %s,
                    cargo_funcao = %s,
                    status = %s
                WHERE id = %s AND excluido_em IS NULL
                """,
                (
                    dados["nome"],
                    valor_ou_none(dados["cpf"]),
                    dados["data_nascimento"],
                    valor_ou_none(dados["endereco"]),
                    valor_ou_none(dados["telefone"]),
                    valor_ou_none(dados["whatsapp"]),
                    valor_ou_none(dados["email"]),
                    valor_ou_none(dados["estado_civil"]),
                    valor_ou_none(dados["profissao"]),
                    dados["data_entrada"],
                    dados["data_batismo"],
                    celula_id,
                    valor_ou_none(dados["cargo_funcao"]),
                    dados["situacao"],
                    membro_id,
                ),
            )
            salvar_vinculos_ministerio(cursor, membro_id, dados["ministerios"])
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()


def obter_nome_membro(membro_id):
    if not membro_id:
        return "Visitante/Não vinculado"
    row = db_one("SELECT nome FROM membros WHERE id = %s AND excluido_em IS NULL", (membro_id,))
    return row["nome"] if row else "Visitante/Não vinculado"


def listar_membros_select():
    return db_select(
        """
        SELECT id, nome
        FROM membros
        WHERE excluido_em IS NULL
        ORDER BY nome
        """
    )


def listar_categorias_financeiras(tipo=None):
    sql = "SELECT id, nome, tipo FROM categorias_financeiras WHERE ativo = 1"
    params = []
    if tipo:
        sql += " AND tipo = %s"
        params.append(tipo)
    sql += " ORDER BY tipo, nome"
    return db_select(sql, params)


def listar_contas_financeiras():
    return db_select(
        """
        SELECT id, nome
        FROM contas_financeiras
        WHERE ativo = 1
        ORDER BY nome
        """
    )


def listar_fornecedores_select():
    return db_select(
        """
        SELECT id, nome
        FROM fornecedores
        WHERE ativo = 1 AND excluido_em IS NULL
        ORDER BY nome
        """
    )


def salvar_upload_imagem(arquivo, subpasta):
    if not arquivo or not arquivo.filename:
        return None

    nome_seguro = secure_filename(arquivo.filename)
    extensao = nome_seguro.rsplit(".", 1)[-1].lower() if "." in nome_seguro else ""
    if extensao not in BANNER_EXTENSOES:
        return None

    pasta = os.path.join(app.static_folder, "imgs", subpasta)
    os.makedirs(pasta, exist_ok=True)
    nome_final = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{nome_seguro}"
    arquivo.save(os.path.join(pasta, nome_final))
    return f"imgs/{subpasta}/{nome_final}"


def salvar_banner_evento(arquivo):
    return salvar_upload_imagem(arquivo, "eventos")


def salvar_imagem_mural(arquivo):
    return salvar_upload_imagem(arquivo, "mural")


def obter_config(chave, padrao=""):
    row = db_one("SELECT valor FROM configuracoes_sistema WHERE chave = %s", (chave,))
    return row["valor"] if row and row.get("valor") is not None else padrao


def salvar_config(chave, valor, descricao):
    db_write(
        """
        INSERT INTO configuracoes_sistema (chave, valor, descricao)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE valor = VALUES(valor), descricao = VALUES(descricao)
        """,
        (chave, valor, descricao),
    )


def obter_igreja():
    igreja = db_one("SELECT * FROM igrejas ORDER BY id LIMIT 1")
    if igreja:
        return igreja
    return {
        "nome": obter_config("igreja.nome", "Igreja Viva"),
        "email": "",
        "telefone": "",
        "endereco": "",
        "logo_path": "static/imgs/logo_church.png",
    }


def montar_grupos_relatorio():
    metricas = gerar_metricas()
    return [
        {
            "modulo": "Pessoas",
            "descricao": "Indicadores de membresia, visitantes, famílias e aniversários.",
            "linhas": [
                ["Membros ativos", metricas["membros_ativos"], "Disponível"],
                ["Membros inativos", metricas["membros_inativos"], "Disponível"],
                ["Visitantes", metricas["visitantes"], "Disponível"],
                ["Famílias", metricas["familias"], "Disponível"],
                [
                    "Aniversariantes do mês",
                    db_scalar(
                        "SELECT COUNT(*) AS valor FROM membros WHERE data_nascimento IS NOT NULL AND excluido_em IS NULL AND MONTH(data_nascimento) = MONTH(CURDATE())"
                    ),
                    "Disponível",
                ],
            ],
        },
        {
            "modulo": "Eclesiástico",
            "descricao": "Acompanhamento espiritual, crescimento e vínculos ministeriais.",
            "linhas": [
                ["Batizados", db_scalar("SELECT COUNT(*) AS valor FROM historico_espiritual WHERE tipo = 'Batismo'"), "Disponível"],
                ["Novos membros", db_scalar("SELECT COUNT(*) AS valor FROM membros WHERE excluido_em IS NULL"), "Disponível"],
                ["Membros por ministério", metricas["ministerios"], "Disponível"],
                ["Membros por célula", metricas["celulas"], "Disponível"],
                ["Presença", metricas["presencas"], "Disponível"],
            ],
        },
        {
            "modulo": "Financeiro",
            "descricao": "Entradas, saídas, fornecedores, doações e saldo consolidado.",
            "linhas": [
                ["Receitas", moeda_br(metricas["entradas"]), "Disponível"],
                ["Despesas", moeda_br(metricas["saidas"]), "Disponível"],
                ["Saldo financeiro", moeda_br(metricas["saldo"]), "Disponível"],
                ["Fornecedores", metricas["fornecedores"], "Disponível"],
                ["Doações", moeda_br(metricas["doacoes_valor"]), "Disponível"],
            ],
        },
        {
            "modulo": "Comunicação",
            "descricao": "Publicações, comunicados, mural e conteúdos exibidos no app.",
            "linhas": [
                ["Mural", metricas["mural"], "Disponível"],
                ["Mensagens", metricas["mensagens"], "Disponível"],
                ["Devocionais", gerar_metricas_app()["devocionais"], "Disponível"],
            ],
        },
        {
            "modulo": "Intercessão",
            "descricao": "Pedidos de oração, respostas e testemunhos públicos.",
            "linhas": [
                ["Pedidos de oração", metricas["pedidos_oracao"], "Disponível"],
                ["Testemunhos", db_scalar("SELECT COUNT(*) AS valor FROM pedidos_oracao WHERE status = 'Respondido'"), "Disponível"],
            ],
        },
    ]


def montar_linhas_relatorio():
    linhas = []
    for grupo in montar_grupos_relatorio():
        linhas.extend([[linha[0], grupo["modulo"], linha[1], linha[2]] for linha in grupo["linhas"]])
    return linhas


def pdf_simples(titulo, grupos):
    conteudo = [
        "Igreja Viva - Sistema de Membresia",
        titulo,
        f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        "",
    ]
    for grupo in grupos:
        conteudo.append(grupo["modulo"].upper())
        conteudo.append("Relatório | Indicador | Status")
        conteudo.extend(" | ".join(str(valor) for valor in linha) for linha in grupo["linhas"])
        conteudo.append("")
    comandos = ["BT /F1 10 Tf 50 790 Td 13 TL"]
    for linha in conteudo:
        texto = linha[:95].replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        comandos.append(f"({texto}) Tj T*")
    comandos.append("ET")
    stream = "\n".join(comandos)
    objetos = [
        b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n",
        b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n",
        b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj\n",
        b"4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n",
    ]
    stream_bytes = stream.encode("latin-1", errors="replace")
    objetos.append(
        f"5 0 obj << /Length {len(stream_bytes)} >> stream\n".encode("latin-1")
        + stream_bytes
        + b"\nendstream endobj\n"
    )
    buffer = BytesIO()
    buffer.write(b"%PDF-1.4\n")
    offsets = []
    for objeto in objetos:
        offsets.append(buffer.tell())
        buffer.write(objeto)
    xref = buffer.tell()
    buffer.write(f"xref\n0 {len(objetos) + 1}\n0000000000 65535 f \n".encode("latin-1"))
    for offset in offsets:
        buffer.write(f"{offset:010d} 00000 n \n".encode("latin-1"))
    buffer.write(
        f"trailer << /Size {len(objetos) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF".encode("latin-1")
    )
    return buffer.getvalue()


def ministerio_from_row(row):
    ministerio = dict(row)
    ministerio["lider"] = ministerio.get("lider_nome") or ""
    ministerio["status"] = "Ativo" if ministerio.get("ativo") else "Inativo"
    ministerio["participantes"] = [None] * int(ministerio.get("participantes_total") or 0)
    return ministerio


def listar_ministerios_db(busca="", status=""):
    sql = """
        SELECT mi.*,
               COUNT(mm.membro_id) AS participantes_total
        FROM ministerios mi
        LEFT JOIN membro_ministerio mm ON mm.ministerio_id = mi.id AND mm.ativo = 1
        WHERE mi.excluido_em IS NULL
    """
    params = []
    if status == "Ativo":
        sql += " AND mi.ativo = 1"
    elif status == "Inativo":
        sql += " AND mi.ativo = 0"
    if busca:
        termo = f"%{busca}%"
        sql += """
            AND (
                mi.nome LIKE %s OR mi.lider_nome LIKE %s
                OR mi.dia_reuniao LIKE %s OR mi.vagas LIKE %s
                OR CASE WHEN mi.ativo = 1 THEN 'Ativo' ELSE 'Inativo' END LIKE %s
            )
        """
        params.extend([termo] * 5)
    sql += " GROUP BY mi.id ORDER BY mi.nome"
    return [ministerio_from_row(row) for row in db_select(sql, params)]


def obter_ministerio(ministerio_id):
    row = db_one(
        """
        SELECT mi.*,
               COUNT(mm.membro_id) AS participantes_total
        FROM ministerios mi
        LEFT JOIN membro_ministerio mm ON mm.ministerio_id = mi.id AND mm.ativo = 1
        WHERE mi.id = %s AND mi.excluido_em IS NULL
        GROUP BY mi.id
        """,
        (ministerio_id,),
    )
    return ministerio_from_row(row) if row else None


def gerar_metricas():
    entradas = db_scalar(
        "SELECT COALESCE(SUM(valor), 0) AS valor FROM lancamentos_financeiros WHERE tipo = 'Entrada'"
    )
    saidas = db_scalar(
        "SELECT COALESCE(SUM(valor), 0) AS valor FROM lancamentos_financeiros WHERE tipo = 'Saida'"
    )
    total_pessoas = db_scalar(
        "SELECT COUNT(*) AS valor FROM membros WHERE excluido_em IS NULL"
    )
    return {
        "total_pessoas": total_pessoas,
        "usuarios_ativos": db_scalar(
            "SELECT COUNT(*) AS valor FROM usuarios WHERE ativo = 1 AND bloqueado = 0 AND excluido_em IS NULL"
        ),
        "membros_ativos": db_scalar(
            "SELECT COUNT(*) AS valor FROM membros WHERE status = 'Ativo' AND excluido_em IS NULL"
        ),
        "membros_inativos": db_scalar(
            "SELECT COUNT(*) AS valor FROM membros WHERE status = 'Inativo' AND excluido_em IS NULL"
        ),
        "visitantes": db_scalar(
            "SELECT COUNT(*) AS valor FROM membros WHERE status = 'Visitante' AND excluido_em IS NULL"
        ),
        "familias": db_scalar(
            "SELECT COUNT(*) AS valor FROM familias WHERE ativo = 1 AND excluido_em IS NULL"
        ),
        "aniversariantes_mes": db_scalar(
            """
            SELECT COUNT(*) AS valor
            FROM membros
            WHERE data_nascimento IS NOT NULL
              AND excluido_em IS NULL
              AND MONTH(data_nascimento) = MONTH(CURDATE())
            """
        ),
        "afastados": db_scalar(
            "SELECT COUNT(*) AS valor FROM membros WHERE status = 'Afastado' AND excluido_em IS NULL"
        ),
        "ministerios": db_scalar(
            "SELECT COUNT(*) AS valor FROM ministerios WHERE ativo = 1 AND excluido_em IS NULL"
        ),
        "vagas": db_scalar(
            "SELECT COALESCE(SUM(vagas), 0) AS valor FROM ministerios WHERE ativo = 1 AND excluido_em IS NULL"
        ),
        "celulas": db_scalar(
            "SELECT COUNT(*) AS valor FROM celulas WHERE ativo = 1 AND excluido_em IS NULL"
        ),
        "eventos": db_scalar(
            "SELECT COUNT(*) AS valor FROM eventos WHERE status <> 'Cancelado'"
        ),
        "presencas": db_scalar("SELECT COUNT(*) AS valor FROM presencas WHERE presente = 1"),
        "ausencias": db_scalar("SELECT COUNT(*) AS valor FROM presencas WHERE presente = 0"),
        "entradas": entradas,
        "saidas": saidas,
        "saldo": entradas - saidas,
        "mensagens": db_scalar("SELECT COUNT(*) AS valor FROM mensagens"),
        "fornecedores": db_scalar(
            "SELECT COUNT(*) AS valor FROM fornecedores WHERE ativo = 1 AND excluido_em IS NULL"
        ),
        "mural": db_scalar("SELECT COUNT(*) AS valor FROM mural_avisos WHERE status <> 'Arquivado'"),
        "devocionais": db_scalar(
            "SELECT COUNT(*) AS valor FROM mural_avisos WHERE categoria = 'Devocional' AND status = 'Publicado'"
        ),
        "pedidos_oracao": db_scalar("SELECT COUNT(*) AS valor FROM pedidos_oracao WHERE status <> 'Arquivado'"),
        "testemunhos": db_scalar(
            "SELECT COUNT(*) AS valor FROM pedidos_oracao WHERE status = 'Respondido' AND privado = 0"
        ),
        "doacoes": db_scalar("SELECT COUNT(*) AS valor FROM doacoes WHERE status <> 'Cancelada'"),
        "doacoes_valor": db_scalar(
            "SELECT COALESCE(SUM(valor), 0) AS valor FROM doacoes WHERE status = 'Recebida'"
        ),
    }


def montar_pessoas_por_status():
    linhas = db_select(
        """
        SELECT status, COUNT(*) AS total
        FROM membros
        WHERE excluido_em IS NULL
        GROUP BY status
        """
    )
    totais = {linha["status"]: int(linha["total"] or 0) for linha in linhas}
    total = sum(totais.values())
    ordem = ["Ativo", "Visitante", "Afastado", "Inativo"]
    return [
        {
            "label": status,
            "valor": totais.get(status, 0),
            "percentual": round((totais.get(status, 0) / total) * 100) if total else 0,
        }
        for status in ordem
    ]


def contar_interacoes_app(dias):
    return db_scalar(
        """
        SELECT
            (
                SELECT COUNT(*)
                FROM pedidos_oracao
                WHERE criado_em >= DATE_SUB(NOW(), INTERVAL %s DAY)
            )
            +
            (
                SELECT COUNT(*)
                FROM pedido_oracao_reacoes
                WHERE criado_em >= DATE_SUB(NOW(), INTERVAL %s DAY)
            )
            +
            (
                SELECT COUNT(*)
                FROM pedido_oracao_comentarios
                WHERE criado_em >= DATE_SUB(NOW(), INTERVAL %s DAY)
            ) AS valor
        """,
        (dias, dias, dias),
    )


def montar_engajamento_app(total_pessoas):
    referencia = max(int(total_pessoas or 0), 1)
    linhas = []
    for dias in [7, 30]:
        valor = int(contar_interacoes_app(dias) or 0)
        linhas.append(
            {
                "periodo": f"{dias} dias",
                "valor": valor,
                "percentual": min(round((valor / referencia) * 100), 100),
            }
        )
    return linhas


def montar_modulos_dashboard(metricas=None):
    metricas = metricas or gerar_metricas()
    return [
        {"titulo": "Pessoas", "descricao": "Membros, visitantes, famílias e aniversários.", "rota": "painel_pessoas", "valor": metricas["total_pessoas"], "icone": "PE"},
        {"titulo": "Financeiro", "descricao": "Receitas, despesas, doações e movimentações.", "rota": "painel_financeiro", "valor": moeda_br(metricas["saldo"]), "icone": "R$"},
        {"titulo": "Ministérios", "descricao": "Líderes, participantes e relatórios.", "rota": "painel_ministerios", "valor": metricas["ministerios"], "icone": "MI"},
        {"titulo": "Células", "descricao": "Grupos pequenos, presenças e crescimento.", "rota": "painel_celulas", "valor": metricas["celulas"], "icone": "CE"},
        {"titulo": "Eventos", "descricao": "Agenda, inscrições e listas de presença.", "rota": "listar_eventos", "valor": metricas["eventos"], "icone": "AG"},
        {"titulo": "Comunicação", "descricao": "Feed, comunicados, mural e devocional.", "rota": "painel_comunicacao", "valor": metricas["mural"], "icone": "CO"},
        {"titulo": "Intercessão", "descricao": "Pedidos de oração, respostas e testemunhos.", "rota": "painel_intercessao", "valor": metricas["pedidos_oracao"], "icone": "OR"},
        {"titulo": "App do usuário", "descricao": "Frente pública alimentada pelo painel administrativo.", "rota": "app_usuario_inicio", "valor": metricas["testemunhos"], "icone": "AP"},
        {"titulo": "Relatórios", "descricao": "Indicadores pastorais, financeiros e operacionais.", "rota": "listar_relatorios", "valor": "PDF", "icone": "RE"},
        {"titulo": "Configurações", "descricao": "Igreja, programação, app e permissões.", "rota": "listar_configuracoes", "valor": "OK", "icone": "CF"},
    ]


def card(label, valor):
    return {"label": label, "valor": valor}


def atalho(titulo, descricao, rota, valor="Acessar"):
    return {"titulo": titulo, "descricao": descricao, "rota": rota, "valor": valor}


def bloco_lista(titulo, cabecalhos, linhas):
    return {"titulo": titulo, "cabecalhos": cabecalhos, "linhas": linhas}


def linhas_lancamentos(lancamentos):
    return [
        [
            data_br(lancamento.get("data_lancamento")),
            "Saída" if lancamento.get("tipo") == "Saida" else "Entrada",
            lancamento.get("categoria") or "-",
            lancamento.get("conta") or "-",
            lancamento.get("membro") or lancamento.get("fornecedor") or "-",
            moeda_br(lancamento.get("valor")),
        ]
        for lancamento in lancamentos
    ]


def listar_lancamentos_financeiros(tipo=""):
    sql = """
        SELECT l.id, l.data_lancamento, l.tipo, c.nome AS categoria,
               m.nome AS membro, f.nome AS fornecedor, cf.nome AS conta, l.valor
        FROM lancamentos_financeiros l
        JOIN categorias_financeiras c ON c.id = l.categoria_id
        JOIN contas_financeiras cf ON cf.id = l.conta_id
        LEFT JOIN membros m ON m.id = l.membro_id
        LEFT JOIN fornecedores f ON f.id = l.fornecedor_id
        WHERE 1=1
    """
    params = []
    if tipo:
        sql += " AND l.tipo = %s"
        params.append(tipo)
    sql += " ORDER BY l.data_lancamento DESC, l.id DESC"
    return db_select(sql, params)


def renderizar_lancamentos_financeiros(tipo, titulo_lista, descricao_lista):
    return render_template(
        "financeiro/listar_financeiro.html",
        lancamentos=listar_lancamentos_financeiros(tipo),
        metricas=gerar_metricas(),
        titulo_lista=titulo_lista,
        descricao_lista=descricao_lista,
        tipo_atual=tipo,
    )


def renderizar_resumo_configuracao(titulo, subtitulo, cards, cabecalhos, linhas):
    return render_template(
        "modulos/resumo.html",
        titulo=titulo,
        subtitulo=subtitulo,
        cards=cards,
        filtros=[],
        cabecalhos=cabecalhos,
        linhas=linhas,
        acao_url=url_for("listar_configuracoes"),
        acao_label="Editar configurações",
    )


def listar_eventos_publicos(limite=None):
    sql = """
        SELECT id, nome, descricao, data_inicio, data_fim, local, banner_path, status
        FROM eventos
        WHERE status <> 'Cancelado'
        ORDER BY
            CASE WHEN data_inicio >= NOW() THEN 0 ELSE 1 END,
            data_inicio ASC,
            id DESC
    """
    if limite:
        sql += " LIMIT %s"
        return db_select(sql, (limite,))
    return db_select(sql)


def listar_mural_publico(limite=None, devocional=False):
    sql = """
        SELECT id, titulo, categoria, conteudo, imagem_path, publicado_em, criado_em
        FROM mural_avisos
        WHERE status = 'Publicado'
    """
    params = []
    if devocional:
        sql += " AND (categoria LIKE %s OR titulo LIKE %s)"
        params.extend(["%devoc%", "%devoc%"])
    sql += " ORDER BY COALESCE(publicado_em, criado_em) DESC, id DESC"
    if limite:
        sql += " LIMIT %s"
        params.append(limite)
    return db_select(sql, params)


def gerar_metricas_app():
    return {
        "eventos": db_scalar("SELECT COUNT(*) AS valor FROM eventos WHERE status <> 'Cancelado'"),
        "avisos": db_scalar("SELECT COUNT(*) AS valor FROM mural_avisos WHERE status = 'Publicado'"),
        "devocionais": db_scalar(
            """
            SELECT COUNT(*) AS valor
            FROM mural_avisos
            WHERE status = 'Publicado'
              AND (categoria LIKE '%devoc%' OR titulo LIKE '%devoc%')
            """
        ),
        "testemunhos": db_scalar(
            "SELECT COUNT(*) AS valor FROM pedidos_oracao WHERE status = 'Respondido' AND privado = 0"
        ),
        "visitantes": db_scalar("SELECT COUNT(*) AS valor FROM membros WHERE status = 'Visitante' AND excluido_em IS NULL"),
    }


def pedido_oracao_publico_existe(pedido_id):
    return bool(
        db_one(
            """
            SELECT id
            FROM pedidos_oracao
            WHERE id = %s AND status = 'Respondido' AND privado = 0
            LIMIT 1
            """,
            (pedido_id,),
        )
    )


def listar_comentarios_oracao(pedido_ids):
    if not pedido_ids:
        return {}
    placeholders = ", ".join(["%s"] * len(pedido_ids))
    comentarios = db_select(
        f"""
        SELECT pedido_id, autor_nome, comentario, criado_em
        FROM pedido_oracao_comentarios
        WHERE aprovado = 1 AND pedido_id IN ({placeholders})
        ORDER BY criado_em ASC, id ASC
        """,
        pedido_ids,
    )
    por_pedido = {pedido_id: [] for pedido_id in pedido_ids}
    for comentario in comentarios:
        por_pedido.setdefault(comentario["pedido_id"], []).append(comentario)
    return por_pedido


def email_membro_em_uso(email):
    if not email:
        return False
    return bool(
        db_one(
            """
            SELECT id
            FROM membros
            WHERE email = %s AND excluido_em IS NULL
            LIMIT 1
            """,
            (email,),
        )
    )


def cadastrar_visitante_app(nome, email, telefone, whatsapp, interesse, mensagem, senha):
    observacoes = ["Cadastro realizado pelo app do usuário."]
    if interesse:
        observacoes.append(f"Interesse informado: {interesse}.")
    if mensagem:
        observacoes.append(f"Mensagem: {mensagem}")

    with get_connection() as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO membros
                    (nome, telefone, whatsapp, email, status, data_entrada, observacoes)
                VALUES (%s, %s, %s, %s, 'Visitante', %s, %s)
                """,
                (
                    nome,
                    valor_ou_none(telefone),
                    valor_ou_none(whatsapp),
                    email.lower(),
                    date.today(),
                    "\n".join(observacoes),
                ),
            )
            membro_id = cursor.lastrowid
            cursor.execute(
                """
                INSERT IGNORE INTO perfis (nome, descricao)
                VALUES ('VISITANTE', 'Acesso ao app do usuário sem permissões administrativas')
                """
            )
            cursor.execute(
                """
                INSERT INTO usuarios (nome, email, senha_hash, ativo, bloqueado)
                VALUES (%s, %s, %s, 1, 0)
                """,
                (nome, email.lower(), generate_password_hash(senha)),
            )
            usuario_id = cursor.lastrowid
            cursor.execute(
                """
                INSERT INTO usuario_perfil (usuario_id, perfil_id)
                SELECT %s, id FROM perfis WHERE nome = 'VISITANTE'
                """,
                (usuario_id,),
            )
            connection.commit()
            return {"membro_id": membro_id, "usuario_id": usuario_id}
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()


def resumo_texto(valor, tamanho=130):
    valor = (valor or "").strip()
    if len(valor) <= tamanho:
        return valor
    return valor[: tamanho - 3].rstrip() + "..."


def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not session.get("usuario_logado"):
            flash("Por favor, realize o login para continuar.", "warning")
            return redirect(url_for("login"))
        if perfil_eh_visitante(session.get("usuario_perfil")):
            flash("Seu acesso é do app da igreja. A área administrativa é restrita à equipe autorizada.", "warning")
            return redirect(url_for("app_usuario_inicio"))
        return function(*args, **kwargs)

    return wrapper


def data_hora_br(valor):
    if isinstance(valor, datetime):
        return valor.strftime("%d/%m/%Y %H:%M")
    return str(valor)


@app.template_filter("data_br")
def data_br(valor):
    if not valor:
        return "-"
    if isinstance(valor, datetime):
        return valor.strftime("%d/%m/%Y")
    if isinstance(valor, date):
        return valor.strftime("%d/%m/%Y")
    try:
        return datetime.strptime(str(valor)[:10], "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        return valor


@app.template_filter("moeda_br")
def moeda_br(valor):
    return f"R$ {float(valor or 0):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


@app.template_filter("rotulo")
def rotulo_tela(valor):
    return ROTULOS_TELA.get(valor, valor)


@app.context_processor
def inject_layout_context():
    return {
        "usuario_logado": session.get("usuario_logado"),
        "usuario_nome": session.get("usuario_nome"),
        "usuario_perfil": session.get("usuario_perfil"),
        "metricas_layout": gerar_metricas(),
        "menu_lateral": MENU_LATERAL,
    }


@app.route("/")
def index():
    return render_template("index.html", metricas=gerar_metricas())


@app.route("/app")
@app.route("/app/inicio")
def app_usuario_inicio():
    igreja = obter_igreja()
    eventos = listar_eventos_publicos(4)
    feed = listar_mural_publico(4)
    devocionais = listar_mural_publico(1, devocional=True)
    if not devocionais:
        devocionais = feed[:1]
    programacao = [
        ["Domingo", obter_config("programacao.domingo", "Culto de celebração")],
        ["Quarta", obter_config("programacao.quarta", "Encontro de oração e ensino")],
        ["Células", obter_config("programacao.celulas", "Durante a semana, conforme cada bairro")],
    ]
    doacao = obter_config("doacao.mensagem", "Contribua com alegria e acompanhe a secretaria para obter comprovantes.")
    return render_template(
        "app_usuario/inicio.html",
        igreja=igreja,
        eventos=eventos,
        feed=feed,
        devocional=devocionais[0] if devocionais else None,
        metricas=gerar_metricas(),
        metricas_app=gerar_metricas_app(),
        programacao=programacao,
        doacao=doacao,
    )


@app.route("/app/eventos")
def app_usuario_eventos():
    return render_template(
        "app_usuario/eventos.html",
        igreja=obter_igreja(),
        eventos=listar_eventos_publicos(),
    )


@app.route("/app/eventos/<int:evento_id>")
def app_usuario_evento(evento_id):
    evento = db_one(
        """
        SELECT id, nome, descricao, data_inicio, data_fim, local, banner_path, status
        FROM eventos
        WHERE id = %s AND status <> 'Cancelado'
        LIMIT 1
        """,
        (evento_id,),
    )
    if not evento:
        flash("Evento não encontrado ou indisponível.", "warning")
        return redirect(url_for("app_usuario_eventos"))
    return render_template("app_usuario/evento.html", igreja=obter_igreja(), evento=evento)


@app.route("/app/cultos")
def app_usuario_cultos():
    eventos = db_select(
        """
        SELECT id, nome, descricao, data_inicio, data_fim, local, banner_path, status
        FROM eventos
        WHERE status <> 'Cancelado'
          AND (nome LIKE %s OR descricao LIKE %s)
        ORDER BY data_inicio ASC, id DESC
        """,
        ("%cult%", "%cult%"),
    )
    if not eventos:
        eventos = listar_eventos_publicos(8)
    programacao = [
        ["Domingo", obter_config("programacao.domingo", "Culto de celebracao")],
        ["Quarta", obter_config("programacao.quarta", "Encontro de oração e ensino")],
        ["Células", obter_config("programacao.celulas", "Durante a semana, conforme cada bairro")],
    ]
    return render_template(
        "app_usuario/cultos.html",
        igreja=obter_igreja(),
        eventos=eventos,
        programacao=programacao,
    )


@app.route("/app/feed")
def app_usuario_feed():
    return render_template(
        "app_usuario/feed.html",
        igreja=obter_igreja(),
        itens=listar_mural_publico(),
        titulo="Feed",
        subtitulo="Avisos, comunicados e publicacoes da igreja.",
        aba="feed",
    )


@app.route("/app/devocional")
def app_usuario_devocional():
    itens = listar_mural_publico(devocional=True)
    if not itens:
        itens = listar_mural_publico()
    return render_template(
        "app_usuario/feed.html",
        igreja=obter_igreja(),
        itens=itens,
        titulo="Devocional",
        subtitulo="Reflexoes e conteudos publicados pela equipe.",
        aba="devocional",
    )


@app.route("/app/oracao", methods=["GET", "POST"])
def app_usuario_oracao():
    if request.method == "POST":
        solicitante_nome = request.form.get("solicitante_nome", "").strip()
        contato = request.form.get("contato", "").strip()
        categoria = request.form.get("categoria", "").strip()
        pedido = request.form.get("pedido", "").strip()
        privado = 1 if request.form.get("privado") else 0

        if not solicitante_nome or not pedido:
            flash("Informe seu nome e o pedido de oração.", "danger")
            return redirect(url_for("app_usuario_oracao"))

        if categoria and categoria not in ORACAO_CATEGORIAS:
            flash("Selecione uma categoria válida.", "danger")
            return redirect(url_for("app_usuario_oracao"))

        try:
            db_write(
                """
                INSERT INTO pedidos_oracao (solicitante_nome, contato, categoria, pedido, privado)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    solicitante_nome,
                    valor_ou_none(contato),
                    valor_ou_none(categoria),
                    pedido,
                    privado,
                ),
            )
        except Exception as erro:
            app.logger.error("Erro ao registrar pedido pelo app do usuário: %s", erro)
            flash("Não foi possível enviar o pedido agora. Tente novamente em instantes.", "danger")
            return redirect(url_for("app_usuario_oracao"))

        flash("Pedido enviado para a equipe de intercessao.", "success")
        return redirect(url_for("app_usuario_oracao"))

    testemunhos = db_select(
        """
        SELECT p.id, p.solicitante_nome, p.categoria, p.pedido, p.oracoes, p.criado_em,
               (SELECT COUNT(*) FROM pedido_oracao_reacoes r WHERE r.pedido_id = p.id) AS reacoes_total,
               (SELECT COUNT(*) FROM pedido_oracao_comentarios c WHERE c.pedido_id = p.id AND c.aprovado = 1) AS comentarios_total
        FROM pedidos_oracao p
        WHERE p.status = 'Respondido' AND p.privado = 0
        ORDER BY criado_em DESC, id DESC
        LIMIT 4
        """
    )
    comentarios_por_pedido = listar_comentarios_oracao([pedido["id"] for pedido in testemunhos])
    return render_template(
        "app_usuario/oracao.html",
        igreja=obter_igreja(),
        categorias=ORACAO_CATEGORIAS,
        testemunhos=testemunhos,
        comentarios_por_pedido=comentarios_por_pedido,
        reacoes=ORACAO_REACOES,
    )


@app.route("/app/oracao/<int:pedido_id>/reagir", methods=["POST"])
def app_usuario_reagir_oracao(pedido_id):
    if not pedido_oracao_publico_existe(pedido_id):
        flash("Pedido indisponível para interação pública.", "warning")
        return redirect(url_for("app_usuario_oracao"))

    autor_nome = request.form.get("autor_nome", "").strip() or session.get("usuario_nome") or "Visitante"
    contato = request.form.get("contato", "").strip()
    tipo = request.form.get("tipo", "orando").strip()
    if tipo not in ORACAO_REACOES:
        tipo = "orando"

    try:
        db_write(
            """
            INSERT INTO pedido_oracao_reacoes (pedido_id, autor_nome, contato, tipo)
            VALUES (%s, %s, %s, %s)
            """,
            (pedido_id, autor_nome, valor_ou_none(contato), tipo),
        )
        db_write("UPDATE pedidos_oracao SET oracoes = oracoes + 1 WHERE id = %s", (pedido_id,))
        flash("Reação registrada. Obrigado por participar em oração.", "success")
    except Exception as erro:
        app.logger.error("Erro ao registrar reação no pedido de oração: %s", erro)
        flash("Não foi possível registrar sua reação agora.", "danger")
    return redirect(url_for("app_usuario_oracao"))


@app.route("/app/oracao/<int:pedido_id>/comentar", methods=["POST"])
def app_usuario_comentar_oracao(pedido_id):
    if not pedido_oracao_publico_existe(pedido_id):
        flash("Pedido indisponível para comentário público.", "warning")
        return redirect(url_for("app_usuario_oracao"))

    autor_nome = request.form.get("autor_nome", "").strip() or session.get("usuario_nome") or "Visitante"
    contato = request.form.get("contato", "").strip()
    comentario = request.form.get("comentario", "").strip()
    if not comentario:
        flash("Escreva um comentário antes de enviar.", "danger")
        return redirect(url_for("app_usuario_oracao"))

    try:
        db_write(
            """
            INSERT INTO pedido_oracao_comentarios (pedido_id, autor_nome, contato, comentario, aprovado)
            VALUES (%s, %s, %s, %s, 1)
            """,
            (pedido_id, autor_nome, valor_ou_none(contato), comentario),
        )
        flash("Comentário publicado no testemunho.", "success")
    except Exception as erro:
        app.logger.error("Erro ao comentar pedido de oração: %s", erro)
        flash("Não foi possível publicar o comentário agora.", "danger")
    return redirect(url_for("app_usuario_oracao"))


@app.route("/app/doacoes")
def app_usuario_doacoes():
    linhas = [
        ["PIX", obter_config("doacao.pix", "Informe a chave PIX nas configurações")],
        ["Banco", obter_config("doacao.banco", "Conta principal da igreja")],
        ["Mensagem", obter_config("doacao.mensagem", "Contribua com alegria e acompanhe a secretaria para obter comprovantes.")],
    ]
    return render_template(
        "app_usuario/doacoes.html",
        igreja=obter_igreja(),
        linhas=linhas,
        formas=FORMAS_RECEBIMENTO,
    )


@app.route("/dashboard")
@login_required
def dashboard():
    metricas = gerar_metricas()
    membros_recentes = db_select(
        """
        SELECT id, nome, status AS situacao, telefone
        FROM membros
        WHERE excluido_em IS NULL
        ORDER BY criado_em DESC, id DESC
        LIMIT 5
        """
    )
    eventos = db_select(
        """
        SELECT id, nome, data_inicio AS data, status
        FROM eventos
        WHERE status <> 'Cancelado'
          AND data_inicio >= NOW()
        ORDER BY data_inicio
        LIMIT 5
        """
    )
    return render_template(
        "dashboard.html",
        metricas=metricas,
        modulos=montar_modulos_dashboard(metricas),
        pessoas_por_status=montar_pessoas_por_status(),
        engajamento_app=montar_engajamento_app(metricas["total_pessoas"]),
        membros_recentes=membros_recentes,
        eventos=eventos,
    )


@app.route("/pessoas/painel")
@login_required
def painel_pessoas():
    metricas = gerar_metricas()
    aniversarios = db_select(
        """
        SELECT id, nome, data_nascimento, telefone, status
        FROM membros
        WHERE data_nascimento IS NOT NULL
          AND excluido_em IS NULL
          AND MONTH(data_nascimento) = MONTH(CURDATE())
        ORDER BY DAY(data_nascimento), nome
        LIMIT 6
        """
    )
    recentes = db_select(
        """
        SELECT id, nome, status, telefone
        FROM membros
        WHERE excluido_em IS NULL
        ORDER BY criado_em DESC, id DESC
        LIMIT 6
        """
    )
    return render_template(
        "modulos/painel.html",
        eyebrow="Pessoas",
        titulo="Painel de pessoas",
        subtitulo="Visão de membros, visitantes, famílias, aniversários e cuidado cadastral.",
        cards=[
            card("Membros ativos", metricas["membros_ativos"]),
            card("Visitantes", metricas["visitantes"]),
            card("Famílias", metricas["familias"]),
            card("Afastados", metricas["afastados"]),
        ],
        atalhos=[
            atalho("Membros", "Gerencie cadastros, status, ministérios e histórico.", "listar_membros", metricas["membros_ativos"]),
            atalho("Visitantes", "Acompanhe visitantes e encaminhe integração.", "listar_visitantes", metricas["visitantes"]),
            atalho("Aniversários", "Consulte aniversariantes do mês.", "listar_aniversarios", len(aniversarios)),
        ],
        blocos=[
            bloco_lista(
                "Aniversários do mês",
                ["Nome", "Data", "Contato", "Status"],
                [[p["nome"], data_br(p["data_nascimento"]), p.get("telefone") or "-", p["status"]] for p in aniversarios],
            ),
            bloco_lista(
                "Cadastros recentes",
                ["Nome", "Status", "Contato"],
                [[p["nome"], p["status"], p.get("telefone") or "-"] for p in recentes],
            ),
        ],
    )


@app.route("/pessoas/aniversarios")
@login_required
def listar_aniversarios():
    mes = request.args.get("mes", "").strip()
    if not mes.isdigit() or int(mes) < 1 or int(mes) > 12:
        mes = str(date.today().month)
    aniversarios = db_select(
        """
        SELECT nome, data_nascimento, telefone, email, status
        FROM membros
        WHERE data_nascimento IS NOT NULL
          AND excluido_em IS NULL
          AND MONTH(data_nascimento) = %s
        ORDER BY DAY(data_nascimento), nome
        """,
        (int(mes),),
    )
    linhas = [
        [
            pessoa["nome"],
            data_br(pessoa["data_nascimento"]),
            pessoa.get("telefone") or "-",
            pessoa.get("email") or "-",
            pessoa["status"],
        ]
        for pessoa in aniversarios
    ]
    return render_template(
        "modulos/resumo.html",
        titulo="Aniversários",
        subtitulo="Consulta de aniversariantes por mês para apoiar acompanhamento e comunicação.",
        cards=[card("Aniversariantes", len(aniversarios)), card("Mês", mes), card("Membros ativos", gerar_metricas()["membros_ativos"])],
        filtros=[{"name": "mes", "label": "Mês", "type": "number", "value": mes, "placeholder": "1 a 12"}],
        cabecalhos=["Nome", "Nascimento", "Telefone", "E-mail", "Status"],
        linhas=linhas,
        acao_url=url_for("inserir_membro"),
        acao_label="Cadastrar pessoa",
    )


@app.route("/financeiro/painel")
@login_required
def painel_financeiro():
    metricas = gerar_metricas()
    lancamentos = listar_lancamentos_financeiros()[:6]
    doacoes_pendentes = db_select(
        """
        SELECT doador_nome, tipo, valor, data_doacao, status
        FROM doacoes
        WHERE status = 'Pendente'
        ORDER BY data_doacao DESC, id DESC
        LIMIT 6
        """
    )
    return render_template(
        "modulos/painel.html",
        eyebrow="Financeiro",
        titulo="Painel financeiro",
        subtitulo="Visão de receitas, despesas, doações, movimentações e cadastros auxiliares.",
        cards=[
            card("Receitas", moeda_br(metricas["entradas"])),
            card("Despesas", moeda_br(metricas["saidas"])),
            card("Saldo", moeda_br(metricas["saldo"])),
            card("Doações", moeda_br(metricas["doacoes_valor"])),
        ],
        atalhos=[
            atalho("Receitas", "Entradas financeiras registradas no sistema.", "listar_receitas", moeda_br(metricas["entradas"])),
            atalho("Despesas", "Saídas e gastos vinculados a fornecedores.", "listar_despesas", moeda_br(metricas["saidas"])),
            atalho("Doações", "Doações recebidas, pendentes e canceladas.", "listar_doacoes", metricas["doacoes"]),
            atalho("Movimentações", "Histórico geral de lançamentos.", "listar_financeiro", "Abrir"),
            atalho("Cadastros", "Categorias, contas, formas e fornecedores.", "cadastros_financeiros", "Abrir"),
        ],
        blocos=[
            bloco_lista("Últimas movimentações", ["Data", "Tipo", "Categoria", "Conta", "Pessoa/Fornecedor", "Valor"], linhas_lancamentos(lancamentos)),
            bloco_lista(
                "Doações pendentes",
                ["Doador", "Tipo", "Valor", "Data", "Status"],
                [[d.get("doador_nome") or "-", d["tipo"], moeda_br(d["valor"]), data_br(d["data_doacao"]), d["status"]] for d in doacoes_pendentes],
            ),
        ],
    )


@app.route("/financeiro/receitas")
@login_required
def listar_receitas():
    return renderizar_lancamentos_financeiros("Entrada", "Receitas", "Entradas financeiras registradas por categoria, conta e data.")


@app.route("/financeiro/despesas")
@login_required
def listar_despesas():
    return renderizar_lancamentos_financeiros("Saida", "Despesas", "Saídas financeiras vinculadas a categorias, contas e fornecedores.")


@app.route("/financeiro/cadastros")
@login_required
def cadastros_financeiros():
    categorias = listar_categorias_financeiras()
    contas = listar_contas_financeiras()
    fornecedores = listar_fornecedores_select()
    formas_pagamento = FORMAS_RECEBIMENTO
    return render_template(
        "modulos/painel.html",
        eyebrow="Financeiro",
        titulo="Cadastros financeiros",
        subtitulo="Cadastros auxiliares usados por receitas, despesas, doações e movimentações.",
        cards=[
            card("Categorias", len(categorias)),
            card("Contas bancárias", len(contas)),
            card("Fornecedores", len(fornecedores)),
            card("Formas", len(FORMAS_RECEBIMENTO)),
        ],
        atalhos=[
            atalho("Categorias", "Classificações de receitas e despesas.", "listar_categorias_financeiro", len(categorias)),
            atalho("Centro de custos", "Agrupamento de despesas por categoria.", "listar_centros_custo", len([c for c in categorias if c["tipo"] == "Saida"])),
            atalho("Contas bancárias", "Contas usadas em lançamentos e doações.", "listar_contas_bancarias", len(contas)),
            atalho("Formas de recebimento", "Formas usadas nas doações.", "listar_formas_recebimento", len(FORMAS_RECEBIMENTO)),
            atalho("Formas de pagamento", "Formas consideradas para despesas.", "listar_formas_pagamento", "Abrir"),
            atalho("Novo lançamento", "Cadastre receita ou despesa.", "inserir_lancamento_financeiro", "Novo"),
            atalho("Fornecedores", "Gerencie fornecedores usados nas despesas.", "listar_fornecedores", len(fornecedores)),
        ],
        blocos=[
            bloco_lista("Categorias", ["Nome", "Tipo"], [[c["nome"], rotulo_tela(c["tipo"])] for c in categorias]),
            bloco_lista("Contas bancárias", ["Conta"], [[c["nome"]] for c in contas]),
            bloco_lista("Formas de recebimento", ["Forma"], [[rotulo_tela(forma)] for forma in FORMAS_RECEBIMENTO]),
            bloco_lista("Formas de pagamento", ["Forma"], [[rotulo_tela(forma)] for forma in formas_pagamento]),
        ],
    )


@app.route("/financeiro/categorias")
@login_required
def listar_categorias_financeiro():
    categorias = listar_categorias_financeiras()
    linhas = [[categoria["nome"], categoria["tipo"], "Ativa"] for categoria in categorias]
    return render_template(
        "modulos/resumo.html",
        titulo="Categorias financeiras",
        subtitulo="Categorias usadas para classificar receitas, despesas e doações.",
        cards=[
            card("Categorias", len(categorias)),
            card("Receitas", sum(1 for categoria in categorias if categoria["tipo"] == "Entrada")),
            card("Despesas", sum(1 for categoria in categorias if categoria["tipo"] == "Saida")),
        ],
        filtros=[],
        cabecalhos=["Nome", "Tipo", "Status"],
        linhas=linhas,
        acao_url=url_for("cadastros_financeiros"),
        acao_label="Cadastros financeiros",
    )


@app.route("/financeiro/centros-custo")
@login_required
def listar_centros_custo():
    categorias_saida = listar_categorias_financeiras("Saida")
    linhas = [
        [categoria["nome"], "Saida", moeda_br(db_scalar(
            """
            SELECT COALESCE(SUM(l.valor), 0) AS valor
            FROM lancamentos_financeiros l
            WHERE l.categoria_id = %s AND l.tipo = 'Saida'
            """,
            (categoria["id"],),
        ))]
        for categoria in categorias_saida
    ]
    return render_template(
        "modulos/resumo.html",
        titulo="Centro de custos",
        subtitulo="Visão de custos por categoria de despesa, seguindo o agrupamento financeiro estudado.",
        cards=[
            card("Centros", len(categorias_saida)),
            card("Despesas", moeda_br(gerar_metricas()["saidas"])),
            card("Fornecedores", gerar_metricas()["fornecedores"]),
        ],
        filtros=[],
        cabecalhos=["Centro", "Tipo", "Total movimentado"],
        linhas=linhas,
        acao_url=url_for("listar_despesas"),
        acao_label="Ver despesas",
    )


@app.route("/financeiro/contas")
@login_required
def listar_contas_bancarias():
    contas = db_select(
        """
        SELECT nome, banco, saldo_inicial, ativo
        FROM contas_financeiras
        ORDER BY nome
        """
    )
    linhas = [
        [conta["nome"], conta.get("banco") or "-", moeda_br(conta.get("saldo_inicial")), "Ativa" if conta.get("ativo") else "Inativa"]
        for conta in contas
    ]
    return render_template(
        "modulos/resumo.html",
        titulo="Contas bancárias",
        subtitulo="Contas usadas nos lançamentos financeiros e doações.",
        cards=[
            card("Contas", len(contas)),
            card("Saldo inicial", moeda_br(sum(float(conta.get("saldo_inicial") or 0) for conta in contas))),
            card("Saldo atual", moeda_br(gerar_metricas()["saldo"])),
        ],
        filtros=[],
        cabecalhos=["Conta", "Banco", "Saldo inicial", "Status"],
        linhas=linhas,
        acao_url=url_for("cadastros_financeiros"),
        acao_label="Cadastros financeiros",
    )


@app.route("/financeiro/formas-recebimento")
@login_required
def listar_formas_recebimento():
    linhas = [
        [rotulo_tela(forma), db_scalar("SELECT COUNT(*) AS valor FROM doacoes WHERE forma_recebimento = %s", (forma,)), "Ativa"]
        for forma in FORMAS_RECEBIMENTO
    ]
    return render_template(
        "modulos/resumo.html",
        titulo="Formas de recebimento",
        subtitulo="Formas utilizadas no registro de doações e entradas.",
        cards=[
            card("Formas", len(FORMAS_RECEBIMENTO)),
            card("Doações recebidas", gerar_metricas()["doacoes"]),
            card("Valor recebido", moeda_br(gerar_metricas()["doacoes_valor"])),
        ],
        filtros=[],
        cabecalhos=["Forma", "Doações", "Status"],
        linhas=linhas,
        acao_url=url_for("listar_doacoes"),
        acao_label="Ver doações",
    )


@app.route("/financeiro/formas-pagamento")
@login_required
def listar_formas_pagamento():
    formas_pagamento = ["Dinheiro", "PIX", "Cartão", "Transferência", "Boleto"]
    linhas = [[forma, "Disponível"] for forma in formas_pagamento]
    return render_template(
        "modulos/resumo.html",
        titulo="Formas de pagamento",
        subtitulo="Formas consideradas para organização de despesas e pagamentos.",
        cards=[
            card("Formas", len(formas_pagamento)),
            card("Despesas", moeda_br(gerar_metricas()["saidas"])),
            card("Movimentações", len(listar_lancamentos_financeiros("Saida"))),
        ],
        filtros=[],
        cabecalhos=["Forma", "Status"],
        linhas=linhas,
        acao_url=url_for("listar_despesas"),
        acao_label="Ver despesas",
    )


@app.route("/ministerios/painel")
@login_required
def painel_ministerios():
    metricas = gerar_metricas()
    ministerios = listar_ministerios_db(status="Ativo")[:8]
    return render_template(
        "modulos/painel.html",
        eyebrow="Ministérios",
        titulo="Painel de ministérios",
        subtitulo="Visão de líderes, capacidade, participantes e organização ministerial.",
        cards=[
            card("Ministérios ativos", metricas["ministerios"]),
            card("Vagas", metricas["vagas"]),
            card("Participantes", db_scalar("SELECT COUNT(*) AS valor FROM membro_ministerio WHERE ativo = 1")),
        ],
        atalhos=[
            atalho("Gerenciamento", "Cadastre, edite e acompanhe ministérios.", "listar_ministerios", metricas["ministerios"]),
            atalho("Novo ministério", "Crie um ministério com líder e dia de reunião.", "inserir_ministerio", "Novo"),
        ],
        blocos=[
            bloco_lista(
                "Ministérios ativos",
                ["Nome", "Líder", "Dia", "Participantes", "Vagas"],
                [[m["nome"], m.get("lider") or "-", m.get("dia_reuniao") or "-", len(m.get("participantes") or []), m.get("vagas") or 0] for m in ministerios],
            )
        ],
    )


@app.route("/celulas/painel")
@login_required
def painel_celulas():
    metricas = gerar_metricas()
    celulas = db_select(
        """
        SELECT c.nome, c.lider_nome, c.bairro, c.dia_reuniao,
               COUNT(m.id) AS membros
        FROM celulas c
        LEFT JOIN membros m ON m.celula_id = c.id AND m.excluido_em IS NULL
        WHERE c.excluido_em IS NULL AND c.ativo = 1
        GROUP BY c.id
        ORDER BY c.nome
        LIMIT 8
        """
    )
    return render_template(
        "modulos/painel.html",
        eyebrow="Células",
        titulo="Painel de células",
        subtitulo="Visão de pequenos grupos, líderes, bairros, membros e presenças.",
        cards=[
            card("Células ativas", metricas["celulas"]),
            card("Presenças", metricas["presencas"]),
            card("Ausências", metricas["ausencias"]),
            card("Visitantes", metricas["visitantes"]),
        ],
        atalhos=[
            atalho("Gerenciamento", "Cadastre e acompanhe células.", "listar_celulas", metricas["celulas"]),
            atalho("Nova célula", "Crie uma célula com líder, bairro e horário.", "inserir_celula", "Nova"),
            atalho("Presenças", "Registre frequência por encontro.", "listar_presencas", metricas["presencas"]),
        ],
        blocos=[
            bloco_lista(
                "Células ativas",
                ["Nome", "Líder", "Bairro", "Dia", "Membros"],
                [[c["nome"], c.get("lider_nome") or "-", c.get("bairro") or "-", c.get("dia_reuniao") or "-", c.get("membros") or 0] for c in celulas],
            )
        ],
    )


@app.route("/comunicacao/painel")
@login_required
def painel_comunicacao():
    metricas = gerar_metricas()
    mensagens = db_select(
        """
        SELECT canal, destino_tipo, assunto, status
        FROM mensagens
        ORDER BY criado_em DESC, id DESC
        LIMIT 6
        """
    )
    avisos = db_select(
        """
        SELECT titulo, categoria, status, COALESCE(publicado_em, criado_em) AS data_ref
        FROM mural_avisos
        ORDER BY COALESCE(publicado_em, criado_em) DESC, id DESC
        LIMIT 6
        """
    )
    return render_template(
        "modulos/painel.html",
        eyebrow="Comunicação",
        titulo="Painel de comunicação",
        subtitulo="Visão de feed, comunicados, mural, devocional e relatórios.",
        cards=[
            card("Mensagens", metricas["mensagens"]),
            card("Mural ativo", metricas["mural"]),
            card("Canais", db_scalar("SELECT COUNT(DISTINCT canal) AS valor FROM mensagens")),
            card("Listas", db_scalar("SELECT COUNT(*) AS valor FROM comunicacao_listas WHERE ativo = 1")),
        ],
        atalhos=[
            atalho("Feed", "Acompanhe avisos publicados no mural.", "listar_mural", metricas["mural"]),
            atalho("Comunicados", "Gerencie mensagens internas, WhatsApp e e-mail.", "listar_comunicacao", metricas["mensagens"]),
            atalho("Devocional", "Use o mural para publicar devocionais e avisos.", "listar_mural", "Abrir"),
        ],
        blocos=[
            bloco_lista("Últimos comunicados", ["Canal", "Destino", "Assunto", "Status"], [[rotulo_tela(m["canal"]), rotulo_tela(m["destino_tipo"]), m["assunto"], m["status"]] for m in mensagens]),
            bloco_lista("Feed e mural", ["Título", "Categoria", "Status", "Data"], [[a["titulo"], a.get("categoria") or "-", a["status"], data_br(a["data_ref"])] for a in avisos]),
        ],
    )


@app.route("/intercessao/painel")
@login_required
def painel_intercessao():
    pedidos = db_select(
        """
        SELECT solicitante_nome, categoria, status, oracoes, criado_em
        FROM pedidos_oracao
        ORDER BY criado_em DESC, id DESC
        LIMIT 8
        """
    )
    return render_template(
        "modulos/painel.html",
        eyebrow="Intercessão",
        titulo="Painel de intercessão",
        subtitulo="Visão de pedidos de oração, testemunhos, respostas e acompanhamento pastoral.",
        cards=[
            card("Pedidos abertos", db_scalar("SELECT COUNT(*) AS valor FROM pedidos_oracao WHERE status IN ('Pendente', 'Em oracao')")),
            card("Respondidos", db_scalar("SELECT COUNT(*) AS valor FROM pedidos_oracao WHERE status = 'Respondido'")),
            card("Testemunhos", db_scalar("SELECT COUNT(*) AS valor FROM pedidos_oracao WHERE status = 'Respondido'")),
            card("Orações", db_scalar("SELECT COALESCE(SUM(oracoes), 0) AS valor FROM pedidos_oracao")),
        ],
        atalhos=[
            atalho("Pedidos de oração", "Gerencie pedidos abertos, privados e arquivados.", "listar_intercessao", "Abrir"),
            atalho("Novo pedido", "Cadastre um pedido de oração.", "inserir_intercessao", "Novo"),
            atalho("Testemunhos", "Pedidos respondidos funcionam como base de testemunhos.", "listar_testemunhos", "Abrir"),
        ],
        blocos=[
            bloco_lista("Pedidos recentes", ["Solicitante", "Categoria", "Status", "Orações", "Data"], [[p["solicitante_nome"], rotulo_tela(p.get("categoria")) if p.get("categoria") else "-", rotulo_tela(p["status"]), p["oracoes"], data_br(p["criado_em"])] for p in pedidos])
        ],
    )


@app.route("/intercessao/testemunhos")
@login_required
def listar_testemunhos():
    testemunhos = db_select(
        """
        SELECT solicitante_nome, categoria, pedido, oracoes, criado_em
        FROM pedidos_oracao
        WHERE status = 'Respondido'
        ORDER BY criado_em DESC, id DESC
        """
    )
    linhas = [
        [pedido["solicitante_nome"], rotulo_tela(pedido.get("categoria")) if pedido.get("categoria") else "-", pedido["pedido"][:90], pedido["oracoes"], data_br(pedido["criado_em"])]
        for pedido in testemunhos
    ]
    return render_template(
        "modulos/resumo.html",
        titulo="Testemunhos",
        subtitulo="Pedidos marcados como respondidos para acompanhamento e memória pastoral.",
        cards=[card("Testemunhos", len(testemunhos)), card("Orações", sum(int(p["oracoes"] or 0) for p in testemunhos)), card("Pedidos abertos", db_scalar("SELECT COUNT(*) AS valor FROM pedidos_oracao WHERE status IN ('Pendente', 'Em oracao')"))],
        filtros=[],
        cabecalhos=["Solicitante", "Categoria", "Resumo", "Orações", "Data"],
        linhas=linhas,
        acao_url=url_for("inserir_intercessao"),
        acao_label="Novo pedido",
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

        db_write("UPDATE usuarios SET ultimo_login_em = NOW() WHERE id = %s", (usuario["id"],))
        session["usuario_id"] = usuario["id"]
        session["usuario_logado"] = usuario["email"]
        session["usuario_nome"] = usuario["nome"]
        session["usuario_perfil"] = usuario["perfil"]
        session["usuario_modo"] = "app" if perfil_eh_visitante(usuario["perfil"]) else "admin"
        flash("Login realizado com sucesso!", "success")
        if perfil_eh_visitante(usuario["perfil"]):
            return redirect(url_for("app_usuario_inicio"))
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/recuperar-senha", methods=["GET", "POST"])
def recuperar_senha():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        if not email or not validar_email(email):
            flash("Informe um e-mail válido para recuperação de senha.", "danger")
            return redirect(url_for("recuperar_senha"))

        flash("Se o e-mail estiver cadastrado, as instrucoes de recuperacao serao enviadas.", "info")
        return redirect(url_for("login"))

    return render_template("recuperar_senha.html")


def processar_cadastro_visitante(modo_app=False):
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        telefone = request.form.get("telefone", "").strip()
        whatsapp = request.form.get("whatsapp", "").strip()
        interesse = request.form.get("interesse", "").strip()
        mensagem = request.form.get("mensagem", "").strip()
        senha = request.form.get("senha", "").strip()
        confirmar_senha = request.form.get("confirmar_senha", "").strip()

        if not nome or not email or not senha:
            flash("Informe seu nome, e-mail e senha para acessar o app.", "danger")
            return redirect(url_for("app_usuario_cadastro" if modo_app else "cadastro"))

        if not validar_email(email):
            flash("Informe um e-mail válido.", "danger")
            return redirect(url_for("app_usuario_cadastro" if modo_app else "cadastro"))

        if len(senha) < 8:
            flash("A senha deve ter pelo menos 8 caracteres.", "danger")
            return redirect(url_for("app_usuario_cadastro" if modo_app else "cadastro"))

        if senha != confirmar_senha:
            flash("A confirmação de senha não confere.", "danger")
            return redirect(url_for("app_usuario_cadastro" if modo_app else "cadastro"))

        if telefone and not validar_telefone(telefone):
            flash("Informe um telefone válido com DDD.", "danger")
            return redirect(url_for("app_usuario_cadastro" if modo_app else "cadastro"))

        if whatsapp and not validar_telefone(whatsapp):
            flash("Informe um WhatsApp válido com DDD.", "danger")
            return redirect(url_for("app_usuario_cadastro" if modo_app else "cadastro"))

        if email_membro_em_uso(email):
            flash("Já existe um visitante ou membro com este e-mail.", "danger")
            return redirect(url_for("app_usuario_cadastro" if modo_app else "cadastro"))

        if email_em_uso(email):
            flash("Já existe um acesso com este e-mail. Use o login para entrar no app.", "danger")
            return redirect(url_for("app_usuario_cadastro" if modo_app else "cadastro"))

        try:
            cadastrar_visitante_app(nome, email, telefone, whatsapp, interesse, mensagem, senha)
        except Exception as erro:
            app.logger.error("Erro ao cadastrar visitante pelo app: %s", erro)
            flash("Não foi possível registrar seu cadastro agora. Tente novamente em instantes.", "danger")
            return redirect(url_for("app_usuario_cadastro" if modo_app else "cadastro"))

        flash("Cadastro realizado com sucesso! Entre com seu e-mail e senha para acessar o app.", "success")
        return redirect(url_for("login"))

    return render_template(
        "cadastro.html",
        igreja=obter_igreja(),
        layout_base="app_usuario/base.html" if modo_app else "base_publica.html",
        modo_app=modo_app,
    )


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    return processar_cadastro_visitante(modo_app=False)


@app.route("/app/cadastro", methods=["GET", "POST"])
def app_usuario_cadastro():
    return processar_cadastro_visitante(modo_app=True)


@app.route("/logout")
def logout():
    session.clear()
    flash("Logout realizado com sucesso!", "info")
    return redirect(url_for("login"))


@app.route("/usuarios/listar")
@login_required
def listar_usuarios():
    busca = request.args.get("q", "").strip()
    usuarios = listar_usuarios_db(busca)
    return render_template(
        "usuarios/listar_usuarios.html",
        usuarios=usuarios,
        busca=busca,
        total=db_scalar("SELECT COUNT(*) AS valor FROM usuarios WHERE excluido_em IS NULL"),
    )


@app.route("/usuarios/inserir", methods=["GET", "POST"])
@login_required
def inserir_usuario():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        perfil = request.form.get("perfil", "").strip()
        senha_provisoria = request.form.get("senha_provisoria", "").strip()

        if not nome or not email or not perfil or not senha_provisoria:
            flash("Nome, e-mail, perfil e senha provisória são obrigatórios.", "danger")
            return redirect(url_for("inserir_usuario"))

        if not validar_email(email):
            flash("Informe um e-mail válido.", "danger")
            return redirect(url_for("inserir_usuario"))

        if perfil not in PERFIS_USUARIO:
            flash("Selecione um perfil válido.", "danger")
            return redirect(url_for("inserir_usuario"))

        if len(senha_provisoria) < 8:
            flash("A senha provisória deve ter pelo menos 8 caracteres.", "danger")
            return redirect(url_for("inserir_usuario"))

        if email_em_uso(email):
            flash("Já existe um usuário com este e-mail.", "danger")
            return redirect(url_for("inserir_usuario"))

        try:
            criar_usuario(nome, email, senha_provisoria, perfil)
        except Exception as erro:
            app.logger.error("Erro ao inserir usuário: %s", erro)
            flash("Não foi possível salvar o usuário no banco.", "danger")
            return redirect(url_for("inserir_usuario"))

        flash("Usuário cadastrado com sucesso. Informe a senha provisória para o primeiro acesso.", "success")
        return redirect(url_for("listar_usuarios"))

    return render_template("usuarios/inserir_usuario.html", perfis=PERFIS_USUARIO)


@app.route("/usuarios/editar/<int:usuario_id>", methods=["GET", "POST"])
@login_required
def editar_usuario(usuario_id):
    usuario = obter_usuario(usuario_id)
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

        try:
            atualizar_usuario(usuario_id, nome, email, perfil, status)
        except Exception as erro:
            app.logger.error("Erro ao editar usuário: %s", erro)
            flash("Não foi possível atualizar o usuário no banco.", "danger")
            return redirect(url_for("editar_usuario", usuario_id=usuario_id))

        flash("Usuário atualizado com sucesso.", "success")
        return redirect(url_for("listar_usuarios"))

    return render_template("usuarios/editar_usuario.html", usuario=usuario, perfis=PERFIS_USUARIO, status_opcoes=STATUS_USUARIO)


@app.route("/usuarios/excluir/<int:usuario_id>", methods=["POST"])
@login_required
def excluir_usuario(usuario_id):
    usuario = obter_usuario(usuario_id)
    if not usuario:
        flash("Usuário não encontrado.", "danger")
        return redirect(url_for("listar_usuarios"))

    db_write("UPDATE usuarios SET ativo = 0, excluido_em = NOW() WHERE id = %s", (usuario_id,))
    flash("Usuário inativado por exclusão lógica.", "success")
    return redirect(url_for("listar_usuarios"))


@app.route("/membros/listar")
@login_required
def listar_membros():
    busca = request.args.get("q", "").strip()
    situacao = request.args.get("status", "").strip()
    if situacao not in SITUACOES_MEMBRO:
        situacao = ""
    membros = listar_membros_db(busca, situacao)
    return render_template(
        "membros/listar_membros.html",
        membros=membros,
        busca=busca,
        status_atual=situacao,
        status_opcoes=SITUACOES_MEMBRO,
        titulo_lista="Membros",
        descricao_lista="Gerencie cadastros, status, contato, ministérios e histórico espiritual.",
        novo_url=url_for("inserir_membro"),
        novo_label="Cadastrar membro",
        modo_visitantes=False,
        metricas=gerar_metricas(),
        total=db_scalar("SELECT COUNT(*) AS valor FROM membros WHERE excluido_em IS NULL"),
    )


@app.route("/visitantes/listar")
@login_required
def listar_visitantes():
    busca = request.args.get("q", "").strip()
    membros = listar_membros_db(busca, apenas_visitantes=True)
    return render_template(
        "membros/listar_membros.html",
        membros=membros,
        busca=busca,
        status_atual="Visitante",
        status_opcoes=SITUACOES_MEMBRO,
        titulo_lista="Visitantes",
        descricao_lista="Acompanhe visitantes e encaminhe o cuidado inicial.",
        novo_url=url_for("inserir_membro", situacao="Visitante"),
        novo_label="Cadastrar visitante",
        modo_visitantes=True,
        metricas=gerar_metricas(),
        total=len(membros),
    )


@app.route("/familias/listar")
@login_required
def listar_familias():
    busca = request.args.get("q", "").strip()
    sql = """
        SELECT f.id, f.nome, f.telefone, f.endereco, f.ativo,
               r.nome AS responsavel,
               COUNT(fm.membro_id) AS membros_total,
               GROUP_CONCAT(m.nome ORDER BY m.nome SEPARATOR ', ') AS membros
        FROM familias f
        LEFT JOIN membros r ON r.id = f.responsavel_membro_id
        LEFT JOIN familia_membros fm ON fm.familia_id = f.id
        LEFT JOIN membros m ON m.id = fm.membro_id
        WHERE f.excluido_em IS NULL
    """
    params = []
    if busca:
        termo = f"%{busca}%"
        sql += " AND (f.nome LIKE %s OR f.telefone LIKE %s OR r.nome LIKE %s OR m.nome LIKE %s)"
        params.extend([termo, termo, termo, termo])
    sql += " GROUP BY f.id ORDER BY f.nome"
    familias = db_select(sql, params)
    return render_template(
        "familias/listar_familias.html",
        familias=familias,
        busca=busca,
        metricas=gerar_metricas(),
    )


@app.route("/familias/inserir", methods=["GET", "POST"])
@login_required
def inserir_familia():
    membros = listar_membros_select()

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        responsavel_membro_id = request.form.get("responsavel_membro_id", "").strip()
        telefone = request.form.get("telefone", "").strip()
        endereco = request.form.get("endereco", "").strip()
        observacoes = request.form.get("observacoes", "").strip()
        membros_ids = request.form.getlist("membros")

        if not nome:
            flash("Nome da família é obrigatório.", "danger")
            return redirect(url_for("inserir_familia"))

        if telefone and not validar_telefone(telefone):
            flash("Informe um telefone válido com DDD.", "danger")
            return redirect(url_for("inserir_familia"))

        membros_vinculados = {int(membro_id) for membro_id in membros_ids if membro_id.isdigit()}
        responsavel_id = int(responsavel_membro_id) if responsavel_membro_id.isdigit() else None
        if responsavel_id:
            membros_vinculados.add(responsavel_id)

        with get_connection() as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    """
                    INSERT INTO familias (nome, responsavel_membro_id, telefone, endereco, observacoes, ativo)
                    VALUES (%s, %s, %s, %s, %s, 1)
                    """,
                    (
                        nome,
                        responsavel_id,
                        valor_ou_none(telefone),
                        valor_ou_none(endereco),
                        valor_ou_none(observacoes),
                    ),
                )
                familia_id = cursor.lastrowid
                for membro_id in membros_vinculados:
                    parentesco = "Responsavel" if membro_id == responsavel_id else "Membro"
                    cursor.execute(
                        """
                        INSERT INTO familia_membros (familia_id, membro_id, parentesco)
                        VALUES (%s, %s, %s)
                        """,
                        (familia_id, membro_id, parentesco),
                    )
                connection.commit()
            except Exception:
                connection.rollback()
                raise
            finally:
                cursor.close()

        flash("Família cadastrada com sucesso.", "success")
        return redirect(url_for("listar_familias"))

    return render_template("familias/inserir_familia.html", membros=membros)


@app.route("/familias/excluir/<int:familia_id>", methods=["POST"])
@login_required
def excluir_familia(familia_id):
    db_write("UPDATE familias SET ativo = 0, excluido_em = NOW() WHERE id = %s", (familia_id,))
    flash("Família removida da listagem por exclusão lógica.", "success")
    return redirect(url_for("listar_familias"))


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

        try:
            inserir_membro_db(dados)
        except Exception as erro:
            app.logger.error("Erro ao inserir membro: %s", erro)
            flash("Não foi possível salvar a pessoa no banco.", "danger")
            return redirect(url_for("inserir_membro", situacao=situacao_padrao))

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
    membro = obter_membro(membro_id)
    if not membro:
        flash("Membro não encontrado.", "danger")
        return redirect(url_for("listar_membros"))

    if request.method == "POST":
        dados = obter_dados_membro_form()
        erro = validar_dados_membro(dados, "editar_membro", membro_id=membro_id)
        if erro:
            return erro

        try:
            atualizar_membro_db(membro_id, dados)
        except Exception as erro:
            app.logger.error("Erro ao editar membro: %s", erro)
            flash("Não foi possível atualizar a pessoa no banco.", "danger")
            return redirect(url_for("editar_membro", membro_id=membro_id))

        flash("Cadastro atualizado com sucesso.", "success")
        return redirect(url_for("listar_visitantes" if dados["situacao"] == "Visitante" else "listar_membros"))

    return render_template(
        "membros/editar_membro.html",
        membro=membro,
        ministerios=obter_opcoes_ministerio(),
        celulas=obter_opcoes_celula(),
        situacoes=SITUACOES_MEMBRO,
        estados_civis=ESTADOS_CIVIS,
    )


@app.route("/membros/inativar/<int:membro_id>", methods=["POST"])
@login_required
def inativar_membro(membro_id):
    membro = obter_membro(membro_id)
    if not membro:
        flash("Membro não encontrado.", "danger")
        return redirect(url_for("listar_membros"))

    db_write("UPDATE membros SET status = 'Inativo' WHERE id = %s AND excluido_em IS NULL", (membro_id,))
    flash("Membro inativado com sucesso.", "success")
    return redirect(url_for("listar_membros"))


@app.route("/membros/excluir/<int:membro_id>", methods=["POST"])
@login_required
def excluir_membro(membro_id):
    membro = obter_membro(membro_id)
    if not membro:
        flash("Membro não encontrado.", "danger")
        return redirect(url_for("listar_membros"))

    db_write(
        "UPDATE membros SET status = 'Inativo', excluido_em = NOW() WHERE id = %s",
        (membro_id,),
    )
    flash("Membro removido da listagem por exclusão lógica.", "success")
    return redirect(url_for("listar_membros"))


@app.route("/membros/historico/<int:membro_id>", methods=["GET", "POST"])
@login_required
def historico_membro(membro_id):
    membro = obter_membro(membro_id, incluir_historico=True)
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

        db_write(
            """
            INSERT INTO historico_espiritual
                (membro_id, tipo, data_registro, descricao, responsavel_usuario_id)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (membro_id, tipo, data, descricao, session.get("usuario_id")),
        )
        flash("Histórico espiritual registrado com sucesso.", "success")
        return redirect(url_for("historico_membro", membro_id=membro_id))

    return render_template("membros/historico_membro.html", membro=membro, tipos_historico=TIPOS_HISTORICO)


@app.route("/ministerios/listar")
@login_required
def listar_ministerios():
    busca = request.args.get("q", "").strip()
    status = request.args.get("status", "").strip()
    if status not in STATUS_MINISTERIO:
        status = ""
    ministerios = listar_ministerios_db(busca, status)
    return render_template(
        "ministerios/listar_ministerios.html",
        ministerios=ministerios,
        busca=busca,
        status_atual=status,
        status_opcoes=STATUS_MINISTERIO,
        total=db_scalar("SELECT COUNT(*) AS valor FROM ministerios WHERE excluido_em IS NULL"),
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
            flash("O número de vagas não pode ser negativo.", "danger")
            return redirect(url_for("inserir_ministerio"))

        db_write(
            """
            INSERT INTO ministerios (nome, lider_nome, dia_reuniao, vagas, ativo)
            VALUES (%s, %s, %s, %s, 1)
            """,
            (nome, lider, dia_reuniao, vagas),
        )
        flash("Ministério cadastrado com sucesso!", "success")
        return redirect(url_for("listar_ministerios"))

    return render_template("ministerios/inserir_ministerio.html", dias=DIAS_REUNIAO)


@app.route("/ministerios/editar/<int:ministerio_id>", methods=["GET", "POST"])
@login_required
def editar_ministerio(ministerio_id):
    ministerio = obter_ministerio(ministerio_id)
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

        db_write(
            """
            UPDATE ministerios
            SET nome = %s, lider_nome = %s, dia_reuniao = %s, vagas = %s, ativo = %s
            WHERE id = %s AND excluido_em IS NULL
            """,
            (nome, lider, dia_reuniao, vagas, 1 if status == "Ativo" else 0, ministerio_id),
        )
        flash("Ministério atualizado com sucesso.", "success")
        return redirect(url_for("listar_ministerios"))

    return render_template("ministerios/editar_ministerio.html", ministerio=ministerio, dias=DIAS_REUNIAO, status_opcoes=STATUS_MINISTERIO)


@app.route("/ministerios/excluir/<int:ministerio_id>", methods=["POST"])
@login_required
def excluir_ministerio(ministerio_id):
    ministerio = obter_ministerio(ministerio_id)
    if not ministerio:
        flash("Ministério não encontrado.", "danger")
        return redirect(url_for("listar_ministerios"))

    db_write("UPDATE ministerios SET ativo = 0, excluido_em = NOW() WHERE id = %s", (ministerio_id,))
    flash("Ministério inativado por exclusão lógica.", "success")
    return redirect(url_for("listar_ministerios"))


@app.route("/celulas/listar")
@login_required
def listar_celulas():
    celulas = db_select(
        """
        SELECT c.id, c.nome, c.lider_nome, c.bairro, c.dia_reuniao,
               COUNT(m.id) AS membros,
               SUM(CASE WHEN m.status = 'Visitante' THEN 1 ELSE 0 END) AS visitantes
        FROM celulas c
        LEFT JOIN membros m ON m.celula_id = c.id AND m.excluido_em IS NULL
        WHERE c.excluido_em IS NULL
        GROUP BY c.id
        ORDER BY c.nome
        """
    )
    return render_template(
        "celulas/listar_celulas.html",
        celulas=celulas,
        metricas=gerar_metricas(),
        membros_vinculados=sum(int(celula.get("membros") or 0) for celula in celulas),
        visitantes_vinculados=sum(int(celula.get("visitantes") or 0) for celula in celulas),
    )


@app.route("/celulas/inserir", methods=["GET", "POST"])
@login_required
def inserir_celula():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        lider = request.form.get("lider", "").strip()
        bairro = request.form.get("bairro", "").strip()
        endereco = request.form.get("endereco", "").strip()
        dia_reuniao = request.form.get("dia_reuniao", "").strip()
        horario = request.form.get("horario", "").strip()

        if not nome or not lider or not bairro or not dia_reuniao:
            flash("Nome, líder, bairro e dia de reunião são obrigatórios.", "danger")
            return redirect(url_for("inserir_celula"))

        if dia_reuniao not in DIAS_REUNIAO:
            flash("Selecione um dia de reunião válido.", "danger")
            return redirect(url_for("inserir_celula"))

        db_write(
            """
            INSERT INTO celulas (nome, lider_nome, bairro, endereco, dia_reuniao, horario, ativo)
            VALUES (%s, %s, %s, %s, %s, %s, 1)
            """,
            (nome, lider, bairro, valor_ou_none(endereco), dia_reuniao, valor_ou_none(horario)),
        )
        flash("Célula cadastrada com sucesso.", "success")
        return redirect(url_for("listar_celulas"))

    return render_template("celulas/inserir_celula.html", dias=DIAS_REUNIAO)


@app.route("/presencas/listar")
@login_required
def listar_presencas():
    data = request.args.get("data", "").strip()
    membro_busca = request.args.get("membro", "").strip()
    sql = """
        SELECT p.id, p.data_presenca, p.tipo, p.referencia_nome,
               p.presente, m.nome AS membro_nome
        FROM presencas p
        LEFT JOIN membros m ON m.id = p.membro_id
        WHERE 1=1
    """
    params = []
    if data:
        sql += " AND p.data_presenca = %s"
        params.append(data)
    if membro_busca:
        sql += " AND m.nome LIKE %s"
        params.append(f"%{membro_busca}%")
    sql += " ORDER BY p.data_presenca DESC, p.id DESC"
    presencas = db_select(sql, params)

    linhas = [
        [
            f"#{presenca['id']}",
            data_br(presenca["data_presenca"]),
            presenca["tipo"],
            presenca.get("referencia_nome") or "-",
            presenca.get("membro_nome") or "Visitante/Não vinculado",
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
            {"label": "Baixa frequência", "valor": 0},
        ],
        filtros=[
            {"name": "data", "label": "Data", "type": "date", "value": data},
            {"name": "membro", "label": "Membro", "type": "search", "value": membro_busca, "placeholder": "Buscar membro"},
        ],
        cabecalhos=["ID", "Data", "Tipo", "Referência", "Membro", "Status"],
        linhas=linhas,
        acao_url=url_for("inserir_presenca"),
        acao_label="Registrar presença",
    )


@app.route("/presencas/inserir", methods=["GET", "POST"])
@login_required
def inserir_presenca():
    membros = listar_membros_select()

    if request.method == "POST":
        data_presenca = request.form.get("data_presenca", "").strip()
        tipo = request.form.get("tipo", "").strip()
        referencia_nome = request.form.get("referencia_nome", "").strip()
        membro_id = request.form.get("membro_id", "").strip()
        presente = 1 if request.form.get("presente") else 0

        if not data_presenca or tipo not in ["Culto", "Evento", "Celula"] or not referencia_nome:
            flash("Data, tipo e referência são obrigatórios.", "danger")
            return redirect(url_for("inserir_presenca"))

        db_write(
            """
            INSERT INTO presencas (membro_id, tipo, referencia_nome, data_presenca, presente)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (int(membro_id) if membro_id else None, tipo, referencia_nome, data_presenca, presente),
        )
        flash("Presença registrada com sucesso.", "success")
        return redirect(url_for("listar_presencas"))

    return render_template("presencas/inserir_presenca.html", membros=membros)


@app.route("/eventos/listar")
@login_required
def listar_eventos():
    eventos = db_select(
        """
        SELECT e.id, e.nome, e.data_inicio, e.local, e.status, e.banner_path,
               SUM(CASE WHEN ei.membro_id IS NOT NULL THEN 1 ELSE 0 END) AS membros,
               SUM(CASE WHEN ei.visitante_nome IS NOT NULL THEN 1 ELSE 0 END) AS visitantes,
               SUM(CASE WHEN ei.presente = 1 THEN 1 ELSE 0 END) AS presentes
        FROM eventos e
        LEFT JOIN evento_inscricoes ei ON ei.evento_id = e.id
        GROUP BY e.id
        ORDER BY e.data_inicio
        """
    )
    return render_template(
        "eventos/listar_eventos.html",
        eventos=eventos,
        metricas=gerar_metricas(),
        membros_inscritos=sum(int(evento.get("membros") or 0) for evento in eventos),
        visitantes_inscritos=sum(int(evento.get("visitantes") or 0) for evento in eventos),
    )


@app.route("/eventos/inserir", methods=["GET", "POST"])
@login_required
def inserir_evento():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        descricao = request.form.get("descricao", "").strip()
        data_inicio = request.form.get("data_inicio", "").strip()
        data_fim = request.form.get("data_fim", "").strip()
        local = request.form.get("local", "").strip()
        status = request.form.get("status", "Agendado").strip()
        banner_path = salvar_banner_evento(request.files.get("banner"))

        if not nome or not data_inicio or not local:
            flash("Nome, data e local são obrigatórios.", "danger")
            return redirect(url_for("inserir_evento"))

        if status not in ["Agendado", "Realizado", "Cancelado"]:
            flash("Selecione um status válido.", "danger")
            return redirect(url_for("inserir_evento"))

        db_write(
            """
            INSERT INTO eventos (nome, descricao, data_inicio, data_fim, local, status, banner_path)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                nome,
                valor_ou_none(descricao),
                data_inicio.replace("T", " "),
                data_fim.replace("T", " ") if data_fim else None,
                local,
                status,
                banner_path,
            ),
        )
        flash("Evento cadastrado com sucesso.", "success")
        return redirect(url_for("listar_eventos"))

    return render_template("eventos/inserir_evento.html", status_opcoes=["Agendado", "Realizado", "Cancelado"])


@app.route("/financeiro/listar")
@login_required
def listar_financeiro():
    return renderizar_lancamentos_financeiros("", "Movimentações", "Histórico geral de entradas e saídas financeiras.")


@app.route("/financeiro/lancamentos/inserir", methods=["GET", "POST"])
@login_required
def inserir_lancamento_financeiro():
    categorias = listar_categorias_financeiras()
    contas = listar_contas_financeiras()
    membros = listar_membros_select()
    fornecedores = listar_fornecedores_select()

    if request.method == "POST":
        tipo = request.form.get("tipo", "").strip()
        categoria_id = request.form.get("categoria_id", "").strip()
        conta_id = request.form.get("conta_id", "").strip()
        membro_id = request.form.get("membro_id", "").strip()
        fornecedor_id = request.form.get("fornecedor_id", "").strip()
        descricao = request.form.get("descricao", "").strip()
        valor_raw = request.form.get("valor", "").strip().replace(",", ".")
        data_lancamento = request.form.get("data_lancamento", "").strip()

        if tipo not in ["Entrada", "Saida"] or not categoria_id or not conta_id or not valor_raw or not data_lancamento:
            flash("Tipo, categoria, conta, valor e data são obrigatórios.", "danger")
            return redirect(url_for("inserir_lancamento_financeiro"))

        try:
            valor = float(valor_raw)
        except ValueError:
            flash("Informe um valor válido.", "danger")
            return redirect(url_for("inserir_lancamento_financeiro"))

        if valor < 0:
            flash("Valor não pode ser negativo.", "danger")
            return redirect(url_for("inserir_lancamento_financeiro"))

        db_write(
            """
            INSERT INTO lancamentos_financeiros
                (tipo, categoria_id, conta_id, membro_id, fornecedor_id, descricao, valor, data_lancamento, criado_por_usuario_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                tipo,
                int(categoria_id),
                int(conta_id),
                int(membro_id) if membro_id else None,
                int(fornecedor_id) if fornecedor_id else None,
                valor_ou_none(descricao),
                valor,
                data_lancamento,
                session.get("usuario_id"),
            ),
        )
        flash("Lançamento financeiro cadastrado com sucesso.", "success")
        return redirect(url_for("listar_financeiro"))

    return render_template(
        "financeiro/inserir_lancamento.html",
        categorias=categorias,
        contas=contas,
        membros=membros,
        fornecedores=fornecedores,
    )


@app.route("/fornecedores/listar")
@login_required
def listar_fornecedores():
    busca = request.args.get("q", "").strip()
    sql = """
        SELECT id, nome, documento, telefone, email, endereco, ativo
        FROM fornecedores
        WHERE excluido_em IS NULL
    """
    params = []
    if busca:
        termo = f"%{busca}%"
        sql += " AND (nome LIKE %s OR documento LIKE %s OR telefone LIKE %s OR email LIKE %s)"
        params.extend([termo, termo, termo, termo])
    sql += " ORDER BY nome"
    fornecedores = db_select(sql, params)
    return render_template(
        "fornecedores/listar_fornecedores.html",
        fornecedores=fornecedores,
        busca=busca,
        metricas=gerar_metricas(),
    )


@app.route("/fornecedores/inserir", methods=["GET", "POST"])
@login_required
def inserir_fornecedor():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        documento = request.form.get("documento", "").strip()
        telefone = request.form.get("telefone", "").strip()
        email = request.form.get("email", "").strip().lower()
        endereco = request.form.get("endereco", "").strip()
        observacoes = request.form.get("observacoes", "").strip()

        if not nome:
            flash("Nome do fornecedor é obrigatório.", "danger")
            return redirect(url_for("inserir_fornecedor"))

        if telefone and not validar_telefone(telefone):
            flash("Informe um telefone válido com DDD.", "danger")
            return redirect(url_for("inserir_fornecedor"))

        if email and not validar_email(email):
            flash("Informe um e-mail válido.", "danger")
            return redirect(url_for("inserir_fornecedor"))

        db_write(
            """
            INSERT INTO fornecedores (nome, documento, telefone, email, endereco, observacoes, ativo)
            VALUES (%s, %s, %s, %s, %s, %s, 1)
            """,
            (
                nome,
                valor_ou_none(documento),
                valor_ou_none(telefone),
                valor_ou_none(email),
                valor_ou_none(endereco),
                valor_ou_none(observacoes),
            ),
        )
        flash("Fornecedor cadastrado com sucesso.", "success")
        return redirect(url_for("listar_fornecedores"))

    return render_template("fornecedores/inserir_fornecedor.html")


@app.route("/fornecedores/excluir/<int:fornecedor_id>", methods=["POST"])
@login_required
def excluir_fornecedor(fornecedor_id):
    db_write("UPDATE fornecedores SET ativo = 0, excluido_em = NOW() WHERE id = %s", (fornecedor_id,))
    flash("Fornecedor removido da listagem por exclusão lógica.", "success")
    return redirect(url_for("listar_fornecedores"))


@app.route("/doacoes/listar")
@login_required
def listar_doacoes():
    doacoes = db_select(
        """
        SELECT d.id, d.doador_nome, d.tipo, d.valor, d.data_doacao,
               d.forma_recebimento, d.recorrente, d.status,
               m.nome AS membro, c.nome AS categoria, cf.nome AS conta
        FROM doacoes d
        LEFT JOIN membros m ON m.id = d.membro_id
        LEFT JOIN categorias_financeiras c ON c.id = d.categoria_id
        JOIN contas_financeiras cf ON cf.id = d.conta_id
        ORDER BY d.data_doacao DESC, d.id DESC
        """
    )
    return render_template(
        "doacoes/listar_doacoes.html",
        doacoes=doacoes,
        metricas=gerar_metricas(),
        pendentes=db_scalar("SELECT COUNT(*) AS valor FROM doacoes WHERE status = 'Pendente'"),
    )


@app.route("/doacoes/receber/<int:doacao_id>", methods=["POST"])
@login_required
def receber_doacao(doacao_id):
    doacao = db_one(
        """
        SELECT *
        FROM doacoes
        WHERE id = %s AND status = 'Pendente'
        LIMIT 1
        """,
        (doacao_id,),
    )
    if not doacao:
        flash("Doação pendente não encontrada.", "danger")
        return redirect(url_for("listar_doacoes"))

    with get_connection() as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO lancamentos_financeiros
                    (tipo, categoria_id, conta_id, membro_id, descricao, valor, data_lancamento, criado_por_usuario_id)
                VALUES ('Entrada', %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    doacao["categoria_id"],
                    doacao["conta_id"],
                    doacao["membro_id"],
                    f"Doação - {doacao['tipo']} - {doacao['doador_nome']}",
                    doacao["valor"],
                    doacao["data_doacao"],
                    session.get("usuario_id"),
                ),
            )
            lancamento_id = cursor.lastrowid
            cursor.execute(
                """
                UPDATE doacoes
                SET status = 'Recebida', lancamento_financeiro_id = %s
                WHERE id = %s
                """,
                (lancamento_id, doacao_id),
            )
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()

    flash("Doacao baixada e lancada no financeiro.", "success")
    return redirect(url_for("listar_doacoes"))


@app.route("/doacoes/cancelar/<int:doacao_id>", methods=["POST"])
@login_required
def cancelar_doacao(doacao_id):
    db_write("UPDATE doacoes SET status = 'Cancelada' WHERE id = %s AND status = 'Pendente'", (doacao_id,))
    flash("Doacao pendente cancelada.", "success")
    return redirect(url_for("listar_doacoes"))


@app.route("/doacoes/inserir", methods=["GET", "POST"])
@login_required
def inserir_doacao():
    categorias = listar_categorias_financeiras("Entrada")
    contas = listar_contas_financeiras()
    membros = listar_membros_select()

    if request.method == "POST":
        membro_id = request.form.get("membro_id", "").strip()
        doador_nome = request.form.get("doador_nome", "").strip()
        tipo = request.form.get("tipo", "").strip()
        categoria_id = request.form.get("categoria_id", "").strip()
        conta_id = request.form.get("conta_id", "").strip()
        valor_raw = request.form.get("valor", "").strip().replace(",", ".")
        data_doacao = request.form.get("data_doacao", "").strip()
        forma_recebimento = request.form.get("forma_recebimento", "").strip()
        status = request.form.get("status", "Recebida").strip()
        recorrente = 1 if request.form.get("recorrente") else 0
        observacoes = request.form.get("observacoes", "").strip()

        if not membro_id and not doador_nome:
            flash("Informe o membro ou o nome do doador.", "danger")
            return redirect(url_for("inserir_doacao"))

        if tipo not in TIPOS_DOACAO or forma_recebimento not in FORMAS_RECEBIMENTO or status not in STATUS_DOACAO:
            flash("Revise tipo, forma de recebimento e status.", "danger")
            return redirect(url_for("inserir_doacao"))

        if not categoria_id or not conta_id or not valor_raw or not data_doacao:
            flash("Categoria, conta, valor e data são obrigatórios.", "danger")
            return redirect(url_for("inserir_doacao"))

        try:
            valor = float(valor_raw)
        except ValueError:
            flash("Informe um valor válido.", "danger")
            return redirect(url_for("inserir_doacao"))

        if valor <= 0:
            flash("O valor da doação precisa ser maior que zero.", "danger")
            return redirect(url_for("inserir_doacao"))

        membro_id_db = int(membro_id) if membro_id else None
        doador_final = valor_ou_none(doador_nome) or obter_nome_membro(membro_id_db)
        lancamento_id = None

        with get_connection() as connection:
            cursor = connection.cursor()
            try:
                if status == "Recebida":
                    cursor.execute(
                        """
                        INSERT INTO lancamentos_financeiros
                            (tipo, categoria_id, conta_id, membro_id, descricao, valor, data_lancamento, criado_por_usuario_id)
                        VALUES ('Entrada', %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            int(categoria_id),
                            int(conta_id),
                            membro_id_db,
                            f"Doacao - {tipo} - {doador_final}",
                            valor,
                            data_doacao,
                            session.get("usuario_id"),
                        ),
                    )
                    lancamento_id = cursor.lastrowid

                cursor.execute(
                    """
                    INSERT INTO doacoes (
                        membro_id, doador_nome, tipo, categoria_id, conta_id,
                        lancamento_financeiro_id, valor, data_doacao,
                        forma_recebimento, recorrente, status, observacoes
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        membro_id_db,
                        doador_final,
                        tipo,
                        int(categoria_id),
                        int(conta_id),
                        lancamento_id,
                        valor,
                        data_doacao,
                        forma_recebimento,
                        recorrente,
                        status,
                        valor_ou_none(observacoes),
                    ),
                )
                connection.commit()
            except Exception:
                connection.rollback()
                raise
            finally:
                cursor.close()

        flash("Doacao cadastrada com sucesso.", "success")
        return redirect(url_for("listar_doacoes"))

    return render_template(
        "doacoes/inserir_doacao.html",
        categorias=categorias,
        contas=contas,
        membros=membros,
        tipos=TIPOS_DOACAO,
        formas=FORMAS_RECEBIMENTO,
        status_opcoes=STATUS_DOACAO,
    )


@app.route("/comunicacao/listar")
@login_required
def listar_comunicacao():
    mensagens = db_select(
        """
        SELECT id, canal, destino_tipo, assunto, enviada_em, status
        FROM mensagens
        ORDER BY criado_em DESC, id DESC
        """
    )
    return render_template(
        "comunicacao/listar_comunicacao.html",
        mensagens=mensagens,
        metricas=gerar_metricas(),
        canais=db_scalar("SELECT COUNT(DISTINCT canal) AS valor FROM mensagens"),
        listas=db_scalar("SELECT COUNT(*) AS valor FROM comunicacao_listas WHERE ativo = 1"),
    )


@app.route("/comunicacao/mensagens/inserir", methods=["GET", "POST"])
@login_required
def inserir_mensagem():
    if request.method == "POST":
        canal = request.form.get("canal", "").strip()
        destino_tipo = request.form.get("destino_tipo", "").strip()
        assunto = request.form.get("assunto", "").strip()
        corpo = request.form.get("corpo", "").strip()
        status = request.form.get("status", "Rascunho").strip()
        agendada_para = request.form.get("agendada_para", "").strip()

        canais = ["WhatsApp", "Email", "Interna"]
        destinos = ["Geral", "Ministerio", "Celula", "Lista", "Aniversariantes", "Individual"]
        status_opcoes = ["Rascunho", "Agendada", "Enviada"]

        if canal not in canais or destino_tipo not in destinos or status not in status_opcoes:
            flash("Revise canal, destino e status da mensagem.", "danger")
            return redirect(url_for("inserir_mensagem"))

        if not assunto or not corpo:
            flash("Assunto e mensagem são obrigatórios.", "danger")
            return redirect(url_for("inserir_mensagem"))

        db_write(
            """
            INSERT INTO mensagens
                (canal, assunto, corpo, destino_tipo, status, agendada_para, enviada_em, criado_por_usuario_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                canal,
                assunto,
                corpo,
                destino_tipo,
                status,
                agendada_para.replace("T", " ") if agendada_para else None,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S") if status == "Enviada" else None,
                session.get("usuario_id"),
            ),
        )
        flash("Mensagem registrada com sucesso.", "success")
        return redirect(url_for("listar_comunicacao"))

    return render_template(
        "comunicacao/inserir_mensagem.html",
        canais=["WhatsApp", "Email", "Interna"],
        destinos=["Geral", "Ministerio", "Celula", "Lista", "Aniversariantes", "Individual"],
        status_opcoes=["Rascunho", "Agendada", "Enviada"],
    )


@app.route("/mural/listar")
@login_required
def listar_mural():
    avisos = db_select(
        """
        SELECT id, titulo, categoria, conteudo, imagem_path, status, publicado_em, criado_em
        FROM mural_avisos
        ORDER BY COALESCE(publicado_em, criado_em) DESC, id DESC
        """
    )
    return render_template(
        "mural/listar_mural.html",
        avisos=avisos,
        publicados=db_scalar("SELECT COUNT(*) AS valor FROM mural_avisos WHERE status = 'Publicado'"),
        rascunhos=db_scalar("SELECT COUNT(*) AS valor FROM mural_avisos WHERE status = 'Rascunho'"),
    )


@app.route("/mural/inserir", methods=["GET", "POST"])
@login_required
def inserir_mural():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        categoria = request.form.get("categoria", "").strip()
        conteudo = request.form.get("conteudo", "").strip()
        status = request.form.get("status", "Rascunho").strip()
        imagem_path = salvar_imagem_mural(request.files.get("imagem"))

        if not titulo or not conteudo:
            flash("Título e conteúdo são obrigatórios.", "danger")
            return redirect(url_for("inserir_mural"))

        if status not in STATUS_MURAL:
            flash("Selecione um status válido.", "danger")
            return redirect(url_for("inserir_mural"))

        db_write(
            """
            INSERT INTO mural_avisos
                (titulo, categoria, conteudo, imagem_path, status, publicado_em, criado_por_usuario_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                titulo,
                valor_ou_none(categoria),
                conteudo,
                imagem_path,
                status,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S") if status == "Publicado" else None,
                session.get("usuario_id"),
            ),
        )
        flash("Aviso cadastrado no mural.", "success")
        return redirect(url_for("listar_mural"))

    return render_template("mural/inserir_mural.html", status_opcoes=STATUS_MURAL)


@app.route("/mural/publicar/<int:aviso_id>", methods=["POST"])
@login_required
def publicar_mural(aviso_id):
    db_write(
        "UPDATE mural_avisos SET status = 'Publicado', publicado_em = NOW() WHERE id = %s",
        (aviso_id,),
    )
    flash("Aviso publicado no mural.", "success")
    return redirect(url_for("listar_mural"))


@app.route("/mural/arquivar/<int:aviso_id>", methods=["POST"])
@login_required
def arquivar_mural(aviso_id):
    db_write("UPDATE mural_avisos SET status = 'Arquivado' WHERE id = %s", (aviso_id,))
    flash("Aviso arquivado.", "success")
    return redirect(url_for("listar_mural"))


@app.route("/intercessao/listar")
@login_required
def listar_intercessao():
    pedidos = db_select(
        """
        SELECT p.id, p.solicitante_nome, p.contato, p.categoria, p.pedido, p.status, p.privado, p.oracoes, p.criado_em,
               (SELECT COUNT(*) FROM pedido_oracao_reacoes r WHERE r.pedido_id = p.id) AS reacoes_total,
               (SELECT COUNT(*) FROM pedido_oracao_comentarios c WHERE c.pedido_id = p.id AND c.aprovado = 1) AS comentarios_total
        FROM pedidos_oracao p
        ORDER BY p.criado_em DESC, p.id DESC
        """
    )
    return render_template(
        "intercessao/listar_intercessao.html",
        pedidos=pedidos,
        abertos=db_scalar("SELECT COUNT(*) AS valor FROM pedidos_oracao WHERE status IN ('Pendente', 'Em oracao')"),
        respondidos=db_scalar("SELECT COUNT(*) AS valor FROM pedidos_oracao WHERE status = 'Respondido'"),
    )


@app.route("/intercessao/inserir", methods=["GET", "POST"])
@login_required
def inserir_intercessao():
    if request.method == "POST":
        solicitante_nome = request.form.get("solicitante_nome", "").strip()
        contato = request.form.get("contato", "").strip()
        categoria = request.form.get("categoria", "").strip()
        pedido = request.form.get("pedido", "").strip()
        privado = 1 if request.form.get("privado") else 0

        if not solicitante_nome or not pedido:
            flash("Solicitante e pedido de oração são obrigatórios.", "danger")
            return redirect(url_for("inserir_intercessao"))

        if categoria and categoria not in ORACAO_CATEGORIAS:
            flash("Selecione uma categoria válida.", "danger")
            return redirect(url_for("inserir_intercessao"))

        db_write(
            """
            INSERT INTO pedidos_oracao (solicitante_nome, contato, categoria, pedido, privado)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                solicitante_nome,
                valor_ou_none(contato),
                valor_ou_none(categoria),
                pedido,
                privado,
            ),
        )
        flash("Pedido de oração cadastrado.", "success")
        return redirect(url_for("listar_intercessao"))

    return render_template("intercessao/inserir_intercessao.html", categorias=ORACAO_CATEGORIAS)


@app.route("/intercessao/orar/<int:pedido_id>", methods=["POST"])
@login_required
def orar_intercessao(pedido_id):
    db_write(
        """
        UPDATE pedidos_oracao
        SET oracoes = oracoes + 1,
            status = CASE WHEN status = 'Pendente' THEN 'Em oracao' ELSE status END
        WHERE id = %s
        """,
        (pedido_id,),
    )
    flash("Oração registrada no pedido.", "success")
    return redirect(url_for("listar_intercessao"))


@app.route("/intercessao/responder/<int:pedido_id>", methods=["POST"])
@login_required
def responder_intercessao(pedido_id):
    db_write("UPDATE pedidos_oracao SET status = 'Respondido' WHERE id = %s", (pedido_id,))
    flash("Pedido marcado como respondido.", "success")
    return redirect(url_for("listar_intercessao"))


@app.route("/intercessao/arquivar/<int:pedido_id>", methods=["POST"])
@login_required
def arquivar_intercessao(pedido_id):
    db_write("UPDATE pedidos_oracao SET status = 'Arquivado' WHERE id = %s", (pedido_id,))
    flash("Pedido arquivado.", "success")
    return redirect(url_for("listar_intercessao"))


@app.route("/relatorios/listar")
@login_required
def listar_relatorios():
    grupos = montar_grupos_relatorio()
    linhas = montar_linhas_relatorio()
    return render_template(
        "relatorios/listar_relatorios.html",
        linhas=linhas,
        grupos=grupos,
        metricas=gerar_metricas(),
    )


@app.route("/relatorios/exportar/excel")
@login_required
def exportar_relatorio_excel():
    grupos = montar_grupos_relatorio()
    html = [
        "<html><head><meta charset='utf-8'><style>",
        "body{font-family:Arial,sans-serif;color:#1d2636}",
        "h1{color:#21435e} h2{background:#21435e;color:white;padding:8px}",
        "table{border-collapse:collapse;width:100%;margin-bottom:18px}",
        "th,td{border:1px solid #d8dee6;padding:8px;text-align:left}",
        "th{background:#f5efe6;color:#1d2636}",
        "</style></head><body>",
        "<h1>Igreja Viva - Relatórios do Sistema de Membresia</h1>",
        f"<p>Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>",
    ]
    for grupo in grupos:
        html.append(f"<h2>{grupo['modulo']}</h2>")
        html.append(f"<p>{grupo['descricao']}</p>")
        html.append("<table><tr><th>Relatório</th><th>Indicador</th><th>Status</th></tr>")
        html.extend("<tr>" + "".join(f"<td>{valor}</td>" for valor in linha) + "</tr>" for linha in grupo["linhas"])
        html.append("</table>")
    html.append("</body></html>")
    return Response(
        "\n".join(html),
        headers={"Content-Disposition": "attachment; filename=relatorios_membresia.xls"},
        mimetype="application/vnd.ms-excel",
    )


@app.route("/relatorios/exportar/pdf")
@login_required
def exportar_relatorio_pdf():
    conteudo = pdf_simples("Relatórios por categoria", montar_grupos_relatorio())
    return Response(
        conteudo,
        headers={"Content-Disposition": "attachment; filename=relatorios_membresia.pdf"},
        mimetype="application/pdf",
    )


@app.route("/configuracoes/listar", methods=["GET", "POST"])
@login_required
def listar_configuracoes():
    if request.method == "POST":
        acao = request.form.get("acao", "").strip()
        if acao == "igreja":
            nome = request.form.get("nome", "").strip()
            email = request.form.get("email", "").strip().lower()
            telefone = request.form.get("telefone", "").strip()
            endereco = request.form.get("endereco", "").strip()

            if not nome:
                flash("Nome da igreja é obrigatório.", "danger")
                return redirect(url_for("listar_configuracoes"))

            igreja_atual = db_one("SELECT id FROM igrejas ORDER BY id LIMIT 1")
            if igreja_atual:
                db_write(
                    """
                    UPDATE igrejas
                    SET nome = %s, email = %s, telefone = %s, endereco = %s
                    WHERE id = %s
                    """,
                    (nome, valor_ou_none(email), valor_ou_none(telefone), valor_ou_none(endereco), igreja_atual["id"]),
                )
            else:
                db_write(
                    """
                    INSERT INTO igrejas (nome, email, telefone, endereco)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (nome, valor_ou_none(email), valor_ou_none(telefone), valor_ou_none(endereco)),
                )
            salvar_config("igreja.nome", nome, "Nome exibido no sistema")
            flash("Dados da igreja atualizados.", "success")

        elif acao == "parametros":
            salvar_config("paginacao.tamanho_padrao", request.form.get("paginacao", "20"), "Quantidade padrão de registros por página")
            salvar_config("frequencia.baixa.percentual", request.form.get("frequencia", "50"), "Percentual mínimo de presença mensal antes de alerta")
            salvar_config("backup.agendamento", request.form.get("backup", "Diário às 02:00"), "Rotina recomendada de backup do banco MySQL")
            flash("Parâmetros atualizados.", "success")

        elif acao == "app_usuario":
            salvar_config("programacao.domingo", request.form.get("programacao_domingo", ""), "Programação fixa de domingo exibida no app do usuário")
            salvar_config("programacao.quarta", request.form.get("programacao_quarta", ""), "Programação fixa de quarta exibida no app do usuário")
            salvar_config("programacao.celulas", request.form.get("programacao_celulas", ""), "Programação de células exibida no app do usuário")
            salvar_config("doacao.pix", request.form.get("doacao_pix", ""), "Chave PIX exibida no app do usuário")
            salvar_config("doacao.banco", request.form.get("doacao_banco", ""), "Dados bancários exibidos no app do usuário")
            salvar_config("doacao.mensagem", request.form.get("doacao_mensagem", ""), "Mensagem de contribuição exibida no app do usuário")
            flash("Informações do app do usuário atualizadas.", "success")

        elif acao == "backup":
            salvar_config("backup.ultimo", datetime.now().strftime("%d/%m/%Y %H:%M"), "Ultimo backup logico registrado")
            flash("Backup lógico registrado nas configurações.", "success")

        return redirect(url_for("listar_configuracoes"))

    configuracoes = db_select(
        """
        SELECT chave, valor
        FROM configuracoes_sistema
        ORDER BY chave
        """
    )
    return render_template(
        "configuracoes/listar_configuracoes.html",
        igreja=obter_igreja(),
        configuracoes=configuracoes,
        paginacao=obter_config("paginacao.tamanho_padrao", "20"),
        frequencia=obter_config("frequencia.baixa.percentual", "50"),
        backup=obter_config("backup.agendamento", "Diário às 02:00"),
        ultimo_backup=obter_config("backup.ultimo", "-"),
        programacao_domingo=obter_config("programacao.domingo", "Culto de celebracao"),
        programacao_quarta=obter_config("programacao.quarta", "Encontro de oração e ensino"),
        programacao_celulas=obter_config("programacao.celulas", "Durante a semana, conforme cada bairro"),
        doacao_pix=obter_config("doacao.pix", ""),
        doacao_banco=obter_config("doacao.banco", ""),
        doacao_mensagem=obter_config("doacao.mensagem", "Contribua com alegria e acompanhe a secretaria para obter comprovantes."),
        perfis_total=db_scalar("SELECT COUNT(*) AS valor FROM perfis", default=0),
    )


@app.route("/configuracoes/igreja")
@login_required
def configuracoes_igreja():
    igreja = obter_igreja()
    linhas = [
        ["Nome", igreja.get("nome") or "-"],
        ["E-mail", igreja.get("email") or "-"],
        ["Telefone", igreja.get("telefone") or "-"],
        ["Endereço", igreja.get("endereco") or "-"],
    ]
    return renderizar_resumo_configuracao(
        "Igreja",
        "Dados institucionais usados no sistema.",
        [card("Igreja", igreja.get("nome") or "-"), card("Usuários", gerar_metricas()["usuarios_ativos"]), card("Membros", gerar_metricas()["membros_ativos"])],
        ["Campo", "Valor"],
        linhas,
    )


@app.route("/configuracoes/historia")
@login_required
def configuracoes_historia():
    linhas = [
        ["História da igreja", obter_config("igreja.historia", "Não cadastrada")],
        ["Missão", obter_config("igreja.missao", "Não cadastrada")],
        ["Visão", obter_config("igreja.visao", "Não cadastrada")],
        ["Valores", obter_config("igreja.valores", "Não cadastrados")],
    ]
    return renderizar_resumo_configuracao(
        "História",
        "Informações institucionais da igreja para evolução do módulo público e administrativo.",
        [card("Campos", len(linhas)), card("Igreja", obter_config("igreja.nome", "Igreja Viva")), card("Status", "Base")],
        ["Informação", "Valor"],
        linhas,
    )


@app.route("/configuracoes/informacoes")
@login_required
def configuracoes_informacoes():
    linhas = db_select(
        """
        SELECT chave, valor
        FROM configuracoes_sistema
        WHERE chave LIKE 'igreja.%'
        ORDER BY chave
        """
    )
    return renderizar_resumo_configuracao(
        "Informações",
        "Informações gerais gravadas na configuração da igreja.",
        [card("Registros", len(linhas)), card("Configurações", db_scalar("SELECT COUNT(*) AS valor FROM configuracoes_sistema")), card("Igreja", obter_config("igreja.nome", "Igreja Viva"))],
        ["Chave", "Valor"],
        [[linha["chave"], linha.get("valor") or "-"] for linha in linhas],
    )


@app.route("/configuracoes/programacao")
@login_required
def configuracoes_programacao():
    eventos = db_select(
        """
        SELECT nome, data_inicio, local, status
        FROM eventos
        ORDER BY data_inicio DESC, id DESC
        LIMIT 12
        """
    )
    return render_template(
        "modulos/resumo.html",
        titulo="Programação",
        subtitulo="Eventos cadastrados que compõem a programação da igreja.",
        cards=[
            card("Eventos", gerar_metricas()["eventos"]),
            card("Agendados", db_scalar("SELECT COUNT(*) AS valor FROM eventos WHERE status = 'Agendado'")),
            card("Realizados", db_scalar("SELECT COUNT(*) AS valor FROM eventos WHERE status = 'Realizado'")),
        ],
        filtros=[],
        cabecalhos=["Evento", "Data", "Local", "Status"],
        linhas=[[evento["nome"], data_br(evento["data_inicio"]), evento.get("local") or "-", evento["status"]] for evento in eventos],
        acao_url=url_for("inserir_evento"),
        acao_label="Novo evento",
    )


@app.route("/configuracoes/permissoes")
@login_required
def configuracoes_permissoes():
    linhas = db_select(
        """
        SELECT p.nome, p.descricao, COUNT(pp.permissao_id) AS permissoes
        FROM perfis p
        LEFT JOIN perfil_permissao pp ON pp.perfil_id = p.id
        GROUP BY p.id
        ORDER BY p.nome
        """
    )
    return render_template(
        "modulos/resumo.html",
        titulo="Permissões de acesso",
        subtitulo="Perfis e permissões cadastrados para controle de acesso administrativo.",
        cards=[
            card("Perfis", len(linhas)),
            card("Usuários ativos", gerar_metricas()["usuarios_ativos"]),
            card("Permissões", db_scalar("SELECT COUNT(*) AS valor FROM permissoes")),
        ],
        filtros=[],
        cabecalhos=["Perfil", "Descrição", "Permissões"],
        linhas=[[linha["nome"], linha.get("descricao") or "-", linha.get("permissoes") or 0] for linha in linhas],
        acao_url=url_for("listar_usuarios"),
        acao_label="Gerenciar usuários",
    )


@app.route("/configuracoes/app")
@login_required
def configuracoes_app():
    linhas = [
        ["Frente do usuário", url_for("app_usuario_inicio")],
        ["Programação domingo", obter_config("programacao.domingo", "Culto de celebração")],
        ["Programação quarta", obter_config("programacao.quarta", "Encontro de oração e ensino")],
        ["Programação células", obter_config("programacao.celulas", "Durante a semana, conforme cada bairro")],
        ["Chave PIX", obter_config("doacao.pix", "Não cadastrada")],
        ["Dados bancários", obter_config("doacao.banco", "Não cadastrados")],
        ["Mensagem de doação", obter_config("doacao.mensagem", "Contribua com alegria e acompanhe a secretaria para obter comprovantes.")],
        ["Registros por página", obter_config("paginacao.tamanho_padrao", "20")],
        ["Baixa frequência", f"{obter_config('frequencia.baixa.percentual', '50')}%"],
        ["Backup", obter_config("backup.agendamento", "Diário às 02:00")],
        ["Último backup", obter_config("backup.ultimo", "-")],
    ]
    return renderizar_resumo_configuracao(
        "App",
        "Parâmetros da aplicação administrativa e do app público do usuário.",
        [card("Parâmetros", len(linhas)), card("App usuário", "Ativo"), card("Status", "Ativo")],
        ["Parâmetro", "Valor"],
        linhas,
    )


@app.route("/configuracoes/modulos")
@login_required
def configuracoes_modulos():
    metricas = gerar_metricas()
    modulos = [
        ["Financeiro", "Ativo", moeda_br(metricas["saldo"])],
        ["Pessoal", "Ativo", metricas["membros_ativos"]],
        ["Ministérios", "Ativo", metricas["ministerios"]],
        ["Células", "Ativo", metricas["celulas"]],
        ["Comunicação", "Ativo", metricas["mensagens"]],
        ["Intercessão", "Ativo", metricas["pedidos_oracao"]],
    ]
    return renderizar_resumo_configuracao(
        "Módulos",
        "Visão dos módulos ativos no sistema e seus principais indicadores.",
        [card("Módulos", len(modulos)), card("Usuários", metricas["usuarios_ativos"]), card("Status", "Ativo")],
        ["Módulo", "Status", "Indicador"],
        modulos,
    )


@app.route("/sobre-equipe")
def equipe():
    return render_template("sobre_equipe.html")


if __name__ == "__main__":
    app.run(debug=True)
