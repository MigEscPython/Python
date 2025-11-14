#Suma de valores
v = -1
suma = 0
while True:
    v = int(input("Ingrese un Nro Z+"))
    if v > 0 :
        suma += v
    elif v == 0:
        break

print(f"La suma es: {suma}")