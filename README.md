# 🚀 ApexCRM — System & Pipeline Management

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Cloudflare](https://img.shields.io/badge/Cloudflare_Tunnels-F38020?style=for-the-badge&logo=cloudflare&logoColor=white)

> **ApexCRM** é uma plataforma moderna e desacoplada de Gestão de Relacionamento com Cliente (CRM) e Funil de Vendas (Kanban), projetada com foco em performance, segurança RBAC e arquitetura distribuída em nuvem/edge.

---

## 📐 Arquitetura do Sistema

O projeto adota uma **arquitetura desacoplada (Decoupled Frontend/Backend)**:

* **Frontend (SPA):** Interface estática responsiva com dashboard de métricas em tempo real, Kanban com *drag-and-drop* e suporte a temas.
  * **Hospedagem:** Vercel (`https://apexcrmmateusdg.vercel.app`)
* **Backend (RESTful API):** API robusta construída em Python com FastAPI, autenticação JWT, validação de dados Pydantic V2 e persistência SQLite.
  * **Hospedagem:** Container Docker em servidor privado Linux (`vm-mateus-vdi`).
* **Conectividade Edge:** Acesso público global e seguro HTTPS provisionado via **Cloudflare Tunnels** sem expor portas abertas de firewall doméstico/privado.

---

## ✨ Funcionalidades Principais

* 🔐 **Autenticação & RBAC (Role-Based Access Control):**
  * Níveis de acesso distintos (`admin` e `vendedor`).
  * Criptografia de senhas com `passlib` e emissão de tokens JWT para sessões seguras.
* 📊 **Dashboard & Analytics:**
  * Métricas KPI automatizadas (Total de Clientes, Valor do Pipeline, Vendas Concluídas e Taxa de Conversão).
  * Gráficos dinâmicos renderizados com **Chart.js**.
* 📋 **Pipeline Kanban Interativo:**
  * Movimentação de oportunidades via *drag-and-drop*.
  * Atualização assíncrona de estágios diretamente no banco de dados.
* 👥 **Gestão de Clientes:**
  * Cadastro, listagem e busca em tempo real com vínculo direto às oportunidades de negócio.
* 🧪 **Modo Simulação (Demo Mode):**
  * Alternância dinâmica para testes locais em memória sem dependência de banco de dados ativo.

---

## 🛠️ Tecnologias Utilizadas

### **Backend**
* **Python 3.11**
* **FastAPI** — Framework web assíncrono de altíssimo desempenho.
* **SQLAlchemy** — ORM para manipulação do banco SQLite.
* **Pydantic V2** — Validação e parsing de esquemas de dados.
* **PyJWT & Passlib (Bcrypt)** — Segurança e autenticação.
* **Uvicorn** — Servidor ASGI de alta performance.

### **Frontend**
* **HTML5 / JavaScript (ES6+)**
* **Tailwind CSS** — Estilização moderna e utilitária.
* **Lucide Icons & Chart.js** — Ícones dinâmicos e gráficos interativos.

### **Infraestrutura & DevOps**
* **Docker & Docker Compose** — Conteinerização do ecossistema backend.
* **Vercel** — Deployment do frontend estático.
* **Cloudflare Tunnels (`cloudflared`)** — Exposição de rotas HTTPS seguras.
* **PM2** — Gerenciamento contínuo de processos do servidor em background.

---

## 🚀 Como Rodar o Backend Localmente

### Pré-requisitos
* Python 3.11+
* Docker e Docker Compose (opcional)

### Opção 1: Via Docker Compose (Recomendado)

```bash
# Clone o repositório
git clone [https://github.com/SEU_USUARIO/apexcrm.git](https://github.com/SEU_USUARIO/apexcrm.git)
cd apexcrm

# Suba a aplicação conteinerizada
docker compose up --build -d

# A API estará disponível em: http://localhost:8000/docs
Opção 2: Execução Direta em Python
Bash
# Instale as dependências
pip install -r requirements.txt

# Inicie o servidor Uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
🌐 Configuração do Túnel de Produção (Cloudflare)
Para manter a API exposta de forma fixa e contínua em produção:

Bash
# Executa o túnel gerenciado pelo PM2 na VM
pm2 start "cloudflared tunnel --url http://localhost:8000" --name apexcrm-tunnel

# Salva a lista de processos para inicialização automática no boot do servidor
pm2 save
pm2 startup
