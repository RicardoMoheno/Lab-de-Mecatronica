
#// Librerías a importar
import cv2                      # OpenCV para la captura y procesamiento de imágenes
import kociemba as Cube         # Kociemba para el algoritmo solucionador de cubos
import numpy as np              # numpy para el manejo de números
import serial.tools.list_ports  # PySerial para la comunicación serial
import time                     # time para cuestiones de timing en el envío de datos
import customtkinter as tk      # customtkinter para interfaces bomnitas

#// Empezamos con la comunicación serial, creando una instancia de comunicación serial llamada "arduino"
numberOfPorts = serial.tools.list_ports.comports()
arduino = serial.Serial()
portsList = []

#// Enlistamos los puertos disponibles para elegir el que estemos usando en ese momento
print("Lista de puertos disponibles:")
for port in numberOfPorts:
    portsList.append(str(port))
    print(str(port))

portVar = input("Elija el puerto: COM")
print(" ")

#// Verificamos que el puerto mencionado sea correcto
for x in range(0, len(portsList)):
    if portsList[x].startswith("COM" + str(portVar)):
        com = "COM" + str(portVar)

#// Iniciamos la comunicación con el puerto escogido a una velocidad de 9600 baudios
arduino.baudrate = 9660
arduino.port = com
arduino.open()

#// Creamos una clase para la ventana que nos dará control sobre el cubo
#// una pequeña app con 4 botones para mandar los comandos al arduino
class sendApp(tk.CTk):
    # Creamos la ventana y los widgets que contiene
    def __init__(self):
        super().__init__()
        # Definimos las caracterísiticas de la ventana
        self.geometry("210x200")
        self.title("Enviar comandos")
        self.minsize(200, 100)
        # Primer botónn para enviar los comandos al arduino
        self.sendButton = tk.CTkButton(master=self, command=self.enviar_comandos, text="Enviar comandos al arduino")
        self.sendButton.grid(row=0, column=1, padx=20, pady=(20, 0), sticky="ew")
        # Segundo botón para abrir el robot
        self.openButton = tk.CTkButton(master=self, command=self.abrir_robot, text="Abrir robot")
        self.openButton.grid(row=1, column=1, padx=20,pady=(20, 0), sticky="ew")
        # Tercer botón para cerrar el robot
        self.closeButton = tk.CTkButton(master=self, command=self.cerrar_robot, text="Cerrar robot")
        self.closeButton.grid(row=2, column=1, padx=20, pady=(20, 0), sticky="ew")
        # Cuarto botón para cerrar salir de la app
        self.quitButton = tk.CTkButton(master=self, command=self.quitWindow, text="Salir")
        self.quitButton.grid(row=3, column=1, padx=20, pady=(20, 20), sticky="ew")

    # Función llamada el presionar el botón "Enviar comandos al arduino"
    def enviar_comandos(self):
        # Llamamos a la función para solucionar el cubo y guardamos el string con la solución
        commandList = solve(state)
        # Calculamos la cantidad de instrucciones que tiene la lista
        size = len(commandList)
        # Por cada una de las instrucciones enlistadas mandamos un comando al arduino y, dependiendo de
        # cuanto tarda cada movimiento en realizarse, esperamos un tiempo para mandar el siguiente comando
        for i, command in enumerate(commandList, 1):
            arduino.write(command.encode("utf-8"))
            print("Se está enviando el comando: {}\t\t({}/{})".format(command, i, size))
            if command in ("U", "U'", "U2", "D", "D'", "D2"):
                time.sleep(10)
            else:
                time.sleep(4)
        # Avisamos cuando acaben de realizarse las instrucciones
        print("DONE!\n")

    # Función llamada al presionar el botón "Cerrar robot"
    def cerrar_robot(self):
        # Se envía el comando "C" al arduino para cerrar el robot
        cmd = "C"
        arduino.write(cmd.encode("utf-8"))
        print("Se está enviando el comando: " + cmd)

    # Función llamada al presionar el botón "Abrir robot"
    def abrir_robot(self):
        # Se envía el comando "O" al arduino para abrir el robot
        cmd = "O"
        arduino.write(cmd.encode("utf-8"))
        print("Se está enviando el comando: " + cmd)

    # Función llamada al presionar el botón "Salir"
    def quitWindow(self):
        self.quit()

#// En este diccionario de listas guardamos el estado actual del cubo. En cada una de las caras se guarda, en orden, los colores 
#// de los stickers del cubo
state = {"superior": ["blanco", "blanco", "blanco", "blanco", "blanco", "blanco", "blanco", "blanco", "blanco", ],
         "derecha": ["blanco", "blanco", "blanco", "blanco", "blanco", "blanco", "blanco", "blanco", "blanco", ],
         "frontal": ["blanco", "blanco", "blanco", "blanco", "blanco", "blanco", "blanco", "blanco", "blanco", ],
         "inferior": ["blanco", "blanco", "blanco", "blanco", "blanco", "blanco", "blanco", "blanco", "blanco", ],
         "izquierda": ["blanco", "blanco", "blanco", "blanco", "blanco", "blanco", "blanco", "blanco", "blanco", ],
         "posterior": ["blanco", "blanco", "blanco", "blanco", "blanco", "blanco", "blanco", "blanco", "blanco", ]
         }

#// En este diccionario se guarda la relación entre las caras y el símbolo con notación estándar del cubo de Rubik
sign_conv = {"verde": "F",
             "blanco": "U",
             "azul": "B",
             "rojo": "R",
             "naranja": "L",
             "amarillo": "D"
             }

#// En esta librería se guardan los valores RGB de los colores, esto se usa para los stickers de las ventanas de OpenCV
colores = {"rojo": (0, 0, 255),
           "naranja": (0, 120, 255),
           "azul": (255, 0, 0),
           "verde": (0, 255, 0),
           "blanco": (255, 255, 255),
           "amarillo": (0, 255, 255)
           }

#// La posición de los stickers para las ventanas de OpenCV
stickers = {"principal": [[200, 120], [300, 120], [400, 120],
                          [200, 220], [300, 220], [400, 220],
                          [200, 320], [300, 320], [400, 320]],
            "actual": [[20, 20], [54, 20], [88, 20],
                       [20, 54], [54, 54], [88, 54],
                       [20, 88], [54, 88], [88, 88]],
            "preview": [[20, 130], [54, 130], [88, 130],
                        [20, 164], [54, 164], [88, 164],
                        [20, 198], [54, 198], [88, 198]],
            "izquierda": [[50, 280], [94, 280], [138, 280],
                          [50, 324], [94, 324], [138, 324],
                          [50, 368], [94, 368], [138, 368]],
            "frontal": [[188, 280], [232, 280], [276, 280],
                        [188, 324], [232, 324], [276, 324],
                        [188, 368], [232, 368], [276, 368]],
            "derecha": [[326, 280], [370, 280], [414, 280],
                        [326, 324], [370, 324], [414, 324],
                        [326, 368], [370, 368], [414, 368]],
            "superior": [[188, 128], [232, 128], [276, 128],
                         [188, 172], [232, 172], [276, 172],
                         [188, 216], [232, 216], [276, 216]],
            "inferior": [[188, 434], [232, 434], [276, 434],
                         [188, 478], [232, 478], [276, 478],
                         [188, 522], [232, 522], [276, 522]],
            "posterior": [[464, 280], [508, 280], [552, 280],
                          [464, 324], [508, 324], [552, 324],
                          [464, 368], [508, 368], [552, 368]],
            }

#// La font a utilizar al escribir en las ventanas de OpenCV
font = cv2.FONT_HERSHEY_SIMPLEX

#// Las coordenadas, colores y contenido del labels de las ventanas de OpenCV
textPoints = {"superior": [["U", 242, 202], ["B", (100, 100, 100), 260, 208]],
              "derecha":  [["R", 380, 354], ["R", (0, 0, 255), 398, 360]],
              "frontal":  [["F", 242, 354], ["V", (0, 255, 0), 260, 360]],
              "inferior": [["D", 242, 508], ["Am", (0, 255, 255), 260, 514]],
              "izquierda": [["L", 104, 354], ["N", (0, 120, 255), 122, 360]],
              "posterior": [["B", 518, 354], ["Az", (255, 0, 0), 536, 360]],
              }

#// Una lista donde se guardarán temporalmente los valores de los colores de las caras del cubo
#// para mandarlo al diccionario "State"
check_state = []

#// Creamos una instancia con la camara a utilizar (0 es la cámara integrada de la computadora, 1 es una cámara externa)
cap = cv2.VideoCapture(1)

#// Creamos una ventana de OpenCV llamada "frame"
cv2.namedWindow("frame")

#// Funcion que se llama para generar la lista con los comando para enviar al arduino
def solve(state):
    # Se crea un string vacío llamado raw en el que se guardará el estado del cubo. El estado es generando cambiando cada
    # uno de los colores extraidos del cubo a su notación estándar y ordenándolos en la posición correcta, de la siguiente manera:
    #               |*************|
    #               |* 1 * 2 * 3 *|
    #               |*************|
    #               |* 4 * 5 * 6 *|
    #               |*************|
    #               |* 7 * 8 * 9 *|
    #               |*************|
    # |*************|*************|*************|*************|
    # |* 37* 38* 39*|* 19* 20* 21*|* 10* 11* 12*|* 46* 47* 48*|
    # |*************|*************|*************|*************|
    # |* 40* 41* 42*|* 22* 23* 24*|* 13* 14* 15*|* 49* 50* 51*|
    # |*************|*************|*************|*************|
    # |* 43* 44* 45*|* 25* 26* 27*|* 16* 17* 18*|* 52* 53* 54*|
    # |*************|*************|*************|*************|
    #               |*************|
    #               |* 28* 29* 30*|
    #               |*************|
    #               |* 31* 32* 33*|
    #               |*************|
    #               |* 34* 35* 36*|
    #               |*************|
    # Entonces un estado "resuelto" del cubo se vería así: "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
    raw = ""
    for i in state:
        for j in state[i]:
            raw += sign_conv[j]
    # Se envía el estado del cubo a Kociemba para resolverlo
    solution = Cube.solve(raw)
    # El string con la solución se separa en una lista con cada uno de los movimientos
    listOfCommands = solution.split()
    print("La solución es:")
    print(solution + "\n")
    # La función regresa esta lista con los movimientos a realizar
    return (listOfCommands)

#// Aquí se definien los valores h (tono), s (saturación) y v (brillo) que corresoponden a cada color 
#// estos se usan para la parte de detección de color de OpenCV ya que no puede procesar los valores RGB de la imagen.
#// Si se observa dificultad para detectar los colores se puede usar el otro programa para recalcular los valores 
def color_detect(h, s, v):
    if (h < 1 or h > 110) and (s > 100) and (v > 100):
        return "rojo"
    elif (2 < h < 29) and (s > 100) and (v > 100):
        return "naranja"
    elif (29 < h < 60) and (s > 100) and (v > 150):
        return "amarillo"
    elif (60 < h < 95) and (s > 100) and (v > 100):
        return "verde"
    elif (95 < h < 110) and (s > 100) and (v > 100):
        return "azul"
    elif (s < 20) and (v > 160):
        return "blanco"
    return "blanco"

#// Funciónes para generar los stickers, pintarlos de colores y colocar los labels en las ventanas de OpenCV
def draw_stickers(frame, stickers, name):
    for x, y in stickers[name]:
        cv2.rectangle(frame, (x, y), (x + 30, y + 30), (255, 255, 255), 2)

def draw_preview_stickers(frame, stickers):
    stick = ["frontal", "posterior", "izquierda", "derecha", "superior", "inferior"]
    for name in stick:
        for x, y in stickers[name]:
            cv2.rectangle(frame, (x, y), (x + 40, y + 40), (255, 255, 255), 2)

def texton_preview_stickers(frame, stickers):
    stick = ["frontal", "posterior", "izquierda", "derecha", "superior", "inferior"]
    for name in stick:
        for x, y in stickers[name]:
            sym, x1, y1 = textPoints[name][0][0], textPoints[name][0][1], textPoints[name][0][2]
            cv2.putText(preview, sym, (x1, y1), font,
                        1, (0, 0, 0), 1, cv2.LINE_AA)
            sym, col, x1, y1 = textPoints[name][1][0], textPoints[name][
                1][1], textPoints[name][1][2], textPoints[name][1][3]
            cv2.putText(preview, sym, (x1, y1), font, 0.5, col, 1, cv2.LINE_AA)

def fill_stickers(frame, stickers, sides):
    for side, colors in sides.items():
        num = 0
        for x, y in stickers[side]:
            cv2.rectangle(frame, (x, y), (x+40, y+40),
                          colores[colors[num]], -1)
            num += 1

#// Ciclo principal del porgrama
if __name__ == "__main__":
    # Se asigna la clase a la variable "app"
    app = sendApp()
    # Se crea un mapa de color negro de 700x800 para la ventana de referencia del cubo
    preview = np.zeros((700, 800, 3), np.uint8)
    #!! Ciclo contínuo del programa
    while True:
        # Se crea una lista para llenarla con los valores HSV
        hsv = []
        # Se crea un vector para guardar los valores leídos del cubo
        current_state = []
        # Se empieza a grabar la imagen
        ret, img = cap.read()
        # Convierte los valores de la captura de RGB a HSV
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = np.zeros(frame.shape, dtype=np.uint8)
        # Se dibujan los stickers y los labels en las respectivas ventanas
        draw_stickers(img, stickers, "principal")
        draw_stickers(img, stickers, "actual")
        draw_preview_stickers(preview, stickers)
        fill_stickers(preview, stickers, state)
        texton_preview_stickers(preview, stickers)
        # Se añaden los valores al vector HSV
        for i in range(9):
            hsv.append(frame[stickers["principal"][i][1]+10][stickers["principal"][i][0]+10])
        # Se guardan los colores detectados en el vector current_state
        a = 0
        for x, y in stickers["actual"]:
            color_name = color_detect(hsv[a][0], hsv[a][1], hsv[a][2])
            cv2.rectangle(img, (x, y), (x+30, y+30), colores[color_name], -1)
            a += 1
            current_state.append(color_name)
        # Se llama a la función waitKey para esperar a que el usuario presione una tecla.
        k = cv2.waitKey(5) & 0xFF
        if k == 27:                             # Si la tecla es ESC es sale del ciclo infinito
            break
        elif k == ord("u"):                     # Si la teclsa es "u" se guardan los valores que se estén viendo en la cámara en la lista "Superior" de la biblioteca State
            state["superior"] = current_state
            check_state.append("u")
        elif k == ord("r"):                     # Si la teclsa es "r" se guardan los valores que se estén viendo en la cámara en la lista "Derecha" de la biblioteca State
            check_state.append("r")
            state["derecha"] = current_state
        elif k == ord("l"):                     # Si la teclsa es "l" se guardan los valores que se estén viendo en la cámara en la lista "Izquierda" de la biblioteca State
            check_state.append("l")
            state["izquierda"] = current_state
        elif k == ord("d"):                     # Si la teclsa es "d" se guardan los valores que se estén viendo en la cámara en la lista "Inferior" de la biblioteca State
            check_state.append("d")
            state["inferior"] = current_state
        elif k == ord("f"):                     # Si la teclsa es "f" se guardan los valores que se estén viendo en la cámara en la lista "Frontal" de la biblioteca State
            check_state.append("f")
            state["frontal"] = current_state
        elif k == ord("b"):                     # Si la teclsa es "u" se guardan los valores que se estén viendo en la cámara en la lista "Posterior" de la biblioteca State
            check_state.append("b")
            state["posterior"] = current_state
        elif k == ord("\r"):                    # Si se le da a la tecla ENTER lo primero que se hace es checar que se hayan guardado las 6 caras del cubo
            if len(set(check_state)) == 6:      
                try:
                    raw = ""                   
                    for i in state:
                        for j in state[i]:
                            raw += sign_conv[j]
                    Cube.solve(raw)             # Si sí se tiene las 6 caras, se intenta mandar el estado a solucionar con el algoritmo para comprobar que no haya errores
                    app.mainloop()              # En caso de poder resolver el cubo, se manda a llamar a la app creada para enviar los comandos al arduuino
                except:                         # Si el cubo no se puede resolver por algun error en la captura se manda un mensaje de error para volver a capturar
                    print("Error en la lectura de los lados, verifica que se hayan registrado correctamente\n")
            else:                               # En caso de no contar con todos los lados registrados se manda un mensaje para terminar de capturarlos
                print("No se han escaneado todos los lados")
                print("Lados por escanear:", 6-len(set(check_state)))
        # Con estas fucniones se actualizan las ventanas
        cv2.imshow("preview", preview)
        cv2.imshow("frame", img[0:500, 0:500])
    # Al salir del ciclo infinito se detiene la conexión con arduino, se cierra la camara y se destruyen las ventanas creadas
    arduino.close()
    cap.release()
    cv2.destroyAllWindows()
