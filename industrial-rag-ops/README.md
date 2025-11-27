# Industrial RAG Ops

Sistema de procesamiento y búsqueda semántica de documentos industriales para Vaca Muerta.

## Características

- **Procesamiento de documentos** con detección y enmascaramiento de información sensible (PII)
- **Fragmentación lógica** de documentos para una mejor recuperación
- **Búsqueda semántica** utilizando modelos de embeddings
- **API RESTful** con autenticación JWT
- **Monitoreo** con Prometheus y Grafana
- **Escalable** con Docker y Redis para caché
- **Seguridad** con autenticación y control de acceso basado en roles

## Requisitos

- Docker y Docker Compose
- Python 3.9+
- Redis (opcional, para producción)

## Instalación

### Usando Docker (Recomendado)

1. Clonar el repositorio:
   ```bash
   git clone [URL_DEL_REPOSITORIO]
   cd industrial-rag-ops
   ```

2. Copiar el archivo de configuración de ejemplo:
   ```bash
   cp .env.example .env
   ```

3. Editar el archivo `.env` según sea necesario

4. Construir y ejecutar los servicios:
   ```bash
   docker-compose up --build
   ```

5. La aplicación estará disponible en `http://localhost:8000`

### Instalación local

1. Crear un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Instalar el modelo de lenguaje en español para spaCy:
   ```bash
   python -m spacy download es_core_news_sm
   ```

4. Configurar las variables de entorno en `.env`

5. Ejecutar la aplicación:
   ```bash
   uvicorn src.main:app --reload
   ```

## Uso

### Autenticación

1. Obtener un token de acceso:
   ```bash
   curl -X 'POST' \
     'http://localhost:8000/api/v1/token' \
     -H 'accept: application/json' \
     -H 'Content-Type: application/x-www-form-urlencoded' \
     -d 'username=admin&password=admin'
   ```

2. Usar el token en las solicitudes:
   ```
   Authorization: Bearer <token>
   ```

### Subir un documento

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/documents/upload/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <token>' \
  -F 'file=@ruta/al/documento.txt' \
  -F 'metadata={"title":"Informe de inspección","document_type":"inspection_report","source":"Vaca Muerta"}'
```

### Buscar documentos

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/search/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <token>' \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "falla en válvula de seguridad",
    "limit": 5,
    "min_score": 0.5
  }'
```

### Monitoreo

- **Prometheus**: `http://localhost:9090`
- **Grafana**: `http://localhost:3000` (usuario: admin, contraseña: admin)
- **API Docs**: `http://localhost:8000/docs`

## Estructura del Proyecto

```
industrial-rag-ops/
├── data/                    # Datos de la aplicación
│   ├── raw/                 # Documentos sin procesar
│   ├── processed/           # Documentos procesados
│   └── indexed/             # Índices de búsqueda
├── deploy/                  # Configuraciones de despliegue
│   └── prometheus/          # Configuración de Prometheus
├── src/                     # Código fuente
│   ├── __init__.py          # Paquete Python
│   ├── main.py              # Aplicación FastAPI
│   ├── config.py            # Configuración
│   ├── models.py            # Modelos de datos
│   ├── processing.py        # Procesamiento de documentos
│   ├── vector_store.py      # Almacenamiento vectorial
│   ├── security.py          # Utilidades de seguridad
│   └── api.py              # Endpoints de la API
├── tests/                   # Pruebas
├── .env.example            # Variables de entorno de ejemplo
├── .gitignore
├── docker-compose.yml      # Configuración de Docker Compose
├── Dockerfile              # Configuración de Docker
└── README.md               # Este archivo
```

## Despliegue en Producción

1. Configurar un proxy inverso (Nginx, Traefik, etc.)
2. Configurar HTTPS con Let's Encrypt
3. Asegurar las variables de entorno sensibles
4. Configurar copias de seguridad para los volúmenes de datos

## Contribución

1. Hacer un fork del repositorio
2. Crear una rama para tu característica (`git checkout -b feature/nueva-funcionalidad`)
3. Hacer commit de tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Hacer push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
