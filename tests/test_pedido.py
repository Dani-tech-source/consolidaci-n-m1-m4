"""Pruebas del servicio de pedidos con dobles de prueba.

- Fake: RepositorioEnMemoria reemplaza a la base de datos real.
- Mock: Mock(spec=Notificador) reemplaza al envío de correos y permite
  verificar que se llamó, sin mandar nada de verdad.
"""
import unittest
from decimal import Decimal
from unittest.mock import Mock

from repuestos.descuentos import DescuentoPorcentaje
from repuestos.modelos import LineaPedido, Repuesto
from repuestos.notificador import Notificador
from repuestos.pedido import ServicioPedidos, StockInsuficiente
from repuestos.repositorio import RepositorioEnMemoria, RepuestoNoEncontrado


def crear_repositorio():
    return RepositorioEnMemoria([
        Repuesto("FIL-001", "Filtro de aceite", Decimal("450"), 10, "Clase C W205"),
        Repuesto("PAS-002", "Pastillas de freno", Decimal("1500"), 4, "Clase E W213"),
    ])


class TestServicioPedidos(unittest.TestCase):
    def setUp(self):
        self.repositorio = crear_repositorio()
        self.notificador = Mock(spec=Notificador)
        self.servicio = ServicioPedidos(self.repositorio, self.notificador)

    def test_total_incluye_isv_del_15_por_ciento(self):
        # Arrange
        lineas = [LineaPedido("FIL-001", 2)]  # 2 x 450 = 900
        # Act
        total = self.servicio.calcular_total(lineas)
        # Assert
        self.assertEqual(total, Decimal("1035.00"))  # 900 + 15 %

    def test_aplica_el_descuento_antes_del_isv(self):
        lineas = [LineaPedido("PAS-002", 2)]  # 3000

        total = self.servicio.calcular_total(lineas, DescuentoPorcentaje(10))

        self.assertEqual(total, Decimal("3105.00"))  # (3000 - 300) + 15 %

    def test_realizar_pedido_descuenta_existencias(self):
        self.servicio.realizar_pedido("cliente@correo.com", [LineaPedido("PAS-002", 3)])

        self.assertEqual(self.repositorio.obtener("PAS-002").existencias, 1)

    def test_realizar_pedido_notifica_al_cliente_con_el_total(self):
        self.servicio.realizar_pedido("cliente@correo.com", [LineaPedido("FIL-001", 1)])

        self.notificador.notificar.assert_called_once_with(
            "cliente@correo.com", "Su total es L 517.50"
        )

    def test_sin_existencias_suficientes_lanza_error_y_no_notifica(self):
        with self.assertRaises(StockInsuficiente):
            self.servicio.realizar_pedido("cliente@correo.com", [LineaPedido("PAS-002", 99)])

        self.notificador.notificar.assert_not_called()
        self.assertEqual(self.repositorio.obtener("PAS-002").existencias, 4)

    def test_repuesto_inexistente_lanza_error(self):
        with self.assertRaises(RepuestoNoEncontrado):
            self.servicio.calcular_total([LineaPedido("NO-EXISTE", 1)])


if __name__ == "__main__":
    unittest.main()
