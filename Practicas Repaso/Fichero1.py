texto = input('Introduce un texto: ')
nombre_fichero = 'archivo-' + texto + '.txt'
f = open(nombre_fichero, 'w') #apertura w= write, r= read, a= append
f.write(f'{texto}\n')
f.close()

print("Contenido de agenda.txt")
leerfichero = open(nombre_fichero, 'r')
print(leerfichero.read())
leerfichero.close()

print("Contenido de agenda.txt")
leerfichero = open(nombre_fichero, 'a')
print(leerfichero.append())
leerfichero.close()
