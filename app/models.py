# En este archivo van a estar todos los modelos necesarios para la app
import random
import copy
"""
"""
class Carta:
    def __init__(self, valor, palo):
        self.valor = valor
        self.palo = palo
        self.nombreArchivo = valor + "-"+palo +".png"
        
        #Llamarlo valor-palo
    def __str__(self):
        return f"{self.valor} de {self.palo}" # Ejm: 4 de picas uwu
    
    def getValor (self):
        if (self.valor in ["J", "Q", "K"]):
            return 10
        elif (self.valor == "A"):
            return 11 # Esto puede ser 1 o 11 dependiendo del estado de la mano
        else:
            return int(self.valor)
        
class Baraja:
    palos = ["Corazones", "Diamantes", "Tréboles", "Picas"]
    valores = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    
    def __init__(self):
        self.cartas = []
        for palo in self.palos:
            for valor in self.valores:
                self.cartas.append(Carta(valor, palo))
        
        random.shuffle (self.cartas) # Mezclado de cartas
    
    def repartirCarta (self):
        if (self.cartas):
            return self.cartas.pop() # Tomar la carta on top uwu
        else:
            return None # Carta vacia y en caso de que se retorne nulo traemos nueva baraja
        

class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.mano = []
    
    def giveCarta (self, carta):
        self.mano.append(carta)
    
    def calcularPuntuacion (self):
        puntaje = 0
        for carta in self.mano:
            puntaje += carta.getValor ()
        # Esto en caso de que las aces que son 11 o 1
        aces = 0
        for carta in self.mano:
            if carta.valor == "A":
                aces += 1
        
        # Buclesito para tratar de usar aces como 1 en lugar de 11 en caso de que se pase
        while (puntaje > 21 and aces != 0):
            puntaje -= 10
            aces -= 1
        return puntaje
    
    def __str__(self):
        return f"{self.nombre} tiene: {[str(carta) for carta in self.mano]}"
    
    def probabilidadDeNoSuperar21(self, baraja):
        ciclos = 1000
        copiaBaraja = copy.deepcopy(baraja) #Copio la baraja para no afectar las simulaciones siguientes
        copiaJugador = copy.deepcopy(self) 
        #Simulo tomar una carta para ver que sucede
        tomarCarta = 0
        noTomarCarta = 0
        for i in range(ciclos):
            random.shuffle(copiaBaraja.cartas) #La mezclo para que no sea siempre el mismo orden
            carta = copiaBaraja.repartirCarta() #Tomo una carta de la baraja
            copiaJugador.giveCarta(carta) #Le pongo la carta al jugador

            #Ahora calculo su puntuación para ver si se pasa de 21
            if(copiaJugador.calcularPuntuacion() > 21):
                noTomarCarta += 1 #Falló, entonces sumo 1 a no tomar carta
            else:
                tomarCarta +=1
            #Reseteo la baraja y el jugador para simular otra vez
            copiaBaraja = copy.deepcopy(baraja)
            copiaJugador = copy.deepcopy(self) 
        

        probabilidadFracaso = (noTomarCarta / ciclos) * 100
        return int(probabilidadFracaso)

def prueba():
    jugador = Jugador("Leche agria")
    baraja = Baraja()

    #Le doy al menos dos cartas
    for i in range(2):
        jugador.giveCarta(baraja.repartirCarta())
    
    #Para ver la puntuación actual
    print(f"Puntuación actual: {jugador.calcularPuntuacion()}")
    #Montecarlos
    jugador.probabilidadDeNoSuperar21(baraja)
prueba()