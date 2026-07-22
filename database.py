import hashlib
import sqlite3
from datetime import datetime

from config import (
    DATABASE_PATH,
    STATUS_PUBLISHED,
    COOLDOWNS,
)


# ==================================================
# CONEXÃO
# ==================================================

def get_connection():

    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row

    return conn


# ==================================================
# INIT
# ==================================================

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

    cur.execute("""
    CREATE TABLE IF NOT EXISTS recent_items (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        categoria TEXT NOT NULL,

        indice INTEGER NOT NULL,

        usado_em TEXT NOT NULL

    )
    """)

    cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_recent_categoria
    ON recent_items (
        categoria,
        id DESC
    )
    """)

    conn.commit()
    conn.close()


# ==================================================
# HASH
# ==================================================

def gerar_hash(texto):

    return hashlib.sha256(
        texto.encode("utf-8")
    ).hexdigest()


def tweet_existe(texto):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT EXISTS(

            SELECT 1

            FROM tweets

            WHERE hash = ?

        )
        """,
        (
            gerar_hash(texto),
        )
    )

    existe = bool(
        cur.fetchone()[0]
    )

    conn.close()

    return existe


# ==================================================
# TWEETS
# ==================================================

def inserir_tweet(
    texto,
    status=STATUS_PUBLISHED
):

    agora = datetime.utcnow().isoformat()

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            INSERT INTO tweets (

                texto,

                hash,

                status,

                criado_em,

                publicado_em

            )

            VALUES (?, ?, ?, ?, ?)
            """,
            (
                texto,
                gerar_hash(texto),
                status,
                agora,
                agora,
            )
        )

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


# ==================================================
# METADATA
# ==================================================

def set_metadata(
    chave,
    valor
):

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
            str(valor),
        )
    )

    conn.commit()
    conn.close()


def get_metadata(
    chave,
    default=None
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT valor

        FROM metadata

        WHERE chave = ?
        """,
        (
            chave,
        )
    )

    resultado = cur.fetchone()

    conn.close()

    if resultado:

        return resultado["valor"]

    return default


# ==================================================
# COOLDOWN
# ==================================================

def obter_indices_bloqueados(categoria):

    cooldown = COOLDOWNS.get(
        categoria,
        0
    )

    if cooldown <= 0:

        return set()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT indice

        FROM recent_items

        WHERE categoria = ?

        ORDER BY id DESC

        LIMIT ?
        """,
        (
            categoria,
            cooldown,
        )
    )

    resultado = {

        row["indice"]

        for row in cur.fetchall()

    }

    conn.close()

    return resultado


def limpar_recent_items(categoria):

    manter = COOLDOWNS.get(
        categoria,
        0
    ) + 5

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        DELETE FROM recent_items

        WHERE categoria = ?

        AND id NOT IN (

            SELECT id

            FROM recent_items

            WHERE categoria = ?

            ORDER BY id DESC

            LIMIT ?

        )
        """,
        (
            categoria,
            categoria,
            manter,
        )
    )

    conn.commit()
    conn.close()


def registrar_item(
    categoria,
    indice
):

    manter = max(
        COOLDOWNS.get(categoria, 0),
        1,
    )

    conn = get_connection()
    cur = conn.cursor()

    agora = datetime.utcnow().isoformat()

    #
    # Registra o item
    #

    cur.execute(
        """
        INSERT INTO recent_items (

            categoria,

            indice,

            usado_em

        )

        VALUES (?, ?, ?)
        """,
        (
            categoria,
            indice,
            agora,
        )
    )

    #
    # Remove tudo que passou do cooldown
    #

    cur.execute(
        """
        DELETE FROM recent_items

        WHERE categoria = ?

        AND id NOT IN (

            SELECT id

            FROM (

                SELECT id

                FROM recent_items

                WHERE categoria = ?

                ORDER BY id DESC

                LIMIT ?

            )

        )
        """,
        (
            categoria,
            categoria,
            manter,
        )
    )

    conn.commit()
    conn.close()

def registrar_cooldowns(manager):

    cooldowns = manager.cooldowns()

    for categoria, indices in cooldowns.items():

        for indice in indices:

            registrar_item(
                categoria,
                indice,
            )

