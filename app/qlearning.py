import random
import numpy as np
from copy import deepcopy
from models import Jugador

class AgenteQLearning(Jugador):
    def __init__(self, nombre, tasaAprendizaje=0.1, factorDescuento=0.95, tasaExploracion=1.0, decrecimientoExploracion=0.99):
        super().__init__(nombre)  # Inicializamos como un jugador más por lo tanto heremcia
        self.tablaQ = {}  # Tabla Q almacenada como un diccionario {estado: {acción: valor}}
        self.tasaAprendizaje = tasaAprendizaje
        self.factorDescuento = factorDescuento
        self.tasaExploracion = tasaExploracion
        self.decrecimientoExploracion = decrecimientoExploracion

    """
    Genera un estado único combinando el puntaje del jugador y la carta visible del dealer.
    """
    def obtenerEstado(self, puntajeJugador, cartaVisibleDealer):
        return (puntajeJugador, cartaVisibleDealer)

    """
    Selecciona una acción (pedir carta o plantarse) basada en la política ε-greedy.
    """
    def elegirAccion(self, estado):
        if random.random() < self.tasaExploracion:
            return random.choice(['pedir', 'plantarse'])  # Exploración
        return max(self.tablaQ.get(estado, {'pedir': 0, 'plantarse': 0}), key=self.tablaQ.get(estado, {}).get)  # Explotación

    """
    Actualiza el valor Q usando la fórmula del aprendizaje reforzado.
    """
    def actualizarValorQ(self, estado, accion, recompensa, siguienteEstado):
        valorAnterior = self.tablaQ.get(estado, {}).get(accion, 0)
        futuroMaximo = max(self.tablaQ.get(siguienteEstado, {'pedir': 0, 'plantarse': 0}).values(), default=0)
        nuevoValor = valorAnterior + self.tasaAprendizaje * (recompensa + self.factorDescuento * futuroMaximo - valorAnterior)

        if estado not in self.tablaQ:
            self.tablaQ[estado] = {}
        self.tablaQ[estado][accion] = nuevoValor

    """
    Entrena la IA simulando rondas de Blackjack.
    """
    def entrenar(self, baraja, numeroEpisodios=1000):
        for _ in range(numeroEpisodios):
            copiaBaraja = deepcopy(baraja)
            self.mano = []  # Resetea la mano del agente


            self.giveCarta(copiaBaraja.repartirCarta())
            self.giveCarta(copiaBaraja.repartirCarta())
            puntajeJugador = self.calcularPuntuacion()
            cartaVisibleDealer = copiaBaraja.cartas[0].valor
            estado = self.obtenerEstado(puntajeJugador, cartaVisibleDealer)

            terminado = False
            while not terminado:
                accion = self.elegirAccion(estado)
                if accion == 'pedir':
                    self.giveCarta(copiaBaraja.repartirCarta())
                else:  # plantarse
                    terminado = True

                siguienteEstado = self.obtenerEstado(self.calcularPuntuacion(), cartaVisibleDealer)
                recompensa = self.calcularRecompensa(self, copiaBaraja)
                self.actualizarValorQ(estado, accion, recompensa, siguienteEstado)

                estado = siguienteEstado

            self.tasaExploracion *= self.decrecimientoExploracion

    def calcularRecompensa(self, jugador, baraja):
        if jugador.calcularPuntuacion() > 21:
            return -1
        elif jugador.calcularPuntuacion() == 21:
            return 1
        else:
            return 0
