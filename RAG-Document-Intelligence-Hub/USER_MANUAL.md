# 📘 MANUAL DEL USUARIO - RAG Demo

**Sistema de Asistencia Inteligente para Data Engineering**

---

## 📑 Contenidos

1. [Introducción](#introducción)
2. [Instalación Rápida](#instalación-rápida)
3. [Guía de Uso](#guía-de-uso)
4. [Ejemplos Prácticos](#ejemplos-prácticos)
5. [Solución de Problemas](#solución-de-problemas)
6. [FAQ](#faq)

---

## 📖 Introducción

### ¿Qué es RAG Demo?

RAG Demo es un asistente inteligente basado en **Retrieval-Augmented Generation** que:

✅ Consulta **16 libros técnicos** sobre Data Engineering, ML, RAG, y dominios especializados  
✅ Analiza **tus propios documentos** (PDF, TXT, CSV, Markdown)  
✅ Genera respuestas con **referencias a fuentes**  
✅ Proporciona **código Python** y ejemplos prácticos

### Capacidades Principales

- 🔍 **Búsqueda semántica** en biblioteca técnica
- 🤖 **Respuestas generadas por GPT-4**
- 📤 **Procesamiento automático** de documentos
- 📊 **Discovery modes** para exploración guiada
- 💡 **Insights** con contexto técnico profundo

---

## 🚀 Instalación Rápida

### Requisitos

- Python 3.8+
- 4 GB RAM mínimo
- API Key de OpenAI
- Conexión a Internet

### Pasos de Instalación

```bash
# 1. Navegar al proyecto
cd /home/sergio/CascadeProjects/rag-demo-data-engineering

# 2. Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate    # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar OpenAI API Key
export OPENAI_API_KEY='sk-...'
# O crear archivo .env con: OPENAI_API_KEY=sk-...

# 5. Lanzar aplicación
streamlit run app/main.py
```

### Verificación

- Abre: http://localhost:5601
- Deberías ver la interfaz principal
- La aplicación pedirá API key si no está configurada

---

## 📚 Guía de Uso

### Interfaz Principal

```
Sidebar (Izquierda):
├─ 📁 Data Source
│  ├─ 📤 Upload Document
│  └─ 📚 Pre-loaded Knowledge Base
└─ ℹ️ About (información del sistema)

Área Principal:
├─ Selección de modo
├─ Inputs/prompts
├─ Botones de acción
└─ Resultados y respuestas
```

---

## 🎯 Modo 1: Pre-loaded Knowledge Base

### ¿Qué hace?

Consulta una biblioteca de **16 libros técnicos** simultáneamente.

### Biblioteca Disponible

**Data Engineering (12 libros):**
- Design Patterns, Cost-Effective Pipelines
- Data Fabric, Quality Monitoring
- Data Observability (2 libros)
- Analytics Engineering
- ML System Design, Generative AI & RAG
- Data Augmentation, Agentic AI
- Kibana 8.x Guide

**Domain Knowledge (4 libros):**
- Oil & Gas Economics (2 libros)
- ML Factor Investing
- Project Management Metrics

### Cómo Usar

**1. Seleccionar en sidebar:**
```
📁 Data Source
  🔘 📚 Pre-loaded Knowledge Base
```

**2. Esperar carga:**
```
📚 Loading knowledge base... (5-15 seg)
✅ Loaded 16 documents
```

**3. Seleccionar Discovery Mode:**

- **Foundational Concepts:** Conceptos básicos
- **Architecture Patterns:** Lambda, Kappa, Medallion
- **Tools & Technologies:** Herramientas específicas
- **Cost Optimization:** Reducción de costos
- **MLOps & Deployment:** Operaciones ML
- **Custom Query:** Pregunta libre

**4. Ejecutar query:**
```
[Selecciona modo o escribe query personalizada]
         ↓
  [🚀 Run Discovery]
         ↓
  💡 Respuesta con fuentes
```

### Ejemplos de Queries

```
✅ "Explain the 5 pillars of data observability"
✅ "Compare Lambda vs Kappa architecture"
✅ "Best practices for Airflow cost optimization"
✅ "How to implement RAG with LangChain?"
✅ "Python code for data augmentation techniques"
```

---

## 📤 Modo 2: Upload Document

### ¿Qué hace?

Analiza **tus propios documentos** con procesamiento automático.

### Formatos Soportados

| Tipo | Extensión | Límite Recomendado |
|------|-----------|-------------------|
| Texto | .txt, .md | < 5 MB |
| PDF | .pdf | < 10 MB, < 100 páginas |
| Datos | .csv | < 2 MB |

### Pipeline Automático

```
Documento → Extracción → Chunking → Embeddings → Vectorstore
                        (800 chars)   (OpenAI)    (ChromaDB)
```

### Cómo Usar

**1. Seleccionar modo:**
```
📁 Data Source
  🔘 📤 Upload Document
```

**2. Subir archivo:**
- Drag & drop desde explorador
- O clic en "Browse files"

**3. Esperar procesamiento:**
```
🔄 Processing document...
✅ Document 'paper.pdf' processed! Ready to query.
```

**4. Hacer preguntas:**
```
💬 Ask Questions
┌────────────────────────────────────┐
│ What are the main conclusions?    │
└────────────────────────────────────┘
      [🔍 Analyze]
```

### Casos de Uso

**Papers Académicos:**
```
"Summarize methodology and key findings"
"What datasets were used?"
"Compare with previous work"
```

**Reportes de Negocio:**
```
"Extract Q3 key metrics"
"List main risks identified"
"Summarize recommendations"
```

**Documentación Técnica:**
```
"How to configure authentication?"
"List all API endpoints"
"Explain deployment process"
```

---

## 💡 Ejemplos Prácticos

### Ejemplo 1: Aprender Data Observability

```
Modo: Pre-loaded
Discovery: Foundational Concepts
Query: "Explain data observability with the 5 pillars 
        and practical examples"

Resultado: Definición + 5 pilares + ejemplos + referencias
```

### Ejemplo 2: Diseñar Arquitectura

```
Modo: Pre-loaded
Discovery: Architecture Patterns
Query: "Compare Lambda vs Kappa for real-time analytics. 
        Consider cost, latency, complexity"

Resultado: Tabla comparativa + casos de uso + recomendación
```

### Ejemplo 3: Analizar Paper ML

```
Modo: Upload Document
Archivo: transformer_paper.pdf
Query 1: "Summarize in 3 paragraphs"
Query 2: "Explain Transformer architecture"
Query 3: "What are key innovations vs RNNs?"

Resultado: Resumen + arquitectura + comparación
```

### Ejemplo 4: Optimizar Costos

```
Modo: Pre-loaded
Discovery: Cost Optimization
Query: "Top 5 strategies to reduce Spark ETL costs on AWS. 
        Include techniques and estimated savings"

Resultado: 5 estrategias + técnicas + estimaciones
```

### Ejemplo 5: Cross-Domain Insight

```
Modo: Pre-loaded
Discovery: Custom Query
Query: "Apply data observability principles to ML model 
        monitoring in production"

Resultado: Mapeo conceptual + herramientas + implementación
```

---

## 🔧 Solución de Problemas

### "No module named 'streamlit'"

**Solución:**
```bash
pip install -r requirements.txt
```

### "OpenAI API key not found"

**Solución:**
```bash
export OPENAI_API_KEY='sk-...'
# O crear .env con la API key
```

### "Port 5601 already in use"

**Solución:**
```bash
# Matar proceso existente
pkill -f streamlit

# O usar otro puerto
streamlit run app/main.py --server.port 8502
```

### Procesamiento Lento

**Causas y soluciones:**
- **Documento grande:** Dividir en archivos más pequeños
- **Internet lento:** Verificar conexión
- **API rate limits:** Esperar unos minutos

### Respuestas Irrelevantes

**Mejora tu query:**
```
❌ "Tell me about data"
✅ "Explain data lineage tracking in production"

❌ "How to optimize?"
✅ "Optimize Spark jobs for cost on AWS EMR"
```

---

## ❓ FAQ

### ¿Cuánto cuesta?

- **App:** Gratuita
- **OpenAI API:** ~$0.01-$0.05 por query
- **Estimado:** $2-5 por 100 queries

### ¿Mis datos son privados?

- **Upload mode:** Documentos NO se guardan (solo en memoria)
- **API calls:** Sujeto a política OpenAI
- **Recomendación:** No subir datos sensibles

### ¿Funciona offline?

- **No**, requiere Internet para OpenAI API
- **Alternativa:** Configurar modelos locales (avanzado)

### ¿Puedo agregar mis libros?

**Sí:**
```bash
cp mi_libro.txt data/
# Reiniciar app
```

### ¿Las respuestas son correctas?

- ✅ Fundamentadas en fuentes
- ⚠️ Puede "alucinar" sin info relevante
- **Siempre verifica información crítica**

### ¿Cuántos documentos simultáneos?

- **Pre-loaded:** 16 libros simultáneos
- **Upload:** 1 documento a la vez

---

## 🎯 Mejores Prácticas

### Escribir Queries Efectivas

✅ **Específico mejor que genérico**
✅ **Incluir contexto técnico**
✅ **Usar estructura clara:** "Compare X vs Y"
✅ **Pedir ejemplos de código** cuando sea relevante

### Exploración Iterativa

```
1. Query amplia → Panorama general
2. Query específica → Profundizar
3. Query práctica → Código/implementación
4. Query comparativa → Decisiones
```

### Gestionar Costos

✅ Queries específicas (respuesta en primer intento)
✅ Guardar resultados (evitar repetición)
✅ Usar GPT-3.5 para queries simples (cambiar en código)

---

## 📞 Recursos Adicionales

### Documentación

- **ARCHITECTURE.md:** Diseño del sistema
- **UPLOAD_GUIDE.md:** Guía detallada de upload
- **SETUP_INSTRUCTIONS.md:** Instalación completa
- **CHANGELOG.md:** Historial de cambios

### Enlaces Útiles

- **LangChain:** https://python.langchain.com/docs/
- **Streamlit:** https://docs.streamlit.io/
- **OpenAI API:** https://platform.openai.com/docs/

---

## 🚀 Próximas Funcionalidades

- [ ] Batch upload (múltiples documentos)
- [ ] Export a PDF/Markdown
- [ ] Historial de queries
- [ ] Modo offline con modelos locales
- [ ] Multi-language support
- [ ] API REST

---

**¡Feliz exploración técnica! 🧠📚🚀**
