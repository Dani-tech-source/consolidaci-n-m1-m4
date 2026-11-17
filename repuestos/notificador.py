"""Notificaciones.

I (Segregación de interfaces): la interfaz tiene un solo método, lo único que
ServicioPedidos necesita. No obliga a implementar SMS, WhatsApp y correo a la vez.
"""
from typing import Protocol


class Notificador(Protocol):
    def notificar(self, cliente: str, mensaje: str) -> None:
        ...


class NotificadorConsola:
    def notificar(self, cliente: str, mensaje: str) -> None:
        print(f"Para {cliente}: {mensaje}")
