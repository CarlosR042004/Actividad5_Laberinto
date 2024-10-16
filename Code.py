import random

# Generar el laberinto de tamaño definido por el usuario
def generar_laberinto(tamaño):
    laberinto = [[random.choice([0, 1]) for _ in range(tamaño)] for _ in range(tamaño)]
    laberinto[0][0] = 0  # Entrada
    laberinto[tamaño - 1][tamaño - 1] = 2  # Salida
    return laberinto

# Algoritmo de búsqueda de camino simple
def buscar_camino(x, y, laberinto):
    # Condición de éxito
    if x == len(laberinto) - 1 and y == len(laberinto[0]) - 1:
        return True
    # Validación de límites y paredes
    if x < 0 or y < 0 or x >= len(laberinto) or y >= len(laberinto[0]) or laberinto[x][y] == 1:
        return False
    # Marcamos la celda actual como visitada temporalmente
    laberinto[x][y] = 1  
    # Cuatro direcciones
    if (buscar_camino(x + 1, y, laberinto) or
        buscar_camino(x, y + 1, laberinto) or
        buscar_camino(x - 1, y, laberinto) or
        buscar_camino(x, y - 1, laberinto)):
        return True
    # Restaurar el estado original si no hay camino
    laberinto[x][y] = 0
    return False
# Imprimir el laberinto para verlo
def imprimir_laberinto(laberinto):
    for fila in laberinto:
        print(" ".join(str(celda) for celda in fila))
# Solicitar tamaño del laberinto al usuario
while True:
    try:
        tamaño = int(input("Ingrese el tamaño del laberinto (n x n), n >= 6: "))
        if tamaño >= 6:
            break
        else:
            print("Por favor, ingrese un tamaño mayor o igual a 6.")
    except ValueError:
        print("Entrada no válida. Por favor ingrese un número entero.")

laberinto = generar_laberinto(tamaño)
imprimir_laberinto(laberinto)

if buscar_camino(0, 0, laberinto):
    print("¡Felicidades, encontraste la salida!")
else:
    print("No se encontró ningún camino hacia la salida.")
