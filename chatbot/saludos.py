import random

patrones_saludo = [r'\b(hola|hey|buenas)\b']
respuestas_saludo = [
    "¡Hola! Soy CineBot 🎬 ¿Cómo te llamas?",
    "¡Buenas! ¿Qué película te interesa hoy?"
]

respuestas_despedida_textos = [
    "¡Hasta luego! 🎬 Que disfrutes tu película.",
    "Nos vemos 👋 Vuelve pronto por más cine."
]


def respuestas_despedida():
    return random.choice(respuestas_despedida_textos)
