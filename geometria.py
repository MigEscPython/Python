PI = 3.14

def menu():
    print("1. Calcular área del triangulo")
    print("2. Calcular perimetro del triangulo")
    print("3. Calcular área del rectangulo")
    print("4. Calcular perimetro del rectangulo")
    print("5. Calcular área del elipse")
    print("6. Calcular perimetro del elipse")
    print("0. Salir")
    op = input("Opcion: ")
    return op

def getAreaTriangulo(base, altura):
    return (base * altura) /2

def getPerimetroTriangulo(lado1, lado2, lado3):
    return lado1 + lado2 + lado3

def getAreaRectangulo(largo,ancho):
    return largo * ancho

def getPerimetroRectangulo(largo,andcho):
    return (largo + ancho) * 2

def getAreaElipse(semiejemayor, semiejemenor, PI):
    return semiejemayor * semiejemenor * PI

def getPerimetroElipse(PI,semiejemayor,semiejemenor):
    return 2*PI*((semiejemayor**2+semiejemenor**2)/2)**(0.5)

if __name__ == "__main__":
    while True:
        opcion = menu()
        if opcion == "1":
            base = float(input("Base: "))
            altura = float(input("Altura: "))
            resultado = getAreaTriangulo(base, altura)
            print(f"El area es {resultado} u²")
        elif opcion == "2":
            l1 = float(input("Lado 1: "))
            l2 = float(input("Lado 2: "))
            l3 = float(input("Lado 3: "))
            resultado = getPerimetroTriangulo(l1,l2,l3)
            print(f"El perimetro es {resultado}")
        elif opcion == "3":
            largo = float(input("Largo: "))
            ancho = float(input("Ancho: "))
            resultado = getAreaRectangulo(largo,ancho)
            print(f"El area es {resultado}")
        elif opcion == "4":
            largo = float(input("Largo: "))
            ancho = float(input("Ancho: "))
            resultado = getPerimetroRectangulo(largo,ancho)
            print(f"El perimetro es {resultado}")
        elif opcion == "5":
            semiejemayor = float(input("Semieje Mayor: "))
            semiejemenor = float(input("Semieje Menor: "))
            resultado = getAreaElipse(semiejemayor,semiejemenor,PI)
            print(f"El area es {resultado}")
        elif opcion == "6":
            semiejemayor = float(input("Semieje Mayor: "))
            semiejemenor = float(input("Semieje Menor: "))
            resultado = getAreaElipse(PI,semiejemayor,semiejemenor)
            print(f"El perimetro es {resultado}")
        elif opcion == "0":
            break