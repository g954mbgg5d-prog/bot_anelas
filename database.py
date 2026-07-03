import sqlite3
import hashlib
from datetime import datetime

from config import (
    DATABASE_PATH,
    STATUS_PENDING,
    STATUS_PUBLISHED,
    STATUS_DISCARDED,
)


def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tweets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        texto TEXT NOT NULL,

        hash TEXT NOT NULL UNIQUE,

        status TEXT NOT NULL,

        criado_em TEXT NOT NULL,

        publicado_em TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS metadata (
        chave TEXT PRIMARY KEY,
        valor TEXT
    )
    """)

    conn.commit()
    conn.close()


def gerar_hash(texto):

    return hashlib.sha256(
        texto.encode("utf-8")
    ).hexdigest()


def tweet_existe(texto):

    tweet_hash = gerar_hash(texto)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id
        FROM tweets
        WHERE hash = ?
        """,
        (tweet_hash,)
    )

    resultado = cur.fetchone()

    conn.close()

    return resultado is not None


def inserir_tweet(
    texto,
    status=STATUS_PENDING
):

    tweet_hash = gerar_hash(texto)

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            INSERT INTO tweets (
                texto,
                hash,
                status,
                criado_em
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                texto,
                tweet_hash,
                status,
                datetime.utcnow().isoformat()
            )
        )

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


def contar_pending():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT COUNT(*)
        FROM tweets
        WHERE status = ?
        """,
        (STATUS_PENDING,)
    )

    total = cur.fetchone()[0]

    conn.close()

    return total


def obter_proximo_pendente():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM tweets
        WHERE status = ?
        ORDER BY criado_em ASC
        LIMIT 1
        """,
        (STATUS_PENDING,)
    )

    tweet = cur.fetchone()

    conn.close()

    return tweet


def marcar_publicado(tweet_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE tweets
        SET
            status = ?,
            publicado_em = ?
        WHERE id = ?
        """,
        (
            STATUS_PUBLISHED,
            datetime.utcnow().isoformat(),
            tweet_id
        )
    )

    conn.commit()
    conn.close()


def marcar_descartado(tweet_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE tweets
        SET status = ?
        WHERE id = ?
        """,
        (
            STATUS_DISCARDED,
            tweet_id
        )
    )

    conn.commit()
    conn.close()


def set_metadata(chave, valor):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR REPLACE INTO metadata (
            chave,
            valor
        )
        VALUES (?, ?)
        """,
        (
            chave,
            str(valor)
        )
    )

    conn.commit()
    conn.close()


def get_metadata(chave, default=None):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT valor
        FROM metadata
        WHERE chave = ?
        """,
        (chave,)
    )

    resultado = cur.fetchone()

    conn.close()

    if resultado:
        return resultado["valor"]

    return default
