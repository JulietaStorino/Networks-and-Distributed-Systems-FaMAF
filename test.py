import requests

# Obtener todas las películas
response = requests.get('http://localhost:5000/peliculas')
peliculas = response.json()
print("Películas existentes:")
for pelicula in peliculas:
    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
print()

# Agregar una nueva película
nueva_pelicula = {
    'titulo': 'Pelicula de prueba',
    'genero': 'Acción'
}
response = requests.post('http://localhost:5000/peliculas', json=nueva_pelicula)
if response.status_code == 201:
    pelicula_agregada = response.json()
    print("Película agregada:")
    print(f"ID: {pelicula_agregada['id']}, Título: {pelicula_agregada['titulo']}, Género: {pelicula_agregada['genero']}")
else:
    print("Error al agregar la película")
print()

# Sugerir según el próximo feriado
genero = 'Ciencia ficción'  # Género de la película a sugerir
response = requests.get(f'http://localhost:5000/peliculas/feriado/{genero}')
if response.status_code == 200:
    feriado = response.json()
    print("Película sugerida para el próximo feriado:")
    print(f"Fecha: {feriado['fecha']}, Motivo: {feriado['motivo']}, Género: {feriado['genero']}, Recomendación: {feriado['recomendacion']}")
else:
    print("Error al sugerir una película para el próximo feriado")
print()

# Obtener detalles de una película específica
id_pelicula = 1 # ID de la película a obtener
response = requests.get(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 200:
    pelicula = response.json()
    print("Detalles de la película:")
    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
else:
    print("Error al obtener los detalles de la película")
print()

# Actualizar los detalles de una película
id_pelicula = 1  # ID de la película a actualizar
datos_actualizados = {
    'titulo': 'Nuevo título',
    'genero': 'Comedia'
}
response = requests.put(f'http://localhost:5000/peliculas/{id_pelicula}', json=datos_actualizados)
if response.status_code == 200:
    pelicula_actualizada = response.json()
    print("Película actualizada:")
    print(f"ID: {pelicula_actualizada['id']}, Título: {pelicula_actualizada['titulo']}, Género: {pelicula_actualizada['genero']}")
else:
    print("Error al actualizar la película")
print()

# Eliminar una película
id_pelicula = 1  # ID de la película a eliminar
response = requests.delete(f'http://localhost:5000/peliculas/{id_pelicula}')
print("Eliminar película:")
if response.status_code == 200:
    print("Película eliminada correctamente")
else:
    print("Error al eliminar la película")
print()

# Obtener todas las películas de un género específico
genero = 'Acción'  # Género de las películas a obtener
response = requests.get(f'http://localhost:5000/peliculas/{genero}')
peliculas_genero = response.json()
print(f"Películas de género {genero}:")
for pelicula in peliculas_genero:
    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
print()

# Buscar películas por nombre
nombre = 'Fight Cl'  # Nombre de la película a buscar
response = requests.get(f'http://localhost:5000/peliculas/buscar/{nombre}')
print(f"Buscar películas que contengan la palabra {nombre}:")
if response.status_code == 404:
    print("Error al buscar la película")
elif len(response.json()) == 0:
    print("Ninguna película encontrada")
else:
    peliculas_nombre = response.json()
    for pelicula in peliculas_nombre:
        print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
print()

# Sugerir una película aleatoria
response = requests.get('http://localhost:5000/peliculas/sugerir')
if response.status_code == 200:
    pelicula_sugerida = response.json()
    print("Película sugerida:")
    print(f"ID: {pelicula_sugerida['id']}, Título: {pelicula_sugerida['titulo']}, Género: {pelicula_sugerida['genero']}")
else:
    print("Error al sugerir una película")
print()

# sugerir un pelicula aleatoria de un genero especifico
genero = 'Acción'
response = requests.get(f'http://localhost:5000/peliculas/sugerir/{genero}')
if response.status_code == 200:
    pelicula = response.json()
    print(f"Película de {pelicula['genero']} sugerida:")
    print(f"Título: {pelicula['titulo']}")
else:
    print("Error al obtener los detalles de la película")
print()
