from flask import Flask, render_template, request, jsonify, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = "aquaguard_secret_key"

# 📦 almacenamiento en memoria
reportes = []


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/mensaje", methods=["POST"])
def mensaje():

    data = request.json
    texto = data.get("mensaje", "").strip().lower()
    gps = data.get("gps", None)

    hora = datetime.now().strftime("%H:%M")

    # inicializar sesión
    if "paso" not in session:
        session["paso"] = 0
        session["datos"] = {}

    paso = session["paso"]
    datos = session["datos"]

    respuesta = ""

    # =========================
    # PASO 0 - INICIO
    # =========================
    if paso == 0:
        datos = {"hora": hora}
        session["datos"] = datos
        session["paso"] = 1
        respuesta = "👋 Hola, ¿cuál es tu nombre?"

    # =========================
    # PASO 1 - NOMBRE
    # =========================
    elif paso == 1:
        datos["nombre"] = texto
        session["paso"] = 2
        respuesta = "📱 Escribe tu número telefónico"

    # =========================
    # PASO 2 - TELÉFONO
    # =========================
    elif paso == 2:
        datos["telefono"] = texto
        session["paso"] = 3
        respuesta = "🚰 Describe el motivo del reporte (con tus palabras)"

    # =========================
    # PASO 3 - MOTIVO
    # =========================
    elif paso == 3:
        datos["motivo"] = texto
        session["paso"] = 4
        respuesta = "📍 ¿Permites usar tu ubicación GPS? (si / no)"

    # =========================
    # PASO 4 - GPS
    # =========================
    elif paso == 4:

        if "si" in texto:
            datos["gps"] = gps
        else:
            datos["gps"] = "No permitido"

        datos["hora"] = hora

        # guardar reporte
        reportes.append(datos.copy())

        session["paso"] = 5

        respuesta = "✅ Reporte guardado. ¿Deseas hacer otro? (si / no)"

    # =========================
    # PASO 5 - NUEVO REPORTE
    # =========================
    elif paso == 5:

        if "si" in texto:
            session["paso"] = 0
            session["datos"] = {}
            respuesta = "👍 Perfecto, iniciemos otro reporte"
        else:
            session["paso"] = 99
            respuesta = "🙏 Gracias por usar Ñätho AquaGuard"

    else:
        respuesta = "Recarga la página para iniciar nuevamente"

    return jsonify({"respuesta": respuesta})


@app.route("/reportes")
def ver_reportes():
    return jsonify(reportes)


if __name__ == "__main__":
    app.run(debug=True)