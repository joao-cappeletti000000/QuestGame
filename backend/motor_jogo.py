"""
Módulo Motor do Jogo - Implementa a lógica central do sistema de quiz gamificado.
Gerencia as questões, controla o fluxo do jogo e calcula pontuações.
"""

import csv
from jogador import Jogador
from questao import QuestaoMultiplaEscolha, QuestaoVerdadeiroFalso


class MotorJogo:
    """
    Classe que implementa a lógica central do jogo de quiz.
    
    Atributos:
        jogador: Jogador - O jogador atual
        questoes: dict - Dicionário com questões organizadas por tema
        questao_atual: Questao - A questão que está sendo respondida
        tentativas: int - Número de tentativas na questão atual
    """
    
    # Constantes de pontuação
    XP_ACERTO_PRIMEIRA = 50
    XP_ACERTO_SEGUNDA = 20
    XP_ERRO = 0
    
    def __init__(self, nome_jogador):
        """
        Inicializa o motor do jogo.
        
        Args:
            nome_jogador (str): Nome do jogador
        """
        self.jogador = Jogador(nome_jogador)
        self.questoes = {}
        self.questao_atual = None
        self.tentativas = 0
    
    def carregar_questoes(self, caminho_arquivo):
        """
        Carrega questões de um arquivo CSV.
        
        Formato esperado do CSV:
        tema,tipo,enunciado,opcoes_ou_na,resposta,dificuldade
        
        Args:
            caminho_arquivo (str): Caminho do arquivo CSV
        """
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                leitor = csv.DictReader(arquivo)
                for linha in leitor:
                    tema = linha['tema']
                    tipo = linha['tipo']
                    enunciado = linha['enunciado']
                    resposta = linha['resposta']
                    dificuldade = int(linha.get('dificuldade', 1))
                    
                    # Inicializa lista de questões por tema se não existir
                    if tema not in self.questoes:
                        self.questoes[tema] = []
                    
                    # Cria questão baseada no tipo
                    if tipo == 'multipla':
                        opcoes = linha['opcoes'].split('|')
                        questao = QuestaoMultiplaEscolha(
                            tema, enunciado, opcoes, resposta, dificuldade
                        )
                    elif tipo == 'verdadeiro_falso':
                        questao = QuestaoVerdadeiroFalso(
                            tema, enunciado, resposta, dificuldade
                        )
                    
                    self.questoes[tema].append(questao)
            
            print(f"✓ Questões carregadas com sucesso de {caminho_arquivo}")
        except FileNotFoundError:
            print(f"✗ Erro: Arquivo {caminho_arquivo} não encontrado.")
        except Exception as erro:
            print(f"✗ Erro ao carregar questões: {erro}")
    
    def obter_temas_disponiveis(self):
        """
        Retorna lista de temas disponíveis.
        
        Returns:
            list: Lista com os temas das questões carregadas
        """
        return list(self.questoes.keys())
    
    def selecionar_questao_aleatoria(self, tema):
        """
        Seleciona uma questão aleatória do tema especificado.
        
        Args:
            tema (str): Tema da questão
            
        Returns:
            Questao: A questão selecionada ou None se tema inválido
        """
        import random
        
        if tema not in self.questoes:
            print(f"✗ Tema '{tema}' não disponível.")
            return None
        
        self.questao_atual = random.choice(self.questoes[tema])
        self.tentativas = 0
        return self.questao_atual
    
    def responder_questao(self, resposta_usuario):
        """
        Processa a resposta do usuário e calcula XP.
        
        Lógica de pontuação:
        - 1ª tentativa correta: +50 XP
        - 2ª tentativa correta: +20 XP
        - Erro: 0 XP
        
        Args:
            resposta_usuario: Resposta fornecida pelo usuário
            
        Returns:
            dict: Dicionário com resultado {'correto': bool, 'xp': int, 'mensagem': str}
        """
        if self.questao_atual is None:
            return {'correto': False, 'xp': 0, 'mensagem': 'Nenhuma questão selecionada.'}
        
        self.tentativas += 1
        correto = self.questao_atual.validar_resposta(resposta_usuario)
        xp_ganho = 0
        mensagem = ""
        
        if correto:
            if self.tentativas == 1:
                xp_ganho = self.XP_ACERTO_PRIMEIRA
                mensagem = f"✓ Correto! +{xp_ganho} XP (Primeira tentativa)"
            elif self.tentativas == 2:
                xp_ganho = self.XP_ACERTO_SEGUNDA
                mensagem = f"✓ Correto! +{xp_ganho} XP (Segunda tentativa)"
            else:
                xp_ganho = 0
                mensagem = f"✗ Resposta correta, mas expirou o número de tentativas. 0 XP"
        else:
            if self.tentativas < 2:
                mensagem = f"✗ Incorreto. Tente novamente. ({self.tentativas} tentativa(s))"
            else:
                mensagem = f"✗ Errado. A resposta correta é: {self.questao_atual._resposta_correta}"
        
        # Adiciona XP ao jogador
        self.jogador.adicionar_xp(xp_ganho)
        
        return {
            'correto': correto,
            'xp': xp_ganho,
            'mensagem': mensagem,
            'resposta_correta': self.questao_atual._resposta_correta
        }
    
    def get_info_jogador(self):
        """
        Retorna informações do jogador.
        
        Returns:
            dict: Dicionário com dados do jogador
        """
        return {
            'nome': self.jogador.get_nome(),
            'xp': self.jogador.get_xp(),
            'nivel': self.jogador.get_nivel(),
            'nome_nivel': self.jogador.get_nome_nivel()
        }
    
    def calcular_nivel(self, xp_atual):
        """
        Calcula o nível baseado no XP.
        
        Args:
            xp_atual (int): Total de XP
            
        Returns:
            int: Nível do jogador
        """
        if xp_atual < 100:
            return 1
        elif xp_atual < 250:
            return 2
        elif xp_atual < 500:
            return 3
        elif xp_atual < 1000:
            return 4
        else:
            return 5
