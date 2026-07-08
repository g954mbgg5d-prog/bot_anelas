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

    if minutos >= 60:
        return 100

    pontos = [
        (15, 1),
        (20, 5),
        (30, 15),
        (40, 30),
        (50, 55),
        (55, 75),
        (60, 100),
    ]

    for i in range(len(pontos) - 1):

        minuto_inicio, chance_inicio = pontos[i]
        minuto_fim, chance_fim = pontos[i + 1]

        if minuto_inicio <= minutos < minuto_fim:

            progresso = (
                minutos - minuto_inicio
            ) / (
                minuto_fim - minuto_inicio
            )

            chance = chance_inicio + progresso * (
                chance_fim - chance_inicio
            )

            return round(chance)

    return 100


def deve_publicar():

    minutos = minutos_desde_ultima_publicacao()

    chance = chance_publicacao(minutos)

    sorteio = random.uniform(0, 100)

    return sorteio <= chance
