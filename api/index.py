from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__, static_url_path="/static", static_folder="static", template_folder="templates")

@app.route('api/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

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
    return render_template('index.html', resultado=resultado, coluna=coluna, valores='\n'.join(valores))

app = app
