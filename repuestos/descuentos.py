
from decimal import Decimal
from typing import Protocol


class Descuento(Protocol):
    def calcular(self, subtotal: Decimal) -> Decimal:
        """Devuelve el monto a descontar.

        Contrato: el resultado nunca es negativo ni mayor que el subtotal.
        """
        ...


class SinDescuento:
    def calcular(self, subtotal: Decimal) -> Decimal:
        return Decimal("0")


class DescuentoPorcentaje:
    def __init__(self, porcentaje: int):
        if not 0 <= porcentaje <= 100:
            raise ValueError("El porcentaje debe estar entre 0 y 100")
        self._fraccion = Decimal(porcentaje) / 100

    def calcular(self, subtotal: Decimal) -> Decimal:
        return subtotal * self._fraccion


class DescuentoFijo:
    def __init__(self, monto: Decimal):
        if monto < 0:
            raise ValueError("El monto no puede ser negativo")
        self._monto = monto

    def calcular(self, subtotal: Decimal) -> Decimal:
        # min() respeta el contrato (Liskov): un descuento fijo de L 500
        # sobre una compra de L 300 descuenta solo L 300, nunca deja el total negativo.
        return min(self._monto, subtotal)
