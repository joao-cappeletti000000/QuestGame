"""
Módulo Principal da Aplicação - Servidor Flask que conecta frontend e backend.
Implementa a API REST para comunicação com a interface web.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from motor_jogo import MotorJogo

app = Flask(__name__)
CORS(app)

# Dicionário para armazenar sessões de jogo
sessoes_jogo = {}


@app.route('/api/criar-jogo', methods=['POST'])
def criar_jogo():
    """
    Cria uma nova sessão de jogo para um jogador.
    
    Dados esperados:
        {
            "nome_jogador": "João",
            "id_sessao": "sessao_123"
        }
    
    Retorna:
        {
            "sucesso": true,
            "mensagem": "Jogo criado com sucesso",
            "jogador": {...}
        }
    """
    dados = request.json
    nome_jogador = dados.get('nome_jogador')
    id_sessao = dados.get('id_sessao', 'default')
    
    if not nome_jogador:
        return jsonify({'sucesso': False, 'mensagem': 'Nome do jogador é obrigatório'}), 400
    
    # Cria nova sessão de jogo
    motor = MotorJogo(nome_jogador)
    sessoes_jogo[id_sessao] = motor
    
    # Carrega questões padrão
    caminho_questoes = os.path.join(os.path.dirname(__file__), '..', 'dados', 'questoes.csv')
    motor.carregar_questoes(caminho_questoes)
    
    return jsonify({
        'sucesso': True,
        'mensagem': 'Jogo criado com sucesso',
        'jogador': motor.get_info_jogador(),
        'temas': motor.obter_temas_disponiveis()
    })


@app.route('/api/temas', methods=['GET'])
def obter_temas():
    """
    Retorna os temas disponíveis.
    
    Parâmetros:
        id_sessao: ID da sessão do jogo
    
    Retorna:
        {
            "sucesso": true,
            "temas": ["Python", "PHP", ...]
        }
    """
    id_sessao = request.args.get('id_sessao', 'default')
    
    if id_sessao not in sessoes_jogo:
        return jsonify({'sucesso': False, 'mensagem': 'Sessão não encontrada'}), 404
    
    motor = sessoes_jogo[id_sessao]
    temas = motor.obter_temas_disponiveis()
    
    return jsonify({'sucesso': True, 'temas': temas})


@app.route('/api/proxima-questao', methods=['POST'])
def proxima_questao():
    """
    Seleciona a próxima questão de um tema específico.
    
    Dados esperados:
        {
            "tema": "Python",
            "id_sessao": "sessao_123"
        }
    
    Retorna:
        {
            "sucesso": true,
            "questao": {
                "enunciado": "O que é Python?",
                "tipo": "multipla",
                "opcoes": ["A", "B", "C", "D"]
            }
        }
    """
    dados = request.json
    tema = dados.get('tema')
    id_sessao = dados.get('id_sessao', 'default')
    
    if id_sessao not in sessoes_jogo:
        return jsonify({'sucesso': False, 'mensagem': 'Sessão não encontrada'}), 404
    
    motor = sessoes_jogo[id_sessao]
    questao = motor.selecionar_questao_aleatoria(tema)
    
    if questao is None:
        return jsonify({'sucesso': False, 'mensagem': 'Tema não disponível'}), 404
    
    return jsonify({
        'sucesso': True,
        'questao': {
            'enunciado': questao.get_enunciado(),
            'opcoes': questao.get_opcoes(),
            'tipo': 'multipla' if hasattr(questao, 'opcoes') else 'verdadeiro_falso'
        }
    })


@app.route('/api/responder', methods=['POST'])
def responder_questao():
    """
    Processa a resposta do usuário e calcula XP.
    
    Dados esperados:
        {
            "resposta": "A",
            "id_sessao": "sessao_123"
        }
    
    Retorna:
        {
            "sucesso": true,
            "correto": true,
            "xp": 50,
            "mensagem": "Correto! +50 XP",
            "jogador": {...}
        }
    """
    dados = request.json
    resposta = dados.get('resposta')
    id_sessao = dados.get('id_sessao', 'default')
    
    if id_sessao not in sessoes_jogo:
        return jsonify({'sucesso': False, 'mensagem': 'Sessão não encontrada'}), 404
    
    motor = sessoes_jogo[id_sessao]
    resultado = motor.responder_questao(resposta)
    
    return jsonify({
        'sucesso': True,
        **resultado,
        'jogador': motor.get_info_jogador()
    })


@app.route('/api/jogador', methods=['GET'])
def obter_jogador():
    """
    Retorna informações do jogador.
    
    Parâmetros:
        id_sessao: ID da sessão do jogo
    
    Retorna:
        {
            "sucesso": true,
            "jogador": {
                "nome": "João",
                "xp": 150,
                "nivel": 2,
                "nome_nivel": "Desenvolvedor Júnior"
            }
        }
    """
    id_sessao = request.args.get('id_sessao', 'default')
    
    if id_sessao not in sessoes_jogo:
        return jsonify({'sucesso': False, 'mensagem': 'Sessão não encontrada'}), 404
    
    motor = sessoes_jogo[id_sessao]
    
    return jsonify({'sucesso': True, 'jogador': motor.get_info_jogador()})


@app.route('/api/saude', methods=['GET'])
def saude():
    """
    Endpoint de verificação de saúde da API.
    
    Retorna:
        {"status": "ok"}
    """
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
