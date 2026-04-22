# QuestGame - O Motor de Conhecimento

Um aplicativo de quiz gamificado desenvolvido com **Programação Orientada a Objetos**, arquitetura clean e interface web moderna.

## 🎮 Sobre o Projeto

QuestGame é uma atividade educacional que ensina alunos a construir um sistema completo de quiz com gamificação, cobrindo:

- **Fase 1**: Paradigmas de POO (Classes, Herança, Polimorfismo, Encapsulamento)
- **Fase 2**: Motor do Jogo (Tipos de dados, Controle de fluxo, Funções)
- **Fase 3**: Persistência de dados (Arquivos CSV)
- **Fase 4**: Interface Visual (HTML, CSS, JavaScript)
- **Fase 5**: Entrega Profissional (Documentação e Deploy)

## ⚡ Sistema de Gamificação

| Evento | XP | Descrição |
|--------|-----|-----------|
| ✓ Acerto 1ª tentativa | +50 | Resposta correta na primeira |
| ✓ Acerto 2ª tentativa | +20 | Resposta correta na segunda |
| ✗ Erro | 0 | Resposta incorreta |

### Progressão de Níveis

| Nível | Nome | XP Mínimo |
|-------|------|-----------|
| 1 | Iniciante | 0 XP |
| 2 | Padawan | 100 XP |
| 3 | Desenvolvedor Júnior | 250 XP |
| 4 | Desenvolvedor Pleno | 500 XP |
| 5 | Desenvolvedor Sênior | 1000 XP |

## 📁 Estrutura do Projeto

```
QuestGame/
├── backend/                    # Lógica do jogo e servidor
│   ├── jogador.py             # Classe Jogador (Encapsulamento)
│   ├── questao.py             # Classes Questao, QuestaoMultiplaEscolha, QuestaoVerdadeiroFalso
│   ├── motor_jogo.py          # MotorJogo (Controle de fluxo, Coleções)
│   ├── app.py                 # Servidor Flask (API REST)
│   └── requirements.txt        # Dependências Python
├── frontend/                   # Interface web
│   ├── index.html             # Estrutura HTML
│   ├── styles.css             # Estilos CSS
│   └── script.js              # Lógica JavaScript
├── dados/                     # Banco de dados
│   └── questoes.csv           # Questões e respostas
└── docs/                      # Documentação
    └── README.md              # Este arquivo
```

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)
- Navegador web moderno

### Instalação

1. **Clone ou extraia o projeto:**
   ```bash
   cd QuestGame
   ```

2. **Instale as dependências Python:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Inicie o servidor Flask:**
   ```bash
   python app.py
   ```
   
   Você verá: `Running on http://127.0.0.1:5000`

4. **Abra o navegador:**
   - Abra `frontend/index.html` em seu navegador
   - Ou acesse via servidor local

## 🎯 Como Jogar

1. **Digite seu nome** de jogador
2. **Escolha um tema** (Python, PHP, Paradigmas, Dados)
3. **Responda as perguntas** do tema escolhido
4. **Ganhe XP** e suba de nível!

## 📚 Conceitos Educacionais

### Fase 1: Paradigmas de POO ✅

- **Classe Jogador**: Exemplo de encapsulamento com atributos privados (`__xp`, `__nivel`)
- **Herança**: `QuestaoMultiplaEscolha` e `QuestaoVerdadeiroFalso` herdam de `Questao`
- **Polimorfismo**: Método `validar_resposta()` implementado diferentemente em cada subclasse
- **Abstração**: Classe abstrata `Questao` define a interface

### Fase 2: Motor do Jogo ✅

- **Tipos de Dados**: int, str, bool, list, dict
- **Coleções**: `questoes` é um dicionário de listas
- **Controle de Fluxo**: if/else para validar respostas
- **Funções**: `responder_questao()`, `calcular_nivel()`
- **Operadores**: `==` para comparação, `+=` para acúmulo

### Fase 3: Persistência de Dados ✅

- **Arquivos CSV**: `dados/questoes.csv` armazena todas as questões
- **Leitura de Arquivo**: Carregamento dinâmico em `motor_jogo.py`

### Fase 4: Interface Visual ✅

- **HTML**: Estrutura semântica com múltiplas telas
- **CSS**: Design responsivo, animações, gradientes
- **JavaScript**: Interatividade e requisições AJAX

## 📝 Documentação do Código

Cada classe e método possui documentação em docstrings:

```python
class Jogador:
    """
    Classe que representa um jogador no jogo de quiz gamificado.
    
    Atributos privados:
        __nome: str - Nome do jogador
        __xp: int - Pontos de experiência do jogador
    """
    
    def adicionar_xp(self, quantidade):
        """Adiciona pontos de experiência ao jogador."""
```

## 🔌 API REST

### Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/criar-jogo` | Cria nova sessão |
| GET | `/api/temas` | Lista temas disponíveis |
| POST | `/api/proxima-questao` | Carrega questão |
| POST | `/api/responder` | Processa resposta |
| GET | `/api/jogador` | Dados do jogador |

## 🛠️ Estendendo o Projeto

### Adicionar Novas Questões

Edite `dados/questoes.csv`:

```csv
tema,tipo,enunciado,opcoes_ou_na,resposta,dificuldade
Python,multipla,"Sua pergunta?","Opção A|Opção B|Opção C|Opção D",A,1
```

### Adicionar Novo Tipo de Questão

1. Crie uma subclasse em `backend/questao.py`:

```python
class QuestaoRespotaAberta(Questao):
    def validar_resposta(self, resposta_usuario):
        # Implementar validação
        pass
``
