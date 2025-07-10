import re
import random
from pyswip import Prolog
from typing import Any, Optional, List
import os


class MovieChatbot:
    def __init__(self):
        """Inicializa el chatbot con la base de conocimiento de Prolog"""
        self.prolog = Prolog()
        self.cargar_base_conocimiento()
        self.usuario_nombre = ""
        self.historial_recomendaciones: List[str] = []

        # Patrones de respuesta
        self.patrones_saludo = [
            r'\b(hola|hey|buenas|saludos)\b',
            r'\b(buenos días|buenas tardes|buenas noches)\b'
        ]

        self.patrones_despedida = [
            r'\b(adiós|chao|hasta luego|bye|nos vemos)\b',
            r'\b(gracias|thank you|thanks)\b'
        ]

        self.patrones_nombre = [
            r'me llamo (\w+)',
            r'soy (\w+)',
            r'mi nombre es (\w+)'
        ]

        # Respuestas personalizadas
        self.respuestas_saludo = [
            "¡Hola! 🎬 Soy CineBot, tu asistente personal de películas.",
            "¡Bienvenido! 🍿 Estoy aquí para ayudarte a encontrar la película perfecta.",
            "¡Hola! 🎭 ¿Listo para descubrir tu próxima película favorita?"
        ]

        self.respuestas_despedida = [
            "¡Hasta luego! 🎬 Espero que disfrutes las películas que te recomendé.",
            "¡Nos vemos! 🍿 Que tengas una excelente sesión de cine.",
            "¡Adiós! 🎭 Vuelve cuando quieras más recomendaciones."
        ]

    def cargar_base_conocimiento(self):
        """Carga la base de conocimiento de Prolog"""
        try:
            # Asume que el archivo peliculas.pl está en el mismo directorio
            kb_content = r'''
% Base de conocimiento de películas
% Hechos sobre películas: pelicula(titulo, genero, año, director, duracion_minutos)
pelicula('El Padrino', drama, 1972, 'Francis Ford Coppola', 175).
pelicula('Pulp Fiction', crimen, 1994, 'Quentin Tarantino', 154).
pelicula('El Caballero Oscuro', accion, 2008, 'Christopher Nolan', 152).
pelicula('Forrest Gump', drama, 1994, 'Robert Zemeckis', 142).
pelicula('Matrix', ciencia_ficcion, 1999, 'Las Wachowski', 136).
pelicula('Titanic', romance, 1997, 'James Cameron', 194).
pelicula('El Rey León', animacion, 1994, 'Roger Allers', 88).
pelicula('Avengers', accion, 2012, 'Joss Whedon', 143).
pelicula('Inception', ciencia_ficcion, 2010, 'Christopher Nolan', 148).
pelicula('La La Land', musical, 2016, 'Damien Chazelle', 128).
pelicula('Joker', drama, 2019, 'Todd Phillips', 122).
pelicula('Toy Story', animacion, 1995, 'John Lasseter', 81).
pelicula('Casablanca', romance, 1942, 'Michael Curtiz', 102).
pelicula('El Exorcista', terror, 1973, 'William Friedkin', 122).
pelicula('Alien', terror, 1979, 'Ridley Scott', 117).

% Hechos sobre géneros y sus características
genero_caracteristica(accion, adrenalina).
genero_caracteristica(accion, espectacular).
genero_caracteristica(drama, emocional).
genero_caracteristica(drama, reflexivo).
genero_caracteristica(terror, suspenso).
genero_caracteristica(terror, miedo).
genero_caracteristica(romance, romantico).
genero_caracteristica(romance, emocional).
genero_caracteristica(ciencia_ficcion, futurista).
genero_caracteristica(ciencia_ficcion, imaginativo).
genero_caracteristica(animacion, familiar).
genero_caracteristica(animacion, divertido).
genero_caracteristica(crimen, intenso).
genero_caracteristica(musical, musical).

% Preferencias de duración
duracion_corta(Pelicula) :- pelicula(Pelicula, _, _, _, Duracion), Duracion < 120.
duracion_media(Pelicula) :- pelicula(Pelicula, _, _, _, Duracion), Duracion >= 120, Duracion =< 150.
duracion_larga(Pelicula) :- pelicula(Pelicula, _, _, _, Duracion), Duracion > 150.

% Épocas
epoca_clasica(Pelicula) :- pelicula(Pelicula, _, Anio, _, _), Anio < 1980.
epoca_moderna(Pelicula) :- pelicula(Pelicula, _, Anio, _, _), Anio >= 1980, Anio < 2000.
epoca_contemporanea(Pelicula) :- pelicula(Pelicula, _, Anio, _, _), Anio >= 2000.

% Reglas de recomendación
recomendar_por_genero(Genero, Pelicula) :-
    pelicula(Pelicula, Genero, _, _, _).

recomendar_por_caracteristica(Caracteristica, Pelicula) :-
    genero_caracteristica(Genero, Caracteristica),
    pelicula(Pelicula, Genero, _, _, _).

recomendar_por_director(Director, Pelicula) :-
    pelicula(Pelicula, _, _, Director, _).

recomendar_por_duracion(corta, Pelicula) :- duracion_corta(Pelicula).
recomendar_por_duracion(media, Pelicula) :- duracion_media(Pelicula).
recomendar_por_duracion(larga, Pelicula) :- duracion_larga(Pelicula).

recomendar_por_epoca(clasica, Pelicula) :- epoca_clasica(Pelicula).
recomendar_por_epoca(moderna, Pelicula) :- epoca_moderna(Pelicula).
recomendar_por_epoca(contemporanea, Pelicula) :- epoca_contemporanea(Pelicula).

% Regla compleja: recomendar película similar
pelicula_similar(Pelicula1, Pelicula2) :-
    pelicula(Pelicula1, Genero, _, _, _),
    pelicula(Pelicula2, Genero, _, _, _),
    Pelicula1 \= Pelicula2.

% Obtener información completa de una película
info_pelicula(Titulo, Genero, Anio, Director, Duracion) :-
    pelicula(Titulo, Genero, Anio, Director, Duracion).

% Reglas de estado de ánimo
para_relajarse(Pelicula) :-
    (pelicula(Pelicula, animacion, _, _, _) ;
     pelicula(Pelicula, romance, _, _, _)),
    duracion_media(Pelicula).

para_emocionarse(Pelicula) :-
    (pelicula(Pelicula, accion, _, _, _) ;
     pelicula(Pelicula, ciencia_ficcion, _, _, _)).

para_reflexionar(Pelicula) :-
    pelicula(Pelicula, drama, _, _, _),
    pelicula(Pelicula, _, Anio, _, _),
    Anio > 1990.

            '''

            # Crear archivo temporal
            with open('temp_kb.pl', 'w', encoding='utf-8') as f:
                f.write(kb_content)

            self.prolog.consult('temp_kb.pl')
            os.remove('temp_kb.pl')
            print("✅ Base de conocimiento cargada exitosamente")

        except Exception as e:
            print(f"❌ Error al cargar la base de conocimiento: {e}")

    def detectar_intencion(self, mensaje: str) -> str:
        """Detecta la intención del usuario basándose en patrones"""
        mensaje_lower = mensaje.lower()

        # Verificar saludos
        for patron in self.patrones_saludo:
            if re.search(patron, mensaje_lower):
                return 'saludo'

        # Verificar despedidas
        for patron in self.patrones_despedida:
            if re.search(patron, mensaje_lower):
                return 'despedida'

        # Verificar nombre
        for patron in self.patrones_nombre:
            match = re.search(patron, mensaje_lower)
            if match:
                self.usuario_nombre = match.group(1).capitalize()
                return 'nombre'

        # Verificar géneros
        generos = ['accion', 'drama', 'terror', 'romance', 'ciencia_ficcion',
                   'animacion', 'crimen', 'musical']
        for genero in generos:
            if genero.replace('_', ' ') in mensaje_lower or genero in mensaje_lower:
                return f'genero_{genero}'

        # Verificar características
        caracteristicas = ['adrenalina', 'emocional', 'suspenso', 'miedo',
                           'romantico', 'futurista', 'familiar', 'divertido', 'intenso']
        for caracteristica in caracteristicas:
            if caracteristica in mensaje_lower:
                return f'caracteristica_{caracteristica}'

        # Verificar duración
        if 'corta' in mensaje_lower or 'rápida' in mensaje_lower:
            return 'duracion_corta'
        elif 'larga' in mensaje_lower:
            return 'duracion_larga'
        elif 'media' in mensaje_lower or 'normal' in mensaje_lower:
            return 'duracion_media'

        # Verificar época
        if 'clásica' in mensaje_lower or 'antigua' in mensaje_lower or 'vieja' in mensaje_lower:
            return 'epoca_clasica'
        elif 'moderna' in mensaje_lower:
            return 'epoca_moderna'
        elif 'contemporánea' in mensaje_lower or 'actual' in mensaje_lower or 'reciente' in mensaje_lower:
            return 'epoca_contemporanea'

        # Verificar estado de ánimo
        if 'relajar' in mensaje_lower or 'tranquilo' in mensaje_lower:
            return 'animo_relajar'
        elif 'emocionar' in mensaje_lower or 'emoción' in mensaje_lower or 'adrenalina' in mensaje_lower:
            return 'animo_emocionar'
        elif 'reflexionar' in mensaje_lower or 'pensar' in mensaje_lower:
            return 'animo_reflexionar'

        # Verificar información específica
        if 'información' in mensaje_lower or 'info' in mensaje_lower or 'datos' in mensaje_lower:
            return 'info_pelicula'

        # Verificar similares
        if 'similar' in mensaje_lower or 'parecida' in mensaje_lower:
            return 'pelicula_similar'

        return 'consulta_general'

    def consultar_prolog(self, query: str) -> list[dict[str, Any]]:
        """Ejecuta una consulta en Prolog y devuelve los resultados"""
        try:
            resultados: list[dict[str, Any]] = list(
                self.prolog.query(query))  # type: ignore
            return resultados
        except Exception as e:
            print(f"Error en consulta Prolog: {e}")
            return []

    def formatear_pelicula(self, titulo: str, genero: Optional[str] = None, año: Optional[int] = None, director: Optional[str] = None, duracion: Optional[int] = None):
        """Formatea la información de una película"""
        info = f"🎬 **{titulo}**"
        if genero:
            info += f"\n   📂 Género: {genero.replace('_', ' ').title()}"
        if año:
            info += f"\n   📅 Año: {año}"
        if director:
            info += f"\n   🎭 Director: {director}"
        if duracion:
            info += f"\n   ⏱️ Duración: {duracion} minutos"
        return info

    def procesar_respuesta(self, intencion: str, mensaje: str) -> str:
        """Procesa la respuesta según la intención detectada"""

        if intencion == 'saludo':
            return random.choice(self.respuestas_saludo) + "\n¿Cómo te llamas?"

        elif intencion == 'despedida':
            return random.choice(self.respuestas_despedida)

        elif intencion == 'nombre':
            return f"¡Mucho gusto, {self.usuario_nombre}! 😊\n¿Qué tipo de película te gustaría ver hoy?"

        elif intencion.startswith('genero_'):
            genero = intencion.replace('genero_', '')
            query = f"recomendar_por_genero({genero}, Pelicula)"
            resultados = self.consultar_prolog(query)

            if resultados:
                peliculas = [r['Pelicula'] for r in resultados]
                respuesta = f"🎬 Te recomiendo estas películas de {genero.replace('_', ' ')}:\n\n"
                for pelicula in peliculas[:3]:  # Limitar a 3 recomendaciones
                    info_query = f"info_pelicula('{pelicula}', Genero, Año, Director, Duracion)"
                    info_result = self.consultar_prolog(info_query)
                    if info_result:
                        info = info_result[0]
                        respuesta += self.formatear_pelicula(
                            pelicula, info['Genero'], info['Año'],
                            info['Director'], info['Duracion']
                        ) + "\n\n"

                self.historial_recomendaciones.extend(peliculas[:3])
                return respuesta
            else:
                return f"Lo siento, no tengo películas de {genero.replace('_', ' ')} en mi base de datos."

        elif intencion.startswith('caracteristica_'):
            caracteristica = intencion.replace('caracteristica_', '')
            query = f"recomendar_por_caracteristica({caracteristica}, Pelicula)"
            resultados = self.consultar_prolog(query)

            if resultados:
                peliculas = [r['Pelicula'] for r in resultados]
                respuesta = f"🎭 Películas {caracteristica}s que te pueden gustar:\n\n"
                for pelicula in peliculas[:3]:
                    info_query = f"info_pelicula('{pelicula}', Genero, Año, Director, Duracion)"
                    info_result = self.consultar_prolog(info_query)
                    if info_result:
                        info = info_result[0]
                        respuesta += self.formatear_pelicula(
                            pelicula, info['Genero'], info['Año'],
                            info['Director'], info['Duracion']
                        ) + "\n\n"

                return respuesta
            else:
                return f"No encontré películas con esa característica específica."

        elif intencion.startswith('duracion_'):
            duracion = intencion.replace('duracion_', '')
            query = f"recomendar_por_duracion({duracion}, Pelicula)"
            resultados = self.consultar_prolog(query)

            if resultados:
                peliculas = [r['Pelicula'] for r in resultados]
                respuesta = f"⏱️ Películas de duración {duracion}:\n\n"
                for pelicula in peliculas[:3]:
                    info_query = f"info_pelicula('{pelicula}', Genero, Año, Director, Duracion)"
                    info_result = self.consultar_prolog(info_query)
                    if info_result:
                        info = info_result[0]
                        respuesta += self.formatear_pelicula(
                            pelicula, info['Genero'], info['Año'],
                            info['Director'], info['Duracion']
                        ) + "\n\n"

                return respuesta
            else:
                return f"No encontré películas de duración {duracion}."

        elif intencion.startswith('epoca_'):
            epoca = intencion.replace('epoca_', '')
            query = f"recomendar_por_epoca({epoca}, Pelicula)"
            resultados = self.consultar_prolog(query)

            if resultados:
                peliculas = [r['Pelicula'] for r in resultados]
                respuesta = f"📅 Películas de época {epoca.replace('_', ' ')}:\n\n"
                for pelicula in peliculas[:3]:
                    info_query = f"info_pelicula('{pelicula}', Genero, Año, Director, Duracion)"
                    info_result = self.consultar_prolog(info_query)
                    if info_result:
                        info = info_result[0]
                        respuesta += self.formatear_pelicula(
                            pelicula, info['Genero'], info['Año'],
                            info['Director'], info['Duracion']
                        ) + "\n\n"

                return respuesta
            else:
                return f"No encontré películas de esa época."

        elif intencion == 'animo_relajar':
            query = "para_relajarse(Pelicula)"
            resultados = self.consultar_prolog(query)

            if resultados:
                peliculas = [r['Pelicula'] for r in resultados]
                respuesta = "😌 Para relajarte, te recomiendo:\n\n"
                for pelicula in peliculas:
                    info_query = f"info_pelicula('{pelicula}', Genero, Año, Director, Duracion)"
                    info_result = self.consultar_prolog(info_query)
                    if info_result:
                        info = info_result[0]
                        respuesta += self.formatear_pelicula(
                            pelicula, info['Genero'], info['Año'],
                            info['Director'], info['Duracion']
                        ) + "\n\n"

                return respuesta
            else:
                return "No encontré películas específicas para relajarse."

        elif intencion == 'animo_emocionar':
            query = "para_emocionarse(Pelicula)"
            resultados = self.consultar_prolog(query)

            if resultados:
                peliculas = [r['Pelicula'] for r in resultados]
                respuesta = "🔥 Para emocionarte, te recomiendo:\n\n"
                for pelicula in peliculas:
                    info_query = f"info_pelicula('{pelicula}', Genero, Año, Director, Duracion)"
                    info_result = self.consultar_prolog(info_query)
                    if info_result:
                        info = info_result[0]
                        respuesta += self.formatear_pelicula(
                            pelicula, info['Genero'], info['Año'],
                            info['Director'], info['Duracion']
                        ) + "\n\n"

                return respuesta
            else:
                return "No encontré películas específicas para emocionarse."

        elif intencion == 'animo_reflexionar':
            query = "para_reflexionar(Pelicula)"
            resultados = self.consultar_prolog(query)

            if resultados:
                peliculas = [r['Pelicula'] for r in resultados]
                respuesta = "🤔 Para reflexionar, te recomiendo:\n\n"
                for pelicula in peliculas:
                    info_query = f"info_pelicula('{pelicula}', Genero, Año, Director, Duracion)"
                    info_result = self.consultar_prolog(info_query)
                    if info_result:
                        info = info_result[0]
                        respuesta += self.formatear_pelicula(
                            pelicula, info['Genero'], info['Año'],
                            info['Director'], info['Duracion']
                        ) + "\n\n"

                return respuesta
            else:
                return "No encontré películas específicas para reflexionar."

        else:
            # Respuesta por defecto
            opciones = [
                "🎬 Puedo ayudarte a encontrar películas por:",
                "• Género (acción, drama, terror, romance, etc.)",
                "• Duración (corta, media, larga)",
                "• Época (clásica, moderna, contemporánea)",
                "• Estado de ánimo (para relajarse, emocionarse, reflexionar)",
                "",
                "Solo dime qué tipo de película buscas 😊"
            ]
            return "\n".join(opciones)

    def chat(self):
        """Función principal del chat"""
        print("🎬 ¡Bienvenido a CineBot! 🍿")
        print("Escribe 'salir' para terminar la conversación")
        print("-" * 50)

        while True:
            try:
                mensaje = input(
                    f"\n{self.usuario_nombre if self.usuario_nombre else 'Tú'}: ").strip()

                if mensaje.lower() in ['salir', 'exit', 'quit']:
                    print("\nCineBot: ¡Hasta luego! 🎬 Que disfrutes tus películas.")
                    break

                if not mensaje:
                    continue

                intencion = self.detectar_intencion(mensaje)
                respuesta = self.procesar_respuesta(intencion, mensaje)

                print(f"\nCineBot: {respuesta}")

            except KeyboardInterrupt:
                print("\n\nCineBot: ¡Hasta luego! 🎬")
                break
            except Exception as e:
                print(f"\nCineBot: Lo siento, ocurrió un error: {e}")


def main():
    """Función principal para ejecutar el chatbot"""
    try:
        bot = MovieChatbot()
        bot.chat()
    except ImportError:
        print("❌ Error: pyswip no está instalado.")
        print("Instálalo con: pip install pyswip")
        print("También necesitas SWI-Prolog instalado en tu sistema.")
    except Exception as e:
        print(f"❌ Error al inicializar el chatbot: {e}")


if __name__ == "__main__":
    main()
