from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/mensaje", methods=["POST"])
def mensaje():
    data = request.json
    texto = data["mensaje"]

    if texto.lower() == "hola":
        respuesta = "Hola mundo"
    else:
        respuesta = "No entiendo el mensaje"

    return jsonify({"respuesta": respuesta})

if __name__ == "__main__":
    app.run(debug=True)