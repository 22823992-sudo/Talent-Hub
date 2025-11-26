"""
Script de inicialización de la base de datos vectorial
Crea la estructura necesaria y carga perfiles de ejemplo
"""

import os
import sys
import json
from pathlib import Path

# Añadir el directorio raíz al path
sys.path.append(str(Path(__file__).parent.parent))

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document

# Configuración
CHROMA_DB_DIR = "./chroma_db"
SAMPLE_DATA_FILE = "./data/sample_profiles.json"

def create_profile_document(profile: dict) -> str:
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

def init_vectorstore():
    """Inicializa la base de datos vectorial"""
    
    print("🚀 Inicializando TalentHub Vector Store...")
    print("-" * 50)
    
    # 1. Crear directorios
    print("📁 Creando directorios...")
    os.makedirs(CHROMA_DB_DIR, exist_ok=True)
    os.makedirs("./cache", exist_ok=True)
    os.makedirs("./data", exist_ok=True)
    print("✅ Directorios creados")
    
    # 2. Inicializar embeddings
    print("\n🤖 Cargando modelo de embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    print("✅ Modelo cargado")
    
    # 3. Crear vector store
    print("\n💾 Creando vector store...")
    vectorstore = Chroma(
        persist_directory=CHROMA_DB_DIR,
        embedding_function=embeddings,
        collection_name="talent_profiles"
    )
    print("✅ Vector store creado")
    
    # 4. Cargar datos de ejemplo
    if os.path.exists(SAMPLE_DATA_FILE):
        print(f"\n📊 Cargando perfiles de ejemplo desde {SAMPLE_DATA_FILE}...")
        
        with open(SAMPLE_DATA_FILE, 'r', encoding='utf-8') as f:
            profiles = json.load(f)
        
        documents = []
        for profile in profiles:
            text = create_profile_document(profile)
            doc = Document(
                page_content=text,
                metadata=profile
            )
            documents.append(doc)
        
        vectorstore.add_documents(documents)
        vectorstore.persist()
        
        print(f"✅ {len(profiles)} perfiles indexados correctamente")
    else:
        print(f"\n⚠️  Archivo de ejemplo no encontrado: {SAMPLE_DATA_FILE}")
        print("💡 Puedes crear perfiles usando el endpoint /api/profiles/index")
    
    # 5. Verificar
    count = vectorstore._collection.count()
    print("\n" + "=" * 50)
    print(f"✅ Inicialización completada")
    print(f"📊 Total de perfiles en la base: {count}")
    print("🎯 Sistema listo para usar")
    print("=" * 50)

if __name__ == "__main__":
    try:
        init_vectorstore()
    except Exception as e:
        print(f"\n❌ Error durante la inicialización: {e}")
        sys.exit(1)