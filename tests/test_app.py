import pytest
from pet_vet_api import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Agendar Consulta' in response.data

def test_veterinarios_endpoint(client):
    response = client.get('/veterinarios')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) > 0
    assert "nome" in data[0]
    assert "especialidade" in data[0]

def test_agendar_consulta(client):
    response = client.post('/agendar_consulta', json={"pet_id": 1, "veterinario_id": 1})
    assert response.status_code == 200
    assert b'Consulta agendada com sucesso!' in response.data
