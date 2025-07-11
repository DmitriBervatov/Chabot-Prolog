from chatbot.responses import detectar_intencion, procesar_respuesta
from chatbot.saludos import respuestas_despedida, respuestas_saludo
from chatbot.prolog_interface import PrologManager
from chatbot.preferencias import PreferenciasUsuario
from chatbot.utils import corregir_genero
from chatbot.formatter import pintar
from chatbot.gemini_interface import GeminiModel
from typing import Set
from chatbot.memory_utils import load_memory, save_memory
import os
import random


class MovieChatbot:
    def __init__(self):
        self.nombre_usuario = ""
        self.historial: list[str] = []
        self.prolog = PrologManager()
        self.preferencias = PreferenciasUsuario()
        self.preferencias.cargar()  # <-- Cargar preferencias al iniciar
        self.peliculas_recomendadas: Set[str] = set()
        self.ultimo_titulo_sugerido = None
        api_key = os.getenv("GEMINI_API_KEY")
        self.gemini = GeminiModel(api_key) if api_key else None
        self.memory = load_memory()  # Cargar memoria si existe

        if self.gemini:
            print("[✔️] GeminiModel fue inicializado correctamente.")
        else:
            print("[❌] No se pudo inicializar GeminiModel. Revisa tu API KEY.")
    # Metodo para mensajes en consola

    def chat(self):
        print(pintar("🎬 ¡Bienvenido a CineBot! 🍿", "cyan"))
        print(pintar("Escribe 'salir' para terminar la conversación", "yellow"))
        print(pintar("Escribe 'ayuda' para ver qué puedes preguntarme", "yellow"))
        print(pintar("-" * 50, "magenta"))
        print(
            pintar(f"\nCineBot: {random.choice(respuestas_saludo)}", "green"))

        while True:
            try:
                mensaje = input(
                    pintar(f"\n{self.nombre_usuario or 'Tú'}: ", "blue")
                ).strip().lower()

                if mensaje in ['salir', 'exit', 'quit']:
                    self.preferencias.guardar()
                    total = len(self.peliculas_recomendadas)
                    if total > 0:
                        lista = list(self.peliculas_recomendadas)
                        if total > 5:
                            lista_mostrar = ", ".join(lista[:3]) + ", ..."
                        else:
                            lista_mostrar = ", ".join(lista)
                        nombre = self.nombre_usuario or ""
                        print(
                            pintar(
                                f"\nCineBot: Hoy te recomendé {total} película(s): {lista_mostrar}. ¡Espero que alguna te guste, {nombre}!",
                                "magenta"
                            )
                        )
                    print(
                        pintar(f"\nCineBot: {respuestas_despedida()}", "cyan"))
                    break

                if mensaje == 'ayuda':
                    print(pintar(
                        "\n🎯 Puedes pedirme:\n"
                        "- 🎬 Películas por género: acción, drama, terror...\n"
                        "- ⏱️ Películas por duración: corta, media, larga\n"
                        "- 📅 Películas clásicas, modernas, contemporáneas\n"
                        "- 😊 Recomendaciones para relajarte, emocionarte o reflexionar\n"
                        "- 🎞️ Algo similar a otra película (ej. “similar a Inception”)\n"
                        "- ℹ️ Información de una película (ej. “info Inception”)\n"
                        "- 👍 Registrar películas o géneros que te gustan\n"
                        "- 👎 Registrar películas que no te gustaron\n"
                        "- 📝 Ver tus preferencias con 'mis preferencias'\n"
                        "¡Y mucho más! Solo escribe lo que buscas 😊",
                        "yellow"
                    ))
                    continue

                if mensaje == 'mis preferencias':
                    resumen = self.preferencias.obtener_resumen()
                    print(pintar(
                        f"\nCineBot: Estas son tus preferencias actuales:\n{resumen}",
                        "cyan"
                    ))
                    continue

                if not mensaje:
                    continue

                # Manejo de contexto para sugerencia de título
                if mensaje in ['si', 'sí'] and self.ultimo_titulo_sugerido:
                    mensaje_corregido = self.ultimo_titulo_sugerido
                    self.ultimo_titulo_sugerido = None  # Limpia el contexto
                    intencion = 'peliculas_similares'
                else:
                    mensaje_corregido = corregir_genero(mensaje)
                    intencion = detectar_intencion(mensaje_corregido, self)

                # Usa Gemini si la intención es 'general' y el modelo está disponible
                if intencion == 'general' and self.gemini:
                    print("[🌐] Usando Gemini para responder a intención 'general'")
                    respuesta = self.gemini.generar_respuesta(mensaje)
                else:
                    print(
                        f"[🧠] Usando lógica Prolog o reglas para intención: {intencion}")
                    respuesta = procesar_respuesta(
                        intencion, self, mensaje_corregido)
                print(pintar(f"\nCineBot: {respuesta}", "green"))

                # Si la respuesta contiene una sugerencia, guarda el título sugerido
                if "¿Quizás quisiste decir '" in respuesta:
                    sugerido = respuesta.split(
                        "¿Quizás quisiste decir '")[-1].split("'")[0]
                    self.ultimo_titulo_sugerido = sugerido
                else:
                    self.ultimo_titulo_sugerido = None

                self.preferencias.guardar()

            except Exception as e:
                print(pintar(f"\nCineBot: Ocurrió un error: {e}", "red"))

    # Metodo para Interfaz grafica
    def respond(self, mensaje: str) -> str:
        if not mensaje:
            return ""

        mensaje_corregido = corregir_genero(mensaje)

        # Contexto por memoria
        if "duración" in mensaje.lower() and "last_title" in self.memory:
            titulo = self.memory["last_title"]
            info = self.prolog.query(f"pelicula('{titulo}', G, A, D, Dur)")[0]
            respuesta = f"La duración de '{titulo}' es de {info['Dur']} minutos."
        elif "director" in mensaje.lower() and "last_title" in self.memory:
            titulo = self.memory["last_title"]
            info = self.prolog.query(f"pelicula('{titulo}', G, A, D, Dur)")[0]
            respuesta = f"El director de '{titulo}' es {info['D']}."
        else:
            intencion = detectar_intencion(mensaje_corregido, self)
            respuesta_base = procesar_respuesta(intencion, self, mensaje_corregido)
            respuesta_base_lc = respuesta_base.lower()

            es_respuesta_generica = any([
                respuesta_base_lc.startswith("lo siento"),
                "no tengo información" in respuesta_base_lc,
                "no tengo informacion" in respuesta_base_lc,
                "no encontré" in respuesta_base_lc,
                "no encontre" in respuesta_base_lc,
                "¿podrías revisar el nombre?" in respuesta_base_lc,
                "¿podrías escribir el título completo?" in respuesta_base_lc,
                "no entendí" in respuesta_base_lc,
                "solo puedo responder" in respuesta_base_lc
            ])

            if self.gemini:
                contexto_memoria = self.construir_contexto_desde_memoria()
                contexto_prolog = self.exportar_conocimiento()
                contexto_total = contexto_memoria + "\n\n" + contexto_prolog

                if es_respuesta_generica:
                    prompt = (
                        f"Eres CineBot, un chatbot experto en películas. Un usuario preguntó:\n"
                        f"'{mensaje}'\n\n"
                        f"Tu base de datos contiene la siguiente información extraída de Prolog.\n"
                        f"Tu sistema respondió: \"{respuesta_base}\"\n\n"
                        f"Ahora, ignora esa respuesta si no es útil, y responde con tu conocimiento general. "
                        f"Evita decir 'no tengo información'. Responde como un experto en cine."
                    )
                else:
                    prompt = (
                        f"El usuario preguntó: '{mensaje}'\n\n"
                        f"Tu sistema base respondió:\n{respuesta_base}\n\n"
                        f"Usando esta base de datos de películas, mejora o complementa la respuesta."
                    )

                respuesta = self.gemini.generar_respuesta(
                    prompt=prompt, contexto=contexto_total)
            else:
                respuesta = respuesta_base

            # Guardar el último título si está presente en el mensaje
            for titulo in self.get_titulos_disponibles():
                if titulo.lower() in mensaje.lower():
                    self.memory["last_title"] = titulo
                    break

            # Guardar info en memoria
            self.memory["ultimo_mensaje"] = mensaje
            self.memory["ultima_respuesta"] = respuesta
            self.memory["ultima_intencion"] = intencion
            self.memory.setdefault("historial", []).append({
                "mensaje": mensaje,
                "respuesta": respuesta,
                "intencion": intencion
            })
            save_memory(self.memory)

        return respuesta

    def exportar_conocimiento(self) -> str:
        peliculas = self.prolog.query("pelicula(P, G, A, D, Dur)")[
            :30]  # Puedes limitar a 30
        conocimiento = "📚 Base de datos de películas:\n"

        for p in peliculas:
            conocimiento += (
                f"- {p['P']} ({p['A']}), género: {p['G']}, "
                f"director: {p['D']}, duración: {p['Dur']} minutos\n"
            )

        return conocimiento

    def get_titulos_disponibles(self) -> list[str]:
        return [
            "Amelie", "El Gran Hotel Budapest", "Interestelar", "Coco", "El Conjuro",
            "La Lista de Schindler", "Whiplash", "El Resplandor", "La Vida es Bella",
            "El Padrino", "Pulp Fiction", "El Caballero Oscuro", "Forrest Gump",
            "Matrix", "Titanic", "El Rey León", "Avengers", "Inception", "La La Land",
            "Joker", "Toy Story", "Casablanca", "El Exorcista", "Alien"
        ]

    def construir_contexto_desde_memoria(self, max_turnos: int = 3) -> str:
        historial = self.memory.get("historial", [])[-max_turnos:]
        if not historial:
            return ""

        contexto = "📖 Conversación reciente:\n"
        for entrada in historial:
            mensaje = entrada.get("mensaje", "")
            respuesta = entrada.get("respuesta", "")
            contexto += f"Usuario: {mensaje}\nCineBot: {respuesta}\n"
        return contexto
