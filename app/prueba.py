import random
from copy import deepcopy
from models import Baraja, Jugador  # Asegúrate de tener estas clases implementadas
from qlearning import AgenteQLearning

# Configuración inicial
def probarIA():
    # Crear baraja y dealer
    baraja = Baraja()
    dealer = Jugador("Dealer")
    ia = AgenteQLearning("IA-Q-Learning")
    
    # Estadísticas
    victorias = 0
    derrotas = 0
    empates = 0
    ciclosEntrenamiento = 50
    numeroSimulaciones = 100
    
    for simulacion in range(numeroSimulaciones):
        print(f"Simulación {simulacion + 1}/{numeroSimulaciones}")
        
        # Reiniciar la baraja y jugadores
        baraja = Baraja()
        random.shuffle(baraja.cartas)
        dealer.mano = []
        ia.mano = []
        
        # Repartir las cartas iniciales
        cartaInicial1 = baraja.repartirCarta()
        cartaInicial2 = baraja.repartirCarta()
        dealer.giveCarta(baraja.repartirCarta())
        dealer.giveCarta(baraja.repartirCarta())
        ia.giveCarta(cartaInicial1)
        ia.giveCarta(cartaInicial2)

        # Entrenamiento con la misma mano
        ia.entrenar(deepcopy(baraja), ciclosEntrenamiento)
        ia.mano = []

        ia.giveCarta(cartaInicial1)
        ia.giveCarta(cartaInicial2)
        
        # Simulación de la partida después del entrenamiento
        manoIA = []
        for i in range (len (ia.mano)):
            manoIA.append(ia.mano[i].__str__())
        
        manoDealer = []
        for i in range (len (dealer.mano)):
            manoIA.append(dealer.mano[i].__str__())
        print(f"Cartas iniciales de IA: {manoIA} | Puntaje: {ia.calcularPuntuacion()}")
        print(f"Cartas iniciales de Dealer: {manoDealer} | Carta visible: {dealer.mano[0].__str__()}")
        
        terminado = False
        while not terminado:
            estado = ia.obtenerEstado(ia.calcularPuntuacion(), dealer.mano[0].valor)
            accion = ia.elegirAccion(estado, baraja)
            if accion == 'pedir':
                ia.giveCarta(baraja.repartirCarta())
                manoIA = []
                for i in range (len (ia.mano)):
                    manoIA.append(ia.mano[i].__str__())
                print(f"IA pide carta: {manoIA} | Puntaje: {ia.calcularPuntuacion()}")
                if ia.calcularPuntuacion() > 21:
                    print("IA se pasó de 21.")
                    terminado = True
            else:
                print("IA se planta.")
                terminado = True

        # Dealer juega
        while dealer.calcularPuntuacion() < 17:
            dealer.giveCarta(baraja.repartirCarta())
            manoDealer = []
            for i in range (len (dealer.mano)):
                manoIA.append(dealer.mano[i].__str__())
            print(f"Dealer toma carta: {manoDealer} | Puntaje: {dealer.calcularPuntuacion()}")

        # Determinar el resultado
        puntajeIA = ia.calcularPuntuacion()
        puntajeDealer = dealer.calcularPuntuacion()
        
        if puntajeIA > 21:
            resultado = "Derrota"
            derrotas += 1
        elif puntajeDealer > 21 or puntajeIA > puntajeDealer:
            resultado = "Victoria"
            victorias += 1
        elif puntajeIA == puntajeDealer:
            resultado = "Empate"
            empates += 1
        else:
            resultado = "Derrota"
            derrotas += 1

        print(f"Resultado de la partida: {resultado}\n")

    # Mostrar estadísticas finales
    print("Estadísticas Finales:")
    print(f"Victorias: {victorias}")
    print(f"Derrotas: {derrotas}")
    print(f"Empates: {empates}")

# Ejecutar las pruebas
if __name__ == "__main__":
    probarIA()
