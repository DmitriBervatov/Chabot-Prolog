GENERO_INTENCIONES = {
    "genero_accion": "accion",
    "genero_drama": "drama",
    "genero_terror": "terror",
    "genero_romance": "romance",
    "genero_animacion": "animacion",
    "genero_crimen": "crimen",
    "genero_ciencia_ficcion": "ciencia_ficcion",
    "genero_musical": "musical",
}

DURACION_INTENCIONES = {
    "duracion_corta": "corta",
    "duracion_media": "media",
    "duracion_larga": "larga"
}

EPOCA_INTENCIONES = {
    "epoca_clasica": "clasica",
    "epoca_moderna": "moderna",
    "epoca_contemporanea": "contemporanea"
}

ANIMO_INTENCIONES = {
    "animo_relajar": "para_relajarse",
    "animo_emocionar": "para_emocionarse",
    "animo_reflexionar": "para_reflexionar",
    "animo_inspirar": "para_inspirarse",
    "animo_reir": "para_reir",
    "animo_sonar": "para_sonar"
}

GENERO_VALIDOS = [
    "accion", "drama", "terror", "romance", "animacion", "crimen",
    "ciencia ficcion", "musical", "comedia", "fantasia", "biografico"
]

PATRONES_INTENCIONES = {
    "genero_romance": [
        r"(novia|novio|pareja|romantica|romantico|amor|enamorar|cita)",
        r"para\s+pareja",
        r"para\s+ver\s+con\s+(mi\s+)?(novia|novio|pareja)",
        r"peli.*pareja",
        r"peli.*novia",
        r"peli.*novio",
        r"pelicula.*pareja",
        r"pelicula.*novia",
        r"pelicula.*novio"
    ],
    "animo_reflexionar": [
        r"llorar", r"triste", r"sentimental", r"emocional", r"lagrimas?", r"para llorar"
    ],
    "duracion_corta": [
        r"no muy largo", r"no muy larga", r"corta", r"rapida", r"breve", r"cortita", r"no sea larga"
    ],
}
