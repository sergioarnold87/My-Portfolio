# 🚀 Quick Start - Document Intelligence Hub V2

## 📥 Instalación en 3 Pasos

### 1. Instalar Dependencias
```bash
cd /home/sergio/CascadeProjects/rag-demo-data-engineering
pip install -r requirements.txt
```

### 2. Configurar API Key
```bash
# Crear archivo .env (si no existe)
cp .env.template .env

# Editar y agregar tu API key
echo "OPENAI_API_KEY=tu-api-key-aqui" > .env
```

### 3. Probar la Instalación
```bash
cd app
python test_new_architecture.py --quick
```

Si ves "✅ Demo completed successfully!" - ¡Estás listo!

---

## 🎯 Uso Básico

### Ejemplo 1: Procesar y Consultar un Documento

```python
from rag_engine_v2 import DocumentIntelligenceHub

# Crear instancia
hub = DocumentIntelligenceHub()

# Procesar documento (PDF, DOCX, EPUB, CSV, TXT, MD)
hub.process_document('mi_documento.pdf')

# Hacer pregunta
resultado = hub.query("¿Cuáles son los conceptos principales?")

print(resultado['answer'])
```

### Ejemplo 2: Quick One-Liner

```python
from rag_engine_v2 import quick_process_and_query

resultado = quick_process_and_query(
    'documento.pdf',
    '¿Qué es prompt engineering?'
)

print(resultado['answer'])
```

### Ejemplo 3: Con Métricas de Calidad

```python
hub = DocumentIntelligenceHub()
hub.process_document('documento.pdf')

resultado = hub.query(
    "Explica el concepto de RAG",
    include_metrics=True  # ← Incluir métricas
)

print(f"Respuesta: {resultado['answer']}")
print(f"Calidad: {resultado['metrics']['response']['quality_grade']}")
print(f"Confianza: {resultado['confidence']:.2f}")
```

---

## 🎨 Configuración Avanzada

### Cambiar Estrategia de Chunking

```python
hub = DocumentIntelligenceHub(
    chunking_strategy='semantic'  # 'recursive', 'semantic', 'sentence', 'paragraph'
)
```

### Usar Modelo GPT-4

```python
hub = DocumentIntelligenceHub(
    llm_model='gpt-4',
    embedding_model='text-embedding-3-large'  # Mejor calidad
)
```

### Activar OCR para PDFs Escaneados

```python
hub.process_document(
    'documento_escaneado.pdf',
    use_ocr=True  # Requiere tesseract instalado
)
```

---

## 📚 Procesamiento de Tu PDF

Para procesar **"Prompt Engineering for AI Systems (MEAP V05).pdf"**:

```python
from rag_engine_v2 import DocumentIntelligenceHub

# Configuración optimizada para libro técnico
hub = DocumentIntelligenceHub(
    chunk_size=800,
    chunk_overlap=100,
    chunking_strategy='semantic',  # Mejor para contenido estructurado
    llm_model='gpt-3.5-turbo'
)

# Procesar el PDF
resultado = hub.process_document(
    'Prompt Engineering for AI Systems (MEAP V05).pdf',
    clean_text=True  # Limpia headers/footers
)

# Verificar
print(f"✅ Procesado: {resultado['document_metadata']['word_count']} palabras")
print(f"✅ Chunks: {resultado['processing_stats']['chunks_created']}")

# Consultar
respuesta = hub.query(
    "¿Cuáles son los patrones de prompt engineering más importantes?",
    analyze_intent=True
)

print(respuesta['answer'])
```

---

## 🧪 Testing

### Test Rápido (2 minutos)
```bash
cd app
python test_new_architecture.py --quick
```

### Test Completo (5 minutos)
```bash
python test_new_architecture.py --full
```

### Verificar Módulos Individualmente

```python
# Test formato
from processor import detect_document_format, get_supported_formats
print(get_supported_formats())

# Test análisis de query
from rag import analyze_query
intent = analyze_query("Compare A and B")
print(intent.query_type)  # COMPARISON

# Test prompts
from prompts import get_system_prompt
print(get_system_prompt('document_assistant'))
```

---

## 🖥️ Usar con Streamlit (Original)

La app original **sigue funcionando** sin cambios:

```bash
streamlit run app/main.py
```

Para usar la nueva arquitectura en Streamlit, reemplazar en `main.py`:

```python
# Antes
from rag_engine import process_uploaded_file

# Después
from rag_engine_v2 import process_uploaded_file  # Compatible!
```

---

## 🎯 Casos de Uso Comunes

### 1. Análisis de Documentación Técnica
```python
hub.process_document('technical_spec.pdf')
hub.query("List all API endpoints mentioned")
```

### 2. Comparar Secciones
```python
hub.query("Compare the approach in Chapter 2 vs Chapter 3")
```

### 3. Resumen Ejecutivo
```python
hub.query("Provide an executive summary of the main findings")
```

### 4. Extracción de Conceptos
```python
resultado = hub.query("Extract all prompt patterns mentioned")
```

---

## 🔧 Troubleshooting

### Error: "No module named 'processor'"
```bash
# Asegúrate de estar en el directorio correcto
cd /home/sergio/CascadeProjects/rag-demo-data-engineering/app
python
```

### Error: "OpenAI API key not found"
```bash
# Verificar .env
cat ../.env

# O exportar directamente
export OPENAI_API_KEY="tu-key-aqui"
```

### Error: "pdfplumber not installed"
```bash
pip install pdfplumber python-docx ebooklib beautifulsoup4
```

### OCR no funciona
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# macOS
brew install tesseract

# Verificar
tesseract --version
```

---

## 📖 Documentación Completa

- **Arquitectura detallada**: Ver `NEW_ARCHITECTURE.md`
- **Arquitectura original**: Ver `ARCHITECTURE.md`
- **Setup original**: Ver `SETUP_INSTRUCTIONS.md`

---

## 💡 Tips Rápidos

1. **Chunking Semántico** → Mejor para libros y artículos
2. **GPT-4** → Mejor calidad, más caro
3. **Include Metrics** → Ver calidad de respuestas
4. **Analyze Intent** → Mejora retrieval automáticamente
5. **Clean Text** → Siempre activar para PDFs

---

## 🎉 ¡Listo!

Ahora puedes:
- ✅ Procesar cualquier documento (PDF, DOCX, EPUB, etc.)
- ✅ Hacer preguntas inteligentes con análisis de intención
- ✅ Obtener métricas de calidad
- ✅ Usar prompts profesionales desde YAML
- ✅ Comparar documentos
- ✅ Generar resúmenes multinivel

**Siguiente paso**: Coloca tu PDF y ejecuta:
```python
from rag_engine_v2 import quick_process_and_query
quick_process_and_query('tu_pdf.pdf', '¿Qué aprenderé en este documento?')
```

---

**¿Preguntas?** Revisa `NEW_ARCHITECTURE.md` para detalles técnicos completos.
