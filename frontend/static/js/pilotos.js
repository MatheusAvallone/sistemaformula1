// Função para carregar todos os pilotos
async function carregarPilotos() {
    try {
        const pilotos = await fetchAPI('/pilotos');
        atualizarTabelaPilotos(pilotos);
    } catch (error) {
        showError('Erro ao carregar pilotos');
    }
}

// Função para atualizar a tabela de pilotos
function atualizarTabelaPilotos(pilotos) {
    const tbody = document.getElementById('pilotosBody');
    tbody.innerHTML = '';

    pilotos.forEach(piloto => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${piloto.numero}</td>
            <td>${piloto.nome}</td>
            <td>${piloto.equipe}</td>
            <td class="text-center">${piloto.pontos || 0}</td>
            <td class="text-center">${piloto.vitorias || 0}</td>
            <td class="text-center">${piloto.poles || 0}</td>
            <td class="acoes-cell">
                <button class="btn btn-acao btn-editar" onclick="editarPiloto(${piloto.numero})">
                    <i class="bi bi-pencil-fill"></i>
                    Editar
                </button>
                <button class="btn btn-acao btn-stats" onclick="abrirModalEstatisticas(${piloto.numero})">
                    <i class="bi bi-trophy-fill"></i>
                    Stats
                </button>
                <button class="btn btn-acao btn-excluir" onclick="excluirPiloto(${piloto.numero})">
                    <i class="bi bi-trash-fill"></i>
                    Excluir
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// Função para adicionar um novo piloto
async function adicionarPiloto(event) {
    event.preventDefault();
    
    const numero = document.getElementById('numero').value;
    const nome = document.getElementById('nome').value;
    const equipe = document.getElementById('equipe').value;

    try {
        await fetchAPI('/pilotos', {
            method: 'POST',
            body: JSON.stringify({ numero, nome, equipe })
        });
        
        document.getElementById('pilotoForm').reset();
        carregarPilotos();
        showSuccess('Piloto adicionado com sucesso!');
    } catch (error) {
        showError('Erro ao adicionar piloto');
    }
}

// Função para editar um piloto
async function editarPiloto(numero) {
    try {
        const piloto = await fetchAPI(`/pilotos/${numero}`);
        
        // Preencher o formulário com os dados do piloto
        document.getElementById('numero').value = piloto.numero;
        document.getElementById('nome').value = piloto.nome;
        document.getElementById('equipe').value = piloto.equipe;
        
        // Mudar o texto do botão
        const submitButton = document.querySelector('#pilotoForm button[type="submit"]');
        submitButton.textContent = 'Atualizar Piloto';
        
        // Adicionar classe para indicar modo de edição
        document.getElementById('pilotoForm').classList.add('modo-edicao');
        document.getElementById('numero').readOnly = true;
    } catch (error) {
        showError('Erro ao carregar dados do piloto');
    }
}

// Função para excluir um piloto
async function excluirPiloto(numero) {
    if (confirm('Tem certeza que deseja excluir este piloto?')) {
        try {
            await fetchAPI(`/pilotos/${numero}`, { method: 'DELETE' });
            carregarPilotos();
            showSuccess('Piloto excluído com sucesso!');
        } catch (error) {
            showError('Erro ao excluir piloto');
        }
    }
}

// Sistema de pontuação F1 2025
const PONTUACAO_F1 = {
    '1': 25,
    '2': 18,
    '3': 15,
    '4': 12,
    '5': 10,
    '6': 8,
    '7': 6,
    '8': 4,
    '9': 2,
    '10': 1
};

// Função para calcular pontos baseado na posição
function calcularPontos(posicao, voltaMaisRapida) {
    let pontos = 0;
    
    // Adiciona pontos pela posição
    if (posicao && posicao !== 'DNF' && PONTUACAO_F1[posicao]) {
        pontos += PONTUACAO_F1[posicao];
        
        // Adiciona ponto extra por volta mais rápida apenas se terminou entre os 10 primeiros
        if (voltaMaisRapida && parseInt(posicao) <= 10) {
            pontos += 1;
        }
    }
    
    return pontos;
}

// Função para abrir o modal de estatísticas
async function abrirModalEstatisticas(numero) {
    try {
        const piloto = await fetchAPI(`/pilotos/${numero}`);
        
        // Preencher o formulário com os dados atuais
        document.getElementById('pilotoNumeroEstatisticas').value = numero;
        document.getElementById('posicaoCorrida').value = piloto.ultimaPosicao || '';
        document.getElementById('voltaMaisRapida').checked = piloto.voltaMaisRapida || false;
        document.getElementById('pontosTotais').value = piloto.pontos || 0;
        document.getElementById('vitorias').value = piloto.vitorias || 0;
        document.getElementById('poles').value = piloto.poles || 0;
        
        // Adicionar event listeners para atualização automática dos pontos
        document.getElementById('posicaoCorrida').addEventListener('change', atualizarPontos);
        document.getElementById('voltaMaisRapida').addEventListener('change', atualizarPontos);
        
        // Abrir o modal
        const modal = new bootstrap.Modal(document.getElementById('atualizarEstatisticasModal'));
        modal.show();
    } catch (error) {
        showError('Erro ao carregar dados do piloto');
    }
}

// Função para atualizar os pontos automaticamente
function atualizarPontos() {
    const posicao = document.getElementById('posicaoCorrida').value;
    const voltaMaisRapida = document.getElementById('voltaMaisRapida').checked;
    const pontosCorrida = calcularPontos(posicao, voltaMaisRapida);
    
    document.getElementById('pontosTotais').value = pontosCorrida;
}

// Função para salvar as estatísticas
async function salvarEstatisticas() {
    const numero = document.getElementById('pilotoNumeroEstatisticas').value;
    const ultimaPosicao = document.getElementById('posicaoCorrida').value;
    const voltaMaisRapida = document.getElementById('voltaMaisRapida').checked;
    const pontos = parseInt(document.getElementById('pontosTotais').value);
    const vitorias = parseInt(document.getElementById('vitorias').value);
    const poles = parseInt(document.getElementById('poles').value);

    try {
        await fetchAPI(`/pilotos/${numero}/estatisticas`, {
            method: 'PUT',
            body: JSON.stringify({
                ultimaPosicao,
                voltaMaisRapida,
                pontos,
                vitorias,
                poles
            })
        });

        // Fechar o modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('atualizarEstatisticasModal'));
        modal.hide();

        // Atualizar a tabela
        carregarPilotos();
        showSuccess('Estatísticas atualizadas com sucesso!');
    } catch (error) {
        showError('Erro ao atualizar estatísticas');
    }
}

// Event Listeners
document.getElementById('pilotoForm').addEventListener('submit', adicionarPiloto);
document.addEventListener('DOMContentLoaded', carregarPilotos); 