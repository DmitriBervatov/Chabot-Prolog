

def format_movie_info(titulo: str, genero: str, anio: int, director: str, duracion: int) -> str:
    return (
        f"🎬 **{titulo}**\n"
        f"   📂 Género: {genero.replace('_', ' ').title()}\n"
        f"   📅 Año: {anio}\n"
        f"   🎭 Director: {director}\n"
        f"   ⏱️ Duración: {duracion} minutos"
    )
    
