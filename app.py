from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "aquaguard_secret_key"

# 🔥 IMPORTANTE: mantener sesión estable
app.config["SESSION_PERMANENT"] = True

reportes = []

EXCEL_FILE = os.path.join(os.path.expanduser("~"), "Desktop", "reportes.xlsx")


@app.route("/")
def inicio():
    return render_template("index.html")


# 📊 guardar en Excel
def guardar_en_excel(nuevo_reporte):

    df_nuevo = pd.DataFrame([nuevo_reporte])

    # si el archivo ya existe, se agrega
    if os.path.exists(EXCEL_FILE):
        df_existente = pd.read_excel(EXCEL_FILE)
        df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
    else:
        df_final = df_nuevo

    df_final.to_excel(EXCEL_FILE, index=False)


@app.route("/mensaje", methods=["POST"])
def mensaje():

    data = request.json
    texto = data.get("mensaje", "").strip().lower()
    gps = data.get("gps", None)

    hora = datetime.now().strftime("%H:%M")

    # 🔥 FORZAR INICIO DE SESIÓN SI NO EXISTE
    session.setdefault("paso", 0)
    session.setdefault("datos", {})

    paso = session.get("paso", 0)
    datos = session.get("datos", {})

    respuesta = ""

    # ======================
    # 0 - NOMBRE
    # ======================
    if paso == 0:
        session["datos"] = {"hora_inicio": hora}
        session["paso"] = 1
        respuesta = "👋 ¿Cuál es tu nombre?"

    # ======================
    # 1 - NOMBRE
    # ======================
    elif paso == 1:
        datos["nombre"] = texto
        session["datos"] = datos
        session["paso"] = 2
        respuesta = "📱 Escribe tu número telefónico"

    # ======================
    # 2 - TELÉFONO
    # ======================
    elif paso == 2:
        datos["telefono"] = texto
        session["datos"] = datos
        session["paso"] = 3
        respuesta = "🚰 Describe el motivo del reporte"

    # ======================
    # 3 - MOTIVO
    # ======================
    elif paso == 3:
        datos["motivo"] = texto
        session["datos"] = datos
        session["paso"] = 4
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

        session["paso"] = 5

        respuesta = "✅ Reporte guardado. ¿Deseas hacer otro? (si / no)"

    # ======================
    # 5 - REPETIR
    # ======================
    elif paso == 5:

        if "si" in texto:
            session["paso"] = 0
            session["datos"] = {}
            respuesta = "👍 Perfecto, iniciemos otro reporte"
        else:
            session.clear()
            respuesta = "🙏 Gracias por usar Ñätho AquaGuard"

    return jsonify({"respuesta": respuesta})

# 📊 ver reportes en JSON
@app.route("/reportes")
def ver_reportes():
    return jsonify(reportes)


if __name__ == "__main__":
    app.run(debug=True)