from decimal import Decimal

MONTO_ENVIO_GRATIS = Decimal ("3000")
COSTO_ENVIO = Decimal("150")


def calcular_envio(subtotal: Decimal) -> Decimal:
 if subtotal >= MONTO_ENVIO_GRATIS:
   return Decimal("0")
 return COSTO_ENVIO

