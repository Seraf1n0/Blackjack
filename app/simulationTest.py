import time
from models import Baraja, Jugador
from copy import deepcopy
from qlearning import AgenteQLearning

def simular_juegos_visibles(agent, baraja, numeroJuegos=10):
    for ronda in range(1, numeroJuegos + 1):
        print(f"\n=== RONDA {ronda} ===")
        time.sleep(1)

        # Reiniciar baraja y manos
        copiaBaraja = deepcopy(baraja)
        agent.mano = []  # Resetea la mano del agente
        dealer = Jugador("Dealer")
        dealer.mano = []

        # Repartir dos cartas al jugador y al dealer
        agent.giveCarta(copiaBaraja.repartirCarta())
        agent.giveCarta(copiaBaraja.repartirCarta())
        dealer.giveCarta(copiaBaraja.repartirCarta())
        dealer.giveCarta(copiaBaraja.repartirCarta())

        cartaVisibleDealer = dealer.mano[0].getValor()
        print(f"Cartas iniciales del Dealer: {dealer.mano[0]} (visible)")
        manoIA = []
        for i in range(len(agent.mano)):
            manoIA.append(agent.mano[i].__str__())
        print(f"Cartas iniciales de {agent.nombre}: {manoIA}")
        time.sleep(1)

        estado = agent.obtenerEstado(agent.calcularPuntuacion(), cartaVisibleDealer)

        # Turno del agente
        print(f"Turno de {agent.nombre}")
        terminado = False
        while not terminado:
            accion = agent.elegirAccion(estado)
            print(f"{agent.nombre} decide: {'PEDIR' if accion == 'pedir' else 'PLANTARSE'}")
            time.sleep(1)

            if accion == 'pedir':
                nueva_carta = copiaBaraja.repartirCarta()
                print(f"{agent.nombre} recibe la carta: {nueva_carta}")
                agent.giveCarta(nueva_carta)

                for i in range(len(agent.mano)):
                    manoIA.append(agent.mano[i].__str__())
                print(f"Cartas actuales: {manoIA}, Puntaje: {agent.calcularPuntuacion()}")
                if agent.calcularPuntuacion() > 21:
                    print(f"{agent.nombre} se pasó de 21 puntos!")
                    terminado = True
            else:
                print(f"{agent.nombre} se planta con un puntaje de {agent.calcularPuntuacion()}")
                terminado = True

            siguienteEstado = agent.obtenerEstado(agent.calcularPuntuacion(), cartaVisibleDealer)
            recompensa = agent.calcularRecompensa(agent, copiaBaraja)
            agent.actualizarValorQ(estado, accion, recompensa, siguienteEstado)

            estado = siguienteEstado

        # Turno del dealer
        print("\nTurno del Dealer")
        while dealer.calcularPuntuacion() < 17:
            nueva_carta = copiaBaraja.repartirCarta()
            dealer.giveCarta(nueva_carta)
            print(f"Dealer recibe la carta: {nueva_carta}")
            time.sleep(1)

        manoDealer = []
        for i in range(len(dealer.mano)):
            manoDealer.append(dealer.mano[i].__str__())
        print(f"Cartas finales del Dealer: {manoDealer}, Puntaje: {dealer.calcularPuntuacion()}")
        time.sleep(1)


        puntuacionAgent = agent.calcularPuntuacion()
        puntuacionDealer = dealer.calcularPuntuacion()

        if puntuacionAgent > 21:
            print(f"{agent.nombre} pierde por pasarse de 21.")
        elif puntuacionDealer > 21 or puntuacionAgent > puntuacionDealer:
            print(f"{agent.nombre} gana esta ronda!")
        elif puntuacionAgent == puntuacionDealer:
            print("¡Empate!")
        else:
            print(f"{agent.nombre} pierde contra el Dealer.")

        print("\n=== FIN DE LA RONDA ===")
        time.sleep(2)



if __name__ == "__main__":
    baraja = Baraja()
    agente = AgenteQLearning("IA Blackjack")

    print("Iniciando simulación visible...")
    simular_juegos_visibles(agente, baraja, numeroJuegos=10)
