import requests
import json

API_BASE = "http://localhost:8000"

# Datos de prueba - 5 profesionales
profiles = [
    {
        "id": 1,
        "name": "María González",
        "title": "Desarrolladora Full Stack Senior",
        "skills": ["React", "FastAPI", "Python", "TypeScript", "PostgreSQL", "Docker"],
        "location": {
            "city": "Palermo",
            "distance": 5,
            "lat": -34.5889,
            "lng": -58.4199
        },
        "workMode": ["Remoto", "Híbrido"],
        "experience": "8 años en desarrollo web",
        "certifications": ["AWS Certified Solutions Architect", "Scrum Master"],
        "description": "Experta en desarrollo web moderno con enfoque en arquitecturas escalables y microservicios.",
        "salary": "5000",
        "rating": 4.8,
        "availability": "Inmediata"
    },
    {
        "id": 2,
        "name": "Juan Pérez",
        "title": "Data Scientist",
        "skills": ["Python", "Machine Learning", "TensorFlow", "SQL", "Docker", "Spark"],
        "location": {
            "city": "Recoleta",
            "distance": 3,
            "lat": -34.5875,
            "lng": -58.3964
        },
        "workMode": ["Remoto"],
        "experience": "5 años en análisis de datos",
        "certifications": ["Google ML Engineer", "Data Science Specialization"],
        "description": "Especialista en modelos predictivos y análisis de datos complejos.",
        "salary": "4500",
        "rating": 4.9,
        "availability": "2 semanas"
    },
    {
        "id": 3,
        "name": "Laura Martínez",
        "title": "Diseñadora UX/UI Senior",
        "skills": ["Figma", "Adobe XD", "User Research", "Prototyping", "Design Systems"],
        "location": {
            "city": "Belgrano",
            "distance": 8,
            "lat": -34.5625,
            "lng": -58.4575
        },
        "workMode": ["Híbrido", "Presencial"],
        "experience": "6 años en diseño digital",
        "certifications": ["Nielsen Norman Group UX Certified", "Google UX Design"],
        "description": "Creadora de experiencias digitales centradas en el usuario.",
        "salary": "3500",
        "rating": 4.7,
        "availability": "Inmediata"
    },
    {
        "id": 4,
        "name": "Carlos Rodríguez",
        "title": "DevOps Engineer",
        "skills": ["AWS", "Kubernetes", "Terraform", "CI/CD", "Python", "Ansible"],
        "location": {
            "city": "San Telmo",
            "distance": 2,
            "lat": -34.6210,
            "lng": -58.3726
        },
        "workMode": ["Remoto", "Híbrido"],
        "experience": "7 años en infraestructura cloud",
        "certifications": ["AWS DevOps Professional", "Kubernetes CKA"],
        "description": "Experto en automatización y orquestación de infraestructura.",
        "salary": "6000",
        "rating": 4.9,
        "availability": "1 mes"
    },
    {
        "id": 5,
        "name": "Ana Silva",
        "title": "Product Manager",
        "skills": ["Product Strategy", "Agile", "Data Analysis", "User Stories", "SQL"],
        "location": {
            "city": "Caballito",
            "distance": 6,
            "lat": -34.6158,
            "lng": -58.4392
        },
        "workMode": ["Híbrido"],
        "experience": "9 años gestionando productos digitales",
        "certifications": ["Certified Scrum Product Owner", "Product Management Certification"],
        "description": "Product Manager con track record de lanzar productos exitosos.",
        "salary": "5500",
        "rating": 4.8,
        "availability": "Inmediata"
    }
]

print("🚀 Iniciando indexación de perfiles...\n")

try:
    response = requests.post(
        f"{API_BASE}/api/profiles/index-batch",
        json=profiles,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        result = response.json()
        print("✅ ÉXITO!")
        print(f"📊 {result['message']}")
        print(f"\n💾 Perfiles indexados:")
        for i, profile in enumerate(profiles, 1):
            print(f"  {i}. {profile['name']} - {profile['title']}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)

except requests.exceptions.ConnectionError:
    print("❌ ERROR: No se pudo conectar al backend")
    print("   Asegúrate de que el servidor esté corriendo en http://localhost:8000")
except Exception as e:
    print(f"❌ Error inesperado: {e}")