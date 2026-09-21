from flask import Flask, request, jsonify

app = Flask(__name__)

# Lista para armazenar as temperaturas registradas em memória
leituras_temperatura = []

# Rota para receber a leitura do sensor (Método POST)
@app.route('/sensores/clima', methods=['POST'])
def registrar_leitura():
    dados = request.get_json()
    
    dispositivo_id = dados.get('id')
    temperatura = dados.get('temperatura')
    
    # Adiciona a temperatura informada à nossa lista
    if temperatura is not None:
        leituras_temperatura.append(temperatura)
    
    resposta = {
        "mensagem": f"Leitura do sensor {dispositivo_id} recebida com sucesso!",
        "status": "ativo",
        "temperatura_registrada": temperatura
    }
    
    return jsonify(resposta), 201

# Rota para consultar o resumo das leituras (Método GET)
@app.route('/sensores/clima', methods=['GET'])
def consultar_resumo():
    # Verifica se a lista está vazia para evitar erro de divisão por zero
    if len(leituras_temperatura) == 0:
        return jsonify({"mensagem": "Nenhuma leitura registrada ainda."}), 404
        
    # Calcula a média das temperaturas
    media = sum(leituras_temperatura) / len(leituras_temperatura)
    
    # Lógica de verificação dos alertas
    alerta = "Clima agradável"
    if media > 30:
        alerta = "Alerta de calor"
    elif media < 15:
        alerta = "Alerta de frio"
        
    # Monta a resposta JSON
    resposta = {
        "total_de_leituras": len(leituras_temperatura),
        "media_temperatura": round(media, 2), # Arredonda para 2 casas decimais
        "status_alerta": alerta
    }
    
    return jsonify(resposta), 200




if __name__ == '__main__':
    app.run(debug=True)
