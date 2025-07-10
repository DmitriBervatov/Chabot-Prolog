from chatbot.responses import detectar_intencion, procesar_respuesta
from chatbot.saludos import respuestas_despedida
from chatbot.prolog_interface import PrologManager
from chatbot.responses import respuestas_saludo
from chatbot.preferencias import PreferenciasUsuario
import random


class MovieChatbot:
    def __init__(self):
        self.nombre_usuario = ""
        self.historial: list[str] = []
        self.prolog = PrologManager()
        self.preferencias = PreferenciasUsuario()

    def chat(self):
        print("🎬 ¡Bienvenido a CineBot! 🍿")
        print("Escribe 'salir' para terminar la conversación")
        print("Escribe 'mis preferencias' para ver tus preferencias guardadas")
        print("-" * 50)

        # Saludo dinámico inicial
        print(f"\nCineBot: {random.choice(respuestas_saludo)}")

        while True:
            try:
                mensaje = input(
                    f"\n{self.nombre_usuario or 'Tú'}: ").strip().lower()

                if mensaje in ['salir', 'exit', 'quit']:
                    print(f"\nCineBot: {respuestas_despedida()}")
                    break

                if mensaje == 'mis preferencias':
                    resumen = self.preferencias.obtener_resumen()
                    print(
                        f"\nCineBot: Estas son tus preferencias actuales:\n{resumen}")
                    continue

                if not mensaje:
                    continue

                self.historial.append(mensaje)
                intencion = detectar_intencion(mensaje, self)
                respuesta = procesar_respuesta(intencion, self, mensaje)
                print(f"\nCineBot: {respuesta}")

            except Exception as e:
                print(f"\nCineBot: Ocurrió un error: {e}")
