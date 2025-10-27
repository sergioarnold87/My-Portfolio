#!/bin/bash

echo "🚀 Git Setup - RAG Demo Data Engineering"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Verificar si git está instalado
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git no está instalado.${NC}"
    echo "Instala git con: sudo apt install git"
    exit 1
fi

echo -e "${GREEN}✓${NC} Git encontrado: $(git --version)"
echo ""

# Verificar configuración de git
echo "🔧 Verificando configuración de Git..."
GIT_USER=$(git config --global user.name)
GIT_EMAIL=$(git config --global user.email)

if [ -z "$GIT_USER" ] || [ -z "$GIT_EMAIL" ]; then
    echo -e "${YELLOW}⚠ Configuración de Git incompleta${NC}"
    echo ""
    read -p "Ingresa tu nombre para Git: " git_name
    read -p "Ingresa tu email para Git: " git_email
    
    git config --global user.name "$git_name"
    git config --global user.email "$git_email"
    echo -e "${GREEN}✓${NC} Git configurado correctamente"
else
    echo -e "${GREEN}✓${NC} Usuario: $GIT_USER"
    echo -e "${GREEN}✓${NC} Email: $GIT_EMAIL"
fi

echo ""

# Verificar si ya es un repositorio git
if [ -d ".git" ]; then
    echo -e "${YELLOW}⚠ Este directorio ya es un repositorio Git${NC}"
    read -p "¿Quieres reinicializar? (s/n): " reinit
    if [ "$reinit" = "s" ] || [ "$reinit" = "S" ]; then
        rm -rf .git
        echo -e "${GREEN}✓${NC} Repositorio anterior eliminado"
    else
        echo "Operación cancelada"
        exit 0
    fi
fi

# Inicializar repositorio
echo ""
echo "📦 Inicializando repositorio Git..."
git init
git branch -M main
echo -e "${GREEN}✓${NC} Repositorio inicializado (rama: main)"

# Verificar .gitignore
echo ""
echo "🔒 Verificando .gitignore..."
if [ -f ".gitignore" ]; then
    echo -e "${GREEN}✓${NC} .gitignore encontrado"
    
    # Verificar que .env esté en gitignore
    if grep -q "^\.env$" .gitignore; then
        echo -e "${GREEN}✓${NC} .env está en .gitignore"
    else
        echo ".env" >> .gitignore
        echo -e "${YELLOW}⚠${NC} .env agregado a .gitignore"
    fi
else
    echo -e "${RED}❌ .gitignore no encontrado${NC}"
    echo "Creando .gitignore básico..."
    cat > .gitignore << 'EOF'
# Environment
.env
venv/
__pycache__/
*.pyc

# ChromaDB
chroma_db/

# IDE
.vscode/
.idea/

# OS
.DS_Store
EOF
    echo -e "${GREEN}✓${NC} .gitignore creado"
fi

# Staging de archivos
echo ""
echo "📋 Agregando archivos al staging..."
git add .
echo -e "${GREEN}✓${NC} Archivos agregados"

# Mostrar status
echo ""
echo "📊 Estado del repositorio:"
git status --short

# Primer commit
echo ""
echo "💾 Creando commit inicial..."
git commit -m "feat: initial commit - RAG demo for data engineering

- Complete RAG implementation with LangChain + ChromaDB
- 6 comprehensive data engineering knowledge base files
- Streamlit interactive UI with 5 discovery modes
- Full documentation (README, QUICKSTART, guides)
- Automated setup script
- GitHub workflows and templates
- MIT License

Built in Neuquén, Argentina 🇦🇷"

echo -e "${GREEN}✓${NC} Commit inicial creado"

# Mostrar log
echo ""
echo "📜 Historial de commits:"
git log --oneline --graph --all

echo ""
echo "=========================================="
echo -e "${GREEN}✓ Repositorio Git configurado exitosamente${NC}"
echo ""
echo "📋 Próximos pasos:"
echo ""
echo "1️⃣  Crea un nuevo repositorio en GitHub:"
echo "   https://github.com/new"
echo "   Nombre sugerido: rag-demo-data-engineering"
echo ""
echo "2️⃣  Conecta tu repo local con GitHub:"
echo -e "   ${BLUE}git remote add origin https://github.com/sergioarnold87/rag-demo-data-engineering.git${NC}"
echo ""
echo "3️⃣  Sube tu código:"
echo -e "   ${BLUE}git push -u origin main${NC}"
echo ""
echo "4️⃣  (Opcional) Configura GitHub Pages si creaste docs:"
echo "   Settings → Pages → Source: main branch"
echo ""
echo "5️⃣  Agrega screenshots para hacerlo más visual:"
echo "   Ver: assets/demo-screenshot.md"
echo ""
echo "=========================================="
echo ""
echo "💡 Tip: Para ver tu repo en tu portfolio:"
echo "   1. Ve a tu perfil: https://github.com/sergioarnold87"
echo "   2. Pin este repo (⭐ Pin)"
echo "   3. Agrega topics: rag, data-engineering, llm, python"
echo ""
echo "🎉 ¡Listo para GitHub! 🚀"
