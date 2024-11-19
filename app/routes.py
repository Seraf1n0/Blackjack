from flask import render_template, redirect, url_for, request
from . import app
from .models import Carta, Baraja, Jugador


baraja = Baraja()
jugador = Jugador("Toñito")
dealer = Jugador("Dealer Serafino")
ia1 = Jugador("Cold Lettuce")
ia2 = Jugador("Pop-eye")

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
    for _ in range(2):
        jugador.giveCarta(baraja.repartirCarta())
        dealer.giveCarta(baraja.repartirCarta())
        ia1.giveCarta(baraja.repartirCarta())
        ia2.giveCarta(baraja.repartirCarta())

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
                           estadoJuego=estadoJuego)

@app.route("/hit")
def hit():
    # Solo se permite pedir carta si es turno del jugador, sino no
    if estadoJuego["jugadorTurno"] and not estadoJuego["finalizado"]:
        jugador.giveCarta(baraja.repartirCarta())
        if jugador.calcularPuntuacion() > 21:
            estadoJuego["jugadorTurno"] = False
            estadoJuego["ia1Turno"] = True

    return redirect(url_for('procesarTurnos'))

@app.route("/stand")
def stand():
    # Si es el turno del Jugador pasamos al tirno de la IA 1 
    if estadoJuego["jugadorTurno"] and not estadoJuego["finalizado"]:
        estadoJuego["jugadorTurno"] = False
        estadoJuego["ia1Turno"] = True

    return redirect(url_for('procesarTurnos'))

@app.route("/procesarTurnos")
def procesarTurnos():
    # Turno de IA 1
    if estadoJuego["ia1Turno"] and not estadoJuego["finalizado"]:
        if ia1.calcularPuntuacion() < 17:
            ia1.giveCarta(baraja.repartirCarta())
        if ia1.calcularPuntuacion() > 21 or ia1.calcularPuntuacion() >= 17:
            estadoJuego["ia1Turno"] = False
            estadoJuego["ia2Turno"] = True

    # Turno de IA 2
    elif estadoJuego["ia2Turno"] and not estadoJuego["finalizado"]:
        if ia2.calcularPuntuacion() < 17:
            ia2.giveCarta(baraja.repartirCarta())
        if ia2.calcularPuntuacion() > 21 or ia2.calcularPuntuacion() >= 17:
            estadoJuego["ia2Turno"] = False
            estadoJuego["dealerTurno"] = True

    # Turno de Serafino
    elif estadoJuego["dealerTurno"] and not estadoJuego["finalizado"]:
        while dealer.calcularPuntuacion() < 17:
            dealer.giveCarta(baraja.repartirCarta())
        estadoJuego["dealerTurno"] = False
        estadoJuego["finalizado"] = True
        evaluarResultado()

    return redirect(url_for('juego'))

@app.route("/nuevaRonda")
def nuevaRonda():
    # Unicamente se cambia el estado del juego para que las manos sean reiniciadas y el estado del juego tambien
    # Limpiar las manos de todos los jugadores para repartir nuevamente
    jugador.mano = []
    dealer.mano = []
    ia1.mano = []
    ia2.mano = []

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
