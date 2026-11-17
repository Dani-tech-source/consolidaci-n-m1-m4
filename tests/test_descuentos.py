"""Pruebas unitarias de los descuentos. Cada prueba sigue AAA: Arrange, Act, Assert."""
import unittest
from decimal import Decimal

from repuestos.descuentos import (
    DescuentoFijo,
    DescuentoPorcentaje,
    SinDescuento,
)


class TestDescuentoPorcentaje(unittest.TestCase):
    def test_diez_por_ciento_de_1000_es_100(self):
        # Arrange
        descuento = DescuentoPorcentaje(10)
        # Act
        monto = descuento.calcular(Decimal("1000"))
        # Assert
        self.assertEqual(monto, Decimal("100"))

    def test_rechaza_porcentaje_mayor_a_100(self):
        with self.assertRaises(ValueError):
            DescuentoPorcentaje(150)


class TestDescuentoFijo(unittest.TestCase):
    def test_nunca_descuenta_mas_que_el_subtotal(self):
        # Arrange
        descuento = DescuentoFijo(Decimal("500"))
        # Act
        monto = descuento.calcular(Decimal("300"))
        # Assert
        self.assertEqual(monto, Decimal("300"))


class TestContratoDeDescuentos(unittest.TestCase):
    """Liskov: cualquier descuento debe cumplir el mismo contrato.

    Si alguien agrega un descuento nuevo, basta con sumarlo a la lista:
    esta prueba verifica que se pueda usar en lugar de los demás.
    """

    def test_todos_cumplen_0_menor_igual_descuento_menor_igual_subtotal(self):
        descuentos = [
            SinDescuento(),
            DescuentoPorcentaje(0),
            DescuentoPorcentaje(25),
            DescuentoPorcentaje(100),
            DescuentoFijo(Decimal("50")),
            DescuentoFijo(Decimal("10000")),
        ]
        for subtotal in (Decimal("0"), Decimal("99.99"), Decimal("5000")):
            for descuento in descuentos:
                with self.subTest(descuento=type(descuento).__name__, subtotal=subtotal):
                    monto = descuento.calcular(subtotal)
                    self.assertGreaterEqual(monto, 0)
                    self.assertLessEqual(monto, subtotal)


if __name__ == "__main__":
    unittest.main()
