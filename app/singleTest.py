from models import Baraja, Jugador, Carta
from qlearning import AgenteQLearning

def simular_partida():
    baraja = Baraja()
    
    # Crear jugadores: un humano y el agente QLearning
    jugador_humano = Jugador("Humano")
    agente_ia = AgenteQLearning("Agente Q-Learning")
    dealer = Jugador("Dealer")
    
    # Repartir dos cartas iniciales a todos los jugadores
    for _ in range(2):
        jugador_humano.giveCarta(baraja.repartirCarta())
        agente_ia.giveCarta(baraja.repartirCarta())
        dealer.giveCarta(baraja.repartirCarta())
    
    print(f"\n{jugador_humano}")
    print(f"\n{agente_ia}")
    print(f"\nDealer muestra: {dealer.mano[0]}\n")
    
    # Turno del jugador humano
    while True:
        print(f"Puntuación actual: {jugador_humano.calcularPuntuacion()}")
        decision = input("¿Deseas pedir carta (hit) o plantarte (stand)? ").lower()
        if decision == "hit":
            jugador_humano.giveCarta(baraja.repartirCarta())
            print(f"\n{jugador_humano}")
            if jugador_humano.calcularPuntuacion() > 21:
                print("¡Te has pasado de 21! Has perdido.")
                return
        elif decision == "stand":
            break
        else:
            print("Opción no válida. Por favor escribe 'hit' o 'stand'.")
    
    # Turno del agente QLearning
    print(f"\nTurno de {agente_ia.nombre}:")
    while agente_ia.calcularPuntuacion() < 21:
        estado = agente_ia.obtenerEstado(agente_ia.calcularPuntuacion(), dealer.mano[0].getValor())
        accion = agente_ia.elegirAccion(estado)
        print(f"El agente decide: {accion}")
        if accion == "pedir":
            agente_ia.giveCarta(baraja.repartirCarta())
            print(f"\n{agente_ia}")
            if agente_ia.calcularPuntuacion() > 21:
                print("¡El agente se ha pasado de 21!")
                break
        elif accion == "plantarse":
            break
    
    # Turno del dealer
    print(f"\nTurno del Dealer:")
    while dealer.calcularPuntuacion() < 17:
        dealer.giveCarta(baraja.repartirCarta())
    print(f"\n{dealer}")
    if dealer.calcularPuntuacion() > 21:
        print("¡El dealer se ha pasado de 21!")
    
    # Resultados finales
    print("\nResultados finales:")
    print(f"Jugador Humano: {jugador_humano.calcularPuntuacion()}")
    print(f"Agente Q-Learning: {agente_ia.calcularPuntuacion()}")
    print(f"Dealer: {dealer.calcularPuntuacion()}")
    
    # Determinar el ganador
    def determinar_ganador(puntaje_jugador, puntaje_dealer):
        if puntaje_jugador > 21:
            return "Perdió"
        if puntaje_dealer > 21 or puntaje_jugador > puntaje_dealer:
            return "Ganó"
        if puntaje_jugador == puntaje_dealer:
            return "Empate"
        return "Perdió"
    
    print(f"\nResultado Humano: {determinar_ganador(jugador_humano.calcularPuntuacion(), dealer.calcularPuntuacion())}")
    print(f"Resultado Agente: {determinar_ganador(agente_ia.calcularPuntuacion(), dealer.calcularPuntuacion())}")

if __name__ == "__main__":
    simular_partida()
