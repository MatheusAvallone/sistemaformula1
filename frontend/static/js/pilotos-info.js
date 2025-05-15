// Cache de imagens e variáveis globais
const imageCache = new Map();
let modalBootstrap;

// Função para pré-carregar uma imagem
function preloadImage(src) {
    return new Promise((resolve, reject) => {
        const img = new Image();
        img.onload = () => {
            imageCache.set(src, img.src);
            resolve(img);
        };
        img.onerror = reject;
        img.src = src;
    });
}

// Função para carregar e exibir as informações dos pilotos
async function carregarInfoPilotos() {
    try {
        const pilotos = await fetchAPI('/pilotos');
        
        // Pré-carrega todas as imagens
        await Promise.all(pilotos.map(piloto => 
            preloadImage(`static/img/pilotos/${piloto.numero}.jpg`)
                .catch(() => console.log(`Imagem não encontrada para piloto ${piloto.numero}`))
        ));
        
        atualizarInfoPilotos(pilotos);
    } catch (error) {
        showError('Erro ao carregar informações dos pilotos');
    }
}

// Função para abrir o modal de edição de estatísticas
async function editarEstatisticas(numero) {
    try {
        const piloto = await fetchAPI(`/pilotos/${numero}`);
        
        // Preenche o formulário com os dados atuais
        document.getElementById('pilotoNumero').value = piloto.numero;
        document.getElementById('pontos').value = piloto.pontos;
        document.getElementById('vitorias').value = piloto.vitorias;
        document.getElementById('poles').value = piloto.poles;
        document.getElementById('voltasRapidas').value = piloto.voltasRapidas || 0;
        
        // Abre o modal
        modalBootstrap.show();
    } catch (error) {
        showError('Erro ao carregar dados do piloto');
    }
}

// Função para salvar as estatísticas
async function salvarEstatisticas() {
    const numero = document.getElementById('pilotoNumero').value;
    const estatisticas = {
        pontos: parseInt(document.getElementById('pontos').value),
        vitorias: parseInt(document.getElementById('vitorias').value),
        poles: parseInt(document.getElementById('poles').value),
        voltasRapidas: parseInt(document.getElementById('voltasRapidas').value)
    };

    try {
        await fetchAPI(`/pilotos/${numero}/estatisticas`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(estatisticas)
        });
        
        modalBootstrap.hide();
        carregarInfoPilotos();
        showSuccess('Estatísticas atualizadas com sucesso!');
    } catch (error) {
        showError('Erro ao atualizar estatísticas');
    }
}

// Função para mostrar mensagem de sucesso
function showSuccess(message) {
    // Você pode implementar uma notificação mais elegante aqui
    alert(message);
}

// Função para atualizar a exibição das informações dos pilotos
function atualizarInfoPilotos(pilotos) {
    const container = document.getElementById('pilotosInfoContainer');
    container.innerHTML = '';

    pilotos.forEach(piloto => {
        const div = document.createElement('div');
        div.className = 'col-md-4 mb-4';
        
        const imageSrc = `static/img/pilotos/${piloto.numero}.jpg`;
        const imageExists = imageCache.has(imageSrc);
        
        div.innerHTML = `
            <div class="piloto-card">
                <div class="piloto-img-container">
                    <div class="piloto-img-placeholder" style="display: ${imageExists ? 'none' : 'block'}"></div>
                    <img src="${imageSrc}" 
                         alt="Foto do piloto ${piloto.nome}"
                         class="piloto-img ${imageExists ? '' : 'loading'}"
                         style="display: ${imageExists ? 'block' : 'none'}"
                         data-numero="${piloto.numero}"
                         onload="this.classList.remove('loading'); this.style.display='block'; this.previousElementSibling.style.display='none';"
                         onerror="this.style.display='none'; this.previousElementSibling.style.display='block';">
                </div>
                <div class="piloto-info">
                    <div class="piloto-header">
                        <h3>${piloto.nome}</h3>
                        <p class="piloto-numero">Número: ${piloto.numero}</p>
                        <p class="piloto-equipe">${piloto.equipe}</p>
                    </div>
                    
                    <div class="piloto-stats">
                        <div class="piloto-stat">
                            <span>${piloto.pontos}</span>
                            <small>Pontos</small>
                        </div>
                        <div class="piloto-stat">
                            <span>${piloto.vitorias}</span>
                            <small>Vitórias</small>
                        </div>
                        <div class="piloto-stat">
                            <span>${piloto.poles}</span>
                            <small>Poles</small>
                        </div>
                    </div>

                    <div class="piloto-stats mt-2">
                        <div class="piloto-stat">
                            <span>${piloto.voltasRapidas || 0}</span>
                            <small>Voltas<br>Rápidas</small>
                        </div>
                    </div>

                    <div class="piloto-actions mt-3">
                        <button class="btn btn-primary" onclick="editarEstatisticas(${piloto.numero})">
                            Editar
                        </button>
                    </div>
                </div>
            </div>
        `;
        container.appendChild(div);
    });
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Inicializa o modal
    const modalElement = document.getElementById('editarEstatisticasModal');
    modalBootstrap = new bootstrap.Modal(modalElement);
    
    // Carrega os pilotos
    carregarInfoPilotos();
}); 