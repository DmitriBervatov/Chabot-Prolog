:- set_prolog_flag(encoding, utf8).
:- dynamic historial/1.

% --- Base de conocimientos (hechos agrupados) ---
tema(horario, universidad, "Nuestro horario es de lunes a viernes de 9:00 a 18:00.").
tema(contacto, universidad, "Puedes contactarnos al correo: info@universidad.edu").
tema(inscripcion, universidad, "La inscripción está abierta hasta el 30 de septiembre.").
tema(cursos, universidad, "Ofrecemos cursos de ingeniería, derecho y administración.").

% --- Alias (sinónimos o expresiones comunes sin tildes) ---
alias("me quiero inscribir", inscripcion).
alias("como me matriculo", inscripcion).
alias("quiero inscribirme", inscripcion).
alias("contacto", contacto).
alias("como me comunico", contacto).
alias("cursos disponibles", cursos).
alias("que carreras hay", cursos).
alias("horario de clases", horario).
alias("cual es el horario", horario).
alias("que cursos tienen", cursos).
alias("que materias tienen", cursos).
alias("como puedo contactarlos", contacto).
alias("como puedo comunicarme", contacto).
alias("buenas", hola).
alias("chau", adios).
alias("hola", hola).
alias("adios", adios).

% --- Reglas inferenciales desde la base ---
respuesta(Clave, Respuesta) :-
    tema(Clave, _, Respuesta).

% --- Interpretar entrada directa o por palabra clave ---
interpretar_entrada(Entrada, Clave) :-
    alias(Entrada, Clave), !.
interpretar_entrada(Entrada, Clave) :-
    contiene_palabra_clave(Entrada, Clave), !.
interpretar_entrada(_, desconocido).

% --- Detección por palabra clave ---
contiene_palabra_clave(Frase, Clave) :-
    split_string(Frase, " ", "", Palabras),
    member(Palabra, Palabras),
    alias(Palabra, Clave).

% --- Reemplazo básico de vocales con tilde por sin tilde ---
normalizar_tildes(Texto, Normalizado) :-
    string_chars(Texto, Chars),
    maplist(reemplazar_tilde, Chars, CharsSinTilde),
    string_chars(Normalizado, CharsSinTilde).

reemplazar_tilde('á', 'a').
reemplazar_tilde('é', 'e').
reemplazar_tilde('í', 'i').
reemplazar_tilde('ó', 'o').
reemplazar_tilde('ú', 'u').
reemplazar_tilde('Á', 'a').
reemplazar_tilde('É', 'e').
reemplazar_tilde('Í', 'i').
reemplazar_tilde('Ó', 'o').
reemplazar_tilde('Ú', 'u').
reemplazar_tilde('ñ', 'n').
reemplazar_tilde('Ñ', 'n').
reemplazar_tilde(Caracter, Caracter).  % Otros quedan igual

% --- Mostrar historial ---
mostrar_historial :-
    findall(P, historial(P), Preguntas),
    (Preguntas = [] ->
        write("No hay preguntas registradas aún."), nl
    ;
        write("Historial de preguntas:"), nl,
        forall(member(P, Preguntas), format("- ~w~n", [P]))
    ).

% --- Chatbot principal ---
chatbot :-
    write("Escribe tu pregunta (escribe 'salir' para terminar, 'historial' para ver el historial):"), nl,
    read_line_to_string(user_input, EntradaOriginal),
    string_lower(EntradaOriginal, EntradaMin),
    normalizar_tildes(EntradaMin, Entrada),

    (Entrada = "salir" ->
        write("¡Hasta pronto!"), nl

    ; Entrada = "historial" ->
        mostrar_historial,
        chatbot

    ;
        assertz(historial(Entrada)),
        interpretar_entrada(Entrada, Clave),
        (
            Clave = desconocido ->
                write("Chatbot: No entiendo tu pregunta. ¿Puedes reformularla?"), nl
            ;
            (respuesta(Clave, Respuesta) ->
                format("Chatbot: ~w~n", [Respuesta])
            ;
                write("Chatbot: Lo siento, no tengo una respuesta para eso."), nl
            )
        ),
        chatbot
    ).
