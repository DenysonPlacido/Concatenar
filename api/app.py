from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_folder='../static', template_folder='../templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/concatenar', methods=['POST'])
def concatenar():
    data = request.json
    dados_brutos = data['valores']
    tipo = data['tipo']

    valores = [v.strip() for v in dados_brutos.splitlines() if v.strip()]
    blocos = []
    aspas = "'" if tipo == 'string' else ""

    for i in range(0, len(valores), 1000):
        grupo = valores[i:i + 1000]
        grupo_formatado = ','.join(f"{aspas}{v}{aspas}" for v in grupo)
        blocos.append(f"coluna IN ({grupo_formatado})")

    resultado = " OR ".join(blocos)
    return jsonify({"resultado": resultado})

# Vercel usa 'app' como export
handler = app
