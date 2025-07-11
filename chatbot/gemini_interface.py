import google.generativeai as genai
import os
from typing import Optional

class GeminiModel:
    def __init__(self, api_key: Optional[str] = None):
        if api_key is None:
            api_key = os.environ.get("GEMINI_API_KEY")
        genai.configure(api_key=api_key)  # type: ignore

        # Lista de modelos de respaldo
        self.model_names = ["gemini-1.5-flash", "gemini-1.5-pro" , "gemini-pro"]
        self.model_index = 0
        self.model = genai.GenerativeModel( # type: ignore
            self.model_names[self.model_index])  # type: ignore
        
    def generar_respuesta(self, prompt: str, contexto: str = "") -> str:
        # Instrucción base para el sistema
        system_prompt = (
            "Eres un chatbot de películas llamado CineBot. Tu tarea es responder "
            "preguntas relacionadas con películas basándote en la siguiente base de datos "
            "extraída de Prolog. Si la película no está, puedes responder con tu conocimiento general.\n\n"
        )

        full_prompt = system_prompt + contexto + "\n\nUsuario: " + prompt
        print(f"[💬] Generando respuesta con prompt: {full_prompt}")

        for _ in range(len(self.model_names)):
            try:
                response = self.model.generate_content(full_prompt)  # type: ignore
                return getattr(response, 'text', '') or ''
            except Exception as e:
                print(
                    f"[⚠️ ERROR usando {self.model_names[self.model_index]}]: {e}")
                self.model_index += 1
                if self.model_index < len(self.model_names):
                    modelo_siguiente = self.model_names[self.model_index]
                    print(
                        f"[🔁 Cambiando a modelo de respaldo: {modelo_siguiente}]")
                    self.model = genai.GenerativeModel( # type: ignore
                        modelo_siguiente)  # type: ignore
                else:
                    break

        return "Por el momento no puedo responder usando IA, pero puedo ayudarte con funciones básicas de películas 🎬"

