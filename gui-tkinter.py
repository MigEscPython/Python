from tkinter import *
from tkinter import ttk

def saludar():
    print("Hola")

ventana = Tk()
ventana.title("Espacio para Saludar")
ventana.geometry("450x200")
frm = ttk.Frame(ventana, padding=10)
frm.grid()
ttk.Label(frm, text="Saludar").grid(column=0, row=0)
ttk.Button(frm, text="Saludame", command=saludar).grid(column=1, row=0)
mensaje = ttk.Label(frm, text="----------------------").grid(column=0, row=1)
ventana.mainloop()
