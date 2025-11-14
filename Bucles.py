#limite 100
contador = 0
for x in range(100):
    contador += 1
    if x % 2 != 0 :
        print("Valor de x:", x)

print("bucle:", contador)

contador = 0
for x in range(5, 100):
    contador += 1
    if x % 2 != 0 :
        print("Valor de x:", x)

print("bucle:", contador)

contador = 0
for x in range(5,100,5):
    contador += 1
    if x % 2 != 0 :
        print("Valor de x:", x)

print("bucle:", contador)