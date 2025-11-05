# tests/test_companies.py
from fastapi.testclient import TestClient

# El fixture `client` viene de conftest.py


def test_create_company_ok(client: TestClient):
    payload = {
        "name": "Empresa Test SA",
        "razon_social": "Empresa Test SA",
        "rut": "11.111.111-1",
        "giro": "Servicios TI",
        "direccion": "Calle Falsa 123",
        "ciudad": "Santiago",
        "telefono": "+56 9 1234 5678",
        "email": "test@example.com",
    }

    # Ajusta la ruta si tu router tiene otro prefix (ej: "/api/companies")
    response = client.post("/companies", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["id"] is not None
    assert data["name"] == payload["name"]
    assert data["rut"] == payload["rut"]
    assert data["email"] == payload["email"]


def test_create_company_duplicate(client: TestClient):
    payload = {
        "name": "Empresa Duplicada",
        "razon_social": "Empresa Duplicada",
        "rut": "22.222.222-2",
        "giro": "Servicios",
        "direccion": "Otra calle 456",
        "ciudad": "Santiago",
        "telefono": "+56 9 8765 4321",
        "email": "duplicate@example.com",
    }

    # Primera vez: debe crear OK
    resp1 = client.post("/companies", json=payload)
    assert resp1.status_code == 200

    # Segunda vez con los mismos datos: debe fallar por "Company already exists"
    resp2 = client.post("/companies", json=payload)
    assert resp2.status_code == 400
    assert resp2.json()["detail"] == "Company already exists"

def test_get_company_by_id(client: TestClient):
    # Primero, creamos una empresa para obtener su ID
    payload = {
        "name": "Empresa Consulta SA",
        "razon_social": "Empresa Consulta SA",
        "rut": "33.333.333-3",
        "giro": "Comercio",
        "direccion": "Calle Consulta 789",
        "ciudad": "Valparaíso",
        "telefono": "+56 9 1122 3344",
        "email": "p@p.cl",
    }   
    create_resp = client.post("/companies", json=payload)
    assert create_resp.status_code == 200   
    company_id = create_resp.json()["id"]
    # Ahora, consultamos la empresa por ID
    get_resp = client.get(f"/companies/{company_id}")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["id"] == company_id
    assert data["name"] == payload["name"]
    assert data["rut"] == payload["rut"]

def test_get_companies_by_city(client: TestClient):
    # Creamos varias empresas en diferentes ciudades
    companies = [
        {
            "name": "Empresa A",
            "razon_social": "Empresa A",
            "rut": "44.444.444-4",
            "giro": "Servicios",
            "direccion": "Calle A 1",
            "ciudad": "Santiago",
            "telefono": "+56 9 0000 1111",
            "email": "p@t.cl",
        }, 
        {
            "name": "Empresa B",
            "razon_social": "Empresa B",
            "rut": "55.555.555-5",
            "giro": "Comercio",
            "direccion": "Calle B 2",
            "ciudad": "Valparaíso",
            "telefono": "+56 9 2222 3333",
            "email": "o@ocl.cl|",
        }
    ]
    for comp in companies:
        resp = client.post("/companies", json=comp)
        assert resp.status_code == 200  
    # Ahora, consultamos empresas en Santiago
    get_resp = client.get("/companies/by-city/Santiago")    
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert len(data) >= 1
    for company in data:
        assert "Santiago" in company["ciudad"]

def test_create_companies_bulk(client: TestClient):
    payload = [
        {
            "name": "Empresa Bulk 1",
            "razon_social": "Empresa Bulk 1",
            "rut": "66.666.666-6",
            "giro": "Servicios",
            "direccion": "Calle Bulk 1",
            "ciudad": "Concepción",
            "telefono": "+56 9 4444 5555",
            "email": "o@j.cl",
        },
        {
            "name": "Empresa Bulk 2",
            "razon_social": "Empresa Bulk 2",
            "rut": "77.777.777-7",
            "giro": "Comercio",
            "direccion": "Calle Bulk 2",
            "ciudad": "La Serena",
            "telefono": "+56 9 6666 7777",
            "email": "ji@ji.cl"
        }
    ]
    response = client.post("/companies/bulk", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    for i in range(2):
        assert data[i]["name"] == payload[i]["name"]
        assert data[i]["rut"] == payload[i]["rut"]
        assert data[i]["email"] == payload[i]["email"]    
    
