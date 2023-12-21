import numpy as np
import cv2
import time

from screeninfo import get_monitors

import gspread
from oauth2client.service_account import ServiceAccountCredentials

def listaDePernosQueNecesito(values_list):
    lista_final = [[], [], []]
    index_que_me_importan = [[4, 19, 35], [3, 18, 34], [2, 17, 33]]
    for i in range(0, len(values_list)-1):
        for cuadrante in range(0,3):
            if i in index_que_me_importan[cuadrante]:
                lista_a_unir = values_list[i]
                lista_a_unir.append("I"+str(i+1))
                lista_a_unir.pop(0)
                lista_final[cuadrante].append(lista_a_unir)
    return lista_final

def subirPernosAExcel(pernosActualizados, excelBaseDeDatos):
    for seccion in pernosActualizados:
        for perno in seccion:
            #print(perno)
            excelBaseDeDatos.update(range_name=perno[8], values=perno[7])

#Preparar drive API
myscope = ['https://spreadsheets.google.com/feeds', 
            'https://www.googleapis.com/auth/drive']
credenciales = ServiceAccountCredentials.from_json_keyfile_name('my-project-twinviz-d279dede6608.json',myscope)
client = gspread.authorize(credenciales)

excel = client.open("BD_Prototipo").sheet1
excelEnLista = excel.get_all_values()
pernos = listaDePernosQueNecesito(excelEnLista)

#Parametros camara
nCam = 0
cap = cv2.VideoCapture(nCam)

color1_hsv = np.array([0, 0, 0])
last_print_time = time.time()

if cap is not None and cap.isOpened():
    cap.open(nCam)

#Ventanas
cv2.namedWindow('frame', cv2.WINDOW_AUTOSIZE)
cv2.moveWindow('frame', 30, 100)
# screen_width = get_monitors()[0].width
# screen_height = get_monitors()[0].height

# cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('frame', int(screen_width * 0.9), int(screen_height * 0.9))  # Adjust the factor as needed

#Ventana de mascara
# cv2.namedWindow('frame2')
# cv2.moveWindow('frame2', 700, 100)

#Color
# lower_color = np.array([160, 90, 150])  # Valor HSV para rosado cartulina
# upper_color = np.array([175, 105, 178])  # Valor HSV para rosado cartulina

# lower_color = np.array([150, 80, 160])  # Valor HSV para perno
# upper_color = np.array([165, 90, 181])  # Valor HSV para perno

# lower_color = np.array([130, 15, 135])  # Valor HSV para perno 2
# upper_color = np.array([150, 53, 180])  # Valor HSV para perno 2

lower_color = np.array([35, 50, 50])  # Valor HSV para verde
upper_color = np.array([95, 255, 255])  # Valor HSV para verde


while True:
    ret, frame = cap.read()

    #creacion de mascara
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask_color = cv2.inRange(hsv_frame, lower_color, upper_color)
    hsv_frame_mask = cv2.bitwise_and(frame, frame, mask=mask_color)

    # Dividir la imagen en una cuadrícula 3x3
    height, width, _ = frame.shape
    grid_size = 3
    cell_height = height // grid_size
    cell_width = width // grid_size

    #Deteccion de masa verde mas grande
    largest_areas = np.zeros((grid_size, grid_size))
    largest_contours = np.empty((grid_size, grid_size), dtype=object)

    for i in range(grid_size):
        for j in range(grid_size):
            cell = frame[i * cell_height:(i + 1) * cell_height, j * cell_width:(j + 1) * cell_width]
            hsv_cell = cv2.cvtColor(cell, cv2.COLOR_BGR2HSV)
            mask_color = cv2.inRange(hsv_cell, lower_color, upper_color)

            # Encontrar contornos en la máscara
            contours, _ = cv2.findContours(mask_color, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            largest_area = 0
            largest_contour = None

            for contour in contours:
                # Encontrar el contorno más grande en cada sección
                area = cv2.contourArea(contour)
                if area > largest_area:
                    largest_area = area
                    largest_contour = contour

            largest_areas[i, j] = largest_area
            largest_contours[i, j] = largest_contour

    #Dibujo de rectangulos y separacion de secciones
    for i in range(grid_size):
        for j in range(grid_size):
            x_offset = j * cell_width
            y_offset = i * cell_height

            if largest_contours[i, j] is not None:
                # Dibujar un rectángulo alrededor del contorno más grande en cada sección
                x, y, w, h = cv2.boundingRect(largest_contours[i, j])
                x += x_offset
                y += y_offset
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Dibujar líneas para separar las secciones
            if j < grid_size - 1:
                cv2.line(frame, (x_offset + cell_width, 0), (x_offset + cell_width, height), (0, 0, 255), 2)
            if i < grid_size - 1:
                cv2.line(frame, (0, y_offset + cell_height), (width, y_offset + cell_height), (0, 0, 255), 2)

    cv2.imshow('frame', frame)
    #cv2.imshow('frame2', hsv_frame_mask)

    # Imprimir la posición de la masa mayoritaria de verde cada 30 segundos
    current_time = time.time()

    if current_time - last_print_time >= 15000:

        for i in range(grid_size):
            for j in range(grid_size):
                #print(largest_contours[i, j])
                if largest_contours[i, j] is None:
                    position_data = f"Sección ({i + 1}, {j + 1}) - MALO. No se encontro perno"
                    print(pernos[i][j])
                    pernos[i][j][7] = "MALO" #Perno numero j de la seccion 1 esta malo
                    print(position_data)
                elif largest_contours[i, j] is not None:
                    x, y, _, _ = cv2.boundingRect(largest_contours[i, j])
                    x_offset = j * cell_width
                    y_offset = i * cell_height
                    position_data = f"Sección ({i + 1}, {j + 1}) - Posición del contorno más grande verde - X: {x + x_offset}, Y: {y + y_offset}"
                    print(pernos[i][j])
                    pernos[i][j][7] = "BUENO" #Perno numero j de la seccion 1 esta bueno
                    print(position_data)
        last_print_time = current_time
        subirPernosAExcel(pernosActualizados=pernos, excelBaseDeDatos=excel)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()