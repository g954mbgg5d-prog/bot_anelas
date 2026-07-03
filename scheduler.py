import random
from datetime import datetime

from database import get_connection


def minutos_desde_ultima_publicacao():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT publicado_em
        FROM tweets
        WHERE status = 'published'
        ORDER BY publicado_em DESC
        LIMIT 1
    """)

    row = cur.fetchone()

    conn.close()

    if row is None:
        return None

    publicado_em = row["publicado_em"]

    if not publicado_em:
        return None

    ultima_data = datetime.fromisoformat(
        publicado_em
    )

    agora = datetime.utcnow()

    return (
        agora - ultima_data
    ).total_seconds() / 60


def chance_publicacao(minutos):

    if minutos is None:
        return 100

    if minutos < 15:
        return 0

    if minutos < 30:
        return 2

    if minutos < 60:
        return 5

    if minutos < 90:
        return 15

    if minutos < 120:
        return 30

    return 60


def deve_publicar():

    minutos = (
        minutos_desde_ultima_publicacao()
    )

    chance = chance_publicacao(
        minutos
    )

    sorteio = random.uniform(
        0,
        100
    )

    return sorteio <= chance
