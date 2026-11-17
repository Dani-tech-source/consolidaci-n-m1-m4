"""Demo: el mismo pedido de modulo1_antes.py, ahora con el código limpio."""
from decimal import Decimal

from repuestos.descuentos import DescuentoPorcentaje
from repuestos.modelos import LineaPedido, Repuesto
from repuestos.notificador import NotificadorConsola
from repuestos.pedido import ServicioPedidos
from repuestos.repositorio import RepositorioEnMemoria


def main() -> None:
    repositorio = RepositorioEnMemoria([
        Repuesto("FIL-001", "Filtro de aceite", Decimal("450"), 10, "Clase C W205"),
        Repuesto("PAS-002", "Pastillas de freno", Decimal("1500"), 4, "Clase E W213"),
    ])
    servicio = ServicioPedidos(repositorio, NotificadorConsola())

    servicio.realizar_pedido(
        "dani@correo.com",
        [LineaPedido("FIL-001", 2), LineaPedido("PAS-002", 1)],
        DescuentoPorcentaje(10),
    )


if __name__ == "__main__":
    main()
