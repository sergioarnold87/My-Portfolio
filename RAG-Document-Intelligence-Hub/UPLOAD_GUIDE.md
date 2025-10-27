# 📤 Guía de Upload Automático — RAG Demo

## 🎯 Descripción General

El sistema ahora soporta **dos modos de operación**:

1. **📤 Upload Document** — Sube tus propios documentos y realiza análisis automático
2. **📚 Pre-loaded Knowledge Base** — Usa documentos pre-cargados en el directorio `data/`

---

## 🚀 Flujo Automático de Procesamiento

Cuando subes un archivo, el sistema ejecuta automáticamente:

### 1️⃣ **Extracción de Texto**
- **TXT/MD**: Lectura directa
- **PDF**: Extracción con PyPDF2
- **CSV**: Conversión a texto estructurado con pandas

### 2️⃣ **Chunking Inteligente**
- Usa `RecursiveCharacterTextSplitter`
- Tamaño de chunk: **800 caracteres**
- Overlap: **100 caracteres**

### 3️⃣ **Generación de Embeddings**
- OpenAI Embeddings automáticos
- Almacenamiento en ChromaDB

### 4️⃣ **Retrieval Semántico**
- Top-k retrieval (k=3)
- QA Chain lista para consultas

### 5️⃣ **Respuestas con LLM**
- OpenAI GPT con temperatura 0.3
- Respuestas basadas en contexto recuperado

---

## 📁 Formatos Soportados

| Formato | Extensión | Método de Extracción |
|---------|-----------|---------------------|
| Texto   | `.txt`    | Lectura UTF-8       |
| Markdown| `.md`     | Lectura UTF-8       |
| PDF     | `.pdf`    | PyPDF2              |
| CSV     | `.csv`    | Pandas              |

---

## 🛠️ Uso del Sistema

### Modo 1: Upload Document

1. **Inicia la aplicación:**
   ```bash
   streamlit run app/main.py
   ```

2. **Selecciona "📤 Upload Document"** en la sidebar

3. **Arrastra o selecciona tu archivo** (txt, pdf, csv, md)

4. **Espera el procesamiento automático**
   - El sistema mostrará: `✅ Document processed successfully!`

5. **Haz tus preguntas** en el área de texto

6. **Click en "🔍 Analyze"** para obtener insights

### Modo 2: Pre-loaded Knowledge Base

1. **Selecciona "📚 Pre-loaded Knowledge Base"** en la sidebar

2. **El sistema carga automáticamente** todos los `.txt` del directorio `data/`

3. **Usa los modos predefinidos** o escribe tus propias consultas

4. **Click en "🚀 Run Discovery"**

---

## 🔧 Configuración de API

Asegúrate de tener tu OpenAI API key configurada:

```bash
# .env file
OPENAI_API_KEY=sk-...
```

---

## 📊 Ejemplos de Uso

### Ejemplo 1: Análisis de PDF Técnico
```
1. Upload: whitepaper.pdf
2. Query: "Summarize the main architectural components"
3. Get instant insights powered by RAG
```

### Ejemplo 2: CSV Data Exploration
```
1. Upload: sales_data.csv
2. Query: "What are the key trends in this dataset?"
3. Semantic analysis of tabular data
```

### Ejemplo 3: Markdown Documentation
```
1. Upload: project_docs.md
2. Query: "List all API endpoints mentioned"
3. Structured extraction from documentation
```

---

## 🎨 Mejoras Opcionales (Roadmap)

### ✅ Ya Implementado
- [x] Multi-format support (TXT, PDF, CSV, MD)
- [x] Automatic chunking
- [x] Embedding generation
- [x] Semantic retrieval
- [x] Dual mode (upload vs pre-loaded)

### 🔮 Próximas Mejoras
- [ ] **Batch Upload**: Múltiples archivos simultáneos
- [ ] **Metadata Extraction**: Autor, fecha, título
- [ ] **Cross-Encoder Re-Ranking**: Mejora de relevancia
- [ ] **Local LLM Support**: Ollama, Llama2
- [ ] **Export Results**: Download de insights en PDF/MD
- [ ] **Vector Persistence**: Guardar vectorstore para reutilización
- [ ] **Advanced Chunking**: Semantic chunking basado en tópicos

---

## 🐛 Troubleshooting

### Error: "No module named 'PyPDF2'"
```bash
pip install -r requirements.txt
```

### Error: "OpenAI API key not found"
```bash
# Verifica tu archivo .env
cat .env

# Debe contener:
OPENAI_API_KEY=sk-...
```

### Error: "No documents found in data/ directory"
```bash
# Asegúrate de tener archivos .txt en data/
ls data/*.txt
```

---

## 📞 Soporte

Para preguntas o mejoras, contacta al equipo de desarrollo o abre un issue en el repositorio.

**¡Happy RAG-ing! 🚀**
