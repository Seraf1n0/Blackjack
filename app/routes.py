from flask import render_template, redirect, url_for, request
from . import app
from .models import Carta, Baraja, Jugador
from .qlearning import AgenteQLearning

baraja = Baraja()
jugador = Jugador("Toñito")
dealer = Jugador("Dealer Serafino")
ia1 = AgenteQLearning("Serafino")
ia2 = AgenteQLearning("Pancho")
probabilidadDeGanar = 0
<<<<<<< HEAD

=======
imagenesDealer = []
>>>>>>> 17a926ee28d5f37ec66f1dfcb9ce88145b491817
# Estado del juego: Esto es muy importante pues nos ayuda a validar los turnos y jugadas
estadoJuego = {
    "jugadorTurno": True,
    "ia1Turno": False,
    "ia2Turno": False,
    "dealerTurno": False,
    "finalizado": False,
    "mensajeFinal": ""
}

def repartirInicio():
    global probabilidadDeGanar, imagenesDealer
    for _ in range(2):
        jugador.giveCarta(baraja.repartirCarta())
        dealer.giveCarta(baraja.repartirCarta())
        
        ia1.giveCarta(baraja.repartirCarta())
        ia2.giveCarta(baraja.repartirCarta())
        probabilidadDeGanar = str(jugador.probabilidadDeNoSuperar21(baraja))
    #Para calcular la probabilidad inicial de ganar

    imagenesDealer.append(dealer.mano[0].nombreArchivo)
    imagenesDealer.append("Volteada.png")
    print(imagenesDealer)
@app.route("/juego")
def juego():
    # Si el juego no ha comenzado, repartir las cartas iniciales
    if len(jugador.mano) == 0:
        repartirInicio()

    return render_template("juego.html", 
                           jugadorCartas=jugador.__str__(), 
                           dealerCartas=dealer.__str__(),
                           ia1Cartas=ia1.__str__(),
                           ia2Cartas=ia2.__str__(),
                           jugadorPuntaje=jugador.calcularPuntuacion(), 
                           dealerPuntaje=dealer.calcularPuntuacion(),
                           ia1Puntaje=ia1.calcularPuntuacion(),
                           ia2Puntaje=ia2.calcularPuntuacion(),
                           estadoJuego=estadoJuego,
<<<<<<< HEAD
                           jugadorProbabilidad=probabilidadDeGanar
=======
                           jugadorProbabilidad = probabilidadDeGanar,
                           jugadorInterfaz = jugador,
                           ia1 = ia1,
                           ia2 = ia2,
                           dealer = imagenesDealer

>>>>>>> 17a926ee28d5f37ec66f1dfcb9ce88145b491817
)

@app.route("/hit")
def hit():
    global probabilidadDeGanar
    # Solo se permite pedir carta si es turno del jugador, sino no
    if estadoJuego["jugadorTurno"] and not estadoJuego["finalizado"]:
        jugador.giveCarta(baraja.repartirCarta())
        probabilidadDeGanar = str(jugador.probabilidadDeNoSuperar21(baraja))
        if jugador.calcularPuntuacion() > 21:
            estadoJuego["jugadorTurno"] = False
            estadoJuego["ia1Turno"] = True
            estadoJuego["ia2Turno"] = True

    return redirect(url_for('procesarTurnos'))

@app.route("/stand")
def stand():
    global probabilidadDeGanar
    # Si es el turno del Jugador pasamos al tirno de la IA 1 
    if estadoJuego["jugadorTurno"] and not estadoJuego["finalizado"]:
        estadoJuego["jugadorTurno"] = False
        estadoJuego["ia1Turno"] = True
        estadoJuego["ia2Turno"] = True
        probabilidadDeGanar = str(jugador.probabilidadDeNoSuperar21(baraja))
        
    return redirect(url_for('procesarTurnos'))

@app.route("/procesarTurnos")
def procesarTurnos():
    global probabilidadDeGanar
    # Turno de IA 1 Serafino
    if estadoJuego["ia1Turno"] and not estadoJuego["finalizado"]:
        # Se entrena a la IA con la mano actual antes de hacer la jugada
        ia1.entrenar(baraja, numeroEpisodios=25)
        accion = ia1.elegirAccion(ia1.obtenerEstado(ia1.calcularPuntuacion(), dealer.mano[0].valor), baraja)
        if accion == "pedir":
            ia1.giveCarta (baraja.repartirCarta())
        else:
            estadoJuego["ia1Turno"] = False
            estadoJuego["ia2Turno"] = True
    
    # Turno de IA 2 Pancho
    if estadoJuego["ia2Turno"] and not estadoJuego["finalizado"]:
        # Entrenamos a la IA con la mano actual anres de hacer la jugada
        ia2.entrenar(baraja, numeroEpisodios=25)
        accion = ia2.elegirAccion(ia2.obtenerEstado(ia2.calcularPuntuacion(), dealer.mano[0].valor), baraja)
        if accion == "pedir":
            ia2.giveCarta(baraja.repartirCarta())
        else:
            estadoJuego["ia2Turno"] = False
            estadoJuego["dealerTurno"] = True

    # Turno de Serafino
    if estadoJuego["dealerTurno"] and not estadoJuego["finalizado"]:
        while dealer.calcularPuntuacion() < 17:
            dealer.giveCarta(baraja.repartirCarta())
        estadoJuego["dealerTurno"] = False
        estadoJuego["finalizado"] = True
        evaluarResultado()

    probabilidadDeGanar = str(jugador.probabilidadDeNoSuperar21(baraja))
    return redirect(url_for('juego'))

@app.route("/nuevaRonda")
def nuevaRonda():
    global probabilidadDeGanar
    # Unicamente se cambia el estado del juego para que las manos sean reiniciadas y el estado del juego tambien
    # Limpiar las manos de todos los jugadores para repartir nuevamente
    jugador.mano = []
    dealer.mano = []
    ia1.mano = []
    ia2.mano = []
    print("Reiniciando todo")
    # Repartir las cartas iniciales
    for _ in range(2):
        jugador.giveCarta(baraja.repartirCarta())
        dealer.giveCarta(baraja.repartirCarta())
        ia1.giveCarta(baraja.repartirCarta())
        ia2.giveCarta(baraja.repartirCarta())

    # El estado del juego se da turno al jugador
    estadoJuego.update({
        "jugadorTurno": True,
        "ia1Turno": False,
        "ia2Turno": False,
        "dealerTurno": False,
        "finalizado": False,
        "mensajeFinal": ""
    })

    probabilidadDeGanar = str(jugador.probabilidadDeNoSuperar21(baraja))
    return redirect(url_for('juego'))


def evaluarResultado():
    """
    Determina quién ganó o perdió y actualiza el estado del juego con el mensaje final.
    """
    jugadorPuntaje = jugador.calcularPuntuacion()
    dealerPuntaje = dealer.calcularPuntuacion()

    if jugadorPuntaje > 21:
        estadoJuego["mensajeFinal"] = "¡Te pasaste de 21, perdiste!"
    elif dealerPuntaje > 21 or jugadorPuntaje > dealerPuntaje:
        estadoJuego["mensajeFinal"] = "¡Ganaste!"
    elif jugadorPuntaje < dealerPuntaje:
        estadoJuego["mensajeFinal"] = "¡El dealer ganó!"
    else:
        estadoJuego["mensajeFinal"] = "¡Empate!"

    # Actualizamos los turnos
    estadoJuego["jugadorTurno"] = False
    estadoJuego["ia1Turno"] = False
    estadoJuego["ia2Turno"] = False
    estadoJuego["dealerTurno"] = False
