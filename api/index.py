from flask import Flask, render_template, request, jsonify
from vercel_flask import VercelHandler  # <- importante

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

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

    resultado = "\n OR ".join(blocos)
    return jsonify({"resultado": resultado})


handler = VercelHandler(app)
