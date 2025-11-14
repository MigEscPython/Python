import os
import time
while True:
    opcion = input("1. Calc \n2. Apagar \n3. Test internet")
    if opcion == "1":
        os.system("calc")
    elif opcion == "2":
        os.system("shutdown -s -t 100")
    elif opcion == "3":
        ip = input("Ingrese IP: ")
        os.system(f"ping {ip}")
    else:
        break

    time.sleep(5)
    os.system("cls")