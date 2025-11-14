## Calculadora
def sumar(x,y):
    return x + y
def restar(x,y):
    return x - y
def multiplicar(x,y):
    return x*y
def dividir(x,y):
    if y != 0 :
        return x / y
    else:
        return "Error. División por cero."

while True:
    opcion = input("1. Sumar\n2. Restar\n3. Multiplicar\n4. Dividir\nElegir operación a realizar:")
    if opcion == "1":
        n1 = float(input("Valor 1: "))
        n2 = float(input("Valor 2: "))
        print(f"{n1} + {n2} = {sumar(n1,n2)}")
    elif opcion == "2":
        n1 = float(input("Valor 1: "))
        n2 = float(input("Valor 2: "))
        print(f"{n1} - {n2} = {restar(n1,n2)}")
    elif opcion == "3":
        n1 = float(input("Valor 1: "))
        n2 = float(input("Valor 2: "))
        print(f"{n1} * {n2} = {multiplicar(n1,n2)}")
    elif opcion == "4":
        n1 = float(input("Valor 1: "))
        n2 = float(input("Valor 2: "))
        print(f"{n1} / {n2} = {dividir(n1,n2)}")        

    else:
        print("bye")
        break
