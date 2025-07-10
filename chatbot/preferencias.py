from typing import List, Optional


class PreferenciasUsuario:
    def __init__(self):
        self.generos_favoritos: List[str] = []
        self.directores_favoritos: List[str] = []
        self.peliculas_vistas: List[str] = []
        self.peliculas_gustadas: List[str] = []
        self.peliculas_no_gustadas: List[str] = []
        self.duracion_preferida: Optional[str] = None
        self.epoca_preferida: Optional[str] = None

    def agregar_genero(self, genero: str) -> None:
        if genero not in self.generos_favoritos:
            self.generos_favoritos.append(genero)

    def agregar_director(self, director: str) -> None:
        if director not in self.directores_favoritos:
            self.directores_favoritos.append(director)

    def marcar_pelicula_vista(self, pelicula: str) -> None:
        if pelicula not in self.peliculas_vistas:
            self.peliculas_vistas.append(pelicula)

    def marcar_pelicula_gustada(self, pelicula: str) -> None:
        if pelicula not in self.peliculas_gustadas:
            self.peliculas_gustadas.append(pelicula)
            if pelicula in self.peliculas_no_gustadas:
                self.peliculas_no_gustadas.remove(pelicula)

    def marcar_pelicula_no_gustada(self, pelicula: str) -> None:
        if pelicula not in self.peliculas_no_gustadas:
            self.peliculas_no_gustadas.append(pelicula)
            if pelicula in self.peliculas_gustadas:
                self.peliculas_gustadas.remove(pelicula)

    def establecer_duracion(self, duracion: str) -> None:
        self.duracion_preferida = duracion

    def establecer_epoca(self, epoca: str) -> None:
        self.epoca_preferida = epoca

    def obtener_resumen(self) -> str:
        resumen: list[str] = []

        if self.generos_favoritos:
            resumen.append(
                f"📌 Géneros favoritos: {', '.join(self.generos_favoritos)}")

        if self.directores_favoritos:
            resumen.append(
                f"🎬 Directores favoritos: {', '.join(self.directores_favoritos)}")

        if self.peliculas_gustadas:
            resumen.append(
                f"👍 Películas que te gustaron: {', '.join(self.peliculas_gustadas)}")

        if self.duracion_preferida:
            resumen.append(
                f"⏱️ Prefieres películas de duración {self.duracion_preferida}")

        if self.epoca_preferida:
            resumen.append(
                f"📅 Prefieres películas de época {self.epoca_preferida}")

        if not resumen:
            return "Aún no tengo registradas tus preferencias. ¡Cuéntame más sobre tus gustos cinematográficos!"

        return "\n".join(resumen)
