from chatbot.intenciones import GENERO_VALIDOS
from difflib import get_close_matches
import difflib
import re
import unicodedata


def match_regex(text: str, patterns: list[str]) -> bool:
    return any(re.search(p, text) for p in patterns)


def extraer_titulo(mensaje: str) -> str:
    patrones = [
        r"(?:similar|parecido) a ['\"]?(.+?)['\"]?$",
        r"(?:similar|parecido) a (.+)$",
    ]
    for patron in patrones:
        match = re.search(patron, mensaje)
        if match:
            return match.group(1).strip().title()
    return ""


def extraer_titulo_info(mensaje: str) -> str:
    mensaje = mensaje.lower()
    patrones = [
        r"(?:quien dirigio|director de) ['\"]?(.+?)['\"]?$",
        r"(?:de que genero es|genero de) ['\"]?(.+?)['\"]?$",
        r"(?:cu[aá]nto dura|duracion de) ['\"]?(.+?)['\"]?$",
        r"(?:informacion|info|detalles|dime sobre|sabes sobre) ['\"]?(.+?)['\"]?$",
        r"(?:informacion|info|detalles|dime sobre|sabes sobre) de ['\"]?(.+?)['\"]?$",
        r"(?:informacion|info|detalles|dime sobre|sabes sobre) (.+)$",
    ]
    for patron in patrones:
        match = re.search(patron, mensaje)
        if match:
            return match.group(1).strip().title()
    return ""


def detectar_pelicula_gustada(mensaje: str) -> str:
    patrones = [
        r"me gust[óoa] ['\"]?(.+?)['\"]?$",
        r"me encant[óoa] ['\"]?(.+?)['\"]?$",
        r"me fascin[óoa] ['\"]?(.+?)['\"]?$",
    ]
    for patron in patrones:
        match = re.search(patron, mensaje)
        if match:
            return match.group(1).strip().title()
    return ""


def detectar_pelicula_no_gustada(mensaje: str) -> str:
    patrones = [
        r"no me gust[óoa] ['\"]?(.+?)['\"]?$",
        r"odié ['\"]?(.+?)['\"]?$",
        r"no me agradó ['\"]?(.+?)['\"]?$",
    ]
    for patron in patrones:
        match = re.search(patron, mensaje)
        if match:
            return match.group(1).strip().title()
    return ""


def detectar_genero_favorito(mensaje: str) -> str:
    patrones = [
        r"me gusta[n]? (?:el género |el |la |los |las )?(?:de )?(accion|drama|terror|romance|animacion|crimen|ciencia ficcion|musical|comedia|fantasia|biografico)",
        r"prefiero (?:el género |el |la |los |las )?(?:de )?(accion|drama|terror|romance|animacion|crimen|ciencia ficcion|musical|comedia|fantasia|biografico)",
        r"me encanta[n]? (?:el género |el |la |los |las )?(?:de )?(accion|drama|terror|romance|animacion|crimen|ciencia ficcion|musical|comedia|fantasia|biografico)",
        r"me interesan (?:el género |el |la |los |las )?(?:de )?(accion|drama|terror|romance|animacion|crimen|ciencia ficcion|musical|comedia|fantasia|biografico)",
    ]
    for patron in patrones:
        match = re.search(patron, mensaje)
        if match:
            genero = match.group(1).lower()
            if genero == "ciencia ficcion":
                return "ciencia_ficcion"
            return genero
    return ""

def corregir_genero(genero: str) -> str:
    palabras = genero.split()
    corregidas: list[str] = []
    for palabra in palabras:
        match = difflib.get_close_matches(palabra, GENERO_VALIDOS, n=1, cutoff=0.8)
        if match:
            corregidas.append(match[0])
        else:
            corregidas.append(palabra)
    return " ".join(corregidas)
    

def normalizar_texto(texto: str) -> str:
    """Convierte a minúsculas y elimina tildes/acentos."""
    texto = texto.lower()
    texto = unicodedata.normalize('NFD', texto)
    texto = texto.encode('ascii', 'ignore').decode('utf-8')
    return texto


def corregir_titulo_similar(titulo: str, titulos_disponibles: list[str]) -> str:
    coincidencias = get_close_matches(
        titulo, titulos_disponibles, n=1, cutoff=0.75)
    return coincidencias[0] if coincidencias else titulo

