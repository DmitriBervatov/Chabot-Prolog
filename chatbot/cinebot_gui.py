import tkinter as tk
from chatbot.core import MovieChatbot
from typing import Optional, Literal
from chatbot.memory_utils import clear_memory


def main():
    bot = MovieChatbot()

    def enviar(event: Optional[tk.Event] = None):
        mensaje = entrada.get()
        if not mensaje.strip():
            return
        entrada.delete(0, tk.END)
        agregar_mensaje("Tú", mensaje, "#d2f8d2", "e")  # Usuario: verde claro

        respuesta = bot.respond(mensaje)
        agregar_mensaje("CineBot", respuesta, "#f0f0f0",
                        "w")  # Bot: gris claro

    def agregar_mensaje(nombre: str, texto: str, color: str, lado: Literal['nw', 'n', 'ne', 'w', 'center', 'e', 'sw', 's', 'se']) -> None:
        contenedor = tk.Frame(scrollable_frame, bg="#ffffff")

        tk.Label(
            contenedor,
            text=nombre,
            font=("Segoe UI", 9, "bold"),
            fg="#555555",
            bg="#ffffff",
            anchor=lado
        ).pack(anchor=lado, padx=6, pady=(4, 0))

        mensaje_label = tk.Label(
            contenedor,
            text=texto,
            font=("Segoe UI", 10),
            bg=color,
            fg="black",
            wraplength=360,
            justify="left",
            padx=10,
            pady=6,
            bd=1,
            relief="solid"
        )
        mensaje_label.pack(anchor=lado, padx=10, pady=2)

        contenedor.pack(fill="both", expand=True, anchor=lado)
        canvas.update_idletasks()
        canvas.yview_moveto(1.0)

    def on_close():
        clear_memory()  # Borra la memoria
        root.destroy()

    # Ventana principal
    root = tk.Tk()
    root.title("🎬 CineBot")
    root.geometry("600x580")
    root.configure(bg="#ffffff")

    # Canvas con scrollbar
    canvas_frame = tk.Frame(root, bg="#ffffff")
    canvas_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(canvas_frame, bg="#ffffff", highlightthickness=0)
    scrollbar = tk.Scrollbar(
        canvas_frame, orient="vertical", command=canvas.yview) # type: ignore
    scrollable_frame = tk.Frame(canvas, bg="#ffffff")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Entrada inferior
    input_frame = tk.Frame(root, bg="#eeeeee")
    input_frame.pack(fill="x", pady=10)

    entrada = tk.Entry(input_frame, font=(
        "Segoe UI", 12), bg="white", fg="black")
    entrada.pack(side="left", fill="x", expand=True, padx=10, pady=10, ipady=6)
    entrada.bind("<Return>", enviar)

    boton = tk.Button(
        input_frame,
        text="Enviar",
        font=("Segoe UI", 10, "bold"),
        bg="#4CAF50",
        fg="white",
        padx=20,
        pady=6,
        relief="flat",
        command=enviar
    )
    boton.pack(side="right", padx=10, pady=10)

    # Bienvenida del bot
    agregar_mensaje(
        "CineBot", "¡Hola! Soy tu asistente de películas. ¿Qué deseas ver hoy? 🎬", "#f0f0f0", "w")

    root.protocol("WM_DELETE_WINDOW", on_close)  # Hook de cierre

    root.mainloop()


if __name__ == "__main__":
    main()
