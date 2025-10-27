# 🤝 Contributing to RAG Demo - Data Engineering

¡Gracias por tu interés en contribuir! Este proyecto demuestra un sistema RAG para descubrimiento de conocimiento en Data Engineering.

## 📋 Cómo Contribuir

### 1. Fork del Proyecto
```bash
# Fork en GitHub y luego clona tu fork
git clone https://github.com/TU_USUARIO/rag-demo-data-engineering.git
cd rag-demo-data-engineering
```

### 2. Crea una Rama
```bash
# Nombra tu rama descriptivamente
git checkout -b feature/nueva-funcionalidad
# o
git checkout -b fix/correccion-bug
```

### 3. Realiza tus Cambios

**Áreas donde puedes contribuir:**
- 📚 Agregar más documentos al knowledge base
- 🎨 Mejorar la interfaz de Streamlit
- 🧪 Agregar más modos de discovery
- 🔧 Optimizar el RAG engine
- 📖 Mejorar la documentación
- 🐛 Corregir bugs

### 4. Prueba tus Cambios
```bash
# Activa el entorno virtual
source venv/bin/activate

# Ejecuta la aplicación
streamlit run app/main.py

# Verifica que todo funcione correctamente
```

### 5. Commit con Buenas Prácticas

Usamos **Conventional Commits**:

```bash
# Formato: tipo(scope): descripción

# Ejemplos:
git commit -m "feat(ui): agregar modo de búsqueda avanzada"
git commit -m "fix(rag): corregir error en embeddings"
git commit -m "docs(readme): actualizar instrucciones de setup"
git commit -m "refactor(engine): optimizar carga de documentos"
git commit -m "test(quality): agregar tests para validación"
```

**Tipos de commit:**
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `style`: Formato, sin cambios de código
- `refactor`: Refactorización de código
- `test`: Agregar o modificar tests
- `chore`: Tareas de mantenimiento

### 6. Push y Pull Request
```bash
# Push a tu fork
git push origin feature/nueva-funcionalidad

# Crea un Pull Request en GitHub con:
# - Título descriptivo
# - Descripción detallada de los cambios
# - Screenshots si aplica
# - Referencias a issues relacionados
```

## 🎯 Guía de Estilo

### Python
```python
# Seguimos PEP 8
# Usa nombres descriptivos
# Agrega docstrings

def create_vectorstore(docs: list) -> Chroma:
    """
    Crea un vector store a partir de documentos.
    
    Args:
        docs (list): Lista de documentos de texto
        
    Returns:
        Chroma: Vector store con embeddings
    """
    # Implementación...
```

### Commits
- Usa mensajes en español
- Primera letra en minúscula
- Modo imperativo: "agregar" no "agregado"
- Máximo 72 caracteres en el título
- Agrega descripción detallada si es necesario

### Documentación
- Actualiza README.md si cambias funcionalidad
- Agrega comentarios en código complejo
- Incluye ejemplos cuando sea útil

## 🧪 Testing

```bash
# Verifica que los documentos cargan correctamente
python -c "from app.rag_engine import load_documents; print(f'OK: {len(load_documents())} docs')"

# Verifica el vector store
python -c "from app.rag_engine import load_documents, create_vectorstore; vs = create_vectorstore(load_documents()); print('OK')"
```

## 📝 Checklist para Pull Requests

Antes de crear tu PR, verifica:

- [ ] El código sigue las guías de estilo
- [ ] Has probado los cambios localmente
- [ ] La documentación está actualizada
- [ ] Los commits siguen Conventional Commits
- [ ] No hay archivos sensibles (.env, claves, etc.)
- [ ] Has actualizado CHANGELOG si es necesario
- [ ] El PR tiene un título descriptivo

## 🐛 Reportar Bugs

Usa GitHub Issues con esta información:

```markdown
**Descripción del Bug**
Descripción clara del problema.

**Pasos para Reproducir**
1. Ir a '...'
2. Ejecutar '...'
3. Ver error

**Comportamiento Esperado**
Qué debería pasar.

**Comportamiento Actual**
Qué pasa realmente.

**Entorno**
- OS: Linux Mint 21
- Python: 3.10
- Versión del proyecto: v1.0.0

**Logs/Screenshots**
Adjunta información relevante.
```

## 💡 Sugerir Mejoras

Usa GitHub Issues con el tag `enhancement`:

```markdown
**Descripción de la Mejora**
Explica tu idea claramente.

**Motivación**
¿Por qué sería útil?

**Alternativas Consideradas**
Otras formas de resolver el problema.

**Contexto Adicional**
Screenshots, ejemplos, etc.
```

## 📞 Preguntas

Si tienes preguntas:
- Abre un GitHub Issue con el tag `question`
- Revisa la documentación en README.md
- Consulta QUICKSTART.md para setup

## 🎖️ Reconocimiento

Los contribuidores serán reconocidos en:
- README.md (sección de Contributors)
- Release notes
- Agradecimientos especiales para contribuciones significativas

## 📜 Código de Conducta

- Sé respetuoso y profesional
- Acepta críticas constructivas
- Enfócate en lo mejor para el proyecto
- Ayuda a otros contribuidores

---

¡Gracias por contribuir al proyecto! 🚀

**Mantenedor:** Sergio Arnold (@sergioarnold87)
