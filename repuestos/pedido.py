
from decimal import ROUND_HALF_UP, Decimal
from typing import List

from repuestos.descuentos import Descuento, SinDescuento
from repuestos.modelos import LineaPedido
from repuestos.notificador import Notificador
from repuestos.repositorio import RepositorioRepuestos

TASA_ISV = Decimal("0.15")
CENTAVOS = Decimal("0.01")


class StockInsuficiente(Exception):
    pass


class ServicioPedidos:
    def __init__(self, repositorio: RepositorioRepuestos, notificador: Notificador):
        self._repositorio = repositorio
        self._notificador = notificador

    def calcular_total(
        self, lineas: List[LineaPedido], descuento: Descuento = SinDescuento()
    ) -> Decimal:
        subtotal = self._calcular_subtotal(lineas)
        subtotal_con_descuento = subtotal - descuento.calcular(subtotal)
        return _redondear(subtotal_con_descuento * (1 + TASA_ISV))

    def realizar_pedido(
        self,
        cliente: str,
        lineas: List[LineaPedido],
        descuento: Descuento = SinDescuento(),
    ) -> Decimal:
        self._verificar_existencias(lineas)
        total = self.calcular_total(lineas, descuento)
        self._descontar_existencias(lineas)
        self._notificador.notificar(cliente, f"Su total es L {total}")
        return total

    def _calcular_subtotal(self, lineas: List[LineaPedido]) -> Decimal:
        return sum(
            (self._repositorio.obtener(linea.codigo_repuesto).precio * linea.cantidad
             for linea in lineas),
            Decimal("0"),
        )

    def _verificar_existencias(self, lineas: List[LineaPedido]) -> None:
        for linea in lineas:
            repuesto = self._repositorio.obtener(linea.codigo_repuesto)
            if repuesto.existencias < linea.cantidad:
                raise StockInsuficiente(
                    f"Solo quedan {repuesto.existencias} de {repuesto.nombre}"
                )

    def _descontar_existencias(self, lineas: List[LineaPedido]) -> None:
        for linea in lineas:
            repuesto = self._repositorio.obtener(linea.codigo_repuesto)
            repuesto.existencias -= linea.cantidad
            self._repositorio.guardar(repuesto)


def _redondear(monto: Decimal) -> Decimal:
    return monto.quantize(CENTAVOS, rounding=ROUND_HALF_UP)
