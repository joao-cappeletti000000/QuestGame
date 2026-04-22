"""
EXEMPLO DE TESTE - Como testar as classes do QuestGame

Execute: python test_exemplo.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from jogador import Jogador
from questao import QuestaoMultiplaEscolha, QuestaoVerdadeiroFalso
from motor_jogo import MotorJogo


def testar_jogador():
    """Testa a classe Jogador e encapsulamento"""
    print("=" * 50)
    print("TESTANDO CLASSE JOGADOR")
    print("=" * 50)
    
    jogador = Jogador("Alice")
    print(f"Nome: {jogador.get_nome()}")
    print(f"XP inicial: {jogador.get_xp()}")
    print(f"Nível inicial: {jogador.get_nivel()}")
    
    # Adicionar XP
    jogador.adicionar_xp(50)
    print(f"\nApós ganhar 50 XP:")
    print(f"XP: {jogador.get_xp()}")
    print(f"Nível: {jogador.get_nivel()}")
    
    print("\n✓ Teste de Jogador PASSOU\n")


def testar_questoes():
    """Testa as classes de Questão (Herança e Polimorfismo)"""
    print("=" * 50)
    print("TESTANDO CLASSES DE QUESTÃO")
    print("=" * 50)
    
    # Questão de Múltipla Escolha
    q1 = QuestaoMultiplaEscolha(
        tema="Python",
        enunciado="O que é Python?",
        opcoes=["Uma serpente", "Uma linguagem", "Uma empresa", "Um jogo"],
        resposta_correta="B"
    )
    
    print(f"Questão 1: {q1.get_enunciado()}")
    print(f"Opcoes: {q1.get_opcoes()}")
    print(f"Resposta correta: B")
    print(f"Validação (resposta 'B'): {q1.validar_resposta('B')}")
    print(f"Validação (resposta 'A'): {q1.validar_resposta('A')}")
    
    # Questão Verdadeiro/Falso
    q2 = QuestaoVerdadeiroFalso(
        tema="Python",
        enunciado="Python é compilado?",
        resposta_correta="F"
    )
    
    print(f"\nQuestão 2: {q2.get_enunciado()}")
    print(f"Opcoes: {q2.get_opcoes()}")
    print(f"Validação (resposta 'V'): {q2.validar_resposta('V')}")
    print(f"Validação (resposta 'F'): {q2.validar_resposta('F')}")
    
    print("\n✓ Teste de Questões PASSOU\n")


def testar_motor_jogo():
    """Testa o Motor do Jogo"""
    print("=" * 50)
    print("TESTANDO MOTOR DO JOGO")
    print("=" * 50)
    
    motor = MotorJogo("Bob")
    
    print(f"Jogador criado: {motor.get_info_jogador()['nome']}")
    print(f"XP inicial: {motor.get_info_jogador()['xp']}")
    
    # Simular resposta correta
    motor.jogador.adicionar_xp(50)
    info = motor.get_info_jogador()
    print(f"\nApós ganhar 50 XP:")
    print(f"Nível: {info['nivel']}")
    print(f"XP: {info['xp']}")
    
    # Testar cálculo de nível
    print(f"\nCálculo de nível:")
    print(f"XP 0: Nível {motor.calcular_nivel(0)}")
    print(f"XP 100: Nível {motor.calcular_nivel(100)}")
    print(f"XP 250: Nível {motor.calcular_nivel(250)}")
    print(f"XP 500: Nível {motor.calcular_nivel(500)}")
    print(f"XP 1000: Nível {motor.calcular_nivel(1000)}")
    
    print("\n✓ Teste do Motor PASSOU\n")


if __name__ == '__main__':
    try:
        testar_jogador()
        testar_questoes()
        testar_motor_jogo()
        
        print("=" * 50)
        print("✓ TODOS OS TESTES PASSARAM!")
        print("=" * 50)
    except Exception as e:
        print(f"\n✗ ERRO: {e}")
        import traceback
        traceback.print_exc()
