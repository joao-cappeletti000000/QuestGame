"""
Módulo Questão - Define as classes para questões do quiz gamificado.
Implementa herança e polimorfismo com a classe base Questao e suas subclasses.
"""

from abc import ABC, abstractmethod


class Questao(ABC):
    """
    Classe abstrata base para todas as questões do jogo.
    Define a interface comum que todas as questões devem seguir.
    
    Atributos:
        _tema: str - Tema da questão (ex: Python, PHP)
        _enunciado: str - Texto da pergunta
        _resposta_correta: str - A resposta correta
        _dificuldade: int - Nível de dificuldade (1-3)
    """
    
    def __init__(self, tema, enunciado, resposta_correta, dificuldade=1):
        """
        Inicializa uma questão.
        
        Args:
            tema (str): Tema da questão
            enunciado (str): Texto da pergunta
            resposta_correta (str): Resposta correta
            dificuldade (int): Nível de dificuldade (padrão: 1)
        """
        self._tema = tema
        self._enunciado = enunciado
        self._resposta_correta = resposta_correta
        self._dificuldade = dificuldade
    
    def get_tema(self):
        """Retorna o tema da questão."""
        return self._tema
    
    def get_enunciado(self):
        """Retorna o enunciado da questão."""
        return self._enunciado
    
    @abstractmethod
    def validar_resposta(self, resposta_usuario):
        """
        Método abstrato para validar a resposta do usuário.
        Deve ser implementado pelas subclasses.
        
        Args:
            resposta_usuario: Resposta fornecida pelo usuário
            
        Returns:
            bool: True se a resposta está correta, False caso contrário
        """
        pass
    
    @abstractmethod
    def get_opcoes(self):
        """
        Método abstrato para retornar as opções de resposta.
        Deve ser implementado pelas subclasses.
        
        Returns:
            list: Lista com as opções de resposta
        """
        pass


class QuestaoMultiplaEscolha(Questao):
    """
    Classe que representa uma questão de múltipla escolha.
    Herda de Questao e implementa as características específicas.
    
    Atributos adicionais:
        opcoes: list - Lista de opções de resposta
    """
    
    def __init__(self, tema, enunciado, opcoes, resposta_correta, dificuldade=1):
        """
        Inicializa uma questão de múltipla escolha.
        
        Args:
            tema (str): Tema da questão
            enunciado (str): Texto da pergunta
            opcoes (list): Lista com as 4 opções (A, B, C, D)
            resposta_correta (str): Letra da resposta correta (A, B, C ou D)
            dificuldade (int): Nível de dificuldade
        """
        super().__init__(tema, enunciado, resposta_correta, dificuldade)
        self.opcoes = opcoes
    
    def validar_resposta(self, resposta_usuario):
        """
        Valida a resposta do usuário para questão de múltipla escolha.
        
        Args:
            resposta_usuario (str): Letra da resposta escolhida
            
        Returns:
            bool: True se a resposta está correta, False caso contrário
        """
        return resposta_usuario.upper() == self._resposta_correta.upper()
    
    def get_opcoes(self):
        """Retorna as opções de resposta."""
        return self.opcoes


class QuestaoVerdadeiroFalso(Questao):
    """
    Classe que representa uma questão de Verdadeiro/Falso.
    Herda de Questao e implementa as características específicas.
    """
    
    def __init__(self, tema, enunciado, resposta_correta, dificuldade=1):
        """
        Inicializa uma questão de Verdadeiro/Falso.
        
        Args:
            tema (str): Tema da questão
            enunciado (str): Texto da pergunta
            resposta_correta (str): "V" ou "F"
            dificuldade (int): Nível de dificuldade
        """
        super().__init__(tema, enunciado, resposta_correta, dificuldade)
    
    def validar_resposta(self, resposta_usuario):
        """
        Valida a resposta do usuário para questão Verdadeiro/Falso.
        
        Args:
            resposta_usuario (str): "V" ou "F"
            
        Returns:
            bool: True se a resposta está correta, False caso contrário
        """
        return resposta_usuario.upper() == self._resposta_correta.upper()
    
    def get_opcoes(self):
        """Retorna as opções padrão (Verdadeiro/Falso)."""
        return ["Verdadeiro", "Falso"]
