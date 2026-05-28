from pathlib import Path

import mysql.connector

from db import DB_CONFIG


BASE_DIR = Path(__file__).resolve().parent
SQL_FILES = [
    BASE_DIR / "database" / "migrations" / "0001_core_security.sql",
    BASE_DIR / "database" / "migrations" / "0002_membresia_core.sql",
    BASE_DIR / "database" / "seeds" / "0001_rbac_perfis_permissoes.sql",
]


def conectar_sem_banco():
    config = dict(DB_CONFIG)
    config.pop("database", None)
    return mysql.connector.connect(**config)


def executar_arquivo(cursor, caminho):
    sql = caminho.read_text(encoding="utf-8")
    comandos = [comando.strip() for comando in sql.split(";") if comando.strip()]
    for comando in comandos:
        cursor.execute(comando)


def coluna_existe(cursor, tabela, coluna):
    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM information_schema.columns
        WHERE table_schema = %s
          AND table_name = %s
          AND column_name = %s
        """,
        (DB_CONFIG["database"], tabela, coluna),
    )
    return cursor.fetchone()[0] > 0


def tabela_existe(cursor, tabela):
    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM information_schema.tables
        WHERE table_schema = %s
          AND table_name = %s
        """,
        (DB_CONFIG["database"], tabela),
    )
    return cursor.fetchone()[0] > 0


def ajustes_compatibilidade(cursor):
    if tabela_existe(cursor, "ministerios") and not coluna_existe(cursor, "ministerios", "vagas"):
        cursor.execute("ALTER TABLE ministerios ADD COLUMN vagas INT NOT NULL DEFAULT 0 AFTER dia_reuniao")

    if tabela_existe(cursor, "historico_espiritual"):
        cursor.execute("ALTER TABLE historico_espiritual MODIFY tipo VARCHAR(80) NOT NULL")

    if tabela_existe(cursor, "eventos") and not coluna_existe(cursor, "eventos", "banner_path"):
        cursor.execute("ALTER TABLE eventos ADD COLUMN banner_path VARCHAR(255) NULL AFTER local")

    if tabela_existe(cursor, "lancamentos_financeiros") and not coluna_existe(cursor, "lancamentos_financeiros", "fornecedor_id"):
        cursor.execute(
            "ALTER TABLE lancamentos_financeiros ADD COLUMN fornecedor_id BIGINT UNSIGNED NULL AFTER membro_id"
        )


def main():
    database = DB_CONFIG["database"]

    conn = conectar_sem_banco()
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{database}` "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    try:
        for caminho in SQL_FILES:
            executar_arquivo(cursor, caminho)
        ajustes_compatibilidade(cursor)
        conn.commit()
        print(f'Banco "{database}" configurado com sucesso.')
        print("Usuario inicial: admin@igreja.org")
        print("Senha inicial: admin123")
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()
