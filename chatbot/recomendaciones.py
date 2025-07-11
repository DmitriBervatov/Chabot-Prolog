from typing import Any
from chatbot.formatter import format_movie_info
import difflib

def sugerir_titulo(bot: Any, titulo_usuario: str) -> str:
    # Obtiene todos los títulos de la base de datos Prolog
    titulos = [r["P"] for r in bot.prolog.query("pelicula(P, _, _, _, _)")]
    sugerencias = difflib.get_close_matches(
        titulo_usuario, titulos, n=1, cutoff=0.6)
    if sugerencias:
        return f"¿Quizás quisiste decir '{sugerencias[0]}'?"
    return ""


def recomendar_peliculas_genero(bot: Any, genero: str) -> str:
    resultados = bot.prolog.query(f"recomendar_por_genero({genero}, P)")
    return formatear_resultado(bot, resultados, f"🎬 Películas de {genero.replace('_', ' ')}:")


def recomendar_peliculas_duracion(bot: Any, duracion: str) -> str:
    resultados = bot.prolog.query(f"recomendar_por_duracion({duracion}, P)")
    return formatear_resultado(bot, resultados, f"⏱️ Películas de duración {duracion}:")


def recomendar_peliculas_epoca(bot: Any, epoca: str) -> str:
    resultados = bot.prolog.query(f"recomendar_por_epoca({epoca}, P)")
    return formatear_resultado(bot, resultados, f"📅 Películas de época {epoca}:")


def recomendar_peliculas_estado_animo(bot: Any, regla: str) -> str:
    resultados = bot.prolog.query(f"{regla}(P)")
    return formatear_resultado(bot, resultados, "🎭 Te recomiendo estas películas para tu estado de ánimo:")


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
        return f"No encontré películas similares a '{titulo}' 😕"

    return formatear_resultado(bot, resultados, f"🎞️ Películas similares a '{titulo}':", clave="P2")


def formatear_resultado(bot: Any, resultados: list[dict[str, Any]], encabezado: str, clave: str = "P") -> str:
    if not resultados:
        return "No encontré películas para esa búsqueda."

    respuesta = f"{encabezado}\n\n"
    for r in resultados[:3]:
        titulo = r[clave]
        # Guarda el título recomendado
        if hasattr(bot, "peliculas_recomendadas"):
            bot.peliculas_recomendadas.add(titulo)
        info = bot.prolog.query(f"info_pelicula('{titulo}', G, A, D, Dur)")
        if info:
            datos = info[0]
            respuesta += format_movie_info(
                titulo, datos["G"], datos["A"], datos["D"], datos["Dur"]
            ) + "\n\n"
    return respuesta.strip()