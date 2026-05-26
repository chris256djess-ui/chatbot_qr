from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# VARIABLES GLOBALES
estado_usuario = "inicio"

nombre_usuario = ""
telefono_usuario = ""

numero_reporte = 1

motivos_validos = [
    "Fuga de agua",
    "Perforacion en tuberias",
    "Tuberia fracturadas",
    "Vandalismo",
    "Otro"
]


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/mensaje", methods=["POST"])
def mensaje():

    global estado_usuario
    global nombre_usuario
    global telefono_usuario
    global numero_reporte

    data = request.json
    texto = data["mensaje"].strip()

    # ---------------- INICIO ----------------

    if estado_usuario == "inicio":

        if texto.lower() == "hola":

            estado_usuario = "pedir_nombre"

            respuesta = (
                "¡Hola! 👋\n\n"
                "Por favor, me puedes proporcionar tu nombre."
            )

        else:

            respuesta = (
                "Para iniciar la conversación escribe:\n\n"
                "Hola"
            )

    # ---------------- NOMBRE ----------------

    elif estado_usuario == "pedir_nombre":

        nombre_usuario = texto

        estado_usuario = "pedir_telefono"

        respuesta = (
            f"Mucho gusto, {nombre_usuario} 😊\n\n"
            "Ahora brindame tu número telefónico."
        )

    # ---------------- TELEFONO ----------------

    elif estado_usuario == "pedir_telefono":

        telefono_usuario = texto

        estado_usuario = "pedir_motivo"

        respuesta = (
            "Selecciona el motivo del reporte:\n\n"
            "• Fuga de agua\n"
            "• Perforacion en tuberias\n"
            "• Tuberia fracturadas\n"
            "• Vandalismo\n"
            "• Otro"
        )

    # ---------------- MOTIVO ----------------

    elif estado_usuario == "pedir_motivo":

        if texto in motivos_validos:

            if texto == "Otro":

                estado_usuario = "explicacion_otro"

                respuesta = (
                    "Por favor escribe la explicación del problema."
                )

            else:

                respuesta = (
                    f"✅ Reporte generado correctamente.\n\n"
                    f"Número de reporte: #{numero_reporte}\n\n"
                    f"Motivo: {texto}\n\n"
                    "¿Deseas generar otro reporte?\n"
                    "Responde: Si o No"
                )

                numero_reporte += 1

                estado_usuario = "otro_reporte"

        else:

            respuesta = (
                "Opción no válida.\n\n"
                "Escribe una de las siguientes opciones:\n\n"
                "• Fuga de agua\n"
                "• Perforacion en tuberias\n"
                "• Tuberia fracturadas\n"
                "• Vandalismo\n"
                "• Otro"
            )

    # ---------------- EXPLICACION OTRO ----------------

    elif estado_usuario == "explicacion_otro":

        explicacion = texto

        respuesta = (
            f"✅ Reporte generado correctamente.\n\n"
            f"Número de reporte: #{numero_reporte}\n\n"
            f"Descripción: {explicacion}\n\n"
            "¿Deseas generar otro reporte?\n"
            "Responde: Si o No"
        )

        numero_reporte += 1

        estado_usuario = "otro_reporte"

    # ---------------- OTRO REPORTE ----------------

    elif estado_usuario == "otro_reporte":

        if texto.lower() == "si":

            estado_usuario = "pedir_motivo"

            respuesta = (
                "Selecciona el motivo del nuevo reporte:\n\n"
                "• Fuga de agua\n"
                "• Perforacion en tuberias\n"
                "• Tuberia fracturadas\n"
                "• Vandalismo\n"
                "• Otro"
            )

        elif texto.lower() == "no":

            estado_usuario = "inicio"

            respuesta = (
                "Gracias por utilizar el sistema de reportes de Ñätho AquaGuard 💧\n\n"
                "Que tengas un excelente día."
            )

        else:

            respuesta = (
                "Por favor responde únicamente:\n\n"
                "Si\n"
                "o\n"
                "No"
            )

    else:

        respuesta = "Ocurrió un error."

    return jsonify({"respuesta": respuesta})


if __name__ == "__main__":
    app.run(debug=True)