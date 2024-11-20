import random
import numpy as np
from copy import deepcopy
from .models import Jugador

class AgenteQLearning(Jugador):
    def __init__(self, nombre, tasaAprendizaje=0.1, factorDescuento=0.95, tasaExploracion=1.0, decrecimientoExploracion=0.99):
        super().__init__(nombre)
        self.tablaQ = {}
        self.tasaAprendizaje = tasaAprendizaje
        self.factorDescuento = factorDescuento
        self.tasaExploracion = tasaExploracion
        self.decrecimientoExploracion = decrecimientoExploracion

    def obtenerEstado(self, puntajeJugador, cartaVisibleDealer):
        return (puntajeJugador, cartaVisibleDealer)

    def probabilidadDeNoSuperar21(self, baraja):
        ciclos = 1000
        copiaBaraja = deepcopy(baraja)
        copiaJugador = deepcopy(self)

        noPasarse = 0
        for _ in range(ciclos):
            random.shuffle(copiaBaraja.cartas)
            carta = copiaBaraja.repartirCarta()
            copiaJugador.giveCarta(carta)

            if copiaJugador.calcularPuntuacion() <= 21:
                noPasarse += 1

            copiaBaraja = deepcopy(baraja)
            copiaJugador = deepcopy(self)

        probabilidadNoPasarse = (noPasarse / ciclos) * 100
        return probabilidadNoPasarse

    def elegirAccion(self, estado, baraja):
        if random.random() < self.tasaExploracion:
            return random.choice(['pedir', 'plantarse'])

        # Obtener la probabilidad de no pasarse al pedir una carta
        probabilidadNoPasarse = self.probabilidadDeNoSuperar21(baraja)

        # Usar la tabla Q, pero dar preferencia a "plantarse" si el riesgo es alto
        valoresAccion = self.tablaQ.get(estado, {'pedir': 0, 'plantarse': 0})
        if probabilidadNoPasarse < 30:  # Riesgo alto
            return 'plantarse'
        return max(valoresAccion, key=valoresAccion.get)

    def actualizarValorQ(self, estado, accion, recompensa, siguienteEstado):
        valorAnterior = self.tablaQ.get(estado, {}).get(accion, 0)
        futuroMaximo = max(self.tablaQ.get(siguienteEstado, {'pedir': 0, 'plantarse': 0}).values(), default=0)
        nuevoValor = valorAnterior + self.tasaAprendizaje * (recompensa + self.factorDescuento * futuroMaximo - valorAnterior)

        if estado not in self.tablaQ:
            self.tablaQ[estado] = {}
        self.tablaQ[estado][accion] = nuevoValor

    def calcularRecompensa(self, jugador, baraja):
        puntaje = jugador.calcularPuntuacion()
        if puntaje > 21:
            return -1
        elif puntaje == 21:
            return 1
        elif puntaje >= 17:  # siempre incentivar a quedarse con 17
            return 0.5
        else:
            return 0

    def entrenar(self, baraja, numeroEpisodios=1000):
        for _ in range(numeroEpisodios):
            copiaBaraja = deepcopy(baraja)
            self.mano = []

            self.giveCarta(copiaBaraja.repartirCarta())
            self.giveCarta(copiaBaraja.repartirCarta())
            puntajeJugador = self.calcularPuntuacion()
            cartaVisibleDealer = copiaBaraja.cartas[0].valor
            estado = self.obtenerEstado(puntajeJugador, cartaVisibleDealer)

            terminado = False
            while not terminado:
                accion = self.elegirAccion(estado, copiaBaraja)
                if accion == 'pedir':
                    self.giveCarta(copiaBaraja.repartirCarta())
                else:
                    terminado = True

                siguienteEstado = self.obtenerEstado(self.calcularPuntuacion(), cartaVisibleDealer)
                recompensa = self.calcularRecompensa(self, copiaBaraja)
                self.actualizarValorQ(estado, accion, recompensa, siguienteEstado)

                estado = siguienteEstado

            self.tasaExploracion *= self.decrecimientoExploracion
        
