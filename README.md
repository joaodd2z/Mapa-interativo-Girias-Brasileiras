# 🇧🇷 Mapa Interativo de Gírias Brasileiras

<div align="center">

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)

**Descubra as gírias de cada estado brasileiro de um jeito interativo e divertido!**

[🎮 **Ver Demo**](https://seuusuario.github.io/mapa-girias-brasil) | [📚 **Como usar**](#-como-usar)

</div>

---

## ✨ **Sobre o Projeto**

Um mapa interativo do Brasil onde você pode explorar as gírias de cada estado. Tem mais de 150 expressões catalogadas, desde "mano" de São Paulo até "eita" do Nordeste. É um projeto educativo que eu criei para mostrar como nossa língua é rica e diversa!

### 🎯 **O que tem de legal**

- 🗺️ Mapa clicável de todos os estados
- 🔍 Busca por estado ou gíria específica  
- 📱 Funciona bem no celular
- 🎨 Visual com as cores do Brasil
- 🧠 Header que some quando você rola a página
- ➖➕ Botões para minimizar/maximizar o cabeçalho
- 🏆 Sistema de conquistas conforme explora

---

## 🚀 **Demo & Screenshots**

### 🖥️ **Desktop**
```
🇧🇷 Mapa Interativo de Gírias Brasileiras
├── Header Inteligente com minimização automática
├── Mapa SVG com animações premium
├── Sistema de busca com sugestões em tempo real
└── Painel de informações com gamificação
```

### 📱 **Mobile**
- Interface adaptativa
- Gestos touch otimizados
- Performance nativa
- Header que se esconde automaticamente

---

## 💻 **Tecnologias**

| Tecnologia | Uso | Versão |
|------------|-----|--------|
| ![HTML5](https://img.shields.io/badge/-HTML5-E34F26?logo=html5&logoColor=white) | Estrutura semântica | 5 |
| ![CSS3](https://img.shields.io/badge/-CSS3-1572B6?logo=css3&logoColor=white) | Design e animações | 3 |
| ![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?logo=javascript&logoColor=black) | Interatividade | ES6+ |
| ![SVG](https://img.shields.io/badge/-SVG-FFB13B?logo=svg&logoColor=black) | Mapa vetorial | 1.1 |

### 🎨 **Design System**
- **Paleta**: Cores da bandeira brasileira modernizadas
- **Tipografia**: Inter (Google Fonts)
- **Iconografia**: Emojis nativos + SVG
- **Animações**: CSS3 + RequestAnimationFrame

---

## 📁 **Estrutura do Projeto**

```
mapa-girias-brasil/
├── 📄 index.html          # Página principal otimizada
├── 🎨 style.css           # Design system brasileiro (7KB)
├── ⚡ script.js           # Engine interativa (15KB)
├── 📊 girias.json         # Base de dados (150+ gírias)
├── 🗂️ assets/
│   └── 🗺️ mapa.svg        # Mapa SVG interativo
├── 📖 README.md           # Documentação completa
└── 🚀 INICIAÇÃO_RÁPIDA.md # Setup em 30 segundos
```

---

## 🎮 **Funcionalidades**

### 🗺️ **Mapa Interativo**
- [x] Clique nos estados para explorar gírias
- [x] Hover com tooltips informativos
- [x] Animações de seleção e destaque
- [x] Suporte completo a teclado (acessibilidade)
- [x] Zoom e controles visuais

### 🔍 **Sistema de Busca**
- [x] Busca em tempo real por estados
- [x] Busca por gírias específicas
- [x] Sugestões inteligentes
- [x] Histórico de pesquisas
- [x] Autocomplete avançado

### 🏆 **Gamificação**
- [x] Sistema de conquistas desbloqueáveis
- [x] Progresso de exploração (0/27 estados)
- [x] Badges de regiões (Nordestino, Sulista, etc.)
- [x] Estatísticas de uso
- [x] Rankings e pontuação

### 📱 **Mobile Premium**
- [x] Design Mobile-First
- [x] Gestos touch otimizados
- [x] Header que se esconde no scroll
- [x] Performance 60fps
- [x] Offline-ready (Service Worker)

### 🧠 **Header Inteligente**
- [x] Minimiza automaticamente no scroll para baixo
- [x] Volta ao rolar para cima
- [x] Botão flutuante quando escondido
- [x] Indicador de progresso de scroll
- [x] Transições suaves

---

## 🚀 **Como Usar**

### ⚡ **Instalação Rápida (30 segundos)**

```bash
# 1. Clone o repositório
git clone https://github.com/SeuUsuario/mapa-girias-brasil.git
cd mapa-girias-brasil

# 2. Abra no navegador
# Opção A: Duplo clique no index.html
# Opção B: Servidor local
python -m http.server 8000  # ou
npx serve .                 # ou
php -S localhost:8000       # ou qualquer servidor HTTP

# 3. Acesse
http://localhost:8000
```

### 🎯 **Testando as Funcionalidades**

1. **🖱️ Clique em São Paulo** → Veja "mano", "bagulho", "trampo"
2. **🔍 Digite "Bahia"** → Explore "axé", "arretado", "mainha"
3. **📱 Teste no mobile** → Header se esconde automaticamente
4. **🏆 Visite 5 estados** → Desbloqueie a conquista "Explorador"

---

## 📊 **Base de Dados**

### 📈 **Estatísticas**
- **150+ gírias** catalogadas
- **27 estados** + Distrito Federal
- **5 regiões** brasileiras cobertas
- **Contexto cultural** para cada expressão

### 📝 **Estrutura JSON**
```json
{
  "sp": {
    "estado": "São Paulo",
    "girias": [
      {
        "termo": "mano",
        "significado": "amigo, parceiro",
        "exemplo": "E aí, mano, beleza?"
      }
    ]
  }
}
```

### 🔄 **Atualização**
- Base de dados em constante crescimento
- Contribuições da comunidade bem-vindas
- Validação linguística rigorosa

---

## 🌐 **Deploy**

### 🚀 **GitHub Pages (Recomendado)**
```bash
# 1. Push para seu repositório
git add .
git commit -m "🇧🇷 Mapa de Gírias Brasileiras"
git push origin main

# 2. Ativar GitHub Pages
# Settings → Pages → Source: Deploy from branch → main

# 3. Acessar
https://seuusuario.github.io/mapa-girias-brasil
```

### ☁️ **Outras Opções**
- **Netlify**: Drag & drop da pasta
- **Vercel**: Conectar repositório GitHub
- **Surge**: `surge dist/`
- **Firebase**: `firebase deploy`

---

## 🤝 **Contribuindo**

### 🎨 **Como Contribuir**

1. **🍴 Fork** o projeto
2. **🌿 Crie** uma branch: `git checkout -b feature/nova-giria`
3. **✨ Commit** mudanças: `git commit -m 'Adiciona gírias do Acre'`
4. **📤 Push** para branch: `git push origin feature/nova-giria`
5. **🔄 Abra** um Pull Request

### 💡 **Ideias de Contribuição**
- 📝 Adicionar novas gírias regionais
- 🎨 Melhorar design e UX
- 🐛 Reportar e corrigir bugs
- 🌍 Traduzir para outros idiomas
- 📱 Otimizar para novos dispositivos
- 🔊 Adicionar áudio de pronúncia

### 📋 **Guidelines**
- Siga o padrão de código existente
- Teste em múltiplos navegadores
- Valide gírias com fontes confiáveis
- Mantenha performance otimizada

---

## 🏆 **Sistema de Conquistas**

| Conquista | Descrição | Requisito |
|-----------|-----------|-----------|
| 🎯 **Primeiro Contato** | Explorou seu primeiro estado | 1 estado |
| 🗺️ **Explorador** | Visitou 5 estados diferentes | 5 estados |
| 🧠 **Conhecedor** | Visitou 10 estados diferentes | 10 estados |
| 🏆 **Especialista Regional** | Visitou 15 estados diferentes | 15 estados |
| 👑 **Mestre das Gírias** | Visitou todos os 27 estados | 27 estados |
| 🌴 **Nordestino de Coração** | Visitou todos os 9 estados do Nordeste | Nordeste completo |
| ❄️ **Sulista Nato** | Visitou todos os 3 estados do Sul | Sul completo |
| 🔍 **Curioso** | Usou a busca 10 vezes | 10 buscas |

---

## 📱 **Compatibilidade**

### ✅ **Navegadores Suportados**
- ![Chrome](https://img.shields.io/badge/-Chrome-4285F4?logo=googlechrome&logoColor=white) **Chrome 60+**
- ![Firefox](https://img.shields.io/badge/-Firefox-FF7139?logo=firefox&logoColor=white) **Firefox 55+**
- ![Safari](https://img.shields.io/badge/-Safari-000000?logo=safari&logoColor=white) **Safari 12+**
- ![Edge](https://img.shields.io/badge/-Edge-0078D7?logo=microsoftedge&logoColor=white) **Edge 79+**

### 📱 **Dispositivos**
- 🖥️ **Desktop** (1920x1080+)
- 💻 **Laptop** (1366x768+)
- 📱 **Mobile** (320x568+)
- 📟 **Tablet** (768x1024+)

---

## 📄 **Licença**

Este projeto está sob a licença **MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

```
MIT License - Sinta-se livre para usar, modificar e distribuir!
```

---

## 👨‍💻 **Autor**

<div align="center">

**João Lucas de Oliveira**

[![GitHub](https://img.shields.io/badge/-GitHub-181717?logo=github&logoColor=white)](https://github.com/seuusuario)
[![LinkedIn](https://img.shields.io/badge/-LinkedIn-0A66C2?logo=linkedin&logoColor=white)](https://linkedin.com/in/seulinkedin)
[![Email](https://img.shields.io/badge/-Email-EA4335?logo=gmail&logoColor=white)](mailto:seu.email@gmail.com)

*"Celebrando a diversidade linguística do Brasil através da tecnologia"*

</div>

---

## 🙏 **Agradecimentos**

- 🇧🇷 **Comunidade Brasileira** pela riqueza linguística
- 📚 **Linguistas** e pesquisadores da cultura popular
- 🎨 **Design System** inspirado na bandeira nacional
- 💻 **Open Source Community** pelas ferramentas incríveis

---

## 📊 **Estatísticas do Projeto**

<div align="center">

![GitHub stars](https://img.shields.io/github/stars/seuusuario/mapa-girias-brasil?style=social)
![GitHub forks](https://img.shields.io/github/forks/seuusuario/mapa-girias-brasil?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/seuusuario/mapa-girias-brasil?style=social)

**🚀 Pronto para deploy! Bora colocar no ar! 🇧🇷**

</div>

---

<div align="center">

**⭐ Se você gostou do projeto, não esqueça de dar uma estrela!**

*Feito com ❤️ para celebrar a cultura brasileira*

</div> 