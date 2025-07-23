from flask import Flask, render_template_string, request

app = Flask(__name__, Imagem_folder='Imagem')

html_template = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Concatenador</title>
    <link rel="icon" type="image/x-icon" href="{{ url_for('Imagem', filename='concatenar.ico') }}">
    <style>
        html, body {
            margin: 0;
            padding: 0;
            height: 100%;
            font-family: Arial, sans-serif;
            background-image: url("/Imagem/background.png");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
            color: rgb(134,134,134);
        }

        .wrapper {
            min-height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }

        .container {
            width: 500px;
            max-width: 450px;
            background-color: rgba(0, 0, 0, 0.80);
            padding: 20px;
            border-radius: 10px;
            box-sizing: border-box;
        }

        input {
            width: 390px;
            margin-top: 8px;
            margin-bottom:8px;
            padding: 8px;
            font-size: 14px;
            border-radius: 5px;
            border: none;
        }
      
      
      textarea {
            width: 390px;
            margin-top: 8px;
            padding: 8px;
            font-size: 14px;
            border-radius: 5px;
            border: none;
        }
      
      
            button {
            width: 15%;
            margin-top: 8px;
           
            padding: 1px;
            font-size: 10px;
            border-radius: 5px;
            border: none;
        }

        textarea {
            height: 100px;
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
            color: white;
            cursor: pointer;
        }

        .result-wrapper {
            position: relative;
            margin-top: 10px;
        }

        .copy-btn {
            position: absolute;
            top: 5px;
            right: 5px;
            background-color: #444;
            color: #fff;
            border: none;
            padding: 4px 8px;
            font-size: 12px;
            border-radius: 4px;
            cursor: pointer;
        }

        .result-box {
            white-space: pre-wrap;
            word-wrap: break-word;
            height: auto;
            background-color: #222;
            color: #ddd;
            border: 1px solid #444;
            padding: 10px;
            border-radius: 5px;
            font-size: 13px;
            min-height: 90px;
        }

        footer {
            text-align: center;
            font-size: 11px;
            color: #ccc;
            margin: 20px 0 10px 0;
        }
    </style>
</head>
<body>
    <div class="wrapper">
        <div class="container">
            <h3 style="text-align:center;">Concatenador para os Melhores da Implantação</h3>
            <form method="post">
                <label>Nome da Coluna:</label>
                <input type="text" name="coluna" value="{{ coluna }}">

                <label>Cole aqui os valores (1 por linha):</label>
                <textarea name="valores">{{ valores }}</textarea>

                <div class="btn-group">
                    <button name="tipo" value="string" class="btn">String</button>
                    <button name="tipo" value="numero" class="btn">Número</button>
                </div>
            </form>

            {% if resultado %}
                <label><strong>Resultado:</strong></label>
                <div class="result-wrapper">
                    <button class="copy-btn" onclick="copiarResultado()">Copiar</button>
                    <div class="result-box" id="resultado">{{ resultado }}</div>
                </div>
            {% endif %}
        </div>
        <footer>Desenvolvido por Denyson Deserto Plácido | WhatsApp: 67 99346-4728</footer>
    </div>

    <script>
        function copiarResultado() {
            const texto = document.getElementById("resultado").innerText;
            navigator.clipboard.writeText(texto).then(() => {
                alert("Copiado!");
            });
        }
    </script>
</body>
</html>


"""

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = ''
    coluna = ''
    valores = ''
    if request.method == 'POST':
        coluna = request.form['coluna'].strip()
        valores = request.form['valores'].strip().splitlines()
        tipo = request.form['tipo']

        
        valores = [v.strip() for v in valores if v.strip()]
        
        
        if tipo == 'string':
            valores = [f"'{v}'" for v in valores]

        
        blocos = [valores[i:i+1000] for i in range(0, len(valores), 1000)]
        resultado = ' OR\n'.join(
            [f"{coluna} IN ({', '.join(bloco)})" for bloco in blocos]
        )

    return render_template_string(html_template, resultado=resultado, coluna=coluna, valores='\n'.join(valores))



app = app


