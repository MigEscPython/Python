import sqlite3

conexion = sqlite3.connect("bdTraductor.db")
cursor = conexion.cursor()

# Verificar si existe la tabla 'traductor'
cursor.execute("""
SELECT name FROM sqlite_master 
WHERE type='table' AND name='traductor';
""")

tabla = cursor.fetchone()

if tabla:
    print("La tabla 'traductor' ya existe. No se recargan los datos.")
else:
    conexion.execute("""
    CREATE TABLE traductor (id INTEGER PRIMARY KEY AUTOINCREMENT, espanol TEXT, ingles TEXT)""")
    print("Se creó la tabla 'traductor'.")
    #cargar datos, mejorar el codigo
    conexion=sqlite3.connect("bdTraductor.db")
    conexion.execute("insert into traductor(espanol, ingles) values (?,?)", ('casa', 'house'))
    conexion.execute("insert into traductor(espanol, ingles) values (?,?)", ('lapiz', 'pen'))
    conexion.execute("insert into traductor(espanol, ingles) values (?,?)", ('oro', 'gold'))
    conexion.commit()

conexion.close()



while True:
    print("Traductor ESPAÑOL a INGLES")
    palabra = input("Ingrese una palabra a traducir: ")
    conexion=sqlite3.connect("bdTraductor.db")
    sentencia = f"select ingles from traductor"
    cursor=conexion.execute(sentencia)

    for registro in cursor:
        print(f"{palabra} : {registro[0]}")
    conexion.close()