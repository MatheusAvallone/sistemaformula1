// Configurações comuns para todas as páginas
const API_URL = 'http://localhost:5000/api';

// Função utilitária para fazer requisições à API
async function fetchAPI(endpoint, options = {}) {
    try {
        const defaultHeaders = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        };

        const response = await fetch(`${API_URL}${endpoint}`, {
            ...options,
            headers: {
                ...defaultHeaders,
                ...(options.headers || {})
            }
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Erro na requisição');
        }
        return await response.json();
    } catch (error) {
        console.error('Erro na requisição:', error);
        throw error;
    }
}

// Função para mostrar mensagens de erro
function showError(message) {
    alert(message);
}

// Função para mostrar mensagens de sucesso
function showSuccess(message) {
    alert(message);
} 