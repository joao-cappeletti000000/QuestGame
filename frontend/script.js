/* ====================================
   QUESTGAME - JAVASCRIPT OTIMIZADO
   Lógica de Jogo - Versão Rápida
   ==================================== */

// Configuração da API
const API_BASE = 'http://localhost:5000/api';
let ID_SESSAO = 'sessao_' + Math.random().toString(36).substr(2, 9);

// Estado do jogo
let estadoJogo = {
    jogador: null,
    temaAtual: null,
    questoes_carregadas: {},
    questao_atual: null,
    resposta_atual: null,
    temas: [],
    tentativas: 0
};

// ====== TROCAR TELAS ======

function mostrarTela(idTela) {
    document.querySelectorAll('.tela').forEach(tela => tela.classList.remove('ativa'));
    document.getElementById(idTela).classList.add('ativa');
}

// ====== INICIAR JOGO ======

function iniciarJogo() {
    const nomeJogador = document.getElementById('nomeJogador').value.trim();

    if (!nomeJogador) {
        alert('Digite seu nome!');
        return;
    }

    // Mostrar carregando
    document.getElementById('nomeJogador').disabled = true;

    fetch(`${API_BASE}/criar-jogo`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            nome_jogador: nomeJogador,
            id_sessao: ID_SESSAO
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.sucesso) {
            estadoJogo.jogador = data.jogador;
            estadoJogo.temas = data.temas;
            estadoJogo.questoes_carregadas = data.temas_questoes || {};
            
            mostrarTela('telaSelecaoTema');
            exibirTemas();
        }
    })
    .catch(erro => alert('Erro de conexão'));
}

// ====== EXIBIR TEMAS ======

function exibirTemas() {
    const container = document.getElementById('containerTemas');
    container.innerHTML = '';

    const emojis = { 'Python': '🐍', 'PHP': '🐘', 'Paradigmas': '🏛️', 'Dados': '💾' };

    estadoJogo.temas.forEach(tema => {
        const botao = document.createElement('button');
        botao.className = 'tema-botao';
        botao.innerHTML = `<span>${emojis[tema] || '📚'}</span>${tema}`;
        botao.onclick = () => selecionarTema(tema);
        container.appendChild(botao);
    });

    atualizarInfoJogador('nomeExibicao', 'nivelExibicao', 'xpExibicao');
}

// ====== SELECIONAR TEMA ======

function selecionarTema(tema) {
    estadoJogo.temaAtual = tema;
    mostrarTela('telaJogo');
    atualizarInfoJogador('nomeExibicao2', 'nivelExibicao2', 'xpExibicao2');
    document.getElementById('temaBadge').textContent = tema;
    carregarNovaQuestao();
}

// ====== CARREGAR QUESTÃO ======

function carregarNovaQuestao() {
    document.getElementById('containerOpcoes').innerHTML = '';
    document.getElementById('mensagemResultado').className = 'mensagem-resultado';
    document.getElementById('mensagemResultado').textContent = '';
    document.getElementById('botaoResponder').style.display = 'inline-block';
    document.getElementById('botaoProxima').style.display = 'none';
    document.getElementById('enunciado').textContent = 'Carregando...';
    estadoJogo.resposta_atual = null;
    estadoJogo.tentativas = 0;

    fetch(`${API_BASE}/proxima-questao`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            tema: estadoJogo.temaAtual,
            id_sessao: ID_SESSAO
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.sucesso) {
            exibirQuestao(data.questao);
        }
    })
    .catch(erro => console.error(erro));
}

// ====== EXIBIR QUESTÃO ======

function exibirQuestao(questao) {
    document.getElementById('enunciado').textContent = questao.enunciado;
    
    const container = document.getElementById('containerOpcoes');
    container.innerHTML = '';

    questao.opcoes.forEach((opcao, indice) => {
        const div = document.createElement('div');
        div.className = 'opcao';
        
        const letra = String.fromCharCode(65 + indice);
        
        div.innerHTML = `
            <input type="radio" id="opcao${indice}" name="resposta" value="${letra}">
            <label for="opcao${indice}" style="flex: 1; cursor: pointer;">
                <strong>${letra})</strong> ${opcao}
            </label>
        `;
        
        div.onclick = () => {
            document.getElementById(`opcao${indice}`).checked = true;
            document.querySelectorAll('.opcao').forEach(o => o.classList.remove('selecionada'));
            div.classList.add('selecionada');
            estadoJogo.resposta_atual = letra;
        };
        
        container.appendChild(div);
    });
}

// ====== ENVIAR RESPOSTA ======

function enviarResposta() {
    if (!estadoJogo.resposta_atual) {
        alert('Selecione uma resposta!');
        return;
    }

    fetch(`${API_BASE}/responder`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            resposta: estadoJogo.resposta_atual,
            id_sessao: ID_SESSAO
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.sucesso) {
            exibirResultado(data);
        }
    })
    .catch(erro => console.error(erro));
}

// ====== EXIBIR RESULTADO ======

function exibirResultado(resultado) {
    const msgDiv = document.getElementById('mensagemResultado');
    msgDiv.className = 'mensagem-resultado ' + (resultado.correto ? 'sucesso' : 'erro');
    msgDiv.textContent = resultado.mensagem;
    
    document.getElementById('botaoResponder').style.display = 'none';
    document.getElementById('botaoProxima').style.display = 'inline-block';
    
    document.querySelectorAll('input[name="resposta"]').forEach(input => input.disabled = true);
    
    atualizarInfoJogador('nomeExibicao2', 'nivelExibicao2', 'xpExibicao2');
}

// ====== ATUALIZAR INFO JOGADOR ======

function atualizarInfoJogador(idNome, idNivel, idXp) {
    fetch(`${API_BASE}/jogador?id_sessao=${ID_SESSAO}`)
    .then(res => res.json())
    .then(data => {
        if (data.sucesso) {
            document.getElementById(idNome).textContent = data.jogador.nome;
            document.getElementById(idNivel).textContent = data.jogador.nivel;
            document.getElementById(idXp).textContent = data.jogador.xp;
        }
    });
}

// ====== VOLTAR AO MENU ======

function voltarAoMenu() {
    mostrarTela('telaSelecaoTema');
    exibirTemas();
}

// ====== REINICIAR ======

function reiniciar() {
    ID_SESSAO = 'sessao_' + Math.random().toString(36).substr(2, 9);
    estadoJogo = {
        jogador: null,
        temaAtual: null,
        questoes_carregadas: {},
        questao_atual: null,
        resposta_atual: null,
        temas: [],
        tentativas: 0
    };
    
    document.getElementById('nomeJogador').value = '';
    document.getElementById('nomeJogador').disabled = false;
    mostrarTela('telaInicio');
}

// ====== ENTER PARA INICIAR ======

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('nomeJogador').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') iniciarJogo();
    });
});
