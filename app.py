import os

from flask import Flask, render_template, request
from nlp_pipeline import DEFAULT_TEXT, NLPipeline

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "clave-desarrollo-nlp")

pipeline = NLPipeline()


@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    texto = DEFAULT_TEXT
    etapa_activa = None

    if request.method == "POST":
        texto = request.form.get("texto", DEFAULT_TEXT)
        if not texto.strip():
            texto = DEFAULT_TEXT

        etapa = request.form.get("etapa", "todas")
        resultado_completo = pipeline.procesar(texto)

        if etapa == "todas":
            resultado = resultado_completo
            etapa_activa = "todas"
        else:
            resultado = {"texto_bruto": texto}
            resultado[etapa] = resultado_completo[etapa]
            etapa_activa = etapa

    return render_template(
        "index.html",
        resultado=resultado,
        texto=texto,
        etapa_activa=etapa_activa,
    )


@app.route("/api/procesar", methods=["POST"])
def api_procesar():
    data = request.get_json(force=True)
    texto = data.get("texto", DEFAULT_TEXT)
    resultado = pipeline.procesar(texto)
    return resultado


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
