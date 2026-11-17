"""Acceso a datos.

D (Inversión de dependencias): ServicioPedidos depende de la abstracción
RepositorioRepuestos, no de una base de datos concreta. Hoy se usa una versión
en memoria; mañana podría ser SQL Server sin tocar la lógica de negocio.
"""
from typing import Iterable, Protocol

from repuestos.modelos import Repuesto


class RepuestoNoEncontrado(Exception):
    pass


class RepositorioRepuestos(Protocol):
    def obtener(self, codigo: str) -> Repuesto:
        ...

    def guardar(self, repuesto: Repuesto) -> None:
        ...


class RepositorioEnMemoria:
    def __init__(self, repuestos: Iterable[Repuesto] = ()):
        self._repuestos = {repuesto.codigo: repuesto for repuesto in repuestos}

    def obtener(self, codigo: str) -> Repuesto:
        try:
            return self._repuestos[codigo]
        except KeyError:
            raise RepuestoNoEncontrado(codigo) from None

    def guardar(self, repuesto: Repuesto) -> None:
        self._repuestos[repuesto.codigo] = repuesto
