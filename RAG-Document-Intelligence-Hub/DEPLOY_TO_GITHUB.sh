#!/bin/bash

# ============================================
# 🚀 SCRIPT COMPLETO PARA SUBIR A GITHUB
# ============================================

clear
echo "╔════════════════════════════════════════════════════════╗"
echo "║  🚀 RAG Demo - Deploy to GitHub                       ║"
echo "║  Portfolio Ready - Sergio Arnold                       ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ====================================
# PASO 1: Verificaciones Pre-Deploy
# ====================================

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}   PASO 1: Verificaciones Pre-Deploy${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Verificar git
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git no está instalado${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} Git instalado: $(git --version)"

# Verificar configuración
GIT_USER=$(git config --global user.name)
GIT_EMAIL=$(git config --global user.email)

if [ -z "$GIT_USER" ] || [ -z "$GIT_EMAIL" ]; then
    echo -e "${YELLOW}⚠ Configurando Git...${NC}"
    git config --global user.name "sergioarnold87"
    git config --global user.email "anol1987.com"
    echo -e "${GREEN}✓${NC} Git configurado"
else
    echo -e "${GREEN}✓${NC} Usuario: $GIT_USER"
    echo -e "${GREEN}✓${NC} Email: $GIT_EMAIL"
fi

# Verificar .env no se va a commitear
if [ -f ".env" ] && ! grep -q "^\.env$" .gitignore; then
    echo -e "${RED}❌ PELIGRO: .env no está en .gitignore${NC}"
    echo ".env" >> .gitignore
    echo -e "${GREEN}✓${NC} .env agregado a .gitignore"
fi

echo -e "${GREEN}✓${NC} Verificaciones completadas"
echo ""

# ====================================
# PASO 2: Inicializar Repositorio
# ====================================

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}   PASO 2: Inicializar Repositorio Git${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

if [ -d ".git" ]; then
    echo -e "${YELLOW}⚠ Repositorio Git ya existe${NC}"
    read -p "¿Reinicializar? (s/n): " reinit
    if [ "$reinit" = "s" ]; then
        rm -rf .git
        git init
        git branch -M main
        echo -e "${GREEN}✓${NC} Repositorio reinicializado"
    fi
else
    git init
    git branch -M main
    echo -e "${GREEN}✓${NC} Repositorio inicializado"
fi

echo ""

# ====================================
# PASO 3: Staging de Archivos
# ====================================

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}   PASO 3: Preparar Archivos${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

echo "Agregando archivos al staging..."
git add .

echo ""
echo "Archivos que se van a commitear:"
echo -e "${BLUE}$(git status --short)${NC}"

echo ""
read -p "¿Continuar con el commit? (s/n): " continue_commit

if [ "$continue_commit" != "s" ]; then
    echo "Operación cancelada"
    exit 0
fi

echo ""

# ====================================
# PASO 4: Commit Inicial
# ====================================

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}   PASO 4: Crear Commit Inicial${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

git commit -m "feat: initial commit - RAG demo for data engineering portfolio

🎯 Características Principales:
- Sistema RAG completo con LangChain + ChromaDB + Streamlit
- 6 documentos técnicos de Data Engineering (110KB knowledge base)
- 5 modos de discovery interactivos
- Soporte para upload de documentos (TXT, PDF, CSV, MD)
- UI moderna e intuitiva con Streamlit

📚 Knowledge Base:
- Design Patterns (Lambda, Kappa, Medallion, CDC)
- Cost Optimization (Compute, Storage, Network)
- Data Fabric (Metadata, Virtualization, Governance)
- Quality Monitoring (Great Expectations, Metrics)
- Data Observability (Logs, Metrics, Traces)
- Analytics Engineering (dbt, Testing, Modeling)

🔧 Stack Tecnológico:
- Python 3.8+
- LangChain (RAG orchestration)
- ChromaDB (vector database)
- Streamlit (interactive UI)
- OpenAI API (LLM & embeddings)

📖 Documentación Completa:
- README con badges profesionales
- Quick Start guide (5 minutos)
- Contributing guidelines
- Security policy
- Code of Conduct
- GitHub workflows
- Issue & PR templates

🌟 Features GitHub:
- Conventional commits
- CI/CD workflows
- Branch protection ready
- Portfolio ready

Built with ❤️ in Neuquén, Argentina 🇦🇷
Author: Sergio Arnold (@sergioarnold87)"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Commit creado exitosamente"
else
    echo -e "${RED}❌ Error al crear commit${NC}"
    exit 1
fi

echo ""

# ====================================
# PASO 5: Instrucciones para GitHub
# ====================================

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}   PASO 5: Próximos Pasos en GitHub${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

echo -e "${YELLOW}┌─────────────────────────────────────────────────────┐${NC}"
echo -e "${YELLOW}│  📋 INSTRUCCIONES PARA SUBIR A GITHUB              │${NC}"
echo -e "${YELLOW}└─────────────────────────────────────────────────────┘${NC}"
echo ""

echo -e "${MAGENTA}1️⃣  Crear Repositorio en GitHub:${NC}"
echo ""
echo "   • Abre: https://github.com/new"
echo "   • Repository name: rag-demo-data-engineering"
echo "   • Description: 🧠 Sistema RAG avanzado para descubrir insights"
echo "     en Data Engineering | LangChain + ChromaDB + Streamlit"
echo "   • Public ✅"
echo "   • NO inicializar con README, .gitignore, o license"
echo "   • Click 'Create repository'"
echo ""

echo -e "${MAGENTA}2️⃣  Conectar Repositorio Local:${NC}"
echo ""
echo -e "   ${BLUE}git remote add origin https://github.com/sergioarnold87/rag-demo-data-engineering.git${NC}"
echo ""

echo -e "${MAGENTA}3️⃣  Verificar Conexión:${NC}"
echo ""
echo -e "   ${BLUE}git remote -v${NC}"
echo ""

echo -e "${MAGENTA}4️⃣  Subir Código:${NC}"
echo ""
echo -e "   ${BLUE}git push -u origin main${NC}"
echo ""
echo "   Si pide credenciales:"
echo "   • Username: sergioarnold87"
echo "   • Password: [Personal Access Token]"
echo "   • Genera token en: https://github.com/settings/tokens"
echo ""

echo -e "${MAGENTA}5️⃣  Configurar Repositorio:${NC}"
echo ""
echo "   a) Agregar Topics:"
echo "      rag, data-engineering, llm, langchain, streamlit,"
echo "      chromadb, python, openai, portfolio, machine-learning"
echo ""
echo "   b) Pinear en tu perfil:"
echo "      Profile → Customize pins → Seleccionar este repo"
echo ""
echo "   c) Agregar screenshot (opcional):"
echo "      - Ejecuta: streamlit run app/main.py"
echo "      - Toma screenshot → Guarda en assets/"
echo "      - Commit y push"
echo ""

echo -e "${YELLOW}┌─────────────────────────────────────────────────────┐${NC}"
echo -e "${YELLOW}│  🎨 CONFIGURACIÓN AVANZADA (OPCIONAL)              │${NC}"
echo -e "${YELLOW}└─────────────────────────────────────────────────────┘${NC}"
echo ""

echo "• Habilitar Dependabot:"
echo "  Settings → Security → Dependabot alerts ✅"
echo ""
echo "• Branch Protection:"
echo "  Settings → Branches → Add rule para 'main'"
echo ""
echo "• GitHub Actions:"
echo "  Ya incluido en .github/workflows/"
echo ""
echo "• Social Preview:"
echo "  Settings → Options → Upload image (1280x640px)"
echo ""

echo -e "${YELLOW}┌─────────────────────────────────────────────────────┐${NC}"
echo -e "${YELLOW}│  📚 RECURSOS CREADOS                                │${NC}"
echo -e "${YELLOW}└─────────────────────────────────────────────────────┘${NC}"
echo ""

echo "Archivos GitHub Professional:"
echo -e "${GREEN}✓${NC} README.md con badges profesionales"
echo -e "${GREEN}✓${NC} LICENSE (MIT)"
echo -e "${GREEN}✓${NC} CODE_OF_CONDUCT.md"
echo -e "${GREEN}✓${NC} CONTRIBUTING.md"
echo -e "${GREEN}✓${NC} SECURITY.md"
echo -e "${GREEN}✓${NC} CHANGELOG.md"
echo -e "${GREEN}✓${NC} .github/workflows/lint.yml"
echo -e "${GREEN}✓${NC} .github/ISSUE_TEMPLATE/"
echo -e "${GREEN}✓${NC} .github/pull_request_template.md"
echo -e "${GREEN}✓${NC} GITHUB_GUIDE.md (guía detallada)"
echo ""

echo -e "${YELLOW}┌─────────────────────────────────────────────────────┐${NC}"
echo -e "${YELLOW}│  🎯 COMANDOS RÁPIDOS                                │${NC}"
echo -e "${YELLOW}└─────────────────────────────────────────────────────┘${NC}"
echo ""

cat << 'COMMANDS'
# Conectar y subir (copia y pega):
git remote add origin https://github.com/sergioarnold87/rag-demo-data-engineering.git
git push -u origin main

# Ver estado:
git status
git log --oneline --graph

# Trabajar en nueva feature:
git checkout -b feature/mi-feature
git add .
git commit -m "feat: descripción"
git push -u origin feature/mi-feature

# Actualizar desde GitHub:
git pull origin main
COMMANDS

echo ""
echo -e "${YELLOW}┌─────────────────────────────────────────────────────┐${NC}"
echo -e "${YELLOW}│  ✨ CHECKLIST FINAL                                 │${NC}"
echo -e "${YELLOW}└─────────────────────────────────────────────────────┘${NC}"
echo ""

echo "Antes de considerar completo:"
echo "  [ ] Repositorio creado en GitHub"
echo "  [ ] Código subido exitosamente"
echo "  [ ] Topics agregados"
echo "  [ ] About section configurada"
echo "  [ ] Repo pinned en perfil"
echo "  [ ] README se ve bien en GitHub"
echo "  [ ] Screenshot agregado (opcional)"
echo "  [ ] Link agregado a LinkedIn/CV"
echo ""

echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✅ Repositorio Local Listo para GitHub              ║${NC}"
echo -e "${GREEN}║  🎉 ¡Ahora sigue las instrucciones arriba!           ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${CYAN}📖 Para más detalles, lee: GITHUB_GUIDE.md${NC}"
echo ""
echo -e "${MAGENTA}Built with ❤️ in Neuquén, Argentina 🇦🇷${NC}"
echo ""
