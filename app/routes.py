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
imagenesDealer = []
# Estado del juego: Esto es muy importante pues nos ayuda a validar los turnos y jugadas
estadoJuego = {
    "jugadorTurno": True,
    "ia1Turno": False,
    "ia2Turno": False,
    "dealerTurno": False,
    "finalizado": False,
    "mensajeFinal": "",
    "juegaJugador": True, #Para saber si aún tienen chance de jugar y revisar el texto
    "juegaIA1": False, #En primera instancia false para que no los revise
    "juegaIA2": False,
    "juegaDealer": False,
    "jugadaIA1": "", #Estos textos son para ingresar si se plantó o no
    "jugadaIA2": "",
    "jugadaDealer": ""
}

@app.route("/")
def index():
    return render_template("inicio.html")

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
    # Si el juego no ha comenzado, repartir las cartas iniciales. Primero va a jugar la persona y luego las ias
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
                           jugadorProbabilidad = probabilidadDeGanar,
                           jugadorInterfaz = jugador,
                           ia1 = ia1,
                           ia2 = ia2,
                           dealer = imagenesDealer
)

@app.route("/hit")
def hit():
    global probabilidadDeGanar
    if estadoJuego["jugadorTurno"] and not estadoJuego["finalizado"]:
        jugador.giveCarta(baraja.repartirCarta())
        probabilidadDeGanar = str(jugador.probabilidadDeNoSuperar21(baraja))
        if jugador.calcularPuntuacion() > 21:  # Si el jugador se pasa, automáticamente pasa al siguiente turno
            estadoJuego["jugadorTurno"] = False
            estadoJuego["ia1Turno"] = True
            return redirect(url_for('procesarTurnos'))

    return redirect(url_for('juego'))

@app.route("/stand")
def stand():
    if estadoJuego["jugadorTurno"] and not estadoJuego["finalizado"]:
        estadoJuego["jugadorTurno"] = False
        estadoJuego["ia1Turno"] = True
        return redirect(url_for('procesarTurnos'))
    return redirect(url_for('juego'))

@app.route("/procesarTurnos")
def procesarTurnos():
    global probabilidadDeGanar

    # Turno de IA 1
    if estadoJuego["ia1Turno"] and not estadoJuego["finalizado"]:
        while True:
            if ia1.calcularPuntuacion() > 21:  # Si la IA ya está fuera del juego, se pasa al siguiente turno
                estadoJuego["ia1Turno"] = False
                estadoJuego["ia2Turno"] = True
                estadoJuego["juegaIA1"] = False
                estadoJuego["jugadaIA1"] = "Se pasó de 21"
                break

            ia1.entrenar(baraja, numeroEpisodios=5)
            accion = ia1.elegirAccion(ia1.obtenerEstado(ia1.calcularPuntuacion(), dealer.mano[0].valor), baraja)

            if accion == "plantarse":
                estadoJuego["ia1Turno"] = False
                estadoJuego["ia2Turno"] = True
                estadoJuego["jugadaIA1"] = "Se plantó"
                break
            else:
                ia1.giveCarta(baraja.repartirCarta())

    # Turno de IA 2
    if estadoJuego["ia2Turno"] and not estadoJuego["finalizado"]:
        while True:
            if ia2.calcularPuntuacion() > 21:  # Si la IA ya está fuera del juego, se pasa al siguiente turno
                estadoJuego["ia2Turno"] = False
                estadoJuego["dealerTurno"] = True
                estadoJuego["juegaIA2"] = False  # Indicar que ya no puede jugar
                estadoJuego["jugadaIA2"] = "Se pasó de 21"
                break

            ia2.entrenar(baraja, numeroEpisodios=5)
            accion = ia2.elegirAccion(ia2.obtenerEstado(ia2.calcularPuntuacion(), dealer.mano[0].valor), baraja)

            if accion == "plantarse":
                estadoJuego["ia2Turno"] = False
                estadoJuego["dealerTurno"] = True
                estadoJuego["jugadaIA2"] = "Se plantó"
                break
            else:
                ia2.giveCarta(baraja.repartirCarta())

    # Turno del Dealer
    if estadoJuego["dealerTurno"] and not estadoJuego["finalizado"]:
        while dealer.calcularPuntuacion() < 17:
            dealer.giveCarta(baraja.repartirCarta())
        estadoJuego["dealerTurno"] = False
        estadoJuego["finalizado"] = True
        evaluarResultado()

    return redirect(url_for('juego'))


@app.route("/nuevaRonda")
def nuevaRonda():
    global probabilidadDeGanar, baraja
    # Unicamente se cambia el estado del juego para que las manos sean reiniciadas y el estado del juego tambien
    # Limpiar las manos de todos los jugadores para repartir nuevamente
    baraja = Baraja() #Para reiniciar la baraja
    jugador.mano = []
    dealer.mano = []
    ia1.mano = []
    ia2.mano = []
    print("Reiniciando todo")
    print(f"Cantidad de cartas en la baraja: {len(baraja.cartas)}")
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
    #estadoJuego["jugadorTurno"] = False
    #estadoJuego["ia1Turno"] = False
    #estadoJuego["ia2Turno"] = False
    #estadoJuego["dealerTurno"] = False
