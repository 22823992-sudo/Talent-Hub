# backend/main.py
"""
TalentHub RAG API - Versión Optimizada
Sistema de búsqueda vectorial sin dependencia de LLM
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import os
from functools import lru_cache
import hashlib
import json

# Imports para RAG
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from sentence_transformers import CrossEncoder

# ==================== CONFIGURACIÓN ====================

app = FastAPI(title="TalentHub RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CHROMA_DB_DIR = "./chroma_db"
CACHE_DIR = "./cache"

# ==================== MODELOS ====================

class QueryRequest(BaseModel):
    query: str
    filters: Optional[Dict] = {}
    top_k: int = 5

class QueryResponse(BaseModel):
    response: str
    professionals: List[Dict]
    query: str
    cached: bool = False

class ProfileIndexRequest(BaseModel):
    id: int
    name: str
    title: str
    skills: List[str]
    location: Dict
    workMode: List[str]
    experience: str
    certifications: List[str]
    description: str
    salary: str
    rating: float
    availability: str

# ==================== INICIALIZACIÓN ====================

print("🚀 Inicializando sistema RAG...")

# 1. EMBEDDINGS
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'}
)

# 2. VECTOR STORE
vectorstore = Chroma(
    persist_directory=CHROMA_DB_DIR,
    embedding_function=embeddings,
    collection_name="talent_profiles"
)

# 3. RE-RANKER
try:
    reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    print("✅ Re-ranker cargado")
except Exception as e:
    print(f"⚠️ Re-ranker no disponible: {e}")
    reranker = None

print("✅ Sistema RAG inicializado\n")

# ==================== FUNCIONES AUXILIARES ====================

# ==================== FUNCIONES AUXILIARES ====================

def flatten_metadata(metadata):
    """Convierte metadata compleja a tipos simples para ChromaDB"""
    flattened = {}
    for key, value in metadata.items():
        if isinstance(value, list):
            flattened[key] = ", ".join(str(v) for v in value)
        elif isinstance(value, dict):
            flattened[key] = json.dumps(value)
        elif isinstance(value, (str, int, float, bool)):
            flattened[key] = value
        else:
            flattened[key] = str(value)
    return flattened

def parse_metadata(metadata):
    """Convierte metadata de vuelta a su forma original"""
    parsed = {}
    for key, value in metadata.items():
        if key in ['skills', 'workMode', 'certifications']:
            # Convertir strings separados por coma de vuelta a listas
            parsed[key] = [v.strip() for v in value.split(',') if v.strip()]
        elif key == 'location':
            # Parsear JSON de location
            try:
                parsed[key] = json.loads(value) if isinstance(value, str) else value
            except:
                parsed[key] = value
        else:
            parsed[key] = value
    return parsed

def create_profile_document(profile: Dict) -> str:
    """Convierte perfil en texto optimizado para embeddings"""
    text = f"""
    Profesional: {profile['name']}
    Cargo: {profile['title']}
    Ubicación: {profile['location']['city']} ({profile['location']['distance']} km del centro)
    
    Habilidades técnicas: {', '.join(profile['skills'])}
    Experiencia: {profile['experience']}
    Certificaciones: {', '.join(profile['certifications'])}
    
    Modalidades de trabajo: {', '.join(profile['workMode'])}
    Disponibilidad: {profile['availability']}
    Salario esperado: {profile['salary']} USD/mes
    
    Rating: {profile['rating']}/5.0
    
    Descripción del perfil:
    {profile['description']}
    """
    return text.strip()

def apply_filters(docs: List[Document], filters: Dict) -> List[Document]:
    """Aplica filtros post-búsqueda"""
    if not filters:
        return docs
    
    filtered = []
    for doc in docs:
        metadata = doc.metadata
        
        if 'skills' in filters and filters['skills']:
            if not any(skill in metadata.get('skills', []) for skill in filters['skills']):
                continue
        
        if 'maxDistance' in filters:
            if metadata.get('location', {}).get('distance', 999) > filters['maxDistance']:
                continue
        
        if 'workMode' in filters and filters['workMode']:
            if not any(mode in metadata.get('workMode', []) for mode in filters['workMode']):
                continue
        
        filtered.append(doc)
    
    return filtered

def rerank_documents(query: str, docs: List[Document]) -> List[Document]:
    """Re-rankea documentos usando cross-encoder"""
    if not reranker or not docs:
        return docs
    
    try:
        pairs = [[query, doc.page_content] for doc in docs]
        scores = reranker.predict(pairs)
        ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
        return [doc for doc, score in ranked]
    except Exception as e:
        print(f"⚠️ Error en re-ranking: {e}")
        return docs
    
def generate_response(query: str, docs: List[Document]) -> str:
    """Genera respuesta estructurada sin LLM"""
    if not docs:
        return "No encontré profesionales que coincidan exactamente con tu búsqueda. Intenta con otros criterios."
    
    response = f"🎯 Encontré {len(docs)} profesionales relevantes para: '{query}'\n\n"
    
    for i, doc in enumerate(docs, 1):
        # Parsear metadata primero
        prof = parse_metadata(doc.metadata)
        
        # Extraer location de forma segura
        location = prof.get('location', {})
        city = location.get('city', 'Sin ciudad') if isinstance(location, dict) else 'Sin ciudad'
        distance = location.get('distance', 0) if isinstance(location, dict) else 0
        
        # Extraer skills de forma segura
        skills = prof.get('skills', [])
        skills_str = ', '.join(skills[:5]) if isinstance(skills, list) else str(skills)
        
        # Extraer workMode de forma segura
        work_mode = prof.get('workMode', [])
        work_mode_str = ', '.join(work_mode) if isinstance(work_mode, list) else str(work_mode)
        
        response += f"{'='*60}\n"
        response += f"{i}. {prof.get('name', 'Sin nombre')} - {prof.get('title', 'Sin título')}\n"
        response += f"   📍 Ubicación: {city} ({distance} km)\n"
        response += f"   💼 Experiencia: {prof.get('experience', 'N/A')}\n"
        response += f"   ⭐ Rating: {prof.get('rating', 0)}/5.0\n"
        response += f"   🔧 Skills principales: {skills_str}\n"
        response += f"   💰 Salario: ${prof.get('salary', '0')}/mes\n"
        response += f"   📅 Disponibilidad: {prof.get('availability', 'N/A')}\n"
        response += f"   🏢 Modalidad: {work_mode_str}\n\n"
    
    return response

def get_cache_key(query: str, filters: Dict) -> str:
    """Genera key única para caché"""
    cache_data = f"{query}_{json.dumps(filters, sort_keys=True)}"
    return hashlib.md5(cache_data.encode()).hexdigest()

# ==================== ENDPOINTS ====================

@app.get("/")
async def root():
    return {
        "service": "TalentHub RAG API",
        "status": "online",
        "version": "optimized",
        "vectorstore_count": vectorstore._collection.count()
    }

@app.post("/api/rag/search", response_model=QueryResponse)
async def rag_search(request: QueryRequest):
    """
    Endpoint principal de búsqueda RAG
    """
    try:
        # Verificar caché
        cache_key = get_cache_key(request.query, request.filters)
        cache_file = f"{CACHE_DIR}/{cache_key}.json"
        
        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                cached_response = json.load(f)
                cached_response['cached'] = True
                return QueryResponse(**cached_response)
        
        # Búsqueda vectorial
        docs = vectorstore.similarity_search(
            request.query,
            k=request.top_k * 2
        )
        
        # Aplicar filtros
        docs = apply_filters(docs, request.filters)
        
        # Re-ranking
        docs = rerank_documents(request.query, docs)
        
        # Limitar a top_k
        docs = docs[:request.top_k]
        
        # Generar respuesta
        response_text = generate_response(request.query, docs)
        
        # Extraer profesionales
        professionals = [doc.metadata for doc in docs]
        
        # Preparar respuesta
        response_data = {
            "response": response_text,
            "professionals": professionals,
            "query": request.query,
            "cached": False
        }
        
        # Guardar en caché
        os.makedirs(CACHE_DIR, exist_ok=True)
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(response_data, f, ensure_ascii=False, indent=2)
        
        return QueryResponse(**response_data)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en búsqueda RAG: {str(e)}")

@app.post("/api/profiles/index")
async def index_profile(profile: ProfileIndexRequest):
    """Indexa un nuevo perfil"""
    try:
        profile_dict = profile.dict()
        text = create_profile_document(profile_dict)
        
        doc = Document(
            page_content=text,
            metadata=flatten_metadata(profile_dict) 
        )
        
        vectorstore.add_documents([doc])
        vectorstore.persist()
        
        return {
            "status": "success",
            "message": f"Perfil de {profile.name} indexado correctamente",
            "profile_id": profile.id
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al indexar perfil: {str(e)}")

@app.post("/api/profiles/index-batch")
async def index_profiles_batch(profiles: List[ProfileIndexRequest]):
    """Indexa múltiples perfiles"""
    try:
        documents = []
        for profile in profiles:
            profile_dict = profile.dict()
            text = create_profile_document(profile_dict)
            doc = Document(page_content=text, metadata=flatten_metadata(profile_dict))
            documents.append(doc)
        
        vectorstore.add_documents(documents)
        vectorstore.persist()
        
        return {
            "status": "success",
            "message": f"{len(profiles)} perfiles indexados correctamente"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al indexar perfiles: {str(e)}")

@app.delete("/api/cache/clear")
async def clear_cache():
    """Limpia el caché"""
    try:
        if os.path.exists(CACHE_DIR):
            for file in os.listdir(CACHE_DIR):
                os.remove(os.path.join(CACHE_DIR, file))
        
        return {"status": "success", "message": "Caché limpiado"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_stats():
    """Estadísticas del sistema"""
    return {
        "total_profiles": vectorstore._collection.count(),
        "cache_size": len(os.listdir(CACHE_DIR)) if os.path.exists(CACHE_DIR) else 0,
        "system_status": "optimized - no LLM required"
    }

# ==================== INICIO ====================

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*50)
    print("🚀 TalentHub RAG Backend - OPTIMIZADO")
    print("="*50)
    print(f"📊 Perfiles indexados: {vectorstore._collection.count()}")
    print(f"🎯 Re-ranker: {'✅ Disponible' if reranker else '❌ No configurado'}")
    print(f"⚡ Modo: Búsqueda vectorial pura (sin LLM)")
    print("\n📡 Servidor iniciando en http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("="*50 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)