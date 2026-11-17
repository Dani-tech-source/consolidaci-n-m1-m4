from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Repuesto:
    codigo: str
    nombre: str
    precio: Decimal
    existencias: int
    modelo_compatible: str


@dataclass(frozen=True)
class LineaPedido:
    codigo_repuesto: str
    cantidad: int
