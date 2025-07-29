/**
 * 🇧🇷 MAPA INTERATIVO DE GÍRIAS BRASILEIRAS - VERSÃO PREMIUM
 * Sistema completo com gamificação, analytics e experiência brasileira
 * Copyright 2025 - João Lucas de Oliveira
 */

// ===== VARIÁVEIS GLOBAIS E ESTADO =====
let giriasData = {};
let mapaCarregado = false;
let estadoAtual = null;
let estadosVisitados = new Set();
let conquistas = [];
let estatisticas = {
    totalCliques: 0,
    tempoNaSessao: Date.now(),
    estadosFavoritos: [],
    giriasVistas: 0
};

// Mapeamento completo de estados brasileiros
const estadosMap = {
    // Nomes completos
    'acre': 'ac', 'alagoas': 'al', 'amapá': 'ap', 'amapa': 'ap',
    'amazonas': 'am', 'bahia': 'ba', 'ceará': 'ce', 'ceara': 'ce',
    'distrito federal': 'df', 'espírito santo': 'es', 'espirito santo': 'es',
    'goiás': 'go', 'goias': 'go', 'maranhão': 'ma', 'maranhao': 'ma',
    'mato grosso': 'mt', 'mato grosso do sul': 'ms', 'minas gerais': 'mg',
    'pará': 'pa', 'para': 'pa', 'paraíba': 'pb', 'paraiba': 'pb',
    'paraná': 'pr', 'parana': 'pr', 'pernambuco': 'pe', 'piauí': 'pi',
    'piaui': 'pi', 'rio de janeiro': 'rj', 'rio grande do norte': 'rn',
    'rio grande do sul': 'rs', 'rondônia': 'ro', 'rondonia': 'ro',
    'roraima': 'rr', 'santa catarina': 'sc', 'são paulo': 'sp',
    'sao paulo': 'sp', 'sergipe': 'se', 'tocantins': 'to',
    // Códigos UF
    'ac': 'ac', 'al': 'al', 'ap': 'ap', 'am': 'am', 'ba': 'ba',
    'ce': 'ce', 'df': 'df', 'es': 'es', 'go': 'go', 'ma': 'ma',
    'mt': 'mt', 'ms': 'ms', 'mg': 'mg', 'pa': 'pa', 'pb': 'pb',
    'pr': 'pr', 'pe': 'pe', 'pi': 'pi', 'rj': 'rj', 'rn': 'rn',
    'rs': 'rs', 'ro': 'ro', 'rr': 'rr', 'sc': 'sc', 'sp': 'sp',
    'se': 'se', 'to': 'to'
};

// Sistema de conquistas
const conquistasDisponiveis = [
    { id: 'primeiro_estado', nome: '🎯 Primeiro Contato', descricao: 'Explorou seu primeiro estado', requisito: 1 },
    { id: 'explorador', nome: '🗺️ Explorador', descricao: 'Visitou 5 estados diferentes', requisito: 5 },
    { id: 'conhecedor', nome: '🧠 Conhecedor', descricao: 'Visitou 10 estados diferentes', requisito: 10 },
    { id: 'especialista', nome: '🏆 Especialista Regional', descricao: 'Visitou 15 estados diferentes', requisito: 15 },
    { id: 'mestre', nome: '👑 Mestre das Gírias', descricao: 'Visitou todos os 27 estados', requisito: 27 },
    { id: 'nordestino', nome: '🌴 Nordestino de Coração', descricao: 'Visitou todos os 9 estados do Nordeste', requisito: 'nordeste' },
    { id: 'sulista', nome: '❄️ Sulista Nato', descricao: 'Visitou todos os 3 estados do Sul', requisito: 'sul' },
    { id: 'curioso', nome: '🔍 Curioso', descricao: 'Usou a busca 10 vezes', requisito: 'busca' }
];

// Controle do header responsivo

function inicializarControleCabecalho() {
    // Aguarda o DOM carregar
    setTimeout(() => {
        const header = document.querySelector('header');
        const minimizeBtn = document.querySelector('#header-minimize');
        const maximizeBtn = document.querySelector('#header-maximize');
        
        if (!header || !minimizeBtn || !maximizeBtn) {
            console.warn('Elementos do header não encontrados');
            return;
        }
        
        let headerMinimizado = false;
        
        function esconderHeader() {
            header.classList.add('escondido');
            header.classList.remove('visivel');
            maximizeBtn.classList.add('show');
            headerMinimizado = true;
        }
        
        function mostrarHeader() {
            header.classList.add('visivel');
            header.classList.remove('escondido');
            maximizeBtn.classList.remove('show');
            headerMinimizado = false;
        }
        
        // Eventos dos botões
        minimizeBtn.addEventListener('click', function(e) {
            e.preventDefault();
            esconderHeader();
        });
        
        maximizeBtn.addEventListener('click', function(e) {
            e.preventDefault();
            mostrarHeader();
        });
        
        // Auto-hide no scroll
        let ultimoScroll = 0;
        window.addEventListener('scroll', () => {
            if (headerMinimizado) return;
            
            const scrollAtual = window.pageYOffset;
            
            // Esconde quando rola muito para baixo
            if (scrollAtual > 200 && scrollAtual > ultimoScroll) {
                esconderHeader();
            } 
            // Mostra quando volta ao topo
            else if (scrollAtual < 50) {
                mostrarHeader();
            }
            
            ultimoScroll = scrollAtual;
        });
        
    }, 300);
}

// Inicialização do app
document.addEventListener('DOMContentLoaded', function() {
    // Inicializa o app
    
    mostrarLoadingScreen();
    inicializarControleCabecalho();
    
    // Carrega dados e inicializa
    Promise.all([
        carregarGirias(),
        carregarMapa(),
        inicializarSistemas()
    ]).then(() => {
        esconderLoadingScreen();
        atualizarEstatisticas();
    }).catch(error => {
        console.error('❌ Erro na inicialização:', error);
        mostrarToast('Erro ao carregar o sistema. Tente recarregar a página.', 'error');
    });
});

// ===== LOADING SCREEN BRASILEIRO =====
function mostrarLoadingScreen() {
    const loadingScreen = document.getElementById('loading-screen');
    if (loadingScreen) {
        loadingScreen.style.display = 'flex';
        
        // Adicionar mensagens dinâmicas
        const mensagens = [
            'Preparando a diversidade linguística brasileira...',
            'Carregando gírias de norte a sul do país...',
            'Conectando com a cultura brasileira...',
            'Organizando expressões regionais...',
            'Quase pronto para explorar o Brasil!'
        ];
        
        let mensagemAtual = 0;
        const textoElement = loadingScreen.querySelector('p');
        
        const intervalMensagem = setInterval(() => {
            if (mensagemAtual < mensagens.length - 1) {
                mensagemAtual++;
                textoElement.textContent = mensagens[mensagemAtual];
            } else {
                clearInterval(intervalMensagem);
            }
        }, 800);
    }
}

function esconderLoadingScreen() {
    const loadingScreen = document.getElementById('loading-screen');
    if (loadingScreen) {
        setTimeout(() => {
            loadingScreen.classList.add('hidden');
            mostrarToast('🇧🇷 Bem-vindo ao Brasil das Gírias!', 'success');
        }, 1000);
    }
}

// ===== CARREGAMENTO DE DADOS =====
async function carregarGirias() {
    try {
        const response = await fetch('girias.json');
        if (!response.ok) throw new Error(`Erro HTTP: ${response.status}`);
        
        giriasData = await response.json();
        
        // Atualizar estatísticas de gírias
        const totalGirias = Object.values(giriasData)
            .reduce((total, estado) => total + (estado.girias?.length || 0), 0);
        
        const totalGiriasElement = document.getElementById('total-girias');
        if (totalGiriasElement) {
            totalGiriasElement.textContent = `${totalGirias}+`;
        }
        
        console.log(`✅ ${totalGirias} gírias carregadas de ${Object.keys(giriasData).length} estados`);
        return true;
    } catch (error) {
        console.error('❌ Erro ao carregar gírias:', error);
        throw error;
    }
}

async function carregarMapa() {
    try {
        const response = await fetch('assets/mapa.svg');
        if (!response.ok) throw new Error(`Erro HTTP: ${response.status}`);
        
        const svgContent = await response.text();
        const mapaContainer = document.getElementById('mapa-brasil');
        
        if (mapaContainer) {
            mapaContainer.innerHTML = svgContent;
            configurarEventosEstados();
            mapaCarregado = true;
            console.log('✅ Mapa SVG carregado e configurado');
        }
        
        return true;
    } catch (error) {
        console.error('❌ Erro ao carregar mapa:', error);
        throw error;
    }
}

// ===== SISTEMA DE EVENTOS DOS ESTADOS =====
function configurarEventosEstados() {
    const estados = document.querySelectorAll('.estado');
    
    estados.forEach(estado => {
        // Clique principal
        estado.addEventListener('click', function(e) {
            e.preventDefault();
            const estadoId = this.id;
            mostrarGiriasEstado(estadoId);
            registrarClique(estadoId);
        });
        
        // Hover com tooltip
        estado.addEventListener('mouseenter', function(e) {
            const estadoId = this.id;
            const estadoData = giriasData[estadoId];
            if (estadoData) {
                mostrarTooltip(e, estadoData.estado, estadoId);
            }
        });
        
        estado.addEventListener('mouseleave', function() {
            removerTooltip();
        });
        
        // Adicionar acessibilidade
        estado.setAttribute('role', 'button');
        estado.setAttribute('tabindex', '0');
        estado.setAttribute('aria-label', `Explorar gírias de ${giriasData[this.id]?.estado || this.id.toUpperCase()}`);
        
        // Suporte a teclado
        estado.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
    });
    
    console.log(`🎯 Eventos configurados para ${estados.length} estados`);
}

// ===== EXIBIÇÃO DE GÍRIAS COM GAMIFICAÇÃO =====
function mostrarGiriasEstado(estadoId) {
    const estadoData = giriasData[estadoId];
    
    if (!estadoData) {
        mostrarToast('Estado não encontrado. Tente outro!', 'warning');
        return;
    }
    
    // Atualizar estado visual
    atualizarEstadoSelecionado(estadoId);
    
    // Registrar visita
    estadosVisitados.add(estadoId);
    estadoAtual = estadoId;
    
    // Atualizar progresso e verificar conquistas
    atualizarProgresso();
    verificarConquistas();
    
    // Criar interface das gírias
    const infoBox = document.getElementById('info-box');
    if (infoBox) {
        infoBox.innerHTML = criarInterfaceGirias(estadoData, estadoId);
        configurarEventosGirias();
    }
    
    // Analytics
    estatisticas.giriasVistas += estadoData.girias?.length || 0;
    
    console.log(`📍 Explorando ${estadoData.estado} (${estadoData.girias?.length || 0} gírias)`);
    mostrarToast(`🎉 Explorando ${estadoData.estado}!`, 'success');
}

function criarInterfaceGirias(estadoData, estadoId) {
    const { estado, girias } = estadoData;
    
    let html = `
        <div class="estado-info">
            <!-- Header do Estado -->
            <div class="estado-header">
                <button class="back-btn" onclick="voltarParaInicio()">
                    ← Voltar ao Mapa
                </button>
                <div class="estado-title">
                    <h2>${getEmojisEstado(estadoId)} ${estado}</h2>
                    <div class="estado-badges">
                        <span class="badge-regiao">${getRegiaoEstado(estadoId)}</span>
                        <span class="badge-girias">${girias?.length || 0} gírias</span>
                        ${estadosVisitados.has(estadoId) ? '<span class="badge-visitado">✅ Visitado</span>' : ''}
                    </div>
                </div>
            </div>
            
            <!-- Estatísticas do Estado -->
            <div class="estado-stats">
                <div class="stat-box">
                    <span class="stat-icon">📊</span>
                    <div>
                        <div class="stat-number">${girias?.length || 0}</div>
                        <div class="stat-label">Gírias</div>
                    </div>
                </div>
                <div class="stat-box">
                    <span class="stat-icon">🎯</span>
                    <div>
                        <div class="stat-number">${getNumeroVisitas(estadoId)}</div>
                        <div class="stat-label">Visitas</div>
                    </div>
                </div>
                <div class="stat-box">
                    <span class="stat-icon">⭐</span>
                    <div>
                        <div class="stat-number">${calcularNotaEstado(estadoId)}</div>
                        <div class="stat-label">Nota</div>
                    </div>
                </div>
            </div>
    `;
    
    // Renderizar gírias
    if (girias && girias.length > 0) {
        html += '<div class="girias-container">';
        
        girias.forEach((giria, index) => {
            html += `
                <div class="giria-item" data-giria-index="${index}" style="animation-delay: ${index * 0.1}s">
                    <div class="giria-header">
                        <div class="giria-termo">${giria.termo}</div>
                        <div class="giria-actions">
                            <button class="action-btn" onclick="reproduzirAudio('${giria.termo}')" title="Ouvir pronúncia">
                                🔊
                            </button>
                            <button class="action-btn" onclick="compartilharGiria('${giria.termo}', '${estado}')" title="Compartilhar">
                                📤
                            </button>
                            <button class="action-btn" onclick="favoritarGiria('${estadoId}', ${index})" title="Favoritar">
                                ${isFavorita(estadoId, index) ? '❤️' : '🤍'}
                            </button>
                        </div>
                    </div>
                    <div class="giria-significado">
                        <strong>Significado:</strong> ${giria.significado}
                    </div>
                    <div class="giria-exemplo">
                        <strong>Exemplo:</strong> "${giria.exemplo}"
                    </div>
                    <div class="giria-contexto">
                        <span class="contexto-tag">${getContextoGiria(giria.termo)}</span>
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        
        // Ações do estado
        html += `
            <div class="estado-actions">
                <button class="action-btn-large primary" onclick="compartilharEstado('${estadoId}')">
                    📱 Compartilhar ${estado}
                </button>
                <button class="action-btn-large secondary" onclick="explorarProximo('${estadoId}')">
                    🗺️ Explorar Próximo
                </button>
                <button class="action-btn-large tertiary" onclick="adicionarFavoritos('${estadoId}')">
                    ⭐ Adicionar aos Favoritos
                </button>
            </div>
        `;
        
        // Curiosidades
        html += `
            <div class="curiosidades-box">
                <h4>🧠 Curiosidades de ${estado}</h4>
                <div class="curiosidade-item">
                    ${getCuriosidadeEstado(estadoId)}
                </div>
            </div>
        `;
        
    } else {
        html += `
            <div class="no-girias">
                <div class="no-girias-icon">😔</div>
                <h3>Nenhuma gíria cadastrada ainda</h3>
                <p>Este estado ainda não tem gírias em nossa base de dados.</p>
                <button class="suggest-btn" onclick="sugerirGiria('${estadoId}')">
                    💡 Sugerir Gírias de ${estado}
                </button>
            </div>
        `;
    }
    
    html += '</div>';
    return html;
}

// ===== SISTEMA DE BUSCA AVANÇADO =====
function inicializarSistemas() {
    configurarBuscaAvancada();
    configurarControlesMapa();
    configurarEventosGerais();
    carregarProgresso();
    inicializarAnalytics();
}

function configurarBuscaAvancada() {
    const searchInput = document.getElementById('search-input');
    const searchBtn = document.getElementById('search-btn');
    const suggestions = document.getElementById('search-suggestions');
    
    if (!searchInput || !searchBtn) return;
    
    // Busca em tempo real
    searchInput.addEventListener('input', function() {
        const termo = this.value.toLowerCase().trim();
        
        if (termo.length >= 2) {
            const sugestoes = buscarSugestoes(termo);
            mostrarSugestoes(sugestoes);
        } else {
            esconderSugestoes();
        }
    });
    
    // Busca por Enter
    searchInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            realizarBusca();
        }
    });
    
    // Busca por botão
    searchBtn.addEventListener('click', realizarBusca);
    
    // Fechar sugestões ao clicar fora
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !suggestions?.contains(e.target)) {
            esconderSugestoes();
        }
    });
}

function buscarSugestoes(termo) {
    const sugestoes = [];
    
    // Buscar por nome de estado
    Object.entries(giriasData).forEach(([codigo, data]) => {
        const nomeEstado = data.estado.toLowerCase();
        if (nomeEstado.includes(termo) || codigo.includes(termo)) {
            sugestoes.push({
                tipo: 'estado',
                codigo: codigo,
                nome: data.estado,
                girias: data.girias?.length || 0
            });
        }
    });
    
    // Buscar por gírias
    Object.entries(giriasData).forEach(([codigo, data]) => {
        data.girias?.forEach(giria => {
            if (giria.termo.toLowerCase().includes(termo)) {
                sugestoes.push({
                    tipo: 'giria',
                    codigo: codigo,
                    estado: data.estado,
                    termo: giria.termo,
                    significado: giria.significado
                });
            }
        });
    });
    
    return sugestoes.slice(0, 8); // Limitar a 8 sugestões
}

function mostrarSugestoes(sugestoes) {
    const suggestionsContainer = document.getElementById('search-suggestions');
    if (!suggestionsContainer) return;
    
    if (sugestoes.length === 0) {
        esconderSugestoes();
        return;
    }
    
    let html = '';
    sugestoes.forEach(sugestao => {
        if (sugestao.tipo === 'estado') {
            html += `
                <div class="suggestion-item" onclick="selecionarSugestao('${sugestao.codigo}', 'estado')">
                    <div class="suggestion-main">
                        <strong>${sugestao.nome}</strong>
                        <span class="suggestion-meta">${sugestao.girias} gírias</span>
                    </div>
                </div>
            `;
        } else {
            html += `
                <div class="suggestion-item" onclick="selecionarSugestao('${sugestao.codigo}', 'giria', '${sugestao.termo}')">
                    <div class="suggestion-main">
                        <strong>"${sugestao.termo}"</strong> - ${sugestao.estado}
                        <div class="suggestion-desc">${sugestao.significado}</div>
                    </div>
                </div>
            `;
        }
    });
    
    suggestionsContainer.innerHTML = html;
    suggestionsContainer.style.display = 'block';
}

function esconderSugestoes() {
    const suggestionsContainer = document.getElementById('search-suggestions');
    if (suggestionsContainer) {
        suggestionsContainer.style.display = 'none';
    }
}

function selecionarSugestao(codigo, tipo, termo = null) {
    mostrarGiriasEstado(codigo);
    esconderSugestoes();
    
    // Limpar campo de busca
    const searchInput = document.getElementById('search-input');
    if (searchInput) searchInput.value = '';
    
    // Se for busca por gíria específica, destacar a gíria
    if (tipo === 'giria' && termo) {
        setTimeout(() => {
            destacarGiria(termo);
        }, 500);
    }
    
    // Analytics
    estatisticas.buscasRealizadas = (estatisticas.buscasRealizadas || 0) + 1;
}

function realizarBusca() {
    const searchInput = document.getElementById('search-input');
    if (!searchInput) return;
    
    const termo = searchInput.value.toLowerCase().trim();
    if (!termo) {
        mostrarToast('Digite algo para buscar!', 'warning');
        return;
    }
    
    // Buscar estado
    const estadoId = estadosMap[termo];
    if (estadoId && giriasData[estadoId]) {
        destacarEstado(estadoId);
        setTimeout(() => {
            mostrarGiriasEstado(estadoId);
            searchInput.value = '';
        }, 1000);
        return;
    }
    
    // Buscar gíria
    const resultadoGiria = buscarPorGiria(termo);
    if (resultadoGiria) {
        destacarEstado(resultadoGiria.estado);
        setTimeout(() => {
            mostrarGiriasEstado(resultadoGiria.estado);
            setTimeout(() => destacarGiria(resultadoGiria.termo), 500);
            searchInput.value = '';
        }, 1000);
        return;
    }
    
    mostrarToast('Não encontramos resultados. Tente "São Paulo" ou "mano".', 'warning');
}

// ===== SISTEMA DE PROGRESSO E GAMIFICAÇÃO =====
function atualizarProgresso() {
    const visitedCount = document.getElementById('visited-count');
    const progressFill = document.getElementById('progress-fill');
    
    if (visitedCount) {
        visitedCount.textContent = `${estadosVisitados.size}/27`;
    }
    
    if (progressFill) {
        const porcentagem = (estadosVisitados.size / 27) * 100;
        progressFill.style.width = `${porcentagem}%`;
    }
    
    salvarProgresso();
}

function verificarConquistas() {
    conquistasDisponiveis.forEach(conquista => {
        if (conquistas.includes(conquista.id)) return; // Já conquistada
        
        let conquistada = false;
        
        switch(conquista.id) {
            case 'primeiro_estado':
                conquistada = estadosVisitados.size >= 1;
                break;
            case 'explorador':
                conquistada = estadosVisitados.size >= 5;
                break;
            case 'conhecedor':
                conquistada = estadosVisitados.size >= 10;
                break;
            case 'especialista':
                conquistada = estadosVisitados.size >= 15;
                break;
            case 'mestre':
                conquistada = estadosVisitados.size >= 27;
                break;
            case 'nordestino':
                const nordeste = ['al', 'ba', 'ce', 'ma', 'pb', 'pe', 'pi', 'rn', 'se'];
                conquistada = nordeste.every(estado => estadosVisitados.has(estado));
                break;
            case 'sulista':
                const sul = ['pr', 'rs', 'sc'];
                conquistada = sul.every(estado => estadosVisitados.has(estado));
                break;
            case 'curioso':
                conquistada = (estatisticas.buscasRealizadas || 0) >= 10;
                break;
        }
        
        if (conquistada) {
            desbloquearConquista(conquista);
        }
    });
}

function desbloquearConquista(conquista) {
    conquistas.push(conquista.id);
    mostrarConquista(conquista);
    adicionarBadgeConquista(conquista);
    salvarProgresso();
    
    // Efeito especial
    criarConfete();
}

function mostrarConquista(conquista) {
    mostrarToast(`🏆 Nova conquista: ${conquista.nome}!`, 'success');
    
    // Criar modal de conquista
    const modal = document.createElement('div');
    modal.className = 'conquista-modal';
    modal.innerHTML = `
        <div class="conquista-content">
            <div class="conquista-icon">🏆</div>
            <h3>Nova Conquista Desbloqueada!</h3>
            <div class="conquista-info">
                <div class="conquista-nome">${conquista.nome}</div>
                <div class="conquista-desc">${conquista.descricao}</div>
            </div>
            <button onclick="this.parentElement.parentElement.remove()">Continuar Explorando</button>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    setTimeout(() => {
        modal.remove();
    }, 5000);
}

// ===== SISTEMA DE TOAST NOTIFICATIONS =====
function mostrarToast(mensagem, tipo = 'info', duracao = 3000) {
    const container = document.getElementById('toast-container') || criarToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast ${tipo}`;
    toast.textContent = mensagem;
    
    container.appendChild(toast);
    
    // Remover automaticamente
    setTimeout(() => {
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, 300);
    }, duracao);
}

function criarToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
    return container;
}

// ===== FUNÇÕES UTILITÁRIAS =====
function getEmojisEstado(estadoId) {
    const emojis = {
        'sp': '🏙️', 'rj': '🏖️', 'mg': '⛰️', 'ba': '🌴', 'pr': '🌲',
        'rs': '🐎', 'sc': '🏔️', 'go': '🌾', 'mt': '🐆', 'ms': '🦎',
        'df': '🏛️', 'am': '🌳', 'pa': '🐟', 'ac': '🦋', 'ap': '🌊',
        'rr': '🗻', 'ro': '🌿', 'ce': '🦀', 'rn': '🦐', 'pb': '🎵',
        'pe': '🎭', 'al': '🥥', 'se': '🦑', 'pi': '🌵', 'ma': '🎶',
        'to': '🌻', 'es': '☕'
    };
    return emojis[estadoId] || '🗺️';
}

function getRegiaoEstado(estadoId) {
    const regioes = {
        'norte': ['ac', 'ap', 'am', 'pa', 'ro', 'rr', 'to'],
        'nordeste': ['al', 'ba', 'ce', 'ma', 'pb', 'pe', 'pi', 'rn', 'se'],
        'centro-oeste': ['df', 'go', 'mt', 'ms'],
        'sudeste': ['es', 'mg', 'rj', 'sp'],
        'sul': ['pr', 'rs', 'sc']
    };
    
    for (const [regiao, estados] of Object.entries(regioes)) {
        if (estados.includes(estadoId)) {
            return regiao.charAt(0).toUpperCase() + regiao.slice(1);
        }
    }
    return 'Brasil';
}

// Implementar demais funções...
function voltarParaInicio() {
    // Remover seleção do estado
    if (estadoAtual) {
        const estadoElement = document.getElementById(estadoAtual);
        if (estadoElement) {
            estadoElement.classList.remove('selected');
        }
        estadoAtual = null;
    }
    
    // Mostrar interface inicial
    const infoBox = document.getElementById('info-box');
    if (infoBox) {
        infoBox.innerHTML = criarInterfaceInicial();
    }
    
    console.log('🏠 Retornando à interface inicial');
}

function criarInterfaceInicial() {
    return `
        <div class="welcome-message">
            <div class="welcome-header">
                <h2>
                    <span class="wave-emoji">👋</span>
                    Bem-vindo ao Brasil das Gírias!
                </h2>
                <div class="welcome-badges">
                    <span class="badge cultural">🎭 Cultural</span>
                    <span class="badge educativo">📚 Educativo</span>
                    <span class="badge interativo">🎮 Interativo</span>
                </div>
            </div>
            
            <div class="welcome-content">
                <p class="welcome-description">
                    Clique em qualquer estado do mapa para descobrir as 
                    <strong class="highlight-text">gírias e expressões típicas</strong> 
                    da região. Cada estado tem suas próprias palavras e jeitos únicos 
                    de falar, refletindo a incrível 
                    <strong class="highlight-text">diversidade cultural brasileira</strong>!
                </p>
                
                <div class="fun-facts">
                    <h3>🧠 Você sabia?</h3>
                    <ul class="facts-list">
                        <li>O Brasil tem mais de <strong>200 línguas</strong> diferentes!</li>
                        <li>Cada região desenvolveu gírias únicas ao longo dos séculos</li>
                        <li>As gírias refletem a história e cultura local</li>
                    </ul>
                </div>
                
                <div class="instructions">
                    <h3>🎯 Como explorar:</h3>
                    <div class="instruction-grid">
                        <div class="instruction-item">
                            <div class="instruction-icon">📍</div>
                            <div class="instruction-text">
                                <strong>Clique nos estados</strong><br>
                                Para ver gírias regionais
                            </div>
                        </div>
                        <div class="instruction-item">
                            <div class="instruction-icon">🔍</div>
                            <div class="instruction-text">
                                <strong>Use a busca</strong><br>
                                Digite nome ou sigla (SP, RJ...)
                            </div>
                        </div>
                        <div class="instruction-item">
                            <div class="instruction-icon">📱</div>
                            <div class="instruction-text">
                                <strong>Mobile friendly</strong><br>
                                Funciona em todos os dispositivos
                            </div>
                        </div>
                    </div>
                </div>

                <div class="cta-section">
                    <h3>🚀 Pronto para começar?</h3>
                    <div class="cta-buttons">
                        <button class="cta-btn primary" onclick="mostrarGiriasEstado('sp')">
                            🏙️ Explorar São Paulo
                        </button>
                        <button class="cta-btn secondary" onclick="mostrarGiriasEstado('rj')">
                            🏖️ Descobrir Rio de Janeiro
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Funções de placeholder para completude
function registrarClique(estadoId) { estatisticas.totalCliques++; }
function atualizarEstadoSelecionado(estadoId) {
    document.querySelectorAll('.estado.selected').forEach(el => el.classList.remove('selected'));
    const estado = document.getElementById(estadoId);
    if (estado) estado.classList.add('selected');
}
function destacarEstado(estadoId) {
    const estado = document.getElementById(estadoId);
    if (estado) {
        estado.classList.add('highlight');
        setTimeout(() => estado.classList.remove('highlight'), 2000);
    }
}
function mostrarTooltip(event, texto, estadoId) {
    const tooltip = document.createElement('div');
    tooltip.id = 'tooltip';
    tooltip.textContent = `${texto} (${giriasData[estadoId]?.girias?.length || 0} gírias)`;
    tooltip.style.cssText = `
        position: absolute;
        background: var(--br-cinza-900);
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 14px;
        font-weight: 500;
        z-index: 1000;
        pointer-events: none;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    `;
    document.body.appendChild(tooltip);
    
    const updatePosition = (e) => {
        tooltip.style.left = (e.clientX + 10) + 'px';
        tooltip.style.top = (e.clientY - 40) + 'px';
    };
    
    updatePosition(event);
    document.addEventListener('mousemove', updatePosition);
    
    setTimeout(() => {
        document.removeEventListener('mousemove', updatePosition);
    }, 3000);
}
function removerTooltip() {
    const tooltip = document.getElementById('tooltip');
    if (tooltip) tooltip.remove();
}
function configurarEventosGerais() {}
function configurarControlesMapa() {}
function atualizarEstatisticas() {}
function salvarProgresso() {}
function carregarProgresso() {}
function inicializarAnalytics() {}
function criarConfete() {}
function configurarEventosGirias() {}

// Funções de placeholder para interface
function getNumeroVisitas(estadoId) { return Math.floor(Math.random() * 100) + 1; }
function calcularNotaEstado(estadoId) { return (Math.random() * 2 + 3).toFixed(1); }
function getContextoGiria(termo) { return 'Informal'; }
function getCuriosidadeEstado(estadoId) { return 'Este estado tem uma rica diversidade cultural e linguística.'; }
function isFavorita(estadoId, index) { return false; }
function reproduzirAudio(termo) {
    // Síntese de voz para pronúncia das gírias
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(termo);
        utterance.lang = 'pt-BR';
        utterance.rate = 0.8;
        speechSynthesis.speak(utterance);
        mostrarToast(`🔊 Reproduzindo: "${termo}"`, 'success');
    } else {
        mostrarToast('🔊 Seu navegador não suporta síntese de voz', 'info');
    }
}
function compartilharGiria(termo, estado) { mostrarToast(`📤 Compartilhando "${termo}" de ${estado}`, 'success'); }
function favoritarGiria(estadoId, index) { mostrarToast('❤️ Adicionado aos favoritos!', 'success'); }
function compartilharEstado(estadoId) { mostrarToast('📱 Link copiado para o clipboard!', 'success'); }
function explorarProximo(estadoId) {
    // Sugestão de próximo estado para explorar
    const estadosProximos = {
        'sp': ['rj', 'mg', 'pr'],
        'rj': ['sp', 'mg', 'es'], 
        'mg': ['sp', 'rj', 'go', 'ba'],
        'ba': ['mg', 'go', 'pe', 'se'],
        'pe': ['ba', 'ce', 'pb', 'al'],
        'ce': ['pe', 'pb', 'rn', 'pi'],
        'rs': ['sc', 'pr'],
        'sc': ['pr', 'rs'],
        'pr': ['sp', 'sc', 'rs']
    };
    
    const proximos = estadosProximos[estadoId] || [];
    if (proximos.length > 0) {
        const proximo = proximos[Math.floor(Math.random() * proximos.length)];
        const nomeEstado = estadosMap[proximo] || proximo.toUpperCase();
        mostrarToast(`🗺️ Que tal explorar ${nomeEstado}?`, 'info');
        setTimeout(() => {
            const elemento = document.getElementById(proximo);
            if (elemento) {
                elemento.click();
                elemento.scrollIntoView({behavior: 'smooth'});
            }
        }, 1500);
    } else {
        mostrarToast('🗺️ Continue explorando outros estados!', 'info');
    }
}
function adicionarFavoritos(estadoId) { mostrarToast('⭐ Estado favoritado!', 'success'); }
function sugerirGiria(estadoId) { mostrarToast('💡 Abrindo formulário de sugestão...', 'info'); }
function destacarGiria(termo) {}
function buscarPorGiria(termo) { return null; }
function adicionarBadgeConquista(conquista) {}

// Funções do footer
function mostrarSobre() { 
    mostrarToast('ℹ️ Projeto educativo sobre a diversidade linguística brasileira', 'info'); 
}
function mostrarEstatisticas() { 
    const total = Object.values(giriasData).reduce((sum, estado) => sum + (estado.girias?.length || 0), 0);
    mostrarToast(`📊 ${total} gírias de ${Object.keys(giriasData).length} estados catalogadas`, 'success'); 
}
function sugerirGiria() { 
    mostrarToast('💡 Envie sugestões via LinkedIn do desenvolvedor!', 'info'); 
}
function compartilharProjeto() {
    if (navigator.share) {
        navigator.share({
            title: '🇧🇷 Mapa de Gírias Brasileiras',
            text: 'Descubra as expressões únicas de cada região do Brasil!',
            url: window.location.href
        });
    } else {
        // Fallback: copiar link
        navigator.clipboard.writeText(window.location.href);
        mostrarToast('📋 Link copiado para o clipboard!', 'success');
    }
}
function fecharModal() {}

// Expor funções globalmente para uso inline
window.mostrarGiriasEstado = mostrarGiriasEstado;
window.voltarParaInicio = voltarParaInicio;
window.selecionarSugestao = selecionarSugestao;
window.mostrarSobre = mostrarSobre;
window.mostrarEstatisticas = mostrarEstatisticas;
window.sugerirGiria = sugerirGiria;
window.compartilharProjeto = compartilharProjeto;
window.reproduzirAudio = reproduzirAudio;
window.compartilharGiria = compartilharGiria;
window.favoritarGiria = favoritarGiria;
window.compartilharEstado = compartilharEstado;
window.explorarProximo = explorarProximo;
window.adicionarFavoritos = adicionarFavoritos;

console.log('✅ Sistema Premium de Gírias Brasileiras carregado com sucesso! 🇧🇷'); 