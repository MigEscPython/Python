from tkinter import *
import os

def abrirCalculadora():
    os.system("calc")

def abrirVisual():
    os.system("ipconfig")

ventana = Tk()
ventana.title("Utilerias de Windows")
ventana.geometry("400x200")

bCalc = Button(text="Calculadora", command=abrirCalculadora)
bCalc.place(x=50, y=50)
bVisual = Button(text="Visual Studio Code", command=abrirVisual)
bVisual.place(x=50, y=80)
#agregar un boton más

ventana.mainloop()