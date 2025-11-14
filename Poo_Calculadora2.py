class Calculadora:
    '''Clase Calculadora que suma dos numeros'''
    #atributos ¿?
    n1,n2 = None, None
    #constructor
    def __init__(self):
        self.n1 = 0
        self.n2 = 0

    def cargaNumeros(self,x,y):
        self.n1 = x
        self.n2 = y

    def sumar(self):
        return self.n1 + self.n2
    
#CalculadoraCientifica hereda de Calculadora
class CalculadoraCientifica(Calculadora):
    '''Hereda de Calculadora, implementa,
    factorial, raiz cuadrada y potencia'''
    def __init__(self):
        super() #llama al constructor de la clase heredada

    def factorial(self):
        ac = 1
        for x in range(1,(self.n1+1)):
            ac = ac * x

        return ac
    
    def calculadoraPotencia(self, base, exponente):
        return base ** exponente
    
    def calculadoraRaizCuadrada(self, valor):
        return valor ** (0.5)
    

if __name__ == "__main__":
    print("Calculadora normal")
    casio = Calculadora()                       #Declaracion y construccion
    casio.cargaNumeros(15,9)                    #metodos
    print(f"La suma es {casio.sumar()}")        #metodos

print("Calculadora cientifica")
casioFX = CalculadoraCientifica()
casioFX.cargaNumeros(5,4)
print(f"La suma es {casioFX.sumar()}")
print(f"El factorial de 5 es: {casioFX.factorial()}")
print(f"Raiz de 25 es: {casioFX.calculadoraRaizCuadrada(25)}")
print(f"5² : {casioFX.calculadoraPotencia(5,2)}")




