from flask import Flask, render_template, request, jsonify
from datetime import datetime
import pandas as pd
import os

app = Flask(__name__)

EXCEL_FILE = "reportes.xlsx"

reportes = []

estado = 0
datos = {}


def guardar_en_excel(nuevo_reporte):

    df_nuevo = pd.DataFrame([nuevo_reporte])

    if os.path.exists(EXCEL_FILE):
        df_existente = pd.read_excel(EXCEL_FILE)
        df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
    else:
        df_final = df_nuevo

    df_final.to_excel(EXCEL_FILE, index=False)


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/mensaje", methods=["POST"])
def mensaje():

    global estado, datos

    data = request.json
    texto = data.get("mensaje", "").strip().lower()
    gps = data.get("gps", None)

    hora = datetime.now().strftime("%H:%M")

    respuesta = ""

    # RESET automático si está en estado inválido
    if estado not in [0,1,2,3,4,5]:
        estado = 0
        datos = {}

    # 0
    if estado == 0:
        estado = 1
        respuesta = "👋 ¿Cuál es tu nombre?"

    # 1
    elif estado == 1:
        datos["nombre"] = texto
        estado = 2
        respuesta = "📱 Escribe tu número"

    # 2
    elif estado == 2:
        datos["telefono"] = texto
        estado = 3
        respuesta = "🚰 Motivo del reporte"

    # 3
    elif estado == 3:
        datos["motivo"] = texto
        estado = 4
        respuesta = "📍 ¿Permites GPS? (si/no)"

    # 4
    elif estado == 4:

        if "si" in texto:
            datos["gps"] = gps
        else:
            datos["gps"] = "No permitido"

        datos["hora_reporte"] = hora

        reportes.append(datos.copy())
        guardar_en_excel(datos.copy())

        estado = 5
        respuesta = "✅ Guardado. ¿Otro reporte? (si/no)"

    # 5
    elif estado == 5:

        if "si" in texto:
            estado = 0
            datos = {}
            respuesta = "👍 Nuevo reporte"
        else:
            estado = 99
            respuesta = "🙏 Fin"

    return jsonify({"respuesta": respuesta})


@app.route("/reportes")
def ver_reportes():
    return jsonify(reportes)


if __name__ == "__main__":
    app.run(debug=True)