from pyswip import Prolog
from typing import Any


class PrologManager:
    def __init__(self):
        self.prolog = Prolog()
        self.cargar_base()

    def cargar_base(self):
        try:
            self.prolog.consult("knowledge/movie_kb.pl")
            print("✅ Base de conocimiento Prolog cargada.")
        except Exception as e:
            print(f"❌ Error al cargar base: {e}")

    def query(self, consulta: str) -> list[dict[str, Any]]:
        try:
            return list(self.prolog.query(consulta)) # type: ignore
        except Exception as e:
            print(f"Error en consulta: {e}")
            return []
