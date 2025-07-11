from typing import Any
from chatbot.recomendaciones import formatear_resultado
import difflib


def recomendar_peliculas_similares(bot: Any, titulo: str) -> str:
    if not titulo:
        return "No entendí a qué película te refieres. ¿Podrías escribir el título completo?"

    # Verifica si la película existe
    existe = bot.prolog.query(f"pelicula('{titulo}', _, _, _, _)")
    if not existe:
        sugerencia = sugerir_titulo(bot, titulo)
        return f"No tengo información sobre '{titulo}'. {sugerencia}".strip()

    # Busca películas similares
    resultados = bot.prolog.query(f"pelicula_similar('{titulo}', P2)")
    if not resultados:
        sugerencia = sugerir_titulo(bot, titulo)
        return f"No encontré películas similares a '{titulo}'. {sugerencia}".strip()

    return formatear_resultado(bot, resultados, f"🎞️ Películas similares a '{titulo}':", clave="P2")


def sugerir_titulo(bot: Any, titulo_usuario: str) -> str:
    titulos = [r["P"] for r in bot.prolog.query("pelicula(P, _, _, _, _)")]
    sugerencias = difflib.get_close_matches(
        titulo_usuario, titulos, n=1, cutoff=0.6)
    if sugerencias:
        return f"¿Quizás quisiste decir '{sugerencias[0]}'?"
    return ""
