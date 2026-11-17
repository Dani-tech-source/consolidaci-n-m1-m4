
import contextlib
import io
import unittest
from decimal import Decimal

import modulo1_antes
from repuestos.descuentos import DescuentoPorcentaje, SinDescuento
from repuestos.modelos import LineaPedido, Repuesto
from repuestos.notificador import NotificadorConsola
from repuestos.pedido import ServicioPedidos
from repuestos.repositorio import RepositorioEnMemoria

PRECIOS = {"FIL-001": 450, "PAS-002": 1500, "AMO-003": 3200}

# tipo de descuento del código viejo -> objeto equivalente del código nuevo
DESCUENTOS = {
    0: SinDescuento(),
    1: DescuentoPorcentaje(10),
    2: DescuentoPorcentaje(20),
}

CASOS = [
    ([("FIL-001", 1)], 0),
    ([("FIL-001", 2), ("PAS-002", 1)], 1),
    ([("AMO-003", 2), ("PAS-002", 3)], 2),
]


def total_codigo_viejo(lineas, tipo_descuento):
    modulo1_antes.d = {
        codigo: {"n": codigo, "p": precio, "s": 100} for codigo, precio in PRECIOS.items()
    }
    with contextlib.redirect_stdout(io.StringIO()):
        return modulo1_antes.proc("cliente", lineas, tipo_descuento)


def total_codigo_nuevo(lineas, tipo_descuento):
    repositorio = RepositorioEnMemoria(
        Repuesto(codigo, codigo, Decimal(precio), 100, "-")
        for codigo, precio in PRECIOS.items()
    )
    servicio = ServicioPedidos(repositorio, NotificadorConsola())
    return servicio.calcular_total(
        [LineaPedido(codigo, cantidad) for codigo, cantidad in lineas],
        DESCUENTOS[tipo_descuento],
    )


class TestRefactorSeguro(unittest.TestCase):
    def test_el_codigo_nuevo_calcula_lo_mismo_que_el_viejo(self):
        for lineas, tipo_descuento in CASOS:
            with self.subTest(lineas=lineas, descuento=tipo_descuento):
                viejo = total_codigo_viejo(lineas, tipo_descuento)
                nuevo = total_codigo_nuevo(lineas, tipo_descuento)
                self.assertAlmostEqual(float(nuevo), viejo, places=2)


if __name__ == "__main__":
    unittest.main()
