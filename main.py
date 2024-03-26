from flask import Flask, jsonify, request
from proximo_feriado import NextHoliday
from random import choice

app = Flask(__name__)
peliculas = [
    {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
    {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'},
    {'id': 3, 'titulo': 'Interstellar', 'genero': 'Ciencia ficción'},
    {'id': 4, 'titulo': 'Jurassic Park', 'genero': 'Aventura'},
    {'id': 5, 'titulo': 'The Avengers', 'genero': 'Acción'},
    {'id': 6, 'titulo': 'Back to the Future', 'genero': 'Ciencia ficción'},
    {'id': 7, 'titulo': 'The Lord of the Rings', 'genero': 'Fantasía'},
    {'id': 8, 'titulo': 'The Dark Knight', 'genero': 'Acción'},
    {'id': 9, 'titulo': 'Inception', 'genero': 'Ciencia ficción'},
    {'id': 10, 'titulo': 'The Shawshank Redemption', 'genero': 'Drama'},
    {'id': 11, 'titulo': 'Pulp Fiction', 'genero': 'Crimen'},
    {'id': 12, 'titulo': 'Fight Club', 'genero': 'Drama'}
]

def buscar_por_id(id):
    for pelicula in peliculas:
        if pelicula['id'] == id:
            return pelicula
    return None

def obtener_peliculas():
    return jsonify(peliculas)


def obtener_pelicula(id):
    # Lógica para buscar la película por su ID y devolver sus detalles
    pelicula_encontrada = buscar_por_id(id)
    if pelicula_encontrada is None:
        return jsonify({'mensaje': 'Película no encontrada'}), 404
    return jsonify(pelicula_encontrada)


def obtener_peliculas_por_genero(genero):
    # Lógica para devolver el listado de películas de un género específico
    peliculas_por_genero = []
    for pelicula in peliculas:
        if pelicula['genero'] == genero:
            peliculas_por_genero.append(pelicula)
    return jsonify(peliculas_por_genero)


def agregar_pelicula():
    nueva_pelicula = {
        'id': obtener_nuevo_id(),
        'titulo': request.json['titulo'],
        'genero': request.json['genero']
    }
    peliculas.append(nueva_pelicula)
    print(peliculas)
    return jsonify(nueva_pelicula), 201


def actualizar_pelicula(id):
    pelicula_actualizada = buscar_por_id(id)
    if pelicula_actualizada is None:
        return jsonify({'mensaje': 'Película no encontrada'}), 404
    
    pelicula_actualizada['titulo'] = request.json.get('titulo', pelicula_actualizada['titulo'])
    pelicula_actualizada['genero'] = request.json.get('genero', pelicula_actualizada['genero'])

    return jsonify(pelicula_actualizada)


def eliminar_pelicula(id):
    # Lógica para buscar la película por su ID y eliminarla
    return jsonify({'mensaje': 'Película eliminada correctamente'})


def obtener_nuevo_id():
    if len(peliculas) > 0:
        ultimo_id = peliculas[-1]['id']
        return ultimo_id + 1
    else:
        return 1

def busqueda_por_nombre(nombre):
    peliculas_encontradas = []
    for pelicula in peliculas:
        if nombre.lower() in pelicula['titulo'].lower():
            peliculas_encontradas.append(pelicula)
    return peliculas_encontradas

def busqueda_por_proximo_feriado(genero):
    # Lógica para buscar el próximo feriado y devolver una recomendación de película
    proximo_feriado = NextHoliday('todos')
    proximo_feriado.fetch_holidays()
    recomendacion = choice(obtener_peliculas_por_genero(peliculas))

    feriado = {
        'fecha': f"{proximo_feriado.holiday['dia']}/{proximo_feriado.holiday['mes']}",
        'motivo': proximo_feriado.holiday['motivo'],
        'genero': recomendacion['genero'],
        'recomendacion': recomendacion['titulo']
    }

    return jsonify(feriado)

app.add_url_rule('/peliculas', 'obtener_peliculas', obtener_peliculas, methods=['GET'])
app.add_url_rule('/peliculas', 'agregar_pelicula', agregar_pelicula, methods=['POST'])
app.add_url_rule('/peliculas/feriado', 'busqueda_por_proximo_feriado', busqueda_por_proximo_feriado, methods=['GET'])
app.add_url_rule('/peliculas/<int:id>', 'obtener_pelicula', obtener_pelicula, methods=['GET'])
app.add_url_rule('/peliculas/<int:id>', 'actualizar_pelicula', actualizar_pelicula, methods=['PUT'])
app.add_url_rule('/peliculas/<int:id>', 'eliminar_pelicula', eliminar_pelicula, methods=['DELETE'])
app.add_url_rule('/peliculas/<string:genero>', 'obtener_peliculas_por_genero', obtener_peliculas_por_genero, methods=['GET'])
app.add_url_rule('/peliculas/buscar/<string:nombre>', 'busqueda_por_nombre', busqueda_por_nombre, methods=['GET'])

if __name__ == '__main__':
    app.run()
