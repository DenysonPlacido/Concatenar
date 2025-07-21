from flask import Flask, request, render_template_string
import os

app = Flask(__name__, static_folder="../static")

html_template = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Concatenador</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-image: url("/static/bg.png");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
            margin: 0;
            padding: 0;
            color: white;
        }
        .container {
            max-width: 500px;
            margin: 30px auto;
            background-color: rgba(0, 0, 0, 0.85);
            padding: 20px;
            border-radius: 10px;
        }
        input, textarea, button {
            width: 100%;
            margin-top: 10px;
            padding: 8px;
            font-size: 14px;
            border-radius: 5px;
        }
        textarea {
            height: 120px;
            resize: vertical;
        }
        .btn-group {
            display: flex;
            justify-content: space-between;
            gap: 10px;
            margin: 10px 0;
        }
        .btn {
            flex: 1;
            padding: 10px;
            background-color: crimson;
            border: none;
            color: white;
            cursor: pointer;
        }
        .result-box {
            height: 100px;
            overflow-y: auto;
            background-color: #222;
            color: #ddd;
            border: 1px solid #444;
            padding: 8px;
            border-radius: 5px;
            font-size: 13px;
        }
        footer {
            text-align: center;
            font-size: 10px;
            margin-top: 10px;
            color: #ccc;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2 style="text-align:center;">Concatenador para os Melhores da Implantação</h2>
        <form method="post">
            <label>Nome da Coluna:</label>
            <input type="text" name="coluna" value="{{ coluna }}">

            <label>Cole aqui os valores (1 por linha):</label>
            <textarea name="valores">{{ valores }}</textarea>

            <div class="btn-group">
                <button name="tipo" value="string" class="btn">String</button>
                <button name="tipo" value="numero" class="btn">Número</button>
                <button type="button" onclick="copiarResultado()" class="btn">Copiar</button>
            </div>
        </form>

        {% if resultado %}
            <strong>Resultado:</strong>
            <div class="result-box" id="resultado">{{ resultado }}</div>
        {% endif %}

        <footer>Desenvolvido por Denyson Deserto Plácido | WhatsApp: 67 99346-4728</footer>
    </div>

    <script>
        function copiarResultado() {
            const resultado = document.getElementById("resultado");
            if (resultado) {
                navigator.clipboard.writeText(resultado.innerText);
                alert("Copiado para a área de transferência!");
            }
        }
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = ""
    coluna = ""
    valores = ""
    if request.method == "POST":
        coluna = request.form.get("coluna", "").strip()
        valores = request.form.get("valores", "").strip()
        tipo = request.form.get("tipo", "string")
        linhas = [linha.strip() for linha in valores.splitlines() if linha.strip()]
        if tipo == "string":
            valores_formatados = ",".join(f"'{v}'" for v in linhas)
        else:
            valores_formatados = ",".join(v for v in linhas)
        resultado = f"{coluna} IN ({valores_formatados})"
    return render_template_string(html_template, resultado=resultado, coluna=coluna, valores=valores)


app = app
