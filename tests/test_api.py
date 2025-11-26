"""
Tests para los endpoints de la API
"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Añadir directorio raíz al path
sys.path.append(str(Path(__file__).parent.parent))

from main import app

client = TestClient(app)

def test_root():
    """Test del endpoint raíz"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert data["service"] == "TalentHub RAG API"
    assert data["status"] == "online"

def test_rag_search_basic():
    """Test de búsqueda básica"""
    response = client.post(
        "/api/rag/search",
        json={
            "query": "desarrollador Python",
            "top_k": 3
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "professionals" in data
    assert "query" in data
    assert isinstance(data["professionals"], list)

def test_rag_search_with_filters():
    """Test de búsqueda con filtros"""
    response = client.post(
        "/api/rag/search",
        json={
            "query": "desarrollador remoto",
            "filters": {
                "workMode": ["Remoto"],
                "maxDistance": 10
            },
            "top_k": 5
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["professionals"]) <= 5

def test_profile_index():
    """Test de indexación de perfil"""
    profile = {
        "id": 999,
        "name": "Test User",
        "title": "Test Developer",
        "skills": ["Python", "Testing"],
        "location": {
            "city": "Test City",
            "distance": 5
        },
        "workMode": ["Remoto"],
        "experience": "3 años",
        "certifications": ["Test Cert"],
        "description": "Test profile for testing",
        "salary": "3000",
        "rating": 4.5,
        "availability": "Inmediata"
    }
    
    response = client.post("/api/profiles/index", json=profile)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "profile_id" in data

def test_stats():
    """Test del endpoint de estadísticas"""
    response = client.get("/api/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_profiles" in data
    assert "cache_size" in data
    assert "system_status" in data

def test_clear_cache():
    """Test de limpieza de caché"""
    response = client.delete("/api/cache/clear")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"

def test_invalid_query():
    """Test con query vacía"""
    response = client.post(
        "/api/rag/search",
        json={
            "query": "",
            "top_k": 5
        }
    )
    # Debería manejar queries vacías correctamente
    assert response.status_code in [200, 400]

def test_large_top_k():
    """Test con top_k muy grande"""
    response = client.post(
        "/api/rag/search",
        json={
            "query": "desarrollador",
            "top_k": 100
        }
    )
    assert response.status_code == 200
    data = response.json()
    # No debería devolver más perfiles de los que existen
    assert len(data["professionals"]) <= 100

def test_batch_indexing():
    """Test de indexación por lotes"""
    profiles = [
        {
            "id": 1000 + i,
            "name": f"Test User {i}",
            "title": "Test Developer",
            "skills": ["Python"],
            "location": {"city": "Test City", "distance": 5},
            "workMode": ["Remoto"],
            "experience": "3 años",
            "certifications": [],
            "description": "Test profile",
            "salary": "3000",
            "rating": 4.5,
            "availability": "Inmediata"
        }
        for i in range(3)
    ]
    
    response = client.post("/api/profiles/index-batch", json=profiles)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "3 perfiles" in data["message"]