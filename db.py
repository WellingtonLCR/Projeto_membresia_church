import os
from contextlib import contextmanager

import mysql.connector
from mysql.connector import pooling


DB_CONFIG = {
    "host": os.environ.get("MYSQL_HOST", "localhost"),
    "port": int(os.environ.get("MYSQL_PORT", "3306")),
    "user": os.environ.get("MYSQL_USER", "root"),
    "password": os.environ.get("MYSQL_PASSWORD", ""),
    "database": os.environ.get("MYSQL_DATABASE", "membresia_church"),
    "charset": "utf8mb4",
    "use_unicode": True,
    "use_pure": True,
    "autocommit": False,
    "connection_timeout": 10,
    "time_zone": "-03:00",
    "sql_mode": (
        "STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,"
        "ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION"
    ),
}

POOL = None


def get_pool():
    global POOL
    if POOL is None:
        POOL = pooling.MySQLConnectionPool(
            pool_name="membresia_pool",
            pool_size=int(os.environ.get("MYSQL_POOL_SIZE", "5")),
            pool_reset_session=True,
            **DB_CONFIG,
        )
    return POOL


@contextmanager
def get_connection():
    connection = get_pool().get_connection()
    try:
        yield connection
    finally:
        connection.close()


def execute_query(sql, params=None, fetch=True):
    with get_connection() as connection:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(sql, params or ())
            if fetch:
                return cursor.fetchall()
            connection.commit()
            return cursor.rowcount
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()


def execute_one(sql, params=None):
    rows = execute_query(sql, params, fetch=True)
    return rows[0] if rows else None
