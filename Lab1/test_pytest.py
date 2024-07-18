import requests
import pytest
import requests_mock

@pytest.fixture
def mock_response():
    with requests_mock.Mocker() as m:
        # Simulamos la respuesta para obtener todas las películas
        m.get('http://localhost:5000/peliculas', json=[
            {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
            {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'}
        ])

        # Simulamos la respuesta para agregar una nueva película
        m.post('http://localhost:5000/peliculas', status_code=201, json={'id': 3, 'titulo': 'Pelicula de prueba', 'genero': 'Acción'})

        # Simulamos la respuesta para obtener una pelicula para el próximo feriado
        genero = 'Ciencia ficción'
        m.get(f'http://localhost:5000/peliculas/feriado/{genero}', status_code=200, json={'fecha': '2024-09-12', 'motivo': 'Día del Programador', 'genero': 'Ciencia ficción', 'recomendacion': 'Interstellar'})

        # Simulamos la respuesta para obtener detalles de una película específica
        m.get('http://localhost:5000/peliculas/1', json={'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'})

        # Simulamos la respuesta para actualizar los detalles de una película
        m.put('http://localhost:5000/peliculas/1', status_code=200, json={'id': 1, 'titulo': 'Nuevo título', 'genero': 'Comedia'})

        # Simulamos la respuesta para eliminar una película
        m.delete('http://localhost:5000/peliculas/1', status_code=200)

        # Simulamos la respuesta para obtener todas las películas de un género específico
        genero = 'Ciencia ficción'
        m.get(f'http://localhost:5000/peliculas/{genero}', status_code=200, json=[
            {'id': 3, 'titulo': 'Interstellar', 'genero': 'Ciencia ficción'},
            {'id': 6, 'titulo': 'Back to the Future', 'genero': 'Ciencia ficción'},
            {'id': 9, 'titulo': 'Inception', 'genero': 'Ciencia ficción'},
        ])

        # Simulamos la respuesta para buscar películas por nombre
        nombre = 'Indian'
        m.get(f'http://localhost:5000/peliculas/buscar/{nombre}', status_code=404, json={'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'})

        # simulamos la respuesta para sugerir una pelicula aleatoria
        m.get('http://localhost:5000/peliculas/sugerir',status_code=200, json={'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'})

        # simulamos la respuesta para sugerir una pelicula aleatoria
        genero = 'Acción'
        m.get(f'http://localhost:5000/peliculas/sugerir/{genero}',status_code=200, json={'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'})

        yield m

def test_obtener_peliculas(mock_response):
    response = requests.get('http://localhost:5000/peliculas')
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_agregar_pelicula(mock_response):
    nueva_pelicula = {'titulo': 'Pelicula de prueba', 'genero': 'Acción'}
    response = requests.post('http://localhost:5000/peliculas', json=nueva_pelicula)
    assert response.status_code == 201
    assert response.json()['id'] == 3

def test_busqueda_por_proximo_feriado(mock_response):
    genero = 'Ciencia ficción'
    response = requests.get(f'http://localhost:5000/peliculas/feriado/{genero}')
    assert response.status_code == 200
    assert response.json()['genero'] == 'Ciencia ficción'

def test_obtener_pelicula(mock_response):
    response = requests.get('http://localhost:5000/peliculas/1')
    assert response.status_code == 200
    assert response.json()['titulo'] == 'Indiana Jones'

def test_actualizar_pelicula(mock_response):
    datos_actualizados = {'titulo': 'Nuevo título', 'genero': 'Comedia'}
    response = requests.put('http://localhost:5000/peliculas/1', json=datos_actualizados)
    assert response.status_code == 200
    assert response.json()['titulo'] == 'Nuevo título'

def test_eliminar_pelicula(mock_response):
    response = requests.delete('http://localhost:5000/peliculas/1')
    assert response.status_code == 200

def test_busqueda_por_genero(mock_response):
    genero = 'Ciencia ficción'
    response = requests.get(f'http://localhost:5000/peliculas/{genero}')
    assert response.status_code == 200
    assert len(response.json()) == 3

def test_busqueda_por_nombre(mock_response):
    nombre = 'Indian'
    response = requests.get(f'http://localhost:5000/peliculas/buscar/{nombre}')
    assert response.status_code == 404

def test_sugerir_pelicula(mock_response):
    response = requests.get('http://localhost:5000/peliculas/sugerir')
    assert response.status_code == 200
    assert 'id' in response.json()  # Ensure the response contains the expected keys
    assert 'titulo' in response.json()
    assert 'genero' in response.json()

def test_sugerir_por_genero(mock_response):
    genero = 'Acción'
    response = requests.get(f'http://localhost:5000/peliculas/sugerir/{genero}')
    
    assert response.status_code == 200
    assert 'id' in response.json()  
    assert 'titulo' in response.json()
    assert 'genero' in response.json()
    
    genero_sugerido = response.json()['genero']  
    assert genero_sugerido == genero 


