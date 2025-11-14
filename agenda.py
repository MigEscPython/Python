#agenda telefonica
#usar dicc: clave:valor, nombre:telefono
agenda = {}
def guardarRegistro(nombre, telefono):
    agenda[nombre] = telefono

def imprimirAgenda():
    print(agenda) # ojo

#menu
while True:
    print("1. Guardar contacto\n2.Imprimir\n0.Salir")
    opcion = input("Opcion: ")
    if opcion == "1":
        nomb = input("Nombre: ")
        tel = input("Telefono: ")
        guardarRegistro(nomb, tel) 
    elif opcion == "2":
        imprimirAgenda()
    elif opcion == "0":
        break
    else:
        print("Opcion invalida")
    