from flask import Flask, request, jsonify

app = Flask(__name__, static_folder='static', static_url_path='/static')

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8" />
  <title>Concatenador</title>
  <style>
    body {
      margin: 0;
      padding: 0;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background-image: url("/static/bg.png");
      background-size: cover;
      background-position: center;
      color: #fff;
      backdrop-filter: brightness(0.7);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    .container {
      max-width: 500px;
      margin: auto;
      padding: 20px;
      background-color: rgba(0, 0, 0, 0.65);
      border-radius: 10px;
      box-shadow: 0 0 10px #000;
    }

    h2 {
      text-align: center;
      font-size: 18px;
      margin-bottom: 15px;
    }

    label {
      font-size: 13px;
    }

    textarea, input[type="text"] {
      width: 100%;
      padding: 8px;
      border-radius: 6px;
      border: none;
      margin-bottom: 12px;
      font-size: 12px;
    }

    textarea {
      height: 120px;
      resize: vertical;
    }

    button {
      margin-top: 5px;
      margin-right: 8px;
      padding: 8px 14px;
      border: none;
      border-radius: 5px;
      background-color: #e63946;
      color: white;
      cursor: pointer;
      font-size: 12px;
      font-weight: bold;
      transition: 0.3s;
    }

    button:hover {
      background-color: #d62828;
    }

    #resultado {
      white-space: pre-wrap;
      background: #f1f1f1;
      color: #222;
      padding: 10px;
      border-radius: 6px;
      margin-top: 15px;
      min-height: 80px;
      font-size: 12px;
      font-family: monospace;
    }

    footer {
      text-align: center;
      font-size: 10px;
      margin-top: auto;
      padding: 10px;
      background-color: rgba(0, 0, 0, 0.7);
      color: #ccc;
    }
  </style>
</head>
<body>
  <div class="container">
    <h2>Concatenador para os Melhores da Implantação</h2>

    <label for="coluna">Nome da Coluna:</label>
    <input type="text" id="coluna" placeholder="Ex: ID_CLIENTE" />

    <label for="entrada">Cole aqui os valores (1 por linha):</label>
    <textarea id="entrada" placeholder="Exemplo:&#10;123&#10;456&#10;789"></textarea>

    <div>
      <button onclick="concatenar('string')">String</button>
      <button onclick="concatenar('number')">Número</button>
      <button onclick="copiarResultado()">Copiar</button>
    </div>

    <h3 style="font-size:14px;margin-top:15px;">Resultado:</h3>
    <div id="resultado"></div>
  </div>

  <footer>
    Desenvolvido por Denyson Deserto Placido | WhatsApp: 67 99346-4728
  </footer>

  <script>
    async function concatenar(tipo) {
      const valores = document.getElementById('entrada').value;
      const coluna = document.getElementById('coluna').value;

      if (!coluna.trim()) {
        alert("Informe o nome da coluna.");
        return;
      }

      const resposta = await fetch('/concatenar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ valores, tipo, coluna })
      });

      const data = await resposta.json();
      document.getElementById('resultado').textContent = data.resultado;
    }

    function copiarResultado() {
      const texto = document.getElementById('resultado').textContent;
      if (!texto) return;

      navigator.clipboard.writeText(texto).then(() => {
        alert('Resultado copiado com sucesso!');
      });
    }
  </script>
</body>
</html>
'''

@app.route('/concatenar', methods=['POST'])
def concatenar():
    data = request.json
    dados_brutos = data['valores']
    tipo = data['tipo']
    nome_coluna = data.get('coluna', 'coluna')

    valores = [v.strip() for v in dados_brutos.splitlines() if v.strip()]
    blocos = []
    aspas = "'" if tipo == 'string' else ""

    for i in range(0, len(valores), 1000):
        grupo = valores[i:i + 1000]
        grupo_formatado = ','.join(f"{aspas}{v}{aspas}" for v in grupo)
        blocos.append(f"{nome_coluna} IN ({grupo_formatado})")

    resultado = " OR ".join(blocos)
    return jsonify({"resultado": resultado})
