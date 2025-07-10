from typing import Any
import difflib


def sugerir_titulo(bot: Any, titulo_usuario: str) -> str:
    titulos = [r["P"] for r in bot.prolog.query("pelicula(P, _, _, _, _)")]
    sugerencias = difflib.get_close_matches(
        titulo_usuario, titulos, n=1, cutoff=0.6)
    if sugerencias:
        return f"¿Quizás quisiste decir '{sugerencias[0]}'?"
    return ""
