from flask import Flask, render_template, request, jsonify
from datetime import datetime
import pandas as pd
import os

app = Flask(__name__)

reportes = []

EXCEL_FILE = os.path.join(os.getcwd(), "reportes.xlsx")

# 🧠 estado global (UNA sola conversación)
paso = 0
datos = {}


@app.route("/")
def inicio():
    return render_template("index.html")


def guardar_en_excel(nuevo_reporte):

    df_nuevo = pd.DataFrame([nuevo_reporte])

    if os.path.exists(EXCEL_FILE):
        df_existente = pd.read_excel(EXCEL_FILE)
        df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
    else:
        df_final = df_nuevo

    df_final.to_excel(EXCEL_FILE, index=False)


@app.route("/mensaje", methods=["POST"])
def mensaje():

    global paso, datos

    data = request.json
    texto = data.get("mensaje", "").strip().lower()
    gps = data.get("gps", None)

    hora = datetime.now().strftime("%H:%M")

    respuesta = ""

    # ======================
    # 0 - NOMBRE
    # ======================
    if paso == 0:
        paso = 1
        respuesta = "👋 ¿Cuál es tu nombre?"

    # ======================
    # 1 - NOMBRE
    # ======================
    elif paso == 1:
        datos = {}
        datos["nombre"] = texto
        paso = 2
        respuesta = "📱 Escribe tu número telefónico"

    # ======================
    # 2 - TELÉFONO
    # ======================
    elif paso == 2:
        datos["telefono"] = texto
        paso = 3
        respuesta = "🚰 Describe el motivo del reporte"

    # ======================
    # 3 - MOTIVO
    # ======================
    elif paso == 3:
        datos["motivo"] = texto
        paso = 4
        respuesta = "📍 ¿Permites usar tu ubicación GPS? (si / no)"

    # ======================
    # 4 - GPS + GUARDADO
    # ======================
    elif paso == 4:

        if "si" in texto:
            datos["gps"] = gps
        else:
            datos["gps"] = "No permitido"

        datos["hora_reporte"] = hora

        reportes.append(datos.copy())
        guardar_en_excel(datos.copy())

        paso = 5

        respuesta = "✅ Reporte guardado. ¿Deseas hacer otro? (si / no)"

    # ======================
    # 5 - REPETIR
    # ======================
    elif paso == 5:

        if "si" in texto:
            paso = 0
            datos = {}
            respuesta = "👍 Iniciemos un nuevo reporte"
        else:
            paso = 99
            respuesta = "🙏 Gracias por usar Ñätho AquaGuard"

    else:
        respuesta = "La conversación ha finalizado. Recarga la página para iniciar de nuevo."

    return jsonify({"respuesta": respuesta})


@app.route("/reportes")
def ver_reportes():
    return jsonify(reportes)


if __name__ == "__main__":
    app.run(debug=True)