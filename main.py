from flask import Flask, jsonify, request
from proximo_feriado import NextHoliday
from random import choice
from urllib.parse import unquote #codificador: https://www.urlencoder.io/ 

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
    pelicula_encontrada = buscar_por_id(id)
    if pelicula_encontrada is None:
        return jsonify({'mensaje': 'Película no encontrada'}), 404
    return jsonify(pelicula_encontrada)


def busqueda_por_genero(genero):
    genero = unquote(genero)
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

    pelicula = buscar_por_id(id)
    if pelicula == none:
        return jsonify({'mensaje': 'Película no encontrada'}), 404
    else:
        peliculas.remove(pelicula)
        return jsonify({'mensaje': 'Película eliminada correctamente'})
    

def obtener_nuevo_id():
    if len(peliculas) > 0:
        ultimo_id = peliculas[-1]['id']
        return ultimo_id + 1
    else:
        return 1

def busqueda_por_nombre(nombre):
    nombre = unquote(nombre)
    peliculas_encontradas = []
    for pelicula in peliculas:
        if nombre.lower() in pelicula['titulo'].lower():
            peliculas_encontradas.append(pelicula)
    if len(peliculas_encontradas) == 0:
        return jsonify({'mensaje': 'Película no encontrada'}), 404
    else:
        return jsonify(peliculas_encontradas)

def sugerir_pelicula():
    pelicula_sugerida = choice(peliculas)
    return jsonify(pelicula_sugerida)

def sugerir_por_genero(genero):
    genero = unquote(genero)
    
    response =  busqueda_por_genero(genero)
    peliculas_list = response.get_json()
    if  len(peliculas_list) == 0:
        return jsonify({'mensaje': 'Género no encontrado'}), 404
    pelicula_sugerida = choice(peliculas_list)
    return jsonify(pelicula_sugerida), 200


def busqueda_por_proximo_feriado(genero):

    genero = unquote(genero)
    proximo_feriado = NextHoliday('todos')
    proximo_feriado.fetch_holidays()
    
    response = busqueda_por_genero(genero)
    peliculas_list = response.get_json()

    if not peliculas_json:
        return jsonify({"error": "No hay películas para el género especificado"})
    recomendacion = choice(peliculas_list)

    feriado = {
        'fecha': f"{proximo_feriado.holiday['dia']}/{proximo_feriado.holiday['mes']}",
        'motivo': proximo_feriado.holiday['motivo'],
        'genero': recomendacion['genero'],
        'recomendacion': recomendacion['titulo']
    }

    return jsonify(feriado)

app.add_url_rule('/peliculas', 'obtener_peliculas', obtener_peliculas, methods=['GET'])
app.add_url_rule('/peliculas', 'agregar_pelicula', agregar_pelicula, methods=['POST'])
app.add_url_rule('/peliculas/feriado/<string:genero>', 'busqueda_por_proximo_feriado', busqueda_por_proximo_feriado, methods=['GET'])
app.add_url_rule('/peliculas/<int:id>', 'obtener_pelicula', obtener_pelicula, methods=['GET'])
app.add_url_rule('/peliculas/<int:id>', 'actualizar_pelicula', actualizar_pelicula, methods=['PUT'])
app.add_url_rule('/peliculas/<int:id>', 'eliminar_pelicula', eliminar_pelicula, methods=['DELETE'])
app.add_url_rule('/peliculas/<string:genero>', 'busqueda_por_genero', busqueda_por_genero, methods=['GET'])
app.add_url_rule('/peliculas/buscar/<string:nombre>', 'busqueda_por_nombre', busqueda_por_nombre, methods=['GET'])
app.add_url_rule('/peliculas/sugerir', 'sugerir_pelicula', sugerir_pelicula, methods=['GET'])
app.add_url_rule('/peliculas/sugerir/<string:genero>', 'sugerir_por_genero', sugerir_por_genero, methods=['GET'])

if __name__ == '__main__':
    app.run()
