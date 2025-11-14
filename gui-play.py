from tkinter import *
from reproductor import Reproductor

musica = Reproductor
def reproducirMusica():
    pass

def pausarMusica():
    pass

def subirVolumen():
    pass

ventana = Tk()
ventana.geometry("400x400")
ventana.title("SPOTIFAY")

lTitulo = Label(text="Estas escuchando...")
lTitulo.place(x=10, y=10)
bPlay = Button(text="▶", command=reproducirMusica)
bPlay.place(x=50, y=50)
bPlay = Button(text="⏸", command=pausarMusica)
bPlay.place(x=80, y=50)

ventana.mainloop()