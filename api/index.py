from flask import Flask, render_template_string, request

app = Flask(__name__, static_folder='static')

html_template = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Concatenar IN SQL</title>
    <link rel="icon" href="{{ url_for('static', filename='concatenar.ico') }}">
    <style>
        body {
            background-image: url('{{ url_for('static', filename='background.png') }}');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            color: white;
        }
        .container {
            max-width: 800px;
            margin: 40px auto;
            background-color: rgba(0, 0, 0, 0.85);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 0 20px rgba(0,0,0,0.6);
        }
        textarea {
            width: 100%;
            height: 120px;
            resize: none;
            padding: 10px;
            font-family: monospace;
            font-size: 14px;
            border-radius: 8px;
            margin-bottom: 10px;
        }
        .resultado {
            background-color: #111;
            padding: 15px;
            border-radius: 8px;
            font-family: monospace;
            font-size: 14px;
            color: #0f0;
            overflow-y: auto;
            max-height: 200px;
            white-space: pre-wrap;
            margin-top: 15px;
        }
        button, select, input[type="text"] {
            padding: 8px 14px;
            border: none;
            border-radius: 6px;
            font-size: 14px;
            margin: 5px 0;
        }
        .btn {
            background-color: #28a745;
            color: white;
            cursor: pointer;
        }
        .btn:hover {
            background-color: #218838;
        }
        .copy-btn {
            float: right;
            background: #444;
            border: none;
            color: white;
            padding: 6px 10px;
            border-radius: 5px;
            font-size: 12px;
            cursor: pointer;
        }
        .copy-btn:hover {
            background: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Concatenar valores para cláusula IN</h2>
        <form method="POST">
            <label>Nome da Coluna:</label><br>
            <input type="text" name="coluna" value="{{coluna}}" required><br>

            <label>Tipo dos Valores:</label><br>
            <select name="tipo">
                <option value="string">Texto (com aspas)</option>
                <option value="number" {% if request.form.get('tipo') == 'number' %}selected{% endif %}>Número (sem aspas)</option>
            </select><br>

            <label>Valores (1 por linha):</label><br>
            <textarea name="valores">{{valores}}</textarea><br>

            <button class="btn" type="submit">Concatenar</button>
        </form>

        {% if resultado %}
        <div class="resultado" id="resultadoBox">
            <button class="copy-btn" onclick="copiarResultado()">Copiar</button>
            {{ resultado }}
        </div>
        {% endif %}
    </div>

    <script>
        function copiarResultado() {
            const texto = document.getElementById("resultadoBox").innerText;
            navigator.clipboard.writeText(texto).then(() => {
                alert("Texto copiado com sucesso!");
            }, () => {
                alert("Erro ao copiar o texto.");
            });
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
            valores_formatados = [f"'{v}'" for v in linhas]
        else:
            valores_formatados = [v for v in linhas]
        # Agrupar a cada 10 por linha
        agrupado = [", ".join(valores_formatados[i:i+10]) for i in range(0, len(valores_formatados), 10)]
        resultado = f"{coluna} IN (\n  " + ",\n  ".join(agrupado) + "\n)"
    return render_template_string(html_template, resultado=resultado, coluna=coluna, valores=valores)

app = app
