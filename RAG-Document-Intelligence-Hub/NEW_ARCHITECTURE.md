# 🏗️ Nueva Arquitectura - Document Intelligence Hub

## 📋 Descripción General

Sistema RAG avanzado con arquitectura modular basada en **Prompt Engineering profesional** y procesamiento multi-formato de documentos.

---

## 🆕 ¿Qué hay de nuevo?

### ✅ Módulos Implementados

#### 1. **Processor Module** (`app/processor/`)
- ✨ **detect_format.py**: Detección inteligente de formatos (PDF, DOCX, EPUB, CSV, imágenes)
- ✨ **extract_text.py**: Extracción multi-formato con soporte OCR
- ✨ **clean_text.py**: Limpieza avanzada de texto (headers, footers, artefactos)
- ✨ **chunker.py**: Chunking semántico adaptativo (4 estrategias)
- ✨ **embeddings.py**: Gestión de embeddings y vectorstores

#### 2. **RAG Module** (`app/rag/`)
- ✨ **query_analyzer.py**: Análisis semántico de queries (8 tipos)
- ✨ **retriever.py**: Retrieval avanzado con re-ranking y MMR
- ✨ **generator.py**: Generación contextual con prompts especializados

#### 3. **Utils Module** (`app/utils/`)
- ✨ **metrics.py**: Métricas de calidad para retrieval y respuestas
- ✨ **language_tools.py**: Detección de idioma, readability, NLP utils

#### 4. **Prompts Module** (`app/prompts/`)
- ✨ **system_prompts.yaml**: 5 roles de sistema configurables
- ✨ **query_prompts.yaml**: 11 templates de consulta
- ✨ **summarization_prompts.yaml**: 7 estrategias de resumen
- ✨ **compare_docs_prompts.yaml**: 6 patrones de comparación
- ✨ **prompt_loader.py**: Cargador dinámico de prompts YAML

#### 5. **Engine V2** (`app/rag_engine_v2.py`)
- ✨ **DocumentIntelligenceHub**: Clase unificada con pipeline completo
- ✨ Backward compatibility con código existente
- ✨ Métricas integradas y análisis de calidad

---

## 🚀 Cómo Usar la Nueva Arquitectura

### Opción 1: API Completa (Recomendada)

```python
from rag_engine_v2 import DocumentIntelligenceHub

# Inicializar
hub = DocumentIntelligenceHub(
    embedding_model='text-embedding-3-small',
    llm_model='gpt-3.5-turbo',
    chunk_size=800,
    chunking_strategy='semantic'  # 'recursive', 'semantic', 'sentence', 'paragraph'
)

# Procesar documento
result = hub.process_document(
    'path/to/document.pdf',  # Soporta: PDF, DOCX, EPUB, CSV, TXT, MD, imágenes
    clean_text=True,
    use_ocr=False
)

# Consultar
answer = hub.query(
    "¿Qué es prompt engineering?",
    analyze_intent=True,      # Análisis automático de intención
    include_metrics=True       # Incluir métricas de calidad
)

print(answer['answer'])
print(f"Confianza: {answer['confidence']}")
print(f"Fuentes: {answer['num_sources']}")
```

### Opción 2: Módulos Individuales

```python
# Procesamiento de documentos
from processor import extract_text_from_document, create_smart_chunks

extraction = extract_text_from_document('document.pdf')
chunks = create_smart_chunks(
    extraction.text,
    strategy='semantic',
    chunk_size=800
)

# Análisis de queries
from rag import analyze_query

intent = analyze_query("Compare A and B")
print(intent.query_type)  # QueryType.COMPARISON
print(intent.keywords)    # ['compare', 'a', 'b']

# Prompts YAML
from prompts import render_prompt

prompt = render_prompt(
    'query.prompts',
    'comparison',
    context="...",
    question="Compare A and B"
)
```

### Opción 3: Quick Start

```python
from rag_engine_v2 import quick_process_and_query

result = quick_process_and_query(
    'document.pdf',
    'What are the main concepts?'
)

print(result['answer'])
```

---

## 📊 Formatos Soportados

| Categoría | Extensiones | Método |
|-----------|-------------|--------|
| **Texto** | .txt, .md, .rst | UTF-8 decode |
| **PDF** | .pdf | pdfplumber / PyPDF2 |
| **Documentos** | .docx, .doc | python-docx |
| **Hojas de cálculo** | .csv, .xlsx | pandas |
| **Ebooks** | .epub | ebooklib |
| **Imágenes** | .png, .jpg, .tiff | Tesseract OCR |

---

## 🎯 Tipos de Query Soportados

El sistema detecta automáticamente el tipo de consulta y adapta la estrategia:

1. **FACTUAL**: "What is X?"
2. **COMPARISON**: "Compare A and B"
3. **SUMMARY**: "Summarize this section"
4. **EXPLANATION**: "Explain how X works"
5. **LISTING**: "List all concepts"
6. **PROCEDURAL**: "How to do X?"
7. **CONCEPTUAL**: "How does X relate to Y?"
8. **DEFINITION**: "Define X"

---

## 🧠 Estrategias de Chunking

### 1. Recursive (Default)
```python
chunking_strategy='recursive'
```
- Mejor para: Documentos generales
- Separadores jerárquicos: `\n\n`, `\n`, `. `, ` `

### 2. Semantic
```python
chunking_strategy='semantic'
```
- Mejor para: Mantener coherencia semántica
- Respeta límites de párrafos

### 3. Sentence
```python
chunking_strategy='sentence'
```
- Mejor para: Precisión máxima
- Chunks basados en oraciones completas

### 4. Paragraph
```python
chunking_strategy='paragraph'
```
- Mejor para: Preservar estructura
- Un chunk = un párrafo

---

## 📈 Métricas de Calidad

### Retrieval Metrics
```python
{
    'num_results': 5,
    'avg_score': 0.82,
    'quality_grade': 'B',
    'above_threshold': 4
}
```

### Response Quality
```python
{
    'quality_score': 0.78,
    'quality_grade': 'B',
    'word_count': 145,
    'has_citations': True,
    'lexical_diversity': 0.65
}
```

---

## 🎨 Sistema de Prompts YAML

### System Prompts (Roles)
- `document_assistant`: Asistente general de documentos
- `technical_analyzer`: Análisis técnico
- `prompt_engineering_expert`: Experto en prompt engineering
- `data_engineering_specialist`: Especialista en data engineering
- `conversational_assistant`: Asistente conversacional

### Query Templates
- `basic_qa`: Preguntas básicas
- `detailed_analysis`: Análisis detallado
- `comparison`: Comparaciones
- `definition`: Definiciones
- `explanation`: Explicaciones
- `summarization`: Resúmenes
- `listing`: Listados
- `procedural`: Procedimientos
- `with_citations`: Con citas explícitas

### Uso
```python
from prompts import get_system_prompt, render_prompt

# Obtener rol de sistema
system = get_system_prompt('technical_analyzer')

# Renderizar template
prompt = render_prompt(
    'query.prompts',
    'comparison',
    context="...",
    question="Compare X and Y"
)
```

---

## 🔧 Testing

### Quick Test
```bash
cd app
python test_new_architecture.py --quick
```

### Full Test Suite
```bash
python test_new_architecture.py --full
```

---

## 🔄 Backward Compatibility

El código existente **sigue funcionando** sin cambios:

```python
# Código antiguo (main.py)
from rag_engine import process_uploaded_file, build_qa_chain

vectorstore = process_uploaded_file(file)  # ✅ Funciona
qa = build_qa_chain(vectorstore)            # ✅ Funciona
```

Las funciones antiguas están implementadas en `rag_engine_v2.py` como wrappers.

---

## 📦 Dependencias Nuevas

Actualizar con:
```bash
pip install -r requirements.txt
```

Dependencias agregadas:
- `pdfplumber` - Mejor extracción de PDFs
- `python-docx` - Soporte DOCX
- `ebooklib` - Soporte EPUB
- `beautifulsoup4` - Parsing HTML
- `pytesseract` - OCR (opcional)
- `Pillow` - Procesamiento de imágenes
- `unidecode` - Normalización Unicode
- `pyyaml` - Carga de prompts
- `faiss-cpu` - Vector store alternativo

---

## 🚦 Próximos Pasos

1. **Probar la nueva arquitectura:**
   ```bash
   python app/test_new_architecture.py --full
   ```

2. **Actualizar main.py (opcional):**
   - Integrar `DocumentIntelligenceHub`
   - Agregar selector de estrategias de chunking
   - Mostrar métricas en UI

3. **Agregar tu PDF:**
   - Colocar "Prompt Engineering for AI Systems (MEAP V05).pdf" en carpeta
   - Procesar con OCR si tiene imágenes escaneadas

4. **Explorar prompts:**
   - Editar YAMLs en `app/prompts/`
   - Crear nuevos roles o templates
   - Personalizar para tu dominio

---

## 💡 Ejemplos de Uso Avanzado

### Procesar PDF con OCR
```python
hub = DocumentIntelligenceHub()
hub.process_document(
    'scanned_document.pdf',
    use_ocr=True  # Activa Tesseract
)
```

### Comparar Documentos
```python
from prompts import render_prompt

prompt = render_prompt(
    'compare.docs.prompts',
    'side_by_side',
    doc_a="Content from doc A",
    doc_b="Content from doc B"
)
```

### Análisis con Métricas Completas
```python
result = hub.query(
    "Explain prompt engineering",
    include_metrics=True
)

print(f"Retrieval: {result['metrics']['retrieval']['quality_grade']}")
print(f"Response: {result['metrics']['response']['quality_grade']}")
print(f"Query Type: {result['metrics']['query_intent']['type']}")
```

---

## 📞 Soporte

Para problemas o preguntas:
1. Revisar `ARCHITECTURE.md` (arquitectura original)
2. Ejecutar tests: `python test_new_architecture.py --full`
3. Verificar logs de procesamiento en consola

---

**Versión:** 2.0 Advanced  
**Fecha:** Octubre 2025  
**Compatibilidad:** Python 3.8+  
**Framework:** LangChain + OpenAI + Streamlit
