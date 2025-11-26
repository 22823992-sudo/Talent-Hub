# 🎯 TalentHub RAG API

Sistema de búsqueda inteligente de profesionales utilizando **Retrieval-Augmented Generation (RAG)** con embeddings vectoriales y re-ranking semántico.

## 🌟 Características

- ✨ **Búsqueda Vectorial**: Utiliza embeddings de última generación para búsquedas semánticas
- 🎯 **Re-ranking Inteligente**: CrossEncoder para mejorar la relevancia de resultados
- ⚡ **Alto Rendimiento**: Sistema de caché para respuestas rápidas
- 🔍 **Filtros Avanzados**: Por habilidades, ubicación, modalidad de trabajo, etc.
- 📊 **Sin LLM Externo**: Respuestas estructuradas sin dependencia de APIs externas
- 🚀 **Escalable**: Indexación por lotes y persistencia en ChromaDB

## 🏗️ Arquitectura
```
┌─────────────┐
│   Cliente   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│     FastAPI Backend             │
│  ┌───────────────────────────┐  │
│  │  Endpoint de Búsqueda     │  │
│  └───────────┬───────────────┘  │
│              │                   │
│              ▼                   │
│  ┌───────────────────────────┐  │
│  │   Sistema de Caché        │  │
│  └───────────┬───────────────┘  │
│              │                   │
│              ▼                   │
│  ┌───────────────────────────┐  │
│  │  Búsqueda Vectorial       │  │
│  │  (HuggingFace Embeddings) │  │
│  └───────────┬───────────────┘  │
│              │                   │
│              ▼                   │
│  ┌───────────────────────────┐  │
│  │   Filtros Post-Búsqueda   │  │
│  └───────────┬───────────────┘  │
│              │                   │
│              ▼                   │
│  ┌───────────────────────────┐  │
│  │  Re-ranking (CrossEncoder)│  │
│  └───────────┬───────────────┘  │
│              │                   │
│              ▼                   │
│  ┌───────────────────────────┐  │
│  │   ChromaDB Vector Store   │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

## 📋 Requisitos

- Python 3.8+
- 4GB RAM mínimo (8GB recomendado)
- 2GB de espacio en disco

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/talenthub-rag-api.git
cd talenthub-rag-api
```

### 2. Crear entorno virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Inicializar la base de datos vectorial
```bash
python scripts/init_vectorstore.py
```

## 🎮 Uso

### Iniciar el servidor
```bash
python main.py
```

El servidor estará disponible en:
- **API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **Redoc**: http://localhost:8000/redoc

### Endpoints Principales

#### 1. Búsqueda RAG
```bash
POST /api/rag/search
```

**Request:**
```json
{
  "query": "desarrollador Python con experiencia en machine learning",
  "filters": {
    "skills": ["Python", "Machine Learning"],
    "maxDistance": 10,
    "workMode": ["Remoto", "Híbrido"]
  },
  "top_k": 5
}
```

**Response:**
```json
{
  "response": "🎯 Encontré 5 profesionales relevantes...",
  "professionals": [
    {
      "id": 1,
      "name": "Juan Pérez",
      "title": "Senior Python Developer",
      "skills": ["Python", "TensorFlow", "Docker"],
      "location": {
        "city": "Buenos Aires",
        "distance": 5
      },
      "rating": 4.8,
      "salary": "3500",
      "availability": "Inmediata"
    }
  ],
  "query": "desarrollador Python...",
  "cached": false
}
```

#### 2. Indexar Perfil
```bash
POST /api/profiles/index
```

#### 3. Indexación por Lotes
```bash
POST /api/profiles/index-batch
```

#### 4. Limpiar Caché
```bash
DELETE /api/cache/clear
```

#### 5. Estadísticas
```bash
GET /api/stats
```

## 🔧 Configuración

Crea un archivo `.env` en la raíz del proyecto:
```env
HOST=0.0.0.0
PORT=8000
CHROMA_DB_DIR=./chroma_db
CACHE_DIR=./cache
```

## 📊 Estructura del Proyecto
```
talenthub-rag-api/
│
├── main.py                 
├── requirements.txt        
├── .env                    
├── .gitignore             
├── README.md              
│
├── scripts/
│   ├── __init__.py
│   └── init_vectorstore.py    
│
├── data/
│   └── sample_profiles.json   
│
├── chroma_db/             
├── cache/                 
│
└── tests/
    ├── __init__.py
    └── test_api.py
```

## 🧪 Testing
```bash
pytest
```

## 📈 Rendimiento

| Métrica | Valor |
|---------|-------|
| Tiempo de búsqueda (sin caché) | ~200-500ms |
| Tiempo de búsqueda (con caché) | ~10-20ms |

## 🤝 Contribuir

Ver [CONTRIBUTING.md](CONTRIBUTING.md)

## 📝 Licencia

MIT License - Ver [LICENSE](LICENSE)

## 👥 Autores

Tu Nombre - [@tu-usuario](https://github.com/tu-usuario)

---

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub!