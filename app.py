import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from androguard.core.apk import APK
from androguard.core.axml import AXMLPrinter

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "mensagem": "API do Painel Mod com manifesto corrigido rodando!"
    })

@app.route('/upload', methods=['POST'])
def upload_apk():
    if 'file' not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"erro": "Nenhum arquivo selecionado"}), 400
    
    if file and file.filename.endswith('.apk'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        tamanho_mb = round(os.path.getsize(filepath) / (1024 * 1024), 2)
        
        try:
            a = APK(filepath)
            nome_pacote = a.get_package()
            nome_app = a.get_app_name()
            versao_codigo = a.get_androidversion_code()
            versao_nome = a.get_androidversion_name()
            
            # Extraindo as permissões
            permissoes = a.get_permissions()
            permissoes_resumo = list(permissoes)[:10] if permissoes else ["Nenhuma permissão especial encontrada"]
            
            # Extraindo e convertendo o AndroidManifest.xml de forma segura
            manifest_bytes = a.get_android_manifest_axml()
            if manifest_bytes:
                axml = AXMLPrinter(manifest_bytes.get_buff())
                manifesto_texto = axml.get_buff_xml().decode('utf-8', errors='ignore')
            else:
                manifesto_texto = "AndroidManifest.xml não encontrado ou ilegível."
                
        except Exception as e:
            nome_pacote = "Desconhecido"
            nome_app = file.filename
            versao_codigo = "N/A"
            versao_nome = "N/A"
            permissoes_resumo = [f"Erro: {str(e)}"]
            manifesto_texto = f"Erro ao extrair o manifesto: {str(e)}"
        
        return jsonify({
            "mensagem": "APK analisado com sucesso!",
            "nome_arquivo": file.filename,
            "tamanho": f"{tamanho_mb} MB",
            "pacote": nome_pacote,
            "nome_app": nome_app,
            "versao_codigo": versao_codigo,
            "versao_nome": versao_nome,
            "permissoes": permissoes_resumo,
            "manifesto": manifesto_texto
        }), 200
    else:
        return jsonify({"erro": "Apenas arquivos .apk são permitidos"}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
