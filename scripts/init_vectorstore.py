import os
import json
from pathlib import Path
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document

# Configuración
CHROMA_DB_DIR = "./chroma_db"
DATA_FILE = "./data/sample_profiles.json"

def flatten_metadata(metadata):
    """
    Convierte listas y objetos complejos a strings para ChromaDB
    ChromaDB solo acepta: str, int, float, bool
    """
    flattened = {}
    
    for key, value in metadata.items():
        if isinstance(value, list):
            # Convertir listas a strings separados por comas
            flattened[key] = ", ".join(str(v) for v in value)
        elif isinstance(value, dict):
            # Convertir diccionarios a JSON string
            flattened[key] = json.dumps(value)
        elif isinstance(value, (str, int, float, bool)):
            flattened[key] = value
        else:
            # Convertir otros tipos a string
            flattened[key] = str(value)
    
    return flattened

def create_profile_document(profile):
    """
    Crea un documento con texto optimizado para embeddings
    y metadata aplanada para ChromaDB
    """
    
    # Crear el contenido textual
    location = profile.get('location', {})
    city = location.get('city', 'Sin ciudad') if isinstance(location, dict) else 'Sin ciudad'
    distance = location.get('distance', 0) if isinstance(location, dict) else 0
    
    text = f"""
Profesional: {profile.get('name', 'Sin nombre')}
Cargo: {profile.get('title', 'Sin cargo')}
Ubicación: {city} ({distance} km del centro)

Habilidades técnicas: {', '.join(profile.get('skills', []))}
Experiencia: {profile.get('experience', 'Sin especificar')}
Certificaciones: {', '.join(profile.get('certifications', []))}

Modalidades de trabajo: {', '.join(profile.get('workMode', []))}
Disponibilidad: {profile.get('availability', 'Sin especificar')}
Salario esperado: {profile.get('salary', '0')} USD/mes

Rating: {profile.get('rating', 0)}/5.0

Descripción del perfil:
{profile.get('description', 'Sin descripción')}
    """.strip()
    
    # Aplanar la metadata
    metadata = flatten_metadata(profile)
    
    return Document(
        page_content=text,
        metadata=metadata
    )

def main():
    print("\n" + "="*60)
    print("🚀 Inicializando TalentHub Vector Store")
    print("="*60 + "\n")
    
    # 1. Verificar/crear directorio de ChromaDB
    print("📁 Creando directorios...")
    os.makedirs(CHROMA_DB_DIR, exist_ok=True)
    os.makedirs("./data", exist_ok=True)
    os.makedirs("./cache", exist_ok=True)
    print("✅ Directorios creados\n")
    
    # 2. Inicializar embeddings
    print("🤖 Cargando modelo de embeddings...")
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        print("✅ Modelo cargado\n")
    except Exception as e:
        print(f"❌ Error al cargar embeddings: {e}")
        return
    
    # 3. Crear/conectar vector store
    print("💾 Creando vector store...")
    try:
        vectorstore = Chroma(
            persist_directory=CHROMA_DB_DIR,
            embedding_function=embeddings,
            collection_name="talent_profiles"
        )
        print("✅ Vector store creado\n")
    except Exception as e:
        print(f"❌ Error al crear vector store: {e}")
        return
    
    # 4. Cargar perfiles
    print(f"📊 Cargando perfiles desde {DATA_FILE}...")
    
    if not os.path.exists(DATA_FILE):
        print(f"⚠️  Archivo no encontrado, creando perfiles de ejemplo...")
        
        sample_profiles = [
            {
                "id": 1,
                "name": "Ana García",
                "title": "Full Stack Developer",
                "skills": ["React", "Node.js", "Python", "PostgreSQL", "Docker"],
                "location": {"city": "Buenos Aires", "distance": 5},
                "workMode": ["Remoto", "Híbrido"],
                "experience": "5 años",
                "certifications": ["AWS Certified", "React Professional"],
                "description": "Desarrolladora full stack con experiencia en aplicaciones web escalables",
                "salary": "3500",
                "rating": 4.8,
                "availability": "Inmediata"
            },
            {
                "id": 2,
                "name": "Carlos Rodríguez",
                "title": "DevOps Engineer",
                "skills": ["Kubernetes", "Terraform", "AWS", "Jenkins", "Python"],
                "location": {"city": "Córdoba", "distance": 700},
                "workMode": ["Remoto"],
                "experience": "7 años",
                "certifications": ["CKA", "AWS Solutions Architect"],
                "description": "Especialista en infraestructura cloud y automatización",
                "salary": "4000",
                "rating": 4.9,
                "availability": "2 semanas"
            },
            {
                "id": 3,
                "name": "María López",
                "title": "Data Scientist",
                "skills": ["Python", "TensorFlow", "Pandas", "SQL", "Machine Learning"],
                "location": {"city": "Buenos Aires", "distance": 8},
                "workMode": ["Híbrido", "Presencial"],
                "experience": "4 años",
                "certifications": ["Google Data Analytics", "Deep Learning Specialization"],
                "description": "Científica de datos especializada en ML y análisis predictivo",
                "salary": "3800",
                "rating": 4.7,
                "availability": "Inmediata"
            }
        ]
        
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(sample_profiles, f, ensure_ascii=False, indent=2)
        
        profiles = sample_profiles
        print(f"✅ Creados {len(profiles)} perfiles de ejemplo\n")
    else:
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                profiles = json.load(f)
            print(f"✅ Cargados {len(profiles)} perfiles\n")
        except Exception as e:
            print(f"❌ Error al leer archivo: {e}")
            return
    
    # 5. Procesar e indexar
    print("🔧 Procesando y creando embeddings...")
    
    try:
        documents = []
        for i, profile in enumerate(profiles, 1):
            print(f"   Procesando {i}/{len(profiles)}: {profile.get('name', 'Sin nombre')}")
            doc = create_profile_document(profile)
            documents.append(doc)
        
        print(f"\n📥 Indexando {len(documents)} documentos...")
        vectorstore.add_documents(documents)
        vectorstore.persist()
        
        print("✅ Indexación completada\n")
        
    except Exception as e:
        print(f"❌ Error durante indexación: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 6. Verificar
    print("🔍 Verificando indexación...")
    try:
        count = vectorstore._collection.count()
        print(f"✅ Total de documentos: {count}\n")
        
        print("🧪 Búsqueda de prueba...")
        results = vectorstore.similarity_search("desarrollador Python", k=2)
        print(f"✅ Encontrados {len(results)} resultados\n")
        
        if results:
            print("📄 Primer resultado:")
            print(f"   Nombre: {results[0].metadata.get('name', 'N/A')}")
            print(f"   Título: {results[0].metadata.get('title', 'N/A')}")
        
    except Exception as e:
        print(f"⚠️  Error en verificación: {e}")
    
    print("\n" + "="*60)
    print("✅ Inicialización completada")
    print("="*60)
    print("\n💡 Ejecuta: python main.py\n")

if __name__ == "__main__":
    main()