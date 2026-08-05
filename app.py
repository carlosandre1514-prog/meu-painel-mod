import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Permite que o front-end no GitHub Pages converse com a API no Render
CORS(app)

# Pasta onde os arquivos enviados serão salvos temporariamente
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "mensagem": "API do Painel Mod rodando com sucesso!"
    })

@app.route('/upload', methods=['POST'])
def upload_apk():
    # Verifica se enviaram algum arquivo na requisição
    if 'file' not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"erro": "Nenhum arquivo selecionado"}), 400
    
    # Verifica se é um arquivo .apk
    if file and file.filename.endswith('.apk'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Pega o tamanho do arquivo salvo em Megabytes (MB)
        tamanho_mb = round(os.path.getsize(filepath) / (1024 * 1024), 2)
        
        return jsonify({
            "mensagem": "APK recebido com sucesso!",
            "nome_arquivo": file.filename,
            "tamanho": f"{tamanho_mb} MB",
            "caminho_servidor": filepath
        }), 200
    else:
        return jsonify({"erro": "Apenas arquivos .apk são permitidos"}), 400

if __name__ == '__main__':
    # Configuração de porta para ambiente local/Render
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
