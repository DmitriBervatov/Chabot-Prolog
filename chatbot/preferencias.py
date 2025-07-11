from typing import List, Optional, Any
import json

class PreferenciasUsuario:
    def __init__(self):
        self.generos_favoritos: List[str] = []
        self.directores_favoritos: List[str] = []
        self.peliculas_vistas: List[str] = []
        self.peliculas_gustadas: List[str] = []
        self.peliculas_no_gustadas: List[str] = []
        self.duracion_preferida: Optional[str] = None
        self.epoca_preferida: Optional[str] = None

    def cargar(self, ruta: str = "preferencias.json") -> None:
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                datos: dict[str, Any] = json.load(f)
                self.generos_favoritos = datos.get("generos_favoritos", [])
                self.directores_favoritos = datos.get(
                    "directores_favoritos", [])
                self.peliculas_vistas = datos.get("peliculas_vistas", [])
                self.peliculas_gustadas = datos.get("peliculas_gustadas", [])
                self.peliculas_no_gustadas = datos.get(
                    "peliculas_no_gustadas", [])
                self.duracion_preferida = datos.get("duracion_preferida")
                self.epoca_preferida = datos.get("epoca_preferida")
        except FileNotFoundError:
            pass  # No hay preferencias guardadas aún

    def guardar(self, ruta: str = "preferencias.json") -> None:
        datos: dict[str, object] = {
            "generos_favoritos": self.generos_favoritos,
            "directores_favoritos": self.directores_favoritos,
            "peliculas_vistas": self.peliculas_vistas,
            "peliculas_gustadas": self.peliculas_gustadas,
            "peliculas_no_gustadas": self.peliculas_no_gustadas,
            "duracion_preferida": self.duracion_preferida,
            "epoca_preferida": self.epoca_preferida,
        }
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)

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
