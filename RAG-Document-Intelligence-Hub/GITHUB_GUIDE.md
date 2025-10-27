# 🚀 Guía Completa para Subir a GitHub

Esta guía te llevará paso a paso para publicar este proyecto en GitHub como parte de tu portfolio profesional.

---

## 📋 Prerequisitos

Antes de comenzar, asegúrate de tener:

- [ ] Cuenta en GitHub (https://github.com)
- [ ] Git instalado en tu sistema
- [ ] Configuración básica de Git completada

### Verificar Git

```bash
# Verifica que git esté instalado
git --version

# Verifica tu configuración
git config --global user.name
git config --global user.email

# Si no está configurado:
git config --global user.name "Sergio Arnold"
git config --global user.email "anol1987.com"
```

---

## 🎯 Opción 1: Método Automático (Recomendado)

### Paso 1: Ejecuta el Script de Setup

```bash
cd /home/sergio/CascadeProjects/rag-demo-data-engineering

# Ejecuta el script automático
./git-setup.sh
```

Este script hará:
- ✅ Verificar configuración de Git
- ✅ Inicializar repositorio
- ✅ Crear primer commit estructurado
- ✅ Configurar rama main
- ✅ Mostrar próximos pasos

### Paso 2: Crea el Repositorio en GitHub

1. Ve a: https://github.com/new
2. Configura el repositorio:
   - **Repository name**: `rag-demo-data-engineering`
   - **Description**: `🧠 Sistema RAG avanzado para descubrimiento de insights en Data Engineering | LangChain + ChromaDB + Streamlit`
   - **Visibility**: Public ✅
   - **NO** inicialices con README (ya lo tienes)
   - **NO** agregues .gitignore (ya lo tienes)
   - **NO** agregues license (ya lo tienes)

3. Click en **"Create repository"**

### Paso 3: Conecta y Sube tu Código

```bash
# Conecta tu repo local con GitHub
git remote add origin https://github.com/sergioarnold87/rag-demo-data-engineering.git

# Verifica la conexión
git remote -v

# Sube tu código
git push -u origin main
```

Si pide credenciales:
```bash
# Usa Personal Access Token (no password)
# Genera uno en: https://github.com/settings/tokens
Username: sergioarnold87
Password: [tu-personal-access-token]
```

---

## 🎯 Opción 2: Método Manual

### Paso 1: Inicializar Git

```bash
cd /home/sergio/CascadeProjects/rag-demo-data-engineering

# Inicializar repositorio
git init

# Configurar rama principal
git branch -M main

# Verificar .gitignore
cat .gitignore  # Debe incluir .env
```

### Paso 2: Primer Commit

```bash
# Agregar todos los archivos
git add .

# Ver qué se va a commitear
git status

# Crear commit inicial
git commit -m "feat: initial commit - RAG demo for data engineering

- Complete RAG implementation with LangChain + ChromaDB
- 6 comprehensive data engineering knowledge base files
- Streamlit interactive UI with 5 discovery modes
- Full documentation and guides
- GitHub workflows and templates
- MIT License

Built in Neuquén, Argentina 🇦🇷"
```

### Paso 3: Crear Repo en GitHub y Conectar

(Sigue los mismos pasos de la Opción 1, Paso 2 y 3)

---

## 🎨 Configuración Profesional del Repositorio

### 1. Agregar Topics (Etiquetas)

En GitHub, ve a tu repo → Click en ⚙️ junto a "About" → Agrega topics:

```
rag
data-engineering
llm
langchain
streamlit
chromadb
python
openai
retrieval-augmented-generation
machine-learning
natural-language-processing
portfolio
```

### 2. Configurar About Section

```
🧠 Sistema RAG avanzado para descubrir insights ocultos en documentación técnica de Data Engineering. Implementa LangChain, ChromaDB y Streamlit con 5 modos de discovery interactivos.
```

Website: `https://github.com/sergioarnold87/rag-demo-data-engineering`

### 3. Pin el Repositorio en tu Perfil

1. Ve a tu perfil: https://github.com/sergioarnold87
2. Scroll a "Pinned repositories"
3. Click "Customize your pins"
4. Selecciona `rag-demo-data-engineering`
5. Arrastra para ordenar (ponlo primero)

### 4. Agregar Screenshot

```bash
# Ejecuta la app
streamlit run app/main.py

# Toma un screenshot (tecla PrtScr)

# Guarda como: assets/screenshot.png

# Commit el screenshot
git add assets/screenshot.png
git commit -m "docs: add demo screenshot"
git push
```

Luego edita el README en GitHub para agregar la imagen al inicio.

---

## 📊 GitHub Features para Habilitar

### 1. GitHub Pages (Opcional - para documentación)

Settings → Pages → Source: main branch → docs/ folder

### 2. Dependabot

Settings → Code security and analysis → Enable:
- ✅ Dependency graph
- ✅ Dependabot alerts
- ✅ Dependabot security updates

### 3. Branch Protection

Settings → Branches → Add rule:
- Branch name pattern: `main`
- ✅ Require a pull request before merging
- ✅ Require status checks to pass

### 4. Social Preview

Settings → Options → Social preview → Upload image:
- Tamaño recomendado: 1280x640px
- Formato: PNG o JPG

---

## 🔄 Workflow de Desarrollo

### Trabajando en Nuevas Features

```bash
# Crear rama para feature
git checkout -b feature/nueva-funcionalidad

# Hacer cambios
# ... edita archivos ...

# Commit con conventional commits
git add .
git commit -m "feat(ui): agregar modo de búsqueda avanzada"

# Subir rama
git push -u origin feature/nueva-funcionalidad

# En GitHub: Crear Pull Request
# Revisar → Aprobar → Merge
```

### Conventional Commits

Formato: `tipo(scope): descripción`

**Tipos**:
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `style`: Formato (no afecta código)
- `refactor`: Refactorización
- `test`: Agregar/modificar tests
- `chore`: Tareas de mantenimiento

**Ejemplos**:
```bash
git commit -m "feat(rag): agregar soporte para archivos PDF"
git commit -m "fix(ui): corregir error en upload de archivos"
git commit -m "docs(readme): actualizar instrucciones de instalación"
git commit -m "refactor(engine): optimizar carga de vectorstore"
```

---

## 📈 Mejorar la Visibilidad del Proyecto

### 1. README Atractivo

Tu README ya incluye:
- ✅ Badges profesionales
- ✅ Descripción clara
- ✅ Instrucciones de instalación
- ✅ Ejemplos de uso
- ✅ Documentación completa

Agregar (opcional):
- Screenshots/GIFs de la app en acción
- Video demo (puede ser YouTube embedded)
- Badges de CI/CD status
- Badge de contributors

### 2. Releases y Versiones

```bash
# Crear un tag para release
git tag -a v2.0.0 -m "Release v2.0.0 - Upload Mode Added"

# Subir el tag
git push origin v2.0.0

# En GitHub: Ir a Releases → Create new release
# - Tag: v2.0.0
# - Title: "v2.0.0 - Upload Mode & Enhanced UI"
# - Description: Usar contenido de CHANGELOG.md
# - Attach binaries (opcional)
```

### 3. Social Media

Comparte en:
- LinkedIn: "Proud to share my latest project..."
- Twitter/X: Con hashtags #DataEngineering #RAG #Python
- Dev.to: Escribe un artículo explicando el proyecto
- Medium: Tutorial de cómo lo construiste

### 4. GitHub Community

- Agregar README.md en tu perfil: https://github.com/sergioarnold87/sergioarnold87
- Contribuir a proyectos similares
- Responder en Discussions si las habilitas
- Participar en GitHub Stars / Trending

---

## 🛠️ Comandos Útiles

### Ver el Estado

```bash
# Estado actual
git status

# Historial de commits
git log --oneline --graph --all

# Ver cambios no commiteados
git diff

# Ver archivos modificados
git diff --name-only
```

### Deshacer Cambios

```bash
# Descartar cambios en un archivo
git checkout -- archivo.py

# Descartar todos los cambios no commiteados
git reset --hard

# Deshacer el último commit (mantiene cambios)
git reset --soft HEAD~1

# Deshacer el último commit (descarta cambios)
git reset --hard HEAD~1
```

### Limpiar

```bash
# Ver qué se va a limpiar
git clean -n

# Limpiar archivos no trackeados
git clean -f

# Limpiar archivos y directorios
git clean -fd
```

### Sincronizar

```bash
# Descargar cambios (sin merge)
git fetch origin

# Descargar y mergear
git pull origin main

# Subir cambios
git push origin main

# Subir todos los tags
git push --tags
```

---

## 🐛 Solución de Problemas

### Error: "Permission denied (publickey)"

```bash
# Generar SSH key
ssh-keygen -t ed25519 -C "anol1987.com"

# Agregar a ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copiar la key pública
cat ~/.ssh/id_ed25519.pub

# Agregar en GitHub: Settings → SSH and GPG keys → New SSH key
```

### Error: "Remote origin already exists"

```bash
# Ver remotes actuales
git remote -v

# Eliminar remote
git remote remove origin

# Agregar de nuevo
git remote add origin https://github.com/sergioarnold87/rag-demo-data-engineering.git
```

### Error: "Failed to push some refs"

```bash
# Hay cambios en GitHub que no tienes local
# Descargar primero
git pull origin main --rebase

# Luego subir
git push origin main
```

### Archivo .env fue commiteado por error

```bash
# Si AÚN NO hiciste push:
git reset HEAD .env
git checkout -- .env

# Si YA hiciste push:
# 1. Elimina el archivo del historial
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# 2. Fuerza el push
git push origin --force --all

# 3. Rota tu API key inmediatamente
# 4. Agrega .env a .gitignore si no está
```

---

## ✅ Checklist Final

Antes de considerar el proyecto completo en GitHub:

### Código
- [ ] Todo el código funciona localmente
- [ ] Sin API keys hardcodeadas
- [ ] .env está en .gitignore
- [ ] Dependencias listadas en requirements.txt
- [ ] Código comentado donde sea necesario

### Documentación
- [ ] README.md completo y profesional
- [ ] LICENSE incluida
- [ ] CONTRIBUTING.md explicando cómo contribuir
- [ ] CHANGELOG.md con historial de versiones
- [ ] CODE_OF_CONDUCT.md
- [ ] SECURITY.md con políticas de seguridad

### GitHub
- [ ] Repositorio público
- [ ] Topics/tags agregados
- [ ] About section completada
- [ ] README muestra bien en GitHub
- [ ] Screenshot/GIF agregado (opcional pero recomendado)
- [ ] Repositorio pinned en perfil
- [ ] Branch protection configurada
- [ ] GitHub Actions funcionando (si las tienes)

### Portfolio
- [ ] Link al repo en tu CV/LinkedIn
- [ ] Descripción clara del proyecto
- [ ] Destacar tecnologías usadas
- [ ] Mencionar en "Proyectos" de LinkedIn
- [ ] Considerar escribir un blog post sobre él

---

## 🎉 ¡Felicitaciones!

Tu proyecto ahora está en GitHub de forma profesional. Algunas ideas finales:

### Mantenimiento Continuo

- Responde issues y PRs prontamente
- Mantén dependencias actualizadas
- Agrega features basadas en feedback
- Documenta decisiones importantes
- Celebra milestones (10 ⭐, 100 ⭐, etc.)

### Promoción

- Comparte en redes sociales
- Escribe un artículo técnico explicándolo
- Preséntalo en meetups locales
- Úsalo como ejemplo en entrevistas
- Sigue mejorándolo basado en feedback

---

**¿Necesitas ayuda?** Revisa la documentación o crea un issue en el repositorio.

**Built with ❤️ in Neuquén, Argentina 🇦🇷**
