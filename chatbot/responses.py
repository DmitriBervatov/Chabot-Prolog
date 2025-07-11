import re
from chatbot.intenciones import GENERO_INTENCIONES, DURACION_INTENCIONES, EPOCA_INTENCIONES, ANIMO_INTENCIONES, PATRONES_INTENCIONES
from chatbot.saludos import respuestas_saludo, patrones_saludo
from chatbot.utils import normalizar_texto
from chatbot.sugerencias import sugerir_titulo
from typing import Any
from chatbot.recomendaciones import (
    recomendar_peliculas_genero,
    recomendar_peliculas_duracion,
    recomendar_peliculas_epoca,
    recomendar_peliculas_estado_animo,
    recomendar_peliculas_similares,
)
from chatbot.utils import (
    match_regex,
    extraer_titulo,
    extraer_titulo_info,
    detectar_pelicula_gustada,
    detectar_pelicula_no_gustada,
    detectar_genero_favorito,
    corregir_titulo_similar
)
from chatbot.formatter import format_movie_info
import random


def detectar_intencion(mensaje: str, bot: Any) -> str:

    mensaje_norm = normalizar_texto(mensaje)

    for intencion, patrones in PATRONES_INTENCIONES.items():
        for patron in patrones:
            if re.search(patron, mensaje_norm):
                # Si es duración, guarda preferencia
                if intencion.startswith("duracion_"):
                    bot.preferencias.establecer_duracion(
                        intencion.replace("duracion_", ""))
                return intencion

    genero_favorito = detectar_genero_favorito(mensaje)
    if genero_favorito:
        bot.preferencias.agregar_genero(genero_favorito)
        return 'genero_favorito'

    # Luego detecta si es una película gustada
    pelicula_gustada = detectar_pelicula_gustada(mensaje)
    if pelicula_gustada:
        bot.preferencias.marcar_pelicula_gustada(pelicula_gustada)
        return 'pelicula_gustada'

    pelicula_no_gustada = detectar_pelicula_no_gustada(mensaje)
    if pelicula_no_gustada:
        bot.preferencias.marcar_pelicula_no_gustada(pelicula_no_gustada)
        return 'pelicula_no_gustada'

    genero_favorito = detectar_genero_favorito(mensaje)
    if genero_favorito:
        bot.preferencias.agregar_genero(genero_favorito)
        return 'genero_favorito'

    # Continúa con la detección normal de intenciones
    if match_regex(mensaje, patrones_saludo):
        return 'saludo'
    elif "me llamo" in mensaje or "soy" in mensaje:
        nombre = mensaje.split()[-1].capitalize()
        bot.nombre_usuario = nombre
        return 'nombre'
    elif "accion" in mensaje:
        return 'genero_accion'
    elif "drama" in mensaje:
        return 'genero_drama'
    elif "terror" in mensaje:
        return 'genero_terror'
    elif "romance" in mensaje:
        return 'genero_romance'
    elif "animacion" in mensaje:
        return 'genero_animacion'
    elif "crimen" in mensaje:
        return 'genero_crimen'
    elif "ciencia ficcion" in mensaje or "ciencia_ficcion" in mensaje:
        return 'genero_ciencia_ficcion'
    elif "musical" in mensaje:
        return 'genero_musical'
    elif "corta" in mensaje:
        bot.preferencias.establecer_duracion("corta")
        return 'duracion_corta'
    elif "media" in mensaje:
        bot.preferencias.establecer_duracion("media")
        return 'duracion_media'
    elif "larga" in mensaje:
        bot.preferencias.establecer_duracion("larga")
        return 'duracion_larga'
    elif "clasica" in mensaje or "antigua" in mensaje:
        bot.preferencias.establecer_epoca("clásica")
        return 'epoca_clasica'
    elif "moderna" in mensaje:
        bot.preferencias.establecer_epoca("moderna")
        return 'epoca_moderna'
    elif "contemporanea" in mensaje or "actual" in mensaje:
        bot.preferencias.establecer_epoca("contemporánea")
        return 'epoca_contemporanea'
    elif "relajar" in mensaje:
        return 'animo_relajar'
    elif "emocionar" in mensaje or "emoción" in mensaje:
        return 'animo_emocionar'
    elif "reflexionar" in mensaje or "pensar" in mensaje:
        return 'animo_reflexionar'
    elif "parecido a" in mensaje or "similar a" in mensaje:
        return "peliculas_similares"
    elif re.search(r"(quien dirigio|director de|dur[aá]|genero de|de que genero es|cu[aá]nto dura|informaci[oó]n|info|detalles|dime sobre|sabes sobre)", mensaje_norm):
        return "info_pelicula"
    elif "recomiendame" in mensaje or "sugiéreme" in mensaje:
        # Usa preferencias guardadas para recomendar
        return "recomendar_personalizado"
    elif "inspirar" in mensaje or "inspiración" in mensaje:
        return 'animo_inspirar'
    elif "reir" in mensaje or "risa" in mensaje or "divertir" in mensaje:
        return 'animo_reir'
    elif "soñar" in mensaje or "fantasía" in mensaje:
        return 'animo_sonar'

    titulos = [r["P"] for r in bot.prolog.query("pelicula(P, _, _, _, _)")]
    mensaje_limpio = mensaje.strip().title()
    if mensaje_limpio in titulos:
        return "info_pelicula"

    # Si el mensaje es "pelicula <titulo>", extrae el título y muestra info
    if mensaje.startswith("pelicula "):
        posible_titulo = mensaje.replace("pelicula ", "").strip().title()
        if posible_titulo in titulos:
            return "info_pelicula"

    return 'general'


def procesar_respuesta(intencion: str, bot: Any, mensaje: str) -> str:
    titulos_disponibles = [r["P"]
                           for r in bot.prolog.query("pelicula(P, _, _, _, _)")]
    print(f"Titulos disponibles: {titulos_disponibles}")
    
    # Respuestas a preferencias expresadas
    if intencion == 'pelicula_gustada':
        pelicula = detectar_pelicula_gustada(mensaje)
        # Validar si la película existe en Prolog
        existe = bot.prolog.query(f"pelicula('{pelicula}', _, _, _, _)")
        if existe:
            bot.preferencias.marcar_pelicula_gustada(pelicula)
            return f"¡Me alegro que te haya gustado '{pelicula}'! Lo tendré en cuenta para futuras recomendaciones."
        else:
            return f"No encontré la película '{pelicula}' en mi base de datos. ¿Podrías revisar el nombre?"

    if intencion == 'pelicula_no_gustada':
        pelicula = detectar_pelicula_no_gustada(mensaje)
        return f"Entendido, '{pelicula}' no te gustó. Evitaré recomendarte películas similares."

    if intencion == 'genero_favorito':
        genero = detectar_genero_favorito(mensaje)
        genero_formato = genero.replace("_", " ")
        return f"¡Genial! He registrado que te gusta el género {genero_formato}. Te recomendaré más películas así."

    if intencion == 'recomendar_personalizado':
        # Si el usuario tiene géneros favoritos, usa el primero para recomendar
        if bot.preferencias.generos_favoritos:
            genero = bot.preferencias.generos_favoritos[0]
            return recomendar_peliculas_genero(bot, genero) + "\n\n(Recomendación basada en tus preferencias de género)"
        # Si no, usa la duración preferida
        elif bot.preferencias.duracion_preferida:
            duracion = bot.preferencias.duracion_preferida
            return recomendar_peliculas_duracion(bot, duracion) + "\n\n(Recomendación basada en tu preferencia de duración)"
        # Si tiene películas que le gustaron, recomienda similares a la primera
        elif bot.preferencias.peliculas_gustadas:
            pelicula = bot.preferencias.peliculas_gustadas[0]
            return recomendar_peliculas_similares(bot, pelicula) + "\n\n(Recomendación basada en películas que te gustaron)"
        # Si tiene preferencia de época
        elif bot.preferencias.epoca_preferida:
            epoca = bot.preferencias.epoca_preferida
            return recomendar_peliculas_epoca(bot, epoca) + "\n\n(Recomendación basada en tu preferencia de época)"
        else:
            return "Para darte recomendaciones personalizadas, cuéntame primero qué géneros o películas te gustan."

    # Saludo
    if intencion == 'saludo':
        return random.choice(respuestas_saludo)

    elif intencion == 'nombre':
        return f"¡Mucho gusto, {bot.nombre_usuario}! ¿Qué género buscas?"


    elif intencion == "peliculas_similares":
        titulo_extraido = extraer_titulo(mensaje)
        titulo_corregido = corregir_titulo_similar(
            titulo_extraido, titulos_disponibles)
        return recomendar_peliculas_similares(bot, titulo_corregido)

    elif intencion == "info_pelicula":
        titulo_extraido = extraer_titulo_info(mensaje)
        print(f"[🕵️‍♂️] Título extraído: {titulo_extraido}")
        if not titulo_extraido:
            titulo_extraido = mensaje.strip().title()
        titulo_corregido = corregir_titulo_similar(
            titulo_extraido, titulos_disponibles)
        print(f"[✅] Título corregido: {titulo_corregido}")
        
        return info_pelicula(bot, titulo_corregido)

    # Por genero
    if intencion in GENERO_INTENCIONES:
        genero = GENERO_INTENCIONES[intencion]
        return recomendar_peliculas_genero(bot, genero)

    # Por duración
    if intencion in DURACION_INTENCIONES:
        dur = DURACION_INTENCIONES[intencion]
        return recomendar_peliculas_duracion(bot, dur)

    # Por época
    if intencion in EPOCA_INTENCIONES:
        epoca = EPOCA_INTENCIONES[intencion]
        return recomendar_peliculas_epoca(bot, epoca)

    # Por estado de ánimo
    if intencion in ANIMO_INTENCIONES:
        regla = ANIMO_INTENCIONES[intencion]
        return recomendar_peliculas_estado_animo(bot, regla)

    return (
        "No entendí bien tu consulta, pero puedo ayudarte a buscar películas por:\n"
        "- 🎬 Género (ej. acción, drama, terror)\n"
        "- ⏱️ Duración (corta, media, larga)\n"
        "- 📅 Época (clásica, moderna, contemporánea)\n"
        "Solo dime qué estás buscando 🎞️"
    )


def info_pelicula(bot: Any, titulo: str) -> str:
    if not titulo:
        return "No entendí el título de la película. ¿Podrías escribirlo completo?"
    info = bot.prolog.query(f"info_pelicula('{titulo}', G, A, D, Dur)")
    if not info:
        sugerencia = sugerir_titulo(bot, titulo)
        return f"No tengo información sobre '{titulo}'. {sugerencia}".strip()
    datos = info[0]
    return format_movie_info(titulo, datos["G"], datos["A"], datos["D"], datos["Dur"])
