"""
Módulo Jogador - Define a classe que representa um jogador no sistema.
Implementa encapsulamento para proteger os dados do jogador contra manipulação indevida.
"""


class Jogador:
    """
    Classe que representa um jogador no jogo de quiz gamificado.
    
    Atributos privados:
        __nome: str - Nome do jogador
        __xp: int - Pontos de experiência do jogador
        __nivel: int - Nível atual do jogador
    
    Constantes de nível:
        NIVEIS: dict - Mapeamento entre experiência e nome do nível
    """
    
    NIVEIS = {
        0: "Iniciante",
        100: "Padawan",
        250: "Desenvolvedor Júnior",
        500: "Desenvolvedor Pleno",
        1000: "Desenvolvedor Sênior"
    }
    
    def __init__(self, nome):
        """
        Inicializa um novo jogador.
        
        Args:
            nome (str): O nome do jogador
        """
        self.__nome = nome
        self.__xp = 0
        self.__nivel = 1
    
    def get_nome(self):
        """Retorna o nome do jogador."""
        return self.__nome
    
    def get_xp(self):
        """Retorna os pontos de experiência do jogador."""
        return self.__xp
    
    def get_nivel(self):
        """Retorna o nível atual do jogador."""
        return self.__nivel
    
    def adicionar_xp(self, quantidade):
        """
        Adiciona pontos de experiência ao jogador e verifica se houve evolução de nível.
        
        Args:
            quantidade (int): Quantidade de XP a adicionar
        """
        self.__xp += quantidade
        self.__atualizar_nivel()
    
    def __atualizar_nivel(self):
        """
        Atualiza o nível do jogador baseado no XP acumulado.
        Método privado que é chamado automaticamente após adicionar XP.
        """
        for xp_minimo, nivel in sorted(self.NIVEIS.items(), reverse=True):
            if self.__xp >= xp_minimo:
                self.__nivel = self.NIVEIS.get(xp_minimo, len(self.NIVEIS))
                break
    
    def get_nome_nivel(self):
        """Retorna o nome do nível atual do jogador."""
        niveis_invertidos = {v: k for k, v in enumerate(self.NIVEIS.values())}
        return niveis_invertidos.get(self.__nivel, "Iniciante")
    
    def __repr__(self):
        """Representação textual do jogador."""
        return f"Jogador({self.__nome}, Nível: {self.__nivel}, XP: {self.__xp})"
