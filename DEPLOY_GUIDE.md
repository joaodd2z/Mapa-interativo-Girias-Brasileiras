# 🚀 Guia de Deploy - Mapa de Gírias Brasileiras

<div align="center">

![Deploy](https://img.shields.io/badge/Deploy-Ready-00875F?style=for-the-badge)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)
![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-222222?style=for-the-badge&logo=github&logoColor=white)

**Guia completo para colocar seu projeto no ar em minutos!**

</div>

---

## 🎯 **Deploy Rápido (Escolha sua opção)**

### 🥇 **Opção 1: Vercel (Recomendado)**
*Deploy automático em 30 segundos*

1. **Acesse** [vercel.com](https://vercel.com)
2. **Conecte** sua conta GitHub
3. **Importe** o repositório `mapa-girias-brasileiras`
4. **Clique** em "Deploy"
5. **Pronto!** Seu projeto estará no ar

✅ **Vantagens:**
- Deploy automático a cada push
- HTTPS gratuito
- CDN global
- Zero configuração

---

### 🥈 **Opção 2: GitHub Pages**
*Hospedagem gratuita no GitHub*

```bash
# 1. Configure o repositório
git add .
git commit -m "🇧🇷 Deploy Mapa de Gírias Brasileiras"
git push origin main

# 2. Ative o GitHub Pages
# Vá em: Settings → Pages → Source: Deploy from branch → main

# 3. Acesse seu site
# https://seu-usuario.github.io/mapa-girias-brasileiras
```

✅ **Vantagens:**
- Totalmente gratuito
- Fácil de configurar
- Integrado com GitHub

---

### 🥉 **Opção 3: Netlify**
*Deploy por drag & drop*

1. **Acesse** [netlify.com](https://netlify.com)
2. **Arraste** a pasta do projeto
3. **Aguarde** o upload
4. **Personalize** o domínio

✅ **Vantagens:**
- Deploy instantâneo
- Formulários gratuitos
- Edge computing

---

## ⚙️ **Configurações Importantes**

### 📁 **Arquivos Essenciais**

Certifique-se que estes arquivos estão corretos:

#### `vercel.json` ✅
```json
{
  "version": 2,
  "name": "mapa-girias-brasileiras",
  "builds": [
    {
      "src": "index.html",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

#### `package.json` ✅
```json
{
  "name": "mapa-girias-brasileiras",
  "version": "2.0.0",
  "scripts": {
    "start": "npx serve . -p 3000",
    "deploy": "vercel --prod"
  }
}
```

---

## 🔧 **Solução de Problemas**

### ❌ **Erro: "Build Failed"**
**Causa:** Referências incorretas ou arquivos em falta

**Solução:**
```bash
# Verifique se todos os arquivos existem
ls -la assets/mapa.svg
ls -la girias.json
ls -la index.html

# Corrija paths relativos
# ✅ Correto: ./assets/mapa.svg
# ❌ Errado: /assets/mapa.svg
```

### ❌ **Erro: "404 Not Found"**
**Causa:** Configuração de rotas incorreta

**Solução:**
- Certifique-se que `index.html` está na raiz
- Verifique se o `vercel.json` está configurado
- Use URLs relativas (sem `/` inicial)

### ❌ **Erro: "Gírias não carregam"**
**Causa:** CORS ou path incorreto do JSON

**Solução:**
```javascript
// ✅ Correto
fetch('./girias.json')

// ❌ Errado
fetch('/girias.json')
fetch('girias.json') // sem o ./
```

---

## 🚀 **Deploy Avançado**

### 🐳 **Docker**
```dockerfile
FROM nginx:alpine
COPY . /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

```bash
docker build -t mapa-girias .
docker run -p 8080:80 mapa-girias
```

### ☁️ **AWS S3 + CloudFront**
```bash
aws s3 sync . s3://mapa-girias-brasileiras --delete
aws cloudfront create-invalidation --distribution-id YOUR_ID --paths "/*"
```

### 🌊 **DigitalOcean App Platform**
```yaml
name: mapa-girias-brasileiras
services:
- name: web
  source_dir: /
  github:
    repo: seu-usuario/mapa-girias-brasileiras
    branch: main
  run_command: npx serve . -p 8080
```

---

## 📊 **Monitoramento e Analytics**

### 📈 **Google Analytics**
Adicione ao `index.html`:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_TRACKING_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_TRACKING_ID');
</script>
```

### 🔍 **Hotjar (Heatmaps)**
```html
<!-- Hotjar Tracking Code -->
<script>
    (function(h,o,t,j,a,r){
        h.hj=h.hj||function(){(h.hj.q=h.hj.q||[]).push(arguments)};
        h._hjSettings={hjid:YOUR_HOTJAR_ID,hjsv:6};
        a=o.getElementsByTagName('head')[0];
        r=o.createElement('script');r.async=1;
        r.src=t+h._hjSettings.hjid+j+h._hjSettings.hjsv;
        a.appendChild(r);
    })(window,document,'https://static.hotjar.com/c/hotjar-','.js?sv=');
</script>
```

---

## 🔒 **Segurança e Performance**

### 🛡️ **Headers de Segurança**
```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-XSS-Protection",
          "value": "1; mode=block"
        }
      ]
    }
  ]
}
```

### ⚡ **Cache Otimizado**
```json
{
  "headers": [
    {
      "source": "/assets/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

---

## 🌍 **Domínio Personalizado**

### 📝 **Configurar DNS**
```
CNAME: www.meudominio.com.br → seu-usuario.github.io
A: meudominio.com.br → 185.199.108.153
A: meudominio.com.br → 185.199.109.153
A: meudominio.com.br → 185.199.110.153
A: meudominio.com.br → 185.199.111.153
```

### 🔐 **HTTPS Gratuito**
- **GitHub Pages:** Automático com Let's Encrypt
- **Vercel:** Automático
- **Netlify:** Automático
- **Cloudflare:** SSL gratuito + CDN

---

## 📱 **PWA (Progressive Web App)**

### 📋 **Manifest**
Crie `manifest.json`:
```json
{
  "name": "Mapa de Gírias Brasileiras",
  "short_name": "Gírias BR",
  "description": "Explore gírias de todos os estados brasileiros",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#00875F",
  "theme_color": "#00875F",
  "icons": [
    {
      "src": "assets/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "assets/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

### 🔧 **Service Worker**
Crie `sw.js`:
```javascript
const CACHE_NAME = 'girias-br-v1';
const urlsToCache = [
  '/',
  '/style.css',
  '/script.js',
  '/girias.json',
  '/assets/mapa.svg'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});
```

---

## ✅ **Checklist Final**

Antes do deploy, verifique:

- [ ] **Arquivos essenciais** existem (index.html, style.css, script.js, girias.json)
- [ ] **Mapa SVG** carrega corretamente
- [ ] **URLs são relativas** (./assets/ não /assets/)
- [ ] **JSON é válido** (use jsonlint.com)
- [ ] **Responsivo** funciona em mobile
- [ ] **Console limpo** sem erros JavaScript
- [ ] **Meta tags** estão preenchidas
- [ ] **Favicon** está configurado
- [ ] **Vercel.json** está correto
- [ ] **HTTPS** está funcionando

---

## 🎊 **Celebrate!**

<div align="center">

🎉 **Parabéns! Seu Mapa de Gírias está no ar!** 🎉

Compartilhe com amigos e celebre nossa diversidade cultural brasileira!

[![Share](https://img.shields.io/badge/Compartilhar-00875F?style=for-the-badge&logo=share&logoColor=white)](#)

</div>

---

## 📞 **Suporte**

Tendo problemas? Abra uma [issue](https://github.com/seu-usuario/mapa-girias-brasileiras/issues) ou entre em contato:

- 💬 **GitHub Issues:** Para bugs e sugestões
- 💼 **LinkedIn:** [João Lucas](https://linkedin.com/in/jasao369)
- 📧 **Email:** contato@projeto.com

---

<div align="center">

**🇧🇷 Feito com ❤️ para o Brasil! 🇧🇷**

</div> 