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
        
        // Preencher os campos de estatísticas
        document.getElementById('pontosEdicao').value = piloto.pontos || 0;
        document.getElementById('vitoriasEdicao').value = piloto.vitorias || 0;
        document.getElementById('polesEdicao').value = piloto.poles || 0;
        
        // Mostrar campos de estatísticas
        document.getElementById('estatisticasEdicao').style.display = 'block';
        
        // Mudar o texto do botão
        const submitButton = document.querySelector('#pilotoForm button[type="submit"]');
        submitButton.textContent = 'Atualizar Piloto';
        
        // Adicionar classe para indicar modo de edição
        document.getElementById('pilotoForm').classList.add('modo-edicao');
        document.getElementById('numero').readOnly = true;

        // Salvar o número do piloto sendo editado
        document.getElementById('pilotoForm').dataset.editandoNumero = numero;
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

// Sistema de pontuação Sprint Race F1 2025
const PONTUACAO_SPRINT = {
    '1': 8,
    '2': 7,
    '3': 6,
    '4': 5,
    '5': 4,
    '6': 3,
    '7': 2,
    '8': 1
};

// Função para calcular pontos baseado na posição
function calcularPontos(posicao, voltaMaisRapida, posicaoSprint) {
    let pontos = 0;
    
    // Adiciona pontos pela posição no GP
    if (posicao && posicao !== 'DNF' && PONTUACAO_F1[posicao]) {
        pontos += PONTUACAO_F1[posicao];
        
        // Adiciona ponto extra por volta mais rápida apenas se terminou entre os 10 primeiros
        if (voltaMaisRapida && parseInt(posicao) <= 10) {
            pontos += 1;
        }
    }

    // Adiciona pontos da Sprint Race
    if (posicaoSprint && PONTUACAO_SPRINT[posicaoSprint]) {
        pontos += PONTUACAO_SPRINT[posicaoSprint];
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
        document.getElementById('posicaoSprint').value = piloto.ultimaPosicaoSprint || '';
        document.getElementById('voltaMaisRapida').checked = piloto.voltaMaisRapida || false;
        document.getElementById('pontosTotais').value = piloto.pontos || 0;
        document.getElementById('vitorias').value = piloto.vitorias || 0;
        document.getElementById('poles').value = piloto.poles || 0;
        
        // Adicionar event listeners para atualização automática dos pontos
        document.getElementById('posicaoCorrida').addEventListener('change', atualizarPontos);
        document.getElementById('posicaoSprint').addEventListener('change', atualizarPontos);
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
    const posicaoSprint = document.getElementById('posicaoSprint').value;
    const voltaMaisRapida = document.getElementById('voltaMaisRapida').checked;
    const pontosCorrida = calcularPontos(posicao, voltaMaisRapida, posicaoSprint);
    
    document.getElementById('pontosTotais').value = pontosCorrida;
}

// Função para salvar as estatísticas
async function salvarEstatisticas() {
    const numero = parseInt(document.getElementById('pilotoNumeroEstatisticas').value);
    const pontos = parseInt(document.getElementById('pontosTotais').value) || 0;
    const vitorias = parseInt(document.getElementById('vitorias').value) || 0;
    const poles = parseInt(document.getElementById('poles').value) || 0;

    try {
        console.log('Enviando dados:', { numero, pontos, vitorias, poles });
        
        await fetchAPI(`/pilotos/${numero}/estatisticas`, {
            method: 'PUT',
            body: JSON.stringify({
                pontos,
                vitorias,
                poles
            })
        });

        // Fechar o modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('atualizarEstatisticasModal'));
        modal.hide();

        // Atualizar a tabela
        await carregarPilotos();
        showSuccess('Estatísticas atualizadas com sucesso!');
    } catch (error) {
        console.error('Erro completo:', error);
        showError('Erro ao atualizar estatísticas');
    }
}

// Função para adicionar ou atualizar um piloto
async function handlePilotoSubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const isEdicao = form.classList.contains('modo-edicao');
    
    const numero = parseInt(document.getElementById('numero').value);
    const nome = document.getElementById('nome').value;
    const equipe = document.getElementById('equipe').value;

    try {
        if (isEdicao) {
            // Modo de edição
            const pontos = parseInt(document.getElementById('pontosEdicao').value) || 0;
            const vitorias = parseInt(document.getElementById('vitoriasEdicao').value) || 0;
            const poles = parseInt(document.getElementById('polesEdicao').value) || 0;

            await fetchAPI(`/pilotos/${numero}`, {
                method: 'PUT',
                body: JSON.stringify({ 
                    numero, 
                    nome, 
                    equipe,
                    pontos,
                    vitorias,
                    poles
                })
            });

            // Resetar o formulário para o modo de adição
            form.classList.remove('modo-edicao');
            document.getElementById('estatisticasEdicao').style.display = 'none';
            document.getElementById('numero').readOnly = false;
            document.querySelector('#pilotoForm button[type="submit"]').textContent = 'Adicionar Piloto';
            showSuccess('Piloto atualizado com sucesso!');
        } else {
            // Modo de adição
            await fetchAPI('/pilotos', {
                method: 'POST',
                body: JSON.stringify({ numero, nome, equipe })
            });
            showSuccess('Piloto adicionado com sucesso!');
        }
        
        form.reset();
        carregarPilotos();
    } catch (error) {
        showError(isEdicao ? 'Erro ao atualizar piloto' : 'Erro ao adicionar piloto');
    }
}

// Event Listeners
document.getElementById('pilotoForm').addEventListener('submit', handlePilotoSubmit);
document.addEventListener('DOMContentLoaded', () => {
    carregarPilotos();
    
    // Resetar o formulário quando clicar em Adicionar Piloto no menu
    document.getElementById('pilotoForm').addEventListener('reset', () => {
        const form = document.getElementById('pilotoForm');
        form.classList.remove('modo-edicao');
        document.getElementById('estatisticasEdicao').style.display = 'none';
        document.getElementById('numero').readOnly = false;
        document.querySelector('#pilotoForm button[type="submit"]').textContent = 'Adicionar Piloto';
    });
}); 