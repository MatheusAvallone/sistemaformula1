// Cache de imagens
const imageCache = new Map();

// Função para obter o nome do arquivo da imagem
function getImageFileName(lendaNome) {
    const nomeMap = {
        'Ayrton Senna': 'senna',
        'Michael Schumacher': 'schumacher',
        'Juan Manuel Fangio': 'fangio',
        'Alain Prost': 'prost',
        'Nelson Piquet': 'piquet'
    };

    return nomeMap[lendaNome] || lendaNome.toLowerCase().replace(/\s+/g, '');
}

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

// Função para carregar e exibir as lendas
async function carregarLendas() {
    try {
        const lendas = await fetchAPI('/lendas');
        
        // Pré-carrega todas as imagens
        await Promise.all(lendas.map(lenda => 
            preloadImage(`static/img/lendas/${getImageFileName(lenda.nome)}.png`)
                .catch(() => console.log(`Imagem não encontrada para lenda ${lenda.nome}`))
        ));
        
        atualizarLendas(lendas);
    } catch (error) {
        console.error('Erro:', error);
        showError('Erro ao carregar lendas');
    }
}

// Função para atualizar a exibição das lendas
function atualizarLendas(lendas) {
    const container = document.getElementById('lendasContainer');
    container.innerHTML = '';

    lendas.forEach(lenda => {
        const div = document.createElement('div');
        div.className = 'col-md-4 mb-4';
        
        const imageSrc = `static/img/lendas/${getImageFileName(lenda.nome)}.png`;
        const imageExists = imageCache.has(imageSrc);
        
        div.innerHTML = `
            <div class="lenda-card">
                <div class="lenda-img-container">
                    <div class="lenda-img-placeholder" style="display: ${imageExists ? 'none' : 'block'}"></div>
                    <img src="${imageSrc}" 
                         alt="Foto de ${lenda.nome}"
                         class="lenda-img ${imageExists ? '' : 'loading'}"
                         style="display: ${imageExists ? 'block' : 'none'}"
                         onload="this.classList.remove('loading'); this.style.display='block'; this.previousElementSibling.style.display='none';"
                         onerror="this.style.display='none'; this.previousElementSibling.style.display='block';">
                </div>
                <div class="card-body">
                    <h5 class="card-title">${lenda.nome}</h5>
                    <div class="lenda-info">
                        <p><strong>Nacionalidade:</strong> ${lenda.nacionalidade}</p>
                        <p>
                            <strong>Títulos:</strong>
                            <span class="stats-badge">${lenda.titulos} 🏆</span>
                        </p>
                        <p>
                            <strong>Vitórias:</strong>
                            <span class="stats-badge">${lenda.vitorias} 🏁</span>
                        </p>
                        <p>
                            <strong>Poles:</strong>
                            <span class="stats-badge">${lenda.poles} ⚡</span>
                        </p>
                        <p>
                            <strong>Pódios:</strong>
                            <span class="stats-badge">${lenda.podios} 🎯</span>
                        </p>
                        <p><strong>Anos Ativos:</strong> ${lenda.anos_ativo}</p>
                        <p><strong>Equipes:</strong> ${lenda.equipes_principais.join(', ')}</p>
                        <div class="lenda-bio">
                            ${lenda.bio}
                        </div>
                    </div>
                </div>
            </div>
        `;
        container.appendChild(div);
    });
}

// Event Listeners
document.addEventListener('DOMContentLoaded', carregarLendas); 