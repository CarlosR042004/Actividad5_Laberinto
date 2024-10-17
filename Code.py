import tkinter as tk
import time

# Definir el laberinto de manera manual
def generar_laberinto():
    # Laberinto de ejemplo: 0 es un camino, 1 es una pared, 2 es la salida
    laberinto = [
        [0, 0, 0, 1, 0, 1],
        [1, 1, 0, 0, 1, 1],
        [0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 1, 1],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 2]  # La salida está en la última celda
    ]
    return laberinto

# Algoritmo de búsqueda de camino con visualización en tkinter
def buscar_camino_iterativo(laberinto, canvas, tamaño_celda, mensaje_label):
    tamaño = len(laberinto)
    stack = [(0, 0, [])]  # Pila para almacenar el camino y las posiciones
    visitado = [[False] * tamaño for _ in range(tamaño)]
    
    while stack:
        x, y, camino = stack.pop()
        
        # Si encontramos la salida
        if laberinto[x][y] == 2:
            camino.append((x, y))
            for cx, cy in camino:
                canvas.create_rectangle(cy * tamaño_celda, cx * tamaño_celda,
                                        (cy + 1) * tamaño_celda, (cx + 1) * tamaño_celda,
                                        fill="blue")
                laberinto[cx][cy] = 'x'
                mensaje_label.config(text="¡Felicidades, encontraste la salida!")
            return True
        
        # Verificar límites y paredes
        if x < 0 or y < 0 or x >= tamaño or y >= tamaño or laberinto[x][y] == 1 or visitado[x][y]:
            continue
        
        # Marcar la celda como visitada
        visitado[x][y] = True
        
        # Dibujar el movimiento en tkinter
        canvas.create_rectangle(y * tamaño_celda, x * tamaño_celda,
                                (y + 1) * tamaño_celda, (x + 1) * tamaño_celda,
                                fill="yellow")
        canvas.update()
        time.sleep(0.1)  # Pausa para ver el movimiento
        
        # Añadir la celda actual al camino
        nuevo_camino = camino + [(x, y)]
        
        # Añadir las celdas vecinas a la pila con el camino actualizado
        # Verifica que las celdas vecinas están dentro de los límites antes de agregarlas
        if x + 1 < tamaño:
            stack.append((x + 1, y, nuevo_camino))  # Abajo
        if y + 1 < tamaño:
            stack.append((x, y + 1, nuevo_camino))  # Derecha
        if x - 1 >= 0:
            stack.append((x - 1, y, nuevo_camino))  # Arriba
        if y - 1 >= 0:
            stack.append((x, y - 1, nuevo_camino))  # Izquierda

    return False

# Configuración de la interfaz tkinter
def crear_interfaz(laberinto):
    tamaño_celda = 50
    tamaño = len(laberinto)
    
    # Crear la ventana y el canvas
    ventana = tk.Tk()
    ventana.title("Laberinto")
    canvas = tk.Canvas(ventana, width=tamaño * tamaño_celda, height=tamaño * tamaño_celda)
    canvas.pack()

    # Crear un label para mostrar mensajes
    mensaje_label = tk.Label(ventana, text="")
    mensaje_label.pack()
    
    # Dibujar el laberinto inicial
    for x in range(tamaño):
        for y in range(tamaño):
            color = "white" if laberinto[x][y] == 0 else "black"
            if laberinto[x][y] == 2:
                color = "green"
            elif laberinto[x][y] == 3:
                color = "red"
            canvas.create_rectangle(y * tamaño_celda, x * tamaño_celda,
                                    (y + 1) * tamaño_celda, (x + 1) * tamaño_celda,
                                    fill=color)
    
    # Iniciar la búsqueda del camino
    buscar_camino_iterativo(laberinto, canvas, tamaño_celda, mensaje_label)

    ventana.mainloop()

# Ejecutar el programa
laberinto = generar_laberinto()
crear_interfaz(laberinto)
