import tkinter as tk
import time
from tkinter import simpledialog, messagebox

# Definir el laberinto de manera manual
def generar_laberinto():
    # Laberinto de ejemplo: 0 es un camino, 1 es una pared, 2 es la salida, 3 es una pregunta, 4 es otra pregunta, 5 es una pregunta súbita
    laberinto = [
        [0, 0, 3, 1, 1, 5],
        [0, 1, 1, 0, 0, 0],
        [0, 0, 1, 0, 1, 1],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 1, 1, 0],
        [4, 0, 0, 1, 3, 2]  # La salida está en la última celda
    ]
    return laberinto

# Pregunta al llegar a un punto rojo (3)
def hacer_pregunta_francia(ventana):
    respuesta = simpledialog.askstring("Pregunta", "¿Cuál es la capital de Francia?", parent=ventana)
    if respuesta and respuesta.strip().upper() == "PARIS":
        return True
    else:
        return False

# Pregunta al llegar a un punto especial (4)
def hacer_pregunta_messi(ventana):
    while True:
        respuesta = simpledialog.askstring("Pregunta", "¿MESSI o CRISTIANO?", parent=ventana)
        if respuesta and respuesta.strip().upper() == "MESSI":
            return True
        else:
            messagebox.showinfo("Error", "Respuesta incorrecta. Debes elegir MESSI.")

# Pregunta súbita al llegar a un punto especial (5)
def hacer_pregunta_subita(ventana):
    respuesta = simpledialog.askstring("Pregunta Súbita", "¿Cuánto es 5 + 2?", parent=ventana)
    if respuesta and respuesta.strip() == "7":
        return True
    else:
        messagebox.showerror("Error", "Respuesta incorrecta. ¡Juego terminado!")
        ventana.destroy()  # Cerrar la ventana y terminar el juego si la respuesta es incorrecta
        return False

# Algoritmo de búsqueda de camino con visualización en tkinter
def buscar_camino_iterativo(laberinto, canvas, tamaño_celda, mensaje_label, ventana):
    tamaño = len(laberinto)
    stack = [(0, 0, [])]  # Pila para almacenar el camino y las posiciones
    visitado = [[False] * tamaño for _ in range(tamaño)]
    pregunta_hecha = False  # Variable para asegurarnos de que la pregunta (capital de Francia) se haga solo una vez
    pregunta_messi_hecha = False  # Variable para la pregunta MESSI
    pregunta_subita_hecha = False  # Variable para la pregunta súbita

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

        # Verificar si es una celda con una pregunta (color rojo, 3)
        if laberinto[x][y] == 3 and not pregunta_hecha:
            if hacer_pregunta_francia(ventana):
                # Si la respuesta es correcta, buscar el siguiente 3 y saltar a él
                for i in range(tamaño):
                    for j in range(tamaño):
                        if laberinto[i][j] == 3 and (i, j) != (x, y):
                            stack.append((i, j, camino + [(x, y)]))
                            break
                pregunta_hecha = True
            else:
                # Si la respuesta es incorrecta, continuar sin hacer nada
                mensaje_label.config(text="RESPUESTA INCORRECTA")
                canvas.update()
                time.sleep(1)  # Pausa para ver el mensaje
                mensaje_label.config(text="")

        # Verificar si es una celda con una pregunta especial (color naranja, 4)
        if laberinto[x][y] == 4 and not pregunta_messi_hecha:
            hacer_pregunta_messi(ventana)
            pregunta_messi_hecha = True

        # Verificar si es una celda con una pregunta súbita (color morado, 5)
        if laberinto[x][y] == 5 and not pregunta_subita_hecha:
            if hacer_pregunta_subita(ventana):
                # Si responde correctamente, continuar el camino
                mensaje_label.config(text="¡Respuesta correcta!")
                canvas.update()
                time.sleep(1)  # Pausa para mostrar el mensaje
                mensaje_label.config(text="")
            else:
                # Si la respuesta es incorrecta, el juego ya terminó
                return False
            pregunta_subita_hecha = True

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
            elif laberinto[x][y] == 4:
                color = "orange"
            elif laberinto[x][y] == 5:
                color = "purple"  # Cambiado a morado
            canvas.create_rectangle(y * tamaño_celda, x * tamaño_celda,
                                    (y + 1) * tamaño_celda, (x + 1) * tamaño_celda,
                                    fill=color)

    # Iniciar la búsqueda del camino
    buscar_camino_iterativo(laberinto, canvas, tamaño_celda, mensaje_label, ventana)

    ventana.mainloop()

# Ejecutar el programa
laberinto = generar_laberinto()
crear_interfaz(laberinto)

