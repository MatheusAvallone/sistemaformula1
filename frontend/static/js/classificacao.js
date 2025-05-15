// Função para carregar e exibir a classificação
async function carregarClassificacao() {
    try {
        const pilotos = await fetchAPI('/pilotos');
        atualizarTabelaClassificacao(pilotos);
    } catch (error) {
        showError('Erro ao carregar classificação');
    }
}

// Função para atualizar a tabela de classificação
function atualizarTabelaClassificacao(pilotos) {
    const tbody = document.getElementById('classificacaoBody');
    tbody.innerHTML = '';

    const pilotosOrdenados = [...pilotos].sort((a, b) => b.pontos - a.pontos);

    pilotosOrdenados.forEach((piloto, index) => {
        const position = index + 1;
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td class="position-cell position-${position}">${position}º</td>
            <td class="piloto-cell">${piloto.nome}</td>
            <td class="equipe-cell">${piloto.equipe}</td>
            <td class="pontos-cell">${piloto.pontos}</td>
            <td class="stats-cell">
                <span class="stats-badge vitorias-badge">${piloto.vitorias}</span>
            </td>
            <td class="stats-cell">
                <span class="stats-badge poles-badge">${piloto.poles || 0}</span>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// Event Listeners
document.addEventListener('DOMContentLoaded', carregarClassificacao); 