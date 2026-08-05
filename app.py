from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Pasta temporária para salvar os APKs enviados
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return "Servidor Backend rodando com sucesso!"

@app.route('/upload', methods=['POST'])
def upload_apk():
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nome de arquivo inválido'}), 400
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    return jsonify({
        'success': True, 
        'message': f'Arquivo {file.filename} recebido e salvo na nuvem com sucesso!'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
