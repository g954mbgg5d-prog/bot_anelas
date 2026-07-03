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

    # Nunca publicou nada
    if minutos is None:
        return 100

    # Janela de silêncio obrigatória
    if minutos < 15:
        return 0

    # Após 1 hora publica obrigatoriamente
    if minutos >= 60:
        return 100

    # Crescimento exponencial entre 15 e 60 min
    progresso = (
        minutos - 15
    ) / 45

    chance = (
        progresso ** 3
    ) * 100

    return round(chance)


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
