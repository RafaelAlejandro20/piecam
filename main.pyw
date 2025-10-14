import datetime
import customtkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import time
import datetime
from PIL import Image
from PIL import ImageTk
import imutils
import cv2
import serial
import threading

try:
    arduino = serial.Serial('COM5',9600)
    print('Conexion hecha con exito')
except:
    print('Arduino no encontrado')

#ESTABLECIMIENTO DE COLORES
blanco = "#ffffff"
negro = "#000000"
gris = "#3c3c3c"
gris_claro = "#e6e6e6"
gris_oscuro = "#1e1e1e"
azul = "#078bf7"
azul_oscuro = "#0767f7"
verde = "#42b300"
verde_oscuro = "#389800"
azul_claro = "#71bfff"
rojo = "#ff4848"
rojo_oscuro = "#ff1616"

#ESTABLECIKMIENTO DE APARIENCIA PREDETERMINADA
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()

#DATOS DE LA VENTANA
root.title("Piecam")
root.geometry("600x480")
root.config(borderwidth=0,background=negro)
root.resizable(0,0)

def gbutton(root,text,color,hover_color,command,r,c,y,x):
    gua = customtkinter.CTkButton(
        root,
        width=300,
        height=30,
        text=text,
        corner_radius=0,
        fg_color=color,
        hover_color=hover_color,
        command=command)
    gua.grid(row=r, column=c, pady=y, padx=x)

def gcombo(root,values,r,c):
    combo = customtkinter.CTkComboBox(
        root,
        values=values,
        width=200,
        border_width=1,
        border_color=gris_claro)
    combo.grid(row=r, column=c)
    return combo

main = customtkinter.CTkFrame(root, width=650, fg_color=blanco)
main.pack(fill='both', expand='true')

global vigilancia
global res
vigilancia = True
respuesta = 0

def hilo():
    global vigilancia
    global respuesta
    while vigilancia == True:
        time.sleep(0.5)
        respuesta = int(arduino.readline().strip().decode())
        print(respuesta)

def visualizar():
    global cap
    global frame
    global respuesta
    global vigilancia
    if cap is not None:
        ret, frame = cap.read()
        if ret == True:
            frame = imutils.resize(frame, width=894)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)

            video.configure(image=img)
            video.image = img
            video.after(10, visualizar)

            if respuesta == 1:
                hora = datetime.datetime.now()
                f_hora = f'./fotos/{hora.year}{hora.month}{hora.day}-{hora.hour}-{hora.minute}-{hora.second}.jpg'
                cv2.imwrite(f_hora,frame)
                print(f_hora)
        else:
            video.image = ""
            cap.release
            vigilancia = False

def iniciar():
    global cap
    global vigilancia
    vigilancia = True
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    thread1 = threading.Thread(target=hilo, daemon=True)
    thread1.start()
    visualizar()

def terminar():
    global cap
    cap.release()

gbutton(main,'Iniciar vigilancia',azul,azul_oscuro,iniciar,0,0,0,0)
gbutton(main,'Terminar vigilancia',azul,azul_oscuro,terminar,0,1,0,0)

video = Label(main, border=0)
video.grid(row=1, column=0, columnspan=2)

img = ImageTk.PhotoImage(file='main.png')
video.configure(image=img)

root.mainloop()