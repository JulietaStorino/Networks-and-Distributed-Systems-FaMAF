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

        # Simulamos la respuesta para obtener todas las películas de un género específico
        genero = 'Acción'
        m.get(f'http://localhost:5000/peliculas/{genero}', status_code=200, json=[
            {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
            {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'},
            {'id': 5, 'titulo': 'The Avengers', 'genero': 'Acción'},
            {'id': 8, 'titulo': 'The Dark Knight', 'genero': 'Acción'},
        ])

        # Simulamos la respuesta para buscar películas por nombre
        nombre = 'Indian'
        m.get(f'http://localhost:5000/peliculas/buscar/{nombre}', status_code=404, json={'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'})

        # Simulamos la respuesta para agregar una nueva película
        m.post('http://localhost:5000/peliculas', status_code=201, json={'id': 3, 'titulo': 'Pelicula de prueba', 'genero': 'Acción'})

        # Simulamos la respuesta para obtener detalles de una película específica
        m.get('http://localhost:5000/peliculas/1', json={'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'})

        # Simulamos la respuesta para actualizar los detalles de una película
        m.put('http://localhost:5000/peliculas/1', status_code=200, json={'id': 1, 'titulo': 'Nuevo título', 'genero': 'Comedia'})

        # simulamos la respuesta para sugerir una pelicula aleatoria
        m.get('http://localhost:5000/peliculas/sugerir',status_code=200, json={'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'})

        # simulamos la respuesta para sugerir una pelicula aleatoria
        m.get('http://localhost:5000/peliculas/sugerir/Acción',status_code=200, json={'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'})

        # Simulamos la respuesta para eliminar una película
        m.delete('http://localhost:5000/peliculas/1', status_code=200)

        yield m

def test_obtener_peliculas(mock_response):
    response = requests.get('http://localhost:5000/peliculas')
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_obtener_peliculas_por_genero(mock_response):
    genero = 'Acción'
    response = requests.get(f'http://localhost:5000/peliculas/{genero}')
    assert response.status_code == 200
    assert len(response.json()) == 4

def test_buscar_pelicula_por_nombre(mock_response):
    nombre = 'Indian'
    response = requests.get(f'http://localhost:5000/peliculas/buscar/{nombre}')
    assert response.status_code == 404

def test_agregar_pelicula(mock_response):
    nueva_pelicula = {'titulo': 'Pelicula de prueba', 'genero': 'Acción'}
    response = requests.post('http://localhost:5000/peliculas', json=nueva_pelicula)
    assert response.status_code == 201
    assert response.json()['id'] == 3

def test_obtener_detalle_pelicula(mock_response):
    response = requests.get('http://localhost:5000/peliculas/1')
    assert response.status_code == 200
    assert response.json()['titulo'] == 'Indiana Jones'

def test_actualizar_detalle_pelicula(mock_response):
    datos_actualizados = {'titulo': 'Nuevo título', 'genero': 'Comedia'}
    response = requests.put('http://localhost:5000/peliculas/1', json=datos_actualizados)
    assert response.status_code == 200
    assert response.json()['titulo'] == 'Nuevo título'

def test_sugerir(mock_response):
    response = requests.get('http://localhost:5000/peliculas/sugerir')
    assert response.status_code == 200
    assert 'id' in response.json()  # Ensure the response contains the expected keys
    assert 'titulo' in response.json()
    assert 'genero' in response.json()

def test_sugerir_por_genero(mock_response):
    genero = 'Acción'
    response = requests.get('http://localhost:5000/peliculas/sugerir/Acción')
    
    assert response.status_code == 200
    assert 'id' in response.json()  
    assert 'titulo' in response.json()
    assert 'genero' in response.json()
    
    genero_sugerido = response.json()['genero']  
    assert genero_sugerido == genero 

def test_eliminar_pelicula(mock_response):
    response = requests.delete('http://localhost:5000/peliculas/1')
    assert response.status_code == 200
