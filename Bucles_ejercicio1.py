### De dos numeros ingresados, muestra el numero mayor y a la vez si es par o impar
num1 = float(input('Ingrese primer numero:'))
num2 = float(input('Ingrese segundo numero:'))

if num1 > num2:
    print("El primer numero es mayor:", num1)
    if num1 % 2 == 1:
        print("Este numero es IMPAR")
    else:
        print("Este numero es PAR")
elif num1 == num2:
    print("Los numeros son inguales:", num1, num2)
else:
    print("El segundo numero es mayor:", num2)
    if num2 % 2 == 1:
        print("Este numero es IMPAR")
    else:
        print("Este numero es PAR")

