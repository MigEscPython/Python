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