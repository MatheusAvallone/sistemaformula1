// Cache de imagens
const imageCache = new Map();

// Função para obter o nome do arquivo da imagem
function getImageFileName(circuitoNome) {
    const nomeMap = {
        'Circuito de Bahrein': 'bahrein',
        'Circuito da Arábia Saudita': 'jeddah',
        'Circuito da Austrália': 'australia',
        'Circuito do Japão': 'japao',
        'Circuito da China': 'china',
        'Circuito de Miami': 'miami',
        'Circuito da Emilia Romagna': 'emilia romagna',
        'Circuito de Mônaco': 'monaco',
        'Circuito do Canadá': 'canada',
        'Circuito da Espanha': 'espanha',
        'Circuito da Áustria': 'austria',
        'Circuito da Grã-Bretanha': 'silverstone',
        'Circuito da Hungria': 'hungria',
        'Circuito da Bélgica': 'belgica',
        'Circuito da Holanda': 'holanda',
        'Circuito da Itália': 'italia',
        'Circuito do Azerbaijão': 'azerbaijao',
        'Circuito de Singapura': 'singapura',
        'Circuito dos Estados Unidos': 'austin',
        'Circuito do México': 'mexico',
        'Circuito do Brasil': 'brasil',
        'Circuito de Las Vegas': 'vegas',
        'Circuito de Abu Dhabi': 'dhabi'
    };

    return nomeMap[circuitoNome] || circuitoNome.toLowerCase();
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

// Função para carregar e exibir os circuitos
async function carregarCircuitos() {
    try {
        const circuitos = await fetchAPI('/circuitos');
        
        // Pré-carrega todas as imagens
        await Promise.all(circuitos.map(circuito => 
            preloadImage(`static/img/circuitos/${getImageFileName(circuito.nome)}.png`)
                .catch(() => console.log(`Imagem não encontrada para circuito ${circuito.nome}`))
        ));
        
        atualizarCircuitos(circuitos);
    } catch (error) {
        console.error('Erro:', error);
        showError('Erro ao carregar circuitos');
    }
}

// Função para atualizar a exibição dos circuitos
function atualizarCircuitos(circuitos) {
    const container = document.getElementById('circuitosContainer');
    container.innerHTML = '';

    circuitos.forEach(circuito => {
        const div = document.createElement('div');
        div.className = 'col-md-4 mb-4';
        
        const imageSrc = `static/img/circuitos/${getImageFileName(circuito.nome)}.png`;
        const imageExists = imageCache.has(imageSrc);
        
        div.innerHTML = `
            <div class="circuito-card">
                <div class="circuito-img-container">
                    <div class="circuito-img-placeholder" style="display: ${imageExists ? 'none' : 'block'}"></div>
                    <img src="${imageSrc}" 
                         alt="Traçado do circuito ${circuito.nome}"
                         class="circuito-img ${imageExists ? '' : 'loading'}"
                         style="display: ${imageExists ? 'block' : 'none'}"
                         onload="this.classList.remove('loading'); this.style.display='block'; this.previousElementSibling.style.display='none';"
                         onerror="this.style.display='none'; this.previousElementSibling.style.display='block';">
                </div>
                <div class="card-body">
                    <h5 class="card-title">${circuito.nome}</h5>
                    <p class="circuito-data">Data: ${new Date(circuito.data_corrida).toLocaleDateString()}</p>
                    <div class="circuito-info">
                        <p><strong>País:</strong> ${circuito.pais}</p>
                        <p><strong>Cidade:</strong> ${circuito.cidade}</p>
                        <p><strong>Comprimento:</strong> ${circuito.comprimento}km</p>
                        <p><strong>Voltas:</strong> ${circuito.num_voltas}</p>
                        <p><strong>Recorde:</strong> ${circuito.recorde_volta || 'N/A'}</p>
                    </div>
                </div>
            </div>
        `;
        container.appendChild(div);
    });
}

// Event Listeners
document.addEventListener('DOMContentLoaded', carregarCircuitos); 