from flask import render_template, redirect, url_for, request
from . import app
from .models import Carta, Baraja, Jugador

baraja = Baraja()
jugador = Jugador("Toñito")
dealer = Jugador("Dealer Serafino")
ia_1 = Jugador("Cold Lettuce")
ia_2 = Jugador("Pop-eye")

def repartirInicio():
    for _ in range(2):
        jugador.giveCarta(baraja.repartirCarta())
        dealer.giveCarta(baraja.repartirCarta())
        ia_1.giveCarta(baraja.repartirCarta())
        ia_2.giveCarta(baraja.repartirCarta())

@app.route("/juego")
def juego():
    repartirInicio()
    return render_template("juego.html", 
                           jugador_cartas=jugador.__str__(), 
                           dealer_cartas=dealer.__str__(),
                           ia1_cartas=ia_1.__str__(),
                           ia2_cartas=ia_2.__str__(),
                           jugador_puntaje=jugador.calcularPuntuacion(), 
                           dealer_puntaje=dealer.calcularPuntuacion(),
                           ia1_puntaje=ia_1.calcularPuntuacion(),
                           ia2_puntaje=ia_2.calcularPuntuacion())


@app.route("/hit")
def hit():
    jugador.giveCarta(baraja.repartirCarta())
    if jugador.calcularPuntuacion() > 21:
        jugador.mano = []
        return redirect(url_for('resultado', mensaje="Te pasaste de 21, ¡perdiste!"))

    for ia in [ia_1, ia_2]:
        if ia.calcularPuntuacion() < 17:  # La ia tiene un puntaje menos a 17 y decide pedir
            ia.giveCarta(baraja.repartirCarta())
        if ia.calcularPuntuacion() > 21:
            ia.mano = []
            return redirect(url_for('resultado', mensaje=f"{ia.nombre} se pasó de 21"))

    # Turno del dealer serafinito
    if dealer.calcularPuntuacion() < 17:
        dealer.giveCarta(baraja.repartirCarta())
    if dealer.calcularPuntuacion() > 21:
        dealer.mano = []
        return redirect(url_for('resultado', mensaje="El dealer se pasó de 21, ¡ganaste!"))

    return redirect(url_for('juego'))

@app.route("/resultado")
def resultado():
    mensaje = request.args.get("mensaje")
    return render_template("resultado.html", mensaje=mensaje)