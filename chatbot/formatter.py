

def format_movie_info(titulo: str, genero: str, anio: int, director: str, duracion: int) -> str:
    return (
        f"🎬 **{titulo}**\n"
        f"   📂 Género: {genero.replace('_', ' ').title()}\n"
        f"   📅 Año: {anio}\n"
        f"   🎭 Director: {director}\n"
        f"   ⏱️ Duración: {duracion} minutos"
    )


def pintar(texto: str, color: str="green") -> str:
    colores = {
        "green": "\033[92m",
        "yellow": "\033[93m",
        "red": "\033[91m",
        "blue": "\033[94m",
        "cyan": "\033[96m",
        "magenta": "\033[95m",
        "reset": "\033[0m"
    }
    return f"{colores.get(color, colores['green'])}{texto}{colores['reset']}"
