# api/index.py

from flask import Flask, request, render_template, send_from_directory
import json


app = Flask(__name__, static_url_path="/api/static", static_folder="static", template_folder="templates")


@app.route('/api/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/', methods=['GET', 'POST'])
def index():
    
    resultado = ''
    coluna = ''
    valores = ''

    
    json_input = ''
    json_output = ''
    json_error = ''

    active_tab = 'concat'  

    if request.method == 'POST':
        form_type = request.form.get('form_type')
        if form_type == 'concat':
            active_tab = 'concat'
            coluna = request.form.get('coluna', '').strip()
            valores = request.form.get('valores', '').strip().splitlines()
            tipo = request.form.get('tipo')
            valores = [v.strip() for v in valores if v.strip()]
            if tipo == 'string':
                valores = [f"'{v}'" for v in valores]
            blocos = [valores[i:i+1000] for i in range(0, len(valores), 1000)]
            resultado = ' OR\n'.join(
                [f"{coluna} IN ({', '.join(bloco)})" for bloco in blocos]
            )
        elif form_type == 'json':
            active_tab = 'json'
            json_input = request.form.get('json_input', '').strip()
            if json_input:
                try:
                    obj = json.loads(json_input)
                    json_output = json.dumps(obj, indent=1, separators=(',', ': '), ensure_ascii=False).replace("    ", "\t")
                except Exception as e:
                    json_error = f"JSON inválido: {e}"
            else:
                json_error = "Por favor, insira um JSON válido."

    return render_template('index.html',
                           resultado=resultado,
                           coluna=coluna,
                           valores='\n'.join(valores),
                           json_input=json_input,
                           json_output=json_output,
                           json_error=json_error,
                           active_tab=active_tab)

if __name__ == '__main__':
    app.run(debug=True)
