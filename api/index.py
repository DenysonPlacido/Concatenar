from flask import Flask, render_template_string, request

app = Flask(__name__, static_folder='static')

html_template = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Concatenador Implantação</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: url('/static/bg.png') no-repeat center center fixed;
            background-size: cover;
            margin: 0;
            padding: 0;
        }

        .container {
            max-width: 500px;
            margin: 40px auto;
            background: rgba(0, 0, 0, 0.9);
            padding: 20px;
            border-radius: 10px;
            color: white;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.4);
        }

        h2 {
            text-align: center;
            margin-bottom: 20px;
        }

        input, textarea, button {
            width: 100%;
            margin-bottom: 12px;
            padding: 8px;
            border-radius: 5px;
            border: none;
            font-size: 14px;
        }

        .buttons {
            display: flex;
            justify-content: space-between;
        }

        .buttons button {
            width: 32%;
            background-color: #d11b42;
            color: white;
            cursor: pointer;
            transition: 0.3s;
        }

        .buttons button:hover {
            background-color: #a91433;
        }

        .output {
            background: #222;
            padding: 10px;
            border-radius: 5px;
            white-space: pre-wrap;
            overflow-x: auto;
            color: #00ff00;
            font-size: 13px;
        }

        .footer {
            text-align: center;
            margin-top: 15px;
            font-size: 11px;
            color: #aaa;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Concatenador para os Melhores da Implantação</h2>
        <form method="post">
            <label>Nome da Coluna:</label>
            <input type="text" name="coluna" required>

            <label>Cole aqui os valores (1 por linha):</label>
            <textarea name="dados" rows="6" required></textarea>

            <div class="buttons">
                <button type="submit" name="tipo" value="string">String</button>
                <button type="submit" name="tipo" value="numero">Número</button>
                <button type="button" onclick="copiarResultado()">Copiar</button>
            </div>
        </form>

        {% if resultado %}
        <p><strong>Resultado:</strong></p>
        <div class="output" id="resultado">{{ resultado }}</div>
        {% endif %}

        <div class="footer">
            Desenvolvido por Denyson Deserto Plácido | WhatsApp: 67 99348-4728
        </div>
    </div>

    <script>
        function copiarResultado() {
            const texto = document.getElementById("resultado").innerText;
            navigator.clipboard.writeText(texto).then(() => {
                alert("Resultado copiado com sucesso!");
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
        
        # Formata valores conforme o tipo
        if tipo == "string":
            valores_formatados = [f"'{v}'" for v in linhas]
        else:
            valores_formatados = [v for v in linhas]
        
        # Agrupa em linhas com 10 valores por linha
        grupos = [", ".join(valores_formatados[i:i+10]) for i in range(0, len(valores_formatados), 10)]
        resultado = f"{coluna} IN (\n  " + ",\n  ".join(grupos) + "\n)"

    return render_template_string(html_template, resultado=resultado, coluna=coluna, valores=valores)


app = app


