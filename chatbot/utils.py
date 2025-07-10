import re


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
    patrones = [
        r"(?:informacion|info|detalles) de ['\"]?(.+?)['\"]?$",
        r"(?:informacion|info|detalles) de (.+)$",
        r"(?:informacion|info|detalles) ['\"]?(.+?)['\"]?$",
        r"(?:informacion|info|detalles) (.+)$",
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
        r"me gusta[n]? (?:el género |los |las )?(?:de )?(accion|drama|terror|romance|animacion|crimen|ciencia ficcion|musical)",
        r"prefiero (?:el género |los |las )?(?:de )?(accion|drama|terror|romance|animacion|crimen|ciencia ficcion|musical)",
    ]
    for patron in patrones:
        match = re.search(patron, mensaje)
        if match:
            genero = match.group(1).lower()
            if genero == "ciencia ficcion":
                return "ciencia_ficcion"
            return genero
    return ""
